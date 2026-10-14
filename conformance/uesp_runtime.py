"""Executable reference runtime for RFC-045 conformance integration tests.

This is a local reference implementation, not a production UbiQ runtime. SQLite
provides real durable state across Runtime instances; ProviderSimulator uses a
separate SQLite database to model an external provider's enforced idempotency.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any


class SimulatedCrash(RuntimeError):
    """Fault injected after provider effect and before settlement."""


class IdempotencyConflict(RuntimeError):
    """An idempotency key was reused with a different payload."""


class StaleFencingEpoch(RuntimeError):
    """A stale execution owner attempted to commit settlement."""


def _connect(path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path), timeout=5.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = FULL")
    return conn


class ProviderSimulator:
    """Persistent external-provider stand-in with enforced idempotency."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        with _connect(self.db_path) as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS effects (
                    idempotency_key TEXT PRIMARY KEY,
                    payload_digest TEXT NOT NULL,
                    result_json TEXT NOT NULL
                )
            """)

    @staticmethod
    def digest(payload: Any) -> str:
        data = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    def apply(self, key: str, payload: Any) -> dict:
        payload_digest = self.digest(payload)
        with _connect(self.db_path) as db:
            row = db.execute(
                "SELECT payload_digest, result_json FROM effects WHERE idempotency_key = ?",
                (key,),
            ).fetchone()
            if row:
                if row["payload_digest"] != payload_digest:
                    raise IdempotencyConflict("idempotency key reused with different payload")
                return json.loads(row["result_json"])
            result = {"provider_reference": "effect-" + payload_digest[:16], "applied": True}
            db.execute(
                "INSERT INTO effects(idempotency_key, payload_digest, result_json) VALUES (?, ?, ?)",
                (key, payload_digest, json.dumps(result, sort_keys=True)),
            )
            return result

    def lookup(self, key: str) -> dict | None:
        with _connect(self.db_path) as db:
            row = db.execute(
                "SELECT result_json FROM effects WHERE idempotency_key = ?", (key,)
            ).fetchone()
            return json.loads(row["result_json"]) if row else None

    def effect_count(self, key: str | None = None) -> int:
        with _connect(self.db_path) as db:
            if key is None:
                return db.execute("SELECT COUNT(*) FROM effects").fetchone()[0]
            return db.execute(
                "SELECT COUNT(*) FROM effects WHERE idempotency_key = ?", (key,)
            ).fetchone()[0]


class Runtime:
    """Durable execution/settlement state machine for the tested RFC-045 subset."""

    def __init__(self, db_path: str | Path, provider: ProviderSimulator):
        self.db_path = Path(db_path)
        self.provider = provider
        with _connect(self.db_path) as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS owners (
                    execution_id TEXT PRIMARY KEY,
                    epoch INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS intents (
                    execution_id TEXT NOT NULL,
                    node_id TEXT NOT NULL,
                    attempt_id TEXT NOT NULL,
                    idempotency_key TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    payload_digest TEXT NOT NULL,
                    effect_class TEXT NOT NULL CHECK(effect_class IN ('E0','E1','E2','E3')),
                    fencing_epoch INTEGER NOT NULL,
                    state TEXT NOT NULL CHECK(state IN ('INTENT_PERSISTED','DISPATCHED','EFFECT_UNKNOWN','QUARANTINED','SETTLED_SUCCESS','SETTLED_FAILURE')),
                    PRIMARY KEY(execution_id, node_id, attempt_id)
                );
                CREATE TABLE IF NOT EXISTS settlements (
                    execution_id TEXT NOT NULL,
                    node_id TEXT NOT NULL,
                    attempt_id TEXT NOT NULL,
                    outcome TEXT NOT NULL,
                    result_json TEXT NOT NULL,
                    fencing_epoch INTEGER NOT NULL,
                    PRIMARY KEY(execution_id, node_id, attempt_id),
                    FOREIGN KEY(execution_id, node_id, attempt_id)
                        REFERENCES intents(execution_id, node_id, attempt_id)
                );
                CREATE TABLE IF NOT EXISTS outbox (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    execution_id TEXT NOT NULL,
                    node_id TEXT NOT NULL,
                    attempt_id TEXT NOT NULL,
                    message_json TEXT NOT NULL,
                    UNIQUE(execution_id, node_id, attempt_id)
                );
            """)

    def acquire_owner(self, execution_id: str) -> int:
        with _connect(self.db_path) as db:
            row = db.execute("SELECT epoch FROM owners WHERE execution_id=?", (execution_id,)).fetchone()
            epoch = 1 if row is None else row["epoch"] + 1
            db.execute(
                "INSERT INTO owners(execution_id, epoch) VALUES (?, ?) "
                "ON CONFLICT(execution_id) DO UPDATE SET epoch=excluded.epoch",
                (execution_id, epoch),
            )
            return epoch

    def _assert_current_epoch(self, db: sqlite3.Connection, execution_id: str, epoch: int) -> None:
        row = db.execute("SELECT epoch FROM owners WHERE execution_id=?", (execution_id,)).fetchone()
        if row is None or row["epoch"] != epoch:
            raise StaleFencingEpoch(f"epoch {epoch} is stale for execution {execution_id}")

    def _persist_intent(self, execution_id: str, node_id: str, attempt_id: str,
                        idempotency_key: str, payload: Any, effect_class: str, epoch: int) -> None:
        payload_json = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        digest = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
        with _connect(self.db_path) as db:
            self._assert_current_epoch(db, execution_id, epoch)
            db.execute("""
                INSERT INTO intents(execution_id,node_id,attempt_id,idempotency_key,
                    payload_json,payload_digest,effect_class,fencing_epoch,state)
                VALUES(?,?,?,?,?,?,?,?, 'INTENT_PERSISTED')
            """, (execution_id, node_id, attempt_id, idempotency_key, payload_json,
                  digest, effect_class, epoch))

    def _settle(self, execution_id: str, node_id: str, attempt_id: str,
                result: dict, epoch: int) -> None:
        with _connect(self.db_path) as db:
            self._assert_current_epoch(db, execution_id, epoch)
            intent = db.execute("""
                SELECT state, fencing_epoch FROM intents
                WHERE execution_id=? AND node_id=? AND attempt_id=?
            """, (execution_id, node_id, attempt_id)).fetchone()
            if intent is None:
                raise ValueError("settlement has no durable intent")
            if intent["fencing_epoch"] > epoch:
                raise StaleFencingEpoch("intent carries a fencing epoch newer than the settlement owner")
            result_json = json.dumps(result, sort_keys=True, separators=(",", ":"))
            message = {
                "type": "ExecutionSettled",
                "execution_id": execution_id,
                "node_id": node_id,
                "attempt_id": attempt_id,
                "outcome": "success",
                "result": result,
            }
            # Settlement and outgoing message commit atomically in one SQLite transaction.
            db.execute("""
                INSERT INTO settlements(execution_id,node_id,attempt_id,outcome,result_json,fencing_epoch)
                VALUES(?,?,?,'success',?,?)
            """, (execution_id, node_id, attempt_id, result_json, epoch))
            db.execute("""
                INSERT INTO outbox(execution_id,node_id,attempt_id,message_json)
                VALUES(?,?,?,?)
            """, (execution_id, node_id, attempt_id, json.dumps(message, sort_keys=True)))
            db.execute("""
                UPDATE intents SET state='SETTLED_SUCCESS'
                WHERE execution_id=? AND node_id=? AND attempt_id=?
            """, (execution_id, node_id, attempt_id))

    def dispatch(self, execution_id: str, node_id: str, attempt_id: str,
                 idempotency_key: str, payload: Any, effect_class: str, epoch: int,
                 crash_after_effect: bool = False) -> dict:
        if effect_class not in {"E0", "E1", "E2", "E3"}:
            raise ValueError("unknown effect class")
        self._persist_intent(execution_id, node_id, attempt_id, idempotency_key,
                             payload, effect_class, epoch)
        with _connect(self.db_path) as db:
            db.execute("""
                UPDATE intents SET state='DISPATCHED'
                WHERE execution_id=? AND node_id=? AND attempt_id=?
            """, (execution_id, node_id, attempt_id))
        result = self.provider.apply(idempotency_key, payload)
        if crash_after_effect:
            with _connect(self.db_path) as db:
                db.execute("""
                    UPDATE intents SET state='EFFECT_UNKNOWN'
                    WHERE execution_id=? AND node_id=? AND attempt_id=?
                """, (execution_id, node_id, attempt_id))
            raise SimulatedCrash("crash injected after provider effect and before settlement")
        self._settle(execution_id, node_id, attempt_id, result, epoch)
        return {"acknowledged": True, "settled": True, "result": result}

    def recover(self) -> dict:
        recovered = 0
        quarantined = 0
        with _connect(self.db_path) as db:
            rows = db.execute("""
                SELECT i.* FROM intents i
                LEFT JOIN settlements s USING(execution_id,node_id,attempt_id)
                WHERE s.attempt_id IS NULL
            """).fetchall()
        current_epochs: dict[str, int] = {}
        for intent in rows:
            execution_id = intent["execution_id"]
            node_id = intent["node_id"]
            attempt_id = intent["attempt_id"]
            if execution_id not in current_epochs:
                current_epochs[execution_id] = self.acquire_owner(execution_id)
            epoch = current_epochs[execution_id]
            if intent["effect_class"] == "E3":
                with _connect(self.db_path) as db:
                    db.execute("""
                        UPDATE intents SET state='QUARANTINED'
                        WHERE execution_id=? AND node_id=? AND attempt_id=?
                    """, (execution_id, node_id, attempt_id))
                quarantined += 1
                continue
            if intent["effect_class"] == "E0":
                result = {"applied": True, "pure_recompute": True}
            else:
                result = self.provider.lookup(intent["idempotency_key"])
                if result is None:
                    # Re-dispatch is only safe for the provider-enforced E1 case.
                    if intent["effect_class"] != "E1":
                        with _connect(self.db_path) as db:
                            db.execute("""
                                UPDATE intents SET state='QUARANTINED'
                                WHERE execution_id=? AND node_id=? AND attempt_id=?
                            """, (execution_id, node_id, attempt_id))
                        quarantined += 1
                        continue
                    result = self.provider.apply(intent["idempotency_key"], json.loads(intent["payload_json"]))
            self._settle(execution_id, node_id, attempt_id, result, epoch)
            recovered += 1
        return {"recovered": recovered, "quarantined": quarantined}

    def state(self, execution_id: str, node_id: str, attempt_id: str) -> str:
        with _connect(self.db_path) as db:
            row = db.execute("""
                SELECT state FROM intents WHERE execution_id=? AND node_id=? AND attempt_id=?
            """, (execution_id, node_id, attempt_id)).fetchone()
            if row is None:
                raise KeyError("unknown attempt")
            return row["state"]

    def settlement_count(self) -> int:
        with _connect(self.db_path) as db:
            return db.execute("SELECT COUNT(*) FROM settlements").fetchone()[0]

    def outbox_count(self) -> int:
        with _connect(self.db_path) as db:
            return db.execute("SELECT COUNT(*) FROM outbox").fetchone()[0]

    def ack_is_permitted(self, execution_id: str, node_id: str, attempt_id: str) -> bool:
        with _connect(self.db_path) as db:
            return db.execute("""
                SELECT 1 FROM settlements WHERE execution_id=? AND node_id=? AND attempt_id=?
            """, (execution_id, node_id, attempt_id)).fetchone() is not None
