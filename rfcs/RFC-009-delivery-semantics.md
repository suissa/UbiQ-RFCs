# RFC-009 — Universal Delivery Semantics

- Status: Draft
- Category: Standards Track

## Abstract

UbiQ exposes delivery semantics independent of the primitive offered by a broker or network protocol.

## Classes

The canonical classes are:

- `best-effort`
- `at-most-once`
- `at-least-once`
- `effectively-once`

`effectively-once` means duplicate transport deliveries may occur, but the UbiQ semantic effect is committed no more than once under the idempotency and settlement rules.

A binding MUST declare its native guarantees. The runtime MAY strengthen them using persistence, deduplication, acknowledgement, idempotency, and UESP settlement.

A runtime MUST NOT claim stronger guarantees than it can demonstrate for the operation. Exactly-once network delivery is not assumed.

Delivery policy MAY be declared per 2flow node. Failure to satisfy a REQUIRED class MUST block dispatch or invoke healing.

## Conformance

Implementations claiming `effectively-once` MUST persist enough evidence to suppress or safely replay duplicates across process restart.