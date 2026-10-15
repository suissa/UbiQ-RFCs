#!/usr/bin/env python3
"""Focused reference-vector checks for UESP E3 recovery behavior."""
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
VECTOR = ROOT / "vectors/RFC-045/effect-unknown-e3.json"


class TestE3UnknownEffect(unittest.TestCase):
    def test_quarantine_without_automatic_retry(self):
        vector = json.loads(VECTOR.read_text(encoding="utf-8"))
        self.assertEqual(vector["rfc"], "RFC-045")
        self.assertEqual(vector["effect_class"], "E3")
        self.assertFalse(vector["provider"]["idempotency_enforced"])
        self.assertFalse(vector["provider"]["reconciliation_available"])
        expected = vector["expected"]
        self.assertEqual(expected["final_state"], "quarantined")
        self.assertEqual(expected["provider_effect_count"], 1)
        self.assertEqual(expected["automatic_retry_count"], 0)
        self.assertIn("blind_retry", vector["forbidden"])
        self.assertIn("claim_effectively_once", vector["forbidden"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
