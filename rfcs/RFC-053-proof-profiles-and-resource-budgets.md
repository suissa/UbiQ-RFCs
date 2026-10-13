# RFC-053 — Proof Profiles and Resource Budgets

- Status: Draft
- Category: Standards Track
- Scope: trust, transport
- Created: 2026-10-13
- Requires: RFC-005, RFC-019, RFC-021, RFC-022, RFC-046, RFC-047
- Updates: RFC-005, RFC-019, RFC-021
- Obsoletes: —
- Threats addressed: A1, A3, A4

## Abstract
This RFC defines proof profiles with explicit size and computational budgets to prevent cryptographic requirements from making a transport unusable or enabling denial of service.

## Motivation
Large post-quantum signatures can exceed practical datagram payload budgets, and per-message asymmetric verification can be abused to exhaust CPU.

## Terminology
A proof profile defines cryptographic algorithms, key binding, permitted uses, size limits, and verification-cost expectations.

## Specification
Every proof profile MUST specify allowed algorithms, key identifiers, domain separation, maximum proof size, maximum message size, and verification-cost limits. Algorithms MUST be selected from trusted key metadata and signed policy; an untrusted message field MUST NOT select the verification algorithm.

Implementations SHOULD define separate profiles for full signatures at trust boundaries or privileged effects, session MACs for hot paths after authenticated session establishment, and batch/Merkle proofs for streams. A session MAC MUST be bound to principal, audience, session key, and protocol version and MUST be re-established after reconnect. Batch proofs MUST bind the item order and the exact batch root.

No profile may assume a universal datagram payload limit. A binding MUST advertise its effective payload budget after headers and proof overhead. If a proof does not fit, the runtime MUST choose an explicitly approved compatible binding or reject; it MUST NOT silently remove or weaken proof material.

## 2flow interaction
Privileged actions and settlements MUST use a proof profile permitted by the pinned policy.

## Security considerations
Verification MUST be rate-limited and performed only after inexpensive structural bounds checks. Algorithm agility MUST use an allowlist and key-bound algorithm selection.

## Privacy considerations
Proof metadata SHOULD use opaque key identifiers where exposing identity is unnecessary.

## Backward compatibility
A profile change MUST be versioned. Downgrades require explicit policy authorization and MUST be logged.

## Conformance
Vectors MUST include oversized proofs, disallowed algorithms, wrong audience/session binding, invalid batch roots, and downgrade attempts.

## References
- RFC-019
- RFC-021
- RFC-022
- RFC 8949
