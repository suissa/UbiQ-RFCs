# RFC-044 — UbiQ Transport Invariance Principle

- Status: Draft
- Category: Standards Track

## Abstract

Transport invariance is the central law that constrains all UbiQ bindings and routing behavior.

## Law

For message `M` and transports `T1`, `T2`:

```text
SemanticEffect(deliver(M,T1)) ≡ SemanticEffect(deliver(M,T2))
```

provided:

```text
capabilities(T1) ⊇ requirements(M)
capabilities(T2) ⊇ requirements(M)
```

Equivalence includes canonical event identity, payload meaning, correlation, causality, idempotency scope, execution identity, authorization semantics, and required delivery guarantees.

Transport-specific timing is not itself a semantic difference unless time/deadline is part of the declared contract.

If a transport cannot preserve a REQUIRED semantic property, it is not an admissible binding for that operation.

## Consequences

Capability negotiation, failover, multipath, federation, and dynamic routing are valid only insofar as they preserve this law.

## Conformance

Each binding SHOULD have cross-binding property tests comparing canonical outcomes for the same corpus of messages and requirements.