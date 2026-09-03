# RFC-015 — Multi-Transport Failover

- Status: Draft
- Category: Standards Track

## Abstract

UbiQ may continue an operation over another transport when the current path becomes unavailable.

## Specification

Failover candidates MUST satisfy the original capability and security requirements. Preference order MAY be policy-driven, for example `QUIC -> NATS -> WebSocket -> HTTP`.

Failover MUST preserve canonical message and execution identities. If delivery status is uncertain, the runtime MUST use idempotency and settlement evidence before re-dispatching an external side effect.

Security downgrade is prohibited unless explicitly allowed by the originating policy. A fallback transport that cannot meet a REQUIRED property is not a valid candidate.

Failover events SHOULD be observable and attached to execution evidence.

## 2flow

Transport failure does not itself imply Action failure. The execution engine first attempts eligible transport recovery; only exhausted transport policy yields a semantic failure transition.