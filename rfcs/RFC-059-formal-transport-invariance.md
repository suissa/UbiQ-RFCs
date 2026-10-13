# RFC-059 — Formal Transport Invariance and Equivalence Oracle

- Status: Draft
- Category: Standards Track
- Scope: semantic, execution, trust, transport
- Created: 2026-10-13
- Requires: RFC-008, RFC-026, RFC-044, RFC-046, RFC-047, RFC-050, RFC-058
- Updates: RFC-008, RFC-044
- Obsoletes: —
- Threats addressed: A1, A3, A4, A5

## Abstract
This RFC defines the observable semantic effect used by the transport invariance principle and establishes a test oracle for comparing bindings.

## Motivation
An equivalence law is not falsifiable until it defines the observer, the normalized outputs, and the treatment of transport metadata and failures.

## Terminology
Semantic effect is the normalized set of durable settlements, semantic output messages, and authorization decisions produced by processing a message under a declared profile. A terminal failure class is the stable failure category after recovery reaches a terminal state.

## Specification
For a message M and binding T, define SE(M,T) as the union of normalized settlements, normalized semantic output messages, and normalized authorization decisions. Normalization MUST preserve message identity, canonical semantic address, payload meaning/digest, causality, idempotency scope, execution/flow identity, authorization outcome, and declared delivery/effect guarantees.

Normalization MAY remove transport-local timestamps, hop transport labels, attempt IDs, trace IDs, and transport scheduling metadata only when those fields are explicitly non-semantic under the selected profile. It MUST NOT remove deadlines, priority, ordering, or causal information when the message contract declares them semantically relevant.

For every message M and pair of bindings T1/T2 whose attested capabilities satisfy the requirements of M, the conformance oracle MUST compare SE(M,T1) and SE(M,T2). Successful executions MUST yield equivalent normalized semantic effects. Under fault injection, both bindings MUST reach equivalent terminal failure classes or equivalent reconciled outcomes; exact wall-clock timing is not compared unless time is explicitly part of the contract.

If a binding cannot preserve a required property, it is ineligible before routing. Security constraints are hard filters; cost and latency may rank only the remaining eligible bindings.

## 2flow interaction
The comparison MUST use the pinned flow digest and settlement evidence. A transport ACK is not part of semantic effect unless the application contract explicitly declares it so.

## Security considerations
Authorization decisions and security-profile selection are part of the observable effect. Normalization MUST NOT erase a downgrade or an authorization difference.

## Privacy considerations
The test corpus MUST use synthetic payloads and avoid secrets. Digest equality alone MUST NOT be interpreted as proof of privacy.

## Backward compatibility
Existing tests that compare only message delivery or timing are insufficient for this profile and MUST be supplemented before conformance claims.

## Conformance
The versioned harness MUST run positive and negative vectors across binding pairs with drop, duplication, reordering, partition, restart, stale epoch, authorization change, and effect-unknown conditions. The test report MUST record binding versions, capability manifests, vector version, and mismatches.

## References
- RFC-008
- RFC-026
- RFC-044
- RFC-047
- RFC-050
- RFC-058
