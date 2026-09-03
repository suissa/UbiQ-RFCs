# RFC-010 — Universal Idempotency

- Status: Draft
- Category: Standards Track

## Abstract

Idempotency belongs to semantic execution, not to a specific broker.

## Specification

Operations capable of external side effects SHOULD carry an `idempotency_key`. The key scope MUST be defined by policy and SHOULD include semantic operation identity and principal scope.

A receiver MUST return or reconstruct the previously settled outcome when it receives the same key for the same semantic operation. Reusing a key for a materially different payload MUST be rejected as a conflict.

Deduplication state MUST survive the failure domain required by the delivery guarantee. In-memory-only deduplication cannot support restart-safe effectively-once semantics.

Idempotency keys MUST NOT be treated as authentication secrets.

## 2flow

The execution engine SHOULD derive stable idempotency keys for replay-sensitive nodes from `execution_id + node_id + semantic operation`, allowing deterministic resume without repeating settled side effects.