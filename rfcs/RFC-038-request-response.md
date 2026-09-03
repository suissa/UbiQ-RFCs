# RFC-038 — Universal Request/Response

- Status: Draft
- Category: Standards Track

## Abstract

Request/response semantics are available even when the underlying transport is asynchronous.

## Specification

A request creates a canonical correlation context and MAY declare deadline, expected response schema, and reply capability. A response MUST correlate to the request and SHOULD set `causation_id` to the triggering message.

Bindings MAY map to HTTP responses, NATS reply subjects, QUIC streams, WebSocket messages, or queue-based callbacks.

Timeout is a semantic outcome governed by RFC-026, not proof that the remote effect never happened. Therefore retries after ambiguous timeout MUST use idempotency/settlement evidence.

Multiple responses MAY be allowed only when the contract declares a streaming or fan-out interaction.

## 2flow

A request node advances only according to the response/timeout transitions declared by its flow contract.