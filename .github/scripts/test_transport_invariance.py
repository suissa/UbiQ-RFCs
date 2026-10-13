#!/usr/bin/env python3
"""Reference mapping check for RFC-059; no live adapters are invoked."""
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
VECTOR = ROOT / "vectors/RFC-059/transport-invariance.json"


class TestTransportInvariance(unittest.TestCase):
    def test_bindings_preserve_the_same_semantic_identity(self):
        vector = json.loads(VECTOR.read_text(encoding="utf-8"))
        canonical = vector["canonical"]
        expected = vector["expected"]
        address = canonical["semantic_address"]

        self.assertEqual(expected["normalized_semantic_address"], address)
        self.assertEqual(expected["message_id"], canonical["message_id"])
        self.assertEqual(expected["execution_id"], canonical["execution_id"])
        self.assertEqual(expected["canonical_digest"], canonical["canonical_digest"])
        self.assertEqual(expected["distinct_semantic_identities"], 1)

        for binding in vector["bindings"]:
            with self.subTest(binding=binding["name"]):
                if binding["name"] == "NATS":
                    normalized = binding["subject"]
                elif binding["name"] == "MQTT":
                    normalized = binding["topic"].replace("/", ".")
                elif binding["name"] == "HTTP":
                    self.assertEqual(binding["method"], "POST")
                    prefix = "/v1/events/"
                    self.assertTrue(binding["path"].startswith(prefix))
                    normalized = binding["path"][len(prefix):]
                elif binding["name"] == "Kafka":
                    normalized = binding["headers"]["ubiq-name"]
                else:
                    self.fail("Unknown binding in fixture: " + binding["name"])
                self.assertEqual(normalized, address)


if __name__ == "__main__":
    unittest.main(verbosity=2)
