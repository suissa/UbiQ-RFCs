# RFC-050 — Delivery and Effect Profiles

- Status: Draft
- Category: Standards Track
- Scope: semantic, execution, transport
- Created: 2026-10-13
- Requires: RFC-009, RFC-010, RFC-045, RFC-046
- Updates: RFC-009
- Obsoletes: —
- Threats addressed: A1, A3, A4

## Abstract
This RFC separates message-delivery guarantees from business-effect guarantees.

## Motivation
Delivery describes message movement; effect guarantees depend on idempotency, settlement, and provider behavior. Combining them overstates what a broker can guarantee.

## Terminology
Delivery guarantee concerns whether a message is delivered. Effect guarantee concerns whether the semantic operation is applied and settled.

## Specification
Implementations MUST model delivery and effect as independent dimensions. Delivery values are none, at-most-once, and at-least-once. Effect values are at-most-once-effect and effectively-once, with the latter permitted only under RFC-045 effect classes E0–E2 and their declared assumptions. E3 MUST NOT claim effectively-once.

A deployment MUST document native transport behavior separately from guarantees added by retries, deduplication, transactions, and provider idempotency. Kafka transactions, MQTT QoS 2, and broker acknowledgements MUST NOT be described as exactly-once external business effects.

## 2flow interaction
Flow progression depends on settlement evidence, not the delivery label.

## Security considerations
A retry MUST preserve message identity for redelivery and MUST NOT bypass authorization or replay controls.

## Privacy considerations
Delivery logs SHOULD avoid copying payloads.

## Backward compatibility
Existing combined labels MUST be mapped explicitly to both dimensions; ambiguous labels MUST NOT be silently reinterpreted.

## Conformance
Vectors MUST distinguish delivery ACKs from settlements and demonstrate that broker-level guarantees do not imply external effect guarantees.

## References
- RFC-009
- RFC-010
- RFC-045
