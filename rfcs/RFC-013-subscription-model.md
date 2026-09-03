# RFC-013 — Subscription Model

- Status: Draft
- Category: Standards Track

## Abstract

UbiQ defines semantic subscriptions independently of topics, queues, and broker consumer groups.

## Specification

A subscription selects canonical semantic addresses plus optional validated predicates. Wildcards MAY be supported over semantic segments, for example `Order.*.completed`.

Delivery mode is declared separately: broadcast, competing consumer, durable replay, ephemeral, or flow-bound subscription.

Bindings map this model to native constructs when possible. If a broker cannot enforce a filter, the UbiQ runtime MAY filter after ingress, but authorization MUST still be evaluated before delivery to application code.

Subscription identity SHOULD be stable across reconnects when durability is requested.

A subscription MUST NOT infer permission merely from the ability to bind to a native topic.

## 2flow

Flow-bound subscriptions MUST terminate or transition according to the lifecycle of the owning execution, preventing leaked listeners.