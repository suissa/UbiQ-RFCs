# RFC-051 — Authorization Enforcement and Delegation

- Status: Draft
- Category: Standards Track
- Scope: trust, execution
- Created: 2026-10-13
- Requires: RFC-003, RFC-013, RFC-018, RFC-020, RFC-029, RFC-046
- Updates: RFC-003, RFC-013, RFC-018
- Obsoletes: —
- Threats addressed: A2, A3, A4, A5

## Abstract
This RFC defines authorization enforcement points for message ingress and delivery, auditable decisions, delegation constraints, and revocation behavior.

## Motivation
A message may wait in a durable queue after credentials or delegation have expired. Ingress-only authorization creates a time-of-check/time-of-use gap.

## Terminology
PEP enforces policy; PDP evaluates policy. Delegation is an explicitly bounded authority chain from a principal to another principal.

## Specification
Authorization MUST be evaluated at ingress and again at delivery for queued or replayed messages. The decision record MUST include message_id, principal, action, enforcement point, policy version, delegation-chain identifiers, decision, and timestamp. A decision MUST be reproducible against the recorded policy version or clearly marked non-reproducible.

Delegation MUST bind issuer, subject, audience, capability/action scope, not-before, expiry, and unique token identifier. Each delegation step MUST attenuate or preserve—not silently expand—the granted scope. Implementations MAY use a reviewed capability-token profile, including macaroons/Biscuit-style attenuation or OAuth token exchange, but MUST specify the exact token format and verification rules.

Revocation MUST have a documented propagation SLO. Once that SLO elapses, queued messages MUST be re-evaluated against current revocation state. If policy or revocation state cannot be checked where required, enforcement MUST fail closed.

## 2flow interaction
Every effect MUST be authorized for the current principal, action, execution, and policy version before dispatch.

## Security considerations
Cached decisions MUST be bounded by policy version and expiry. Stored idempotency outcomes MUST NOT be returned before current authorization succeeds.

## Privacy considerations
Authorization logs SHOULD store stable references and policy digests rather than unnecessary personal attributes.

## Backward compatibility
Ingress-only deployments MUST NOT claim conformance to this profile until delivery-time checks are enabled.

## Conformance
Vectors MUST cover expired credentials in queues, revoked delegation, audience mismatch, scope expansion, policy-version changes, and unauthorized idempotency-result lookup.

## References
- RFC-018
- RFC-020
- RFC 8693
- RFC-046
