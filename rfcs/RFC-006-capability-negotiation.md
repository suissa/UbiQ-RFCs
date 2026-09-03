# RFC-006 — Transport Capability Negotiation

- Status: Draft
- Category: Standards Track

## Abstract

UbiQ selects transports by required capabilities rather than hard-coded protocol names.

## Model

Messages, flows, policies, or endpoints MAY declare requirements such as:

```yaml
requirements:
  ordered: true
  streaming: true
  durable: false
  confidentiality: end-to-end
  max_latency_ms: 50
```

Bindings advertise capability facts. Selection is valid only when:

```text
capabilities(T) ⊇ requirements(M)
```

Negotiation MUST occur before irreversible effects. An implementation MUST reject or heal a route when no available transport satisfies REQUIRED capabilities.

Capability downgrade MUST be explicit. Security-sensitive capabilities MUST NOT be silently downgraded.

Negotiation results SHOULD be attached to execution evidence so later auditing can explain why a transport was selected.

## 2flow

A 2flow node MAY declare transport requirements without naming a specific transport. This allows deployment policy to choose QUIC today and NATS tomorrow without changing orchestration semantics.