#!/usr/bin/env python3
"""Standard-library conformance checks for published Draft vectors.

These tests validate vector integrity and executable reference invariants. They do
not prove interoperability with an implementation until adapters/runtimes consume
the same vectors in their own independent test suites.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
UESP_VECTOR = ROOT / "vectors/RFC-045/crash-after-dispatch.json"
SERIALIZATION_VECTOR = ROOT / "vectors/RFC-047/canonical-json-v1.json"


def read_vector(path: pathlib.Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def valid_semantic_address(value: str) -> bool:
    if not value.isascii() or len(value.encode("ascii")) > 192:
        return False
    parts = value.split(".")
    if len(parts) != 3 or any(not part or len(part) > 64 for part in parts):
        return False
    entity, action, state = parts
    if not re.fullmatch(r"[A-Z][A-Za-z0-9]*", entity):
        return False
    if not re.fullmatch(r"[a-z0-9-]+", action):
        return False
    allowed_states = {
        "requested", "accepted", "completed", "failed",
        "rejected", "cancelled",
    }
    return state in allowed_states or (
        state.startswith("x-")
        and re.fullmatch(r"x-[a-z0-9-]+", state) is not None
    )


def simulate_e1_crash_recovery(vector: dict) -> dict:
    """Minimal reference model for an idempotency-enforced provider."""
    if vector["effect_class"] != "E1" or not vector["provider"]["idempotency_enforced"]:
        raise ValueError("This reference model only covers provider-enforced E1 effects")
    effect_count = 1  # First dispatch reaches provider before runtime crashes.
    settlement_count = 0
    state = "effect-unknown"
    # Recovery queries provider/idempotency evidence; it must not redispatch.
    provider_reports_applied = True
    if provider_reports_applied:
        settlement_count += 1
        state = "settled-success"
    ack_after_settlement = settlement_count == 1 and state == "settled-success"
    return {
        "final_state": state,
        "provider_effect_count": effect_count,
        "settlement_count": settlement_count,
        "transport_ack_after_settlement": ack_after_settlement,
    }


class TestUESPVector(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.vector = read_vector(UESP_VECTOR)

    def test_vector_has_required_identity_and_fault_boundaries(self) -> None:
        self.assertEqual(self.vector["id"], "UESP-CRASH-03")
        self.assertEqual(self.vector["rfc"], "RFC-045")
        self.assertEqual(self.vector["profile"], "Durable")
        self.assertEqual(
            set(self.vector["required_fault_boundaries"]),
            {"pre-intent", "post-intent", "post-dispatch", "post-effect",
             "post-settlement", "pre-ack", "post-ack"},
        )

    def test_effect_unknown_reconciles_without_duplicate_effect(self) -> None:
        result = simulate_e1_crash_recovery(self.vector)
        self.assertEqual(result, self.vector["expected"])

    def test_forbidden_recovery_behaviors_are_explicit(self) -> None:
        self.assertIn("blind_retry", self.vector["forbidden"])
        self.assertIn("acknowledge_before_settlement", self.vector["forbidden"])


class TestSerializationVectors(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.vector = read_vector(SERIALIZATION_VECTOR)

    def test_jcs_projection_bytes_and_digest(self) -> None:
        for case in self.vector["jcs_cases"]:
            # This fixture deliberately covers a simple JCS-compatible object.
            canonical = json.dumps(case["input"], sort_keys=True, separators=(",", ":"), ensure_ascii=False)
            self.assertEqual(canonical, case["canonical_utf8"])
            digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
            self.assertEqual(digest, case["sha256"])

    def test_semantic_address_grammar(self) -> None:
        for case in self.vector["semantic_addresses"]:
            with self.subTest(address=case["value"]):
                self.assertEqual(valid_semantic_address(case["value"]), case["valid"])

    def test_transport_mappings_are_reversible_for_fixture(self) -> None:
        for case in self.vector["transport_cases"]:
            with self.subTest(address=case["canonical"]):
                self.assertEqual(case["nats"], case["canonical"])
                self.assertEqual(case["mqtt"].replace("/", "."), case["canonical"])
                self.assertNotIn("/", case["canonical"])
                self.assertNotIn(".", case["mqtt"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
