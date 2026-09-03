# RFC-043 — Transportless Actor Model

- Status: Draft
- Category: Standards Track

## Abstract

Actors in UbiQ consume and emit semantic messages without owning transport concerns.

## Specification

An Actor MAY know mailbox policy, accepted semantic addresses, state, supervision policy, Action bindings, and 2flow context. It MUST NOT require a specific broker or socket protocol to implement its domain behavior.

The runtime binds Actor mailboxes to one or more transports. Moving an Actor from machine A/NATS to machine B/QUIC MUST preserve its semantic address and accepted contracts.

Supervision failures MUST be distinguished from transport failures. Restarted Actors recover state and unsettled executions from authoritative persistence/settlement evidence.

Mailbox limits and backpressure MUST be explicit; unbounded dynamic memory is not assumed.

## A3 relationship

```text
Agent -> Actor -> Action -> UbiQ -> Binding
```

The Actor is the stateful/supervised execution boundary; Actions remain atomic behaviors and UbiQ provides communication continuity.