# RFC-041 — Universal Queue

- Status: Draft
- Category: Standards Track

## Abstract

UbiQ defines competing-consumer work queues independently of the backing queue technology.

## Specification

A semantic queue declares work address, consumer eligibility, delivery class, visibility/lease behavior, retry/healing policy, ordering requirements, and optional priority.

Bindings MAY map to NATS consumers, Kafka consumer groups, RabbitMQ queues, Redis/BullMQ, or another mechanism. Native behavior MUST be normalized to the declared semantic contract.

A lease expiration does not prove the Action had no effect. Redispatch of ambiguous work MUST use idempotency and settlement evidence.

Poison messages SHOULD enter explicit healing or quarantine rather than infinite retry.

## 2flow

Queue consumption is a dispatch mechanism; the owning 2flow node settles only when the Action's semantic outcome is settled, not when the broker removes a message.