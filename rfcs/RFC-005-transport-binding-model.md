# RFC-005 — Transport Binding Model

- Status: Draft
- Category: Standards Track

## Abstract

This RFC defines the minimum contract implemented by HTTP, QUIC, NATS, Kafka, WebSocket, MQTT, RabbitMQ, Redpanda and future UbiQ adapters.

## Binding contract

A binding MUST implement semantic-address mapping, envelope encode/decode, capability declaration, send/receive, cancellation or termination semantics where supported, health state, and normalization of transport errors into RFC-026 failures.

A binding MUST NOT make domain decisions. It MUST NOT rename events semantically, authorize business operations, mutate payload meaning, or advance a 2flow state by itself.

Each adapter MUST declare its capabilities rather than assuming them. Capabilities include ordering, reliability class, streaming, datagrams, request/reply, durable subscription, maximum payload, encryption properties, and flow control.

## Boundary

```text
Domain -> UbiQ semantic runtime -> binding -> transport
```

Transport-native metadata MAY be retained for diagnostics but MUST remain namespaced and MUST NOT become required domain input.

## Conformance

The same envelope passed through two conforming bindings MUST result in an equivalent canonical envelope at the receiver, subject only to explicitly negotiated capability differences.