# RFC-036 — Semantic Routing

- Status: Draft
- Category: Standards Track

## Abstract

UbiQ routes by semantic meaning and policy before mapping to physical transport destinations.

## Specification

A route selector MAY evaluate canonical entity, intent/action, state, schema, principal, context, 2flow node, and declared requirements.

Example:

```yaml
when:
  entity: Order
  action: create
  state: requested
deliver:
  actor: OrderCreator
```

Physical endpoint resolution occurs after semantic routing. Therefore changing a NATS subject, QUIC endpoint, or Kafka partition does not change the business route.

Semantic predicates MUST be deterministic where they affect exactly-once/effectively-once execution. Authorization is evaluated before application delivery.

Routing rules SHOULD be Everything-as-Code and versioned.

## Principle

The event decides the logical destination; the transport binding decides how to reach the selected runtime endpoint.