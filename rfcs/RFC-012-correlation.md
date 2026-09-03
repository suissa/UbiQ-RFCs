# RFC-012 — Universal Correlation

- Status: Draft
- Category: Standards Track

## Abstract

Correlation provides one identity model for conversations, RPC, asynchronous callbacks, streams, and multi-step flows.

## Specification

`correlation_id` MUST remain stable for the logical interaction it identifies even when transports change. `causation_id` identifies immediate ancestry. `execution_id` identifies a concrete 2flow run and MUST NOT be conflated with correlation.

Request/reply bindings MAY use native correlation fields but MUST map them to the canonical envelope.

A gateway bridging WebSocket to NATS to QUIC MUST preserve the same correlation identity end to end.

Correlation identifiers MUST be globally collision-resistant within their intended scope. They are metadata, not credentials.

## Conformance

A trace reconstructed from canonical envelopes MUST be able to group all messages in a correlated interaction independently of the transports traversed.