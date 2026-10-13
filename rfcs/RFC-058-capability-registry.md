# RFC-058 — Typed Capability Registry

- Status: Draft
- Category: Standards Track
- Scope: transport, trust
- Created: 2026-10-13
- Requires: RFC-005, RFC-006, RFC-035, RFC-044, RFC-046
- Updates: RFC-005, RFC-006, RFC-035
- Obsoletes: —
- Threats addressed: A2, A3, A4, A5

## Abstract
This RFC defines typed capabilities, requirement satisfaction, and the distinction between attested static properties and observed dynamic service levels.

## Motivation
A capability comparison is not meaningful unless its type, scope, and satisfaction relation are explicit. A self-declared adapter capability cannot by itself prove conformance.

## Terminology
A static capability is a versioned property established by implementation and tests. A dynamic SLO is a measured property over a defined observation window. An attestation binds an adapter artifact to a conformance result.

## Specification
Every capability MUST define a type, unit, scope, allowed values, and a satisfies(capability, requirement) relation. Ordering capabilities MUST identify whether ordering is none, per-key, per-stream, or total. Confidentiality levels MUST define an explicit profile ordering or partial order. Numeric limits MUST define units and whether larger or smaller values satisfy a requirement.

Static declarations and dynamic measurements MUST be separate. Latency percentiles, observed availability, queue lag, and throughput MUST NOT be represented as immutable adapter properties. Dynamic SLOs MUST include measurement window, sample basis, and freshness.

A binding manifest SHOULD be signed and MUST include adapter identity/version, supported protocol profile, capability schema version, conformance suite identifier/version, suite digest, result, and expiry or revocation reference. A runtime MUST NOT treat self-asserted capabilities as attested. Requirements that cannot be proven MUST be treated as unsatisfied for security-critical routing.

## 2flow interaction
The admissible transport set is computed by satisfying all required capabilities before applying cost or latency ranking.

## Security considerations
Capabilities are untrusted claims until verified. A malicious adapter must not be able to downgrade a security requirement by lying about its features.

## Privacy considerations
Capability telemetry SHOULD avoid tenant-specific labels and payload content.

## Backward compatibility
Unversioned capability strings require a legacy profile and MUST NOT satisfy typed security requirements by implicit coercion.

## Conformance
Vectors MUST cover type mismatch, unit mismatch, order-scope mismatch, stale SLO measurements, invalid attestation, and unsupported required capabilities.

## References
- RFC-005
- RFC-006
- RFC-035
- RFC-044
