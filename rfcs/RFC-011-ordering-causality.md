# RFC-011 — Ordering and Causality

- Status: Draft
- Category: Standards Track

## Abstract

UbiQ distinguishes transport order from semantic causality.

## Specification

`causation_id` expresses a direct causal edge. `sequence` MAY express order within a defined scope. `correlation_id` groups related messages but does not itself imply order.

Bindings MUST NOT convert arrival order into causal truth. When a flow requires ordering, that requirement MUST be explicit and verified before advancing the 2flow state.

A receiver detecting a missing predecessor MAY buffer, reject, request replay, or invoke healing according to policy. It MUST NOT silently advance a strictly ordered execution.

Parallel 2flow branches MAY have no total order. Implementations SHOULD preserve partial-order evidence rather than inventing a global sequence where none exists.

## Security

Sequence numbers and causation references used for authorization or replay prevention MUST be integrity protected.