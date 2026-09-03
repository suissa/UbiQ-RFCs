# RFC-017 — Cross-Protocol Execution Continuity

- Status: Draft
- Category: Standards Track

## Abstract

A logical execution can continue after changing transport, process, node, or connection.

## Specification

The continuity identity is formed by stable semantic identifiers including `flow_id`, `execution_id`, correlation, causation, message identity, and settled transition state.

A WebSocket disconnect followed by QUIC reconnect MUST NOT create a new execution merely because the transport session changed.

Transport-local sessions MAY be renewed, but the receiver MUST rebind them to the existing semantic execution only after eXtreme Zero Trust verification.

Continuity requires enough persisted state to identify the last settled transition and any in-flight unsettled operation.

## Recovery

On restart, the runtime MUST classify each node as at least `not-started`, `in-flight`, `settled-success`, `settled-failure`, or an equivalent state sufficient for deterministic continuation.

## Conformance

A test MUST demonstrate an execution starting on one transport, losing that transport, continuing on another, and preserving one execution history.