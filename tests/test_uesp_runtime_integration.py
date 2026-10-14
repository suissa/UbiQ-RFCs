import tempfile
import unittest
from pathlib import Path

from conformance.uesp_runtime import ProviderSimulator, Runtime, SimulatedCrash, IdempotencyConflict, StaleFencingEpoch


class RuntimeIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.runtime_db = root / "runtime.sqlite3"
        self.provider_db = root / "provider.sqlite3"
        self.provider = ProviderSimulator(self.provider_db)
        self.runtime = Runtime(self.runtime_db, self.provider)
        self.execution = "tenant.example/execution-001"
        self.node = "write-order"
        self.attempt = "attempt-001"
        self.key = "tenant.example:execution-001:write-order:attempt-001"
        self.payload = {"order_id": "order-9", "amount_minor": 1250, "currency": "BRL"}
        self.epoch = self.runtime.acquire_owner(self.execution)

    def tearDown(self):
        self.tmp.cleanup()

    def test_restart_recovers_e1_without_duplicate_external_effect(self):
        with self.assertRaises(SimulatedCrash):
            self.runtime.dispatch(self.execution, self.node, self.attempt, self.key,
                                  self.payload, "E1", self.epoch, crash_after_effect=True)
        self.assertEqual(self.provider.effect_count(self.key), 1)
        self.assertFalse(self.runtime.ack_is_permitted(self.execution, self.node, self.attempt))
        self.runtime = Runtime(self.runtime_db, self.provider)
        self.assertEqual(self.runtime.recover(), {"recovered": 1, "quarantined": 0})
        self.assertEqual(self.provider.effect_count(self.key), 1)
        self.assertEqual(self.runtime.state(self.execution, self.node, self.attempt), "SETTLED_SUCCESS")
        self.assertEqual(self.runtime.settlement_count(), 1)
        self.assertEqual(self.runtime.outbox_count(), 1)
        self.assertTrue(self.runtime.ack_is_permitted(self.execution, self.node, self.attempt))

    def test_e3_unknown_outcome_is_quarantined_without_retry(self):
        with self.assertRaises(SimulatedCrash):
            self.runtime.dispatch(self.execution, self.node, self.attempt, self.key,
                                  self.payload, "E3", self.epoch, crash_after_effect=True)
        self.runtime = Runtime(self.runtime_db, self.provider)
        self.assertEqual(self.runtime.recover(), {"recovered": 0, "quarantined": 1})
        self.assertEqual(self.runtime.state(self.execution, self.node, self.attempt), "QUARANTINED")
        self.assertEqual(self.provider.effect_count(self.key), 1)
        self.assertEqual(self.runtime.settlement_count(), 0)

    def test_provider_rejects_reused_key_with_different_payload(self):
        self.provider.apply(self.key, self.payload)
        with self.assertRaises(IdempotencyConflict):
            self.provider.apply(self.key, {"order_id": "other-order"})

    def test_stale_owner_cannot_commit_settlement(self):
        self.runtime._persist_intent(self.execution, self.node, self.attempt, self.key,
                                     self.payload, "E1", self.epoch)
        stale_epoch = self.epoch
        self.runtime.acquire_owner(self.execution)
        with self.assertRaises(StaleFencingEpoch):
            self.runtime._settle(self.execution, self.node, self.attempt,
                                 {"applied": True}, stale_epoch)
        self.assertEqual(self.runtime.settlement_count(), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
