import unittest

from conformance.transport import (
    InvalidSemanticAddress,
    from_http_path,
    from_kafka_headers,
    from_mqtt_topic,
    from_nats_subject,
    to_http_path,
    to_kafka_headers,
    to_mqtt_topic,
    to_nats_subject,
    validate_address,
)


class SemanticAddressTests(unittest.TestCase):
    def test_valid_addresses(self):
        for address in (
            "Patient.create.requested",
            "Appointment.cancel.requested",
            "Patient.review.x-needs-human",
        ):
            with self.subTest(address=address):
                self.assertEqual(validate_address(address), address)

    def test_rejects_invalid_or_ambiguous_addresses(self):
        for address in (
            "", "patient.create.requested", "Patient.Create.requested",
            "Patient.create.unknown", "Patient.*.requested",
            "Patient.create/requested", "Patient.create.requested.extra",
            "Patient.create. requested", "Patient..requested",
            "P" * 65 + ".create.requested", "患者.create.requested",
        ):
            with self.subTest(address=address):
                with self.assertRaises(InvalidSemanticAddress):
                    validate_address(address)

    def test_nats_round_trip_and_wildcard_rejection(self):
        address = "Patient.create.requested"
        self.assertEqual(from_nats_subject(to_nats_subject(address)), address)
        with self.assertRaises(InvalidSemanticAddress):
            from_nats_subject("Patient.*.requested")

    def test_mqtt_round_trip_and_malformed_topic_rejection(self):
        address = "Patient.create.requested"
        self.assertEqual(to_mqtt_topic(address), "Patient/create/requested")
        self.assertEqual(from_mqtt_topic(to_mqtt_topic(address)), address)
        for topic in ("Patient/create", "Patient//requested", "Patient/create/requested/extra"):
            with self.subTest(topic=topic):
                with self.assertRaises(InvalidSemanticAddress):
                    from_mqtt_topic(topic)

    def test_http_round_trip_and_noncanonical_encoding_rejection(self):
        address = "Patient.create.requested"
        self.assertEqual(from_http_path(to_http_path(address)), address)
        with self.assertRaises(InvalidSemanticAddress):
            from_http_path("/wrong/Patient.create.requested")

    def test_kafka_header_round_trip_and_type_validation(self):
        address = "Patient.create.requested"
        self.assertEqual(from_kafka_headers(to_kafka_headers(address)), address)
        with self.assertRaises(InvalidSemanticAddress):
            from_kafka_headers({"ubiq-name": "Patient.create.requested"})
        with self.assertRaises(InvalidSemanticAddress):
            from_kafka_headers({"ubiq-name": b"Patient.*.requested"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
