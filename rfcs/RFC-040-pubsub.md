# RFC-040 — Universal Pub/Sub

- Status: Draft
- Category: Standards Track

## Abstract

Pub/Sub is expressed with semantic events and subscriptions rather than broker-specific topics.

## Specification

Publishers emit canonical envelopes to semantic addresses. Subscribers declare RFC-013 subscriptions. The runtime maps these to one or more physical transports.

Broadcast delivery does not imply identical delivery guarantees for every subscriber; each subscription MAY declare durability and delivery semantics.

A publisher MUST NOT need to know subscriber count, broker topic, consumer group, or physical location.

Authorization is evaluated for publish and receive independently.

Cross-transport fan-out MAY deliver the same message over NATS to one subscriber and WebSocket to another while preserving one canonical message identity.

## 2flow

Pub/Sub events MAY trigger new flows or advance explicitly waiting executions when correlation rules identify the target.