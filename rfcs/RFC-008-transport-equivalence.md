# RFC-008 — Transport Equivalence Contract

- Status: Draft
- Category: Standards Track

## Abstract

This RFC defines when two transport paths are interchangeable for a particular UbiQ operation.

## Equivalence

Two transports `T1` and `T2` are equivalent for requirement set `R` when both satisfy `R` and their bindings preserve all semantics observable by the application.

```text
Equivalent(T1,T2,R) := satisfies(T1,R) ∧ satisfies(T2,R) ∧ preserve_semantics
```

Equivalence is contextual, not universal. HTTP and QUIC may be equivalent for a one-shot request but not for a datagram-required operation.

Applications MUST NOT infer equivalence from protocol labels. The runtime derives it from declared capabilities and policy.

Changing between equivalent transports MUST preserve the execution, correlation, causation, idempotency, and security context unless a specific RFC requires re-establishment of transport-local proof.

## Evidence

A runtime SHOULD record the evaluated requirement set and selected transport so failover decisions are auditable.