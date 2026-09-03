# RFC-003 — Universal Semantic Addressing

- Status: Draft
- Category: Standards Track

## Abstract

Semantic addresses identify what communication means, not where bytes are sent.

## Specification

The canonical semantic address is the RFC-001 event name plus optional scope metadata. A transport adapter maps it to a native endpoint.

Example mappings:

```text
Order.create.requested
HTTP       -> /Order.create.requested
NATS       -> Order.create.requested
WebSocket  -> envelope.semantic_address
MQTT       -> Order/create/requested
```

Mappings MUST be deterministic and reversible. A mapping that loses semantic information is non-conforming unless the lost information is preserved in envelope metadata.

Physical concerns such as host, port, topic partition, consumer group, and stream number belong to binding configuration, never to the canonical address.

A deployment MAY alias physical destinations, but an alias MUST resolve to a canonical semantic address before authorization and orchestration decisions are made.

## Security

Authorization MUST be evaluated against the canonical semantic address, preventing an attacker from gaining privilege by selecting an alternate transport representation.