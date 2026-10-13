# RFC-054 — Deterministic and Privacy-Aware Semantic Routing

- Status: Draft
- Category: Standards Track
- Scope: semantic, trust, transport
- Created: 2026-10-13
- Requires: RFC-006, RFC-022, RFC-032, RFC-035, RFC-036, RFC-046
- Updates: RFC-036
- Obsoletes: —
- Threats addressed: A2, A3, A5

## Abstract
This RFC defines deterministic route predicates and separates metadata predicates from payload predicates.

## Motivation
Undeclared predicate languages can make retries non-deterministic, while intermediaries without decryption keys cannot safely evaluate payload predicates. Clear semantic addresses may also leak business context.

## Terminology
A metadata predicate reads only public, schema-defined routing metadata. A payload predicate reads decrypted endpoint payload and is evaluated only by an authorized endpoint.

## Specification
A routing profile MUST define a deterministic, non-Turing-complete predicate language and its version. Evaluation MUST be pure, bounded, and deterministic for the same input. The implementation MUST reject unknown functions, non-finite numbers, implicit network access, current-time reads, and unbounded evaluation.

Intermediaries MAY evaluate metadata predicates only. Payload predicates MUST be evaluated at an authorized endpoint after decryption and authorization. A router MUST NOT claim a payload-based decision was made when it lacks the relevant plaintext and authorization.

For sensitive event classes, deployments SHOULD support blinded semantic addresses or keyed routing tokens. The token scheme MUST specify tenant/key scope, rotation, collision handling, and how authorization is still evaluated against the canonical semantic address at the trusted endpoint.

## 2flow interaction
Routing MUST NOT change the pinned flow, action, or declared effect semantics.

## Security considerations
Predicate evaluation MUST have resource limits. Routing tokens MUST NOT be treated as authorization credentials.

## Privacy considerations
Address classification and metadata leakage MUST be documented. Sensitive payload fields MUST NOT be copied into routing headers.

## Backward compatibility
Legacy arbitrary predicates require a named compatibility profile and MUST NOT claim deterministic conformance.

## Conformance
Vectors MUST cover deterministic evaluation, forbidden operations, payload predicate endpoint enforcement, blinded-address rotation, and unauthorized routing.

## References
- RFC-022
- RFC-035
- RFC-036
