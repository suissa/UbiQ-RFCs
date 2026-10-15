# RFC-052 — Federation Identity and Multipath Coordination

- Status: Draft
- Category: Standards Track
- Scope: trust, execution, transport
- Created: 2026-10-13
- Requires: RFC-002, RFC-016, RFC-029, RFC-045, RFC-046, RFC-047
- Updates: RFC-016, RFC-029
- Obsoletes: —
- Threats addressed: A1, A3, A5

## Abstract
This RFC defines issuer-qualified execution identity, signed hop evidence, loop prevention, and the coordination requirements for concurrent delivery copies.

## Motivation
A remote peer must not collide with a local execution identifier, and simultaneous copies must not execute the same effect independently.

## Terminology
A hop link is an authenticated statement that a peer forwarded a message. An idempotency shard is the single coordination scope responsible for reserving a semantic operation.

## Specification
execution_id MUST include issuer identity and a UUIDv7. The issuer MUST match the authenticated peer or a valid delegation. Federated messages MUST carry a positive hop limit and a path of peer links. Each link MUST bind message_id, prior-link digest, peer identity, and timestamp. Receivers MUST reject a path that exceeds the limit, contains the receiving peer, or has an invalid signature.

Multipath copies MUST converge on a single linearizable deduplication reservation, keyed by a domain-separated idempotency scope. Only the successful reservation owner may begin the effect. A quorum mode MUST define exactly what is counted; quorum of delivery acknowledgements MUST NOT be treated as quorum of business outcomes. Conflicting outcomes MUST enter a declared arbitration path or QUARANTINED state.

Race-first-valid and redundant modes are allowed only for effect classes whose idempotency and reconciliation assumptions make them safe. E3 effects MUST use a single path and explicit human recovery.

## 2flow interaction
Federated execution retains its pinned flow digest, execution identity, and fencing epoch.

## Security considerations
A hop path is evidence, not authority. Each peer MUST reauthorize the operation at its own trust boundary.

## Privacy considerations
Federation metadata SHOULD avoid exposing unnecessary tenant and business identifiers.

## Backward compatibility
Peers without issuer-qualified identities and hop proofs MUST use a separately configured legacy profile and MUST NOT claim Federated conformance.

## Conformance
Tests MUST include forged issuer, invalid hop signature, hop-limit overflow, loop, concurrent duplicate reservation, and conflicting outcomes.

## References
- RFC-016
- RFC-029
- RFC-045
- RFC-047
