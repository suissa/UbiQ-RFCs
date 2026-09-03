# RFC-045 — UbiQ Execution Settlement Protocol (UESP)

- Status: Draft
- Category: Standards Track

## Abstract

UESP defines when a UbiQ execution step is considered irreversibly known by the orchestration runtime, enabling deterministic recovery without confusing transport acknowledgement with business completion.

## Settlement record

A settled transition MUST identify at least:

```text
flow_id
execution_id
node_id
attempt_id
input_message_id
semantic_action
outcome
output_message_id or output_digest
settled_at
```

It SHOULD include idempotency key, causation, schema identity, principal/security evidence reference, 2flow digest, and persistence proof/version.

## States

An operation SHOULD distinguish `not-started`, `dispatched`, `effect-unknown`, `settled-success`, and `settled-failure` or equivalent states. A transport ACK MAY move an operation to `dispatched`; it MUST NOT by itself establish `settled-success`.

When the runtime crashes after dispatch but before settlement, recovery MUST classify the effect as unknown and resolve it using idempotency lookup, provider reconciliation, durable outcome evidence, compensation, or Human-in-the-Healing-Loop. It MUST NOT blindly repeat an irreversible effect.

## 2flow guarantee

A 2flow node advances only from valid settlement evidence. This is the mechanism behind UbiQ orchestration assurance: the runtime can resume from the exact first unsettled semantic step instead of restarting the entire flow.

## Transport independence

Settlement evidence is canonical UbiQ state and MUST survive transport migration, federation, process restart, and Actor restart.

## Security

Settlement records for privileged effects SHOULD be tamper-evident and cryptographically bind execution identity, action, outcome, and 2flow version.

## Conformance

A conforming implementation MUST pass crash tests at every boundary between dispatch, external effect, response, persistence, and acknowledgement without producing duplicate settled effects.