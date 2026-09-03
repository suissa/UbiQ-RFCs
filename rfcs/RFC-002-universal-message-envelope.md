# RFC-002 — Universal Message Envelope

- Status: Draft
- Category: Standards Track

## Abstract

This RFC defines the transport-neutral UbiQ message envelope.

## Required fields

A message MUST carry or resolve:

```text
message_id
semantic_address
created_at
payload
```

When applicable it SHOULD carry:

```text
correlation_id
causation_id
idempotency_key
flow_id
execution_id
sequence
schema_ref
trace_context
security_context
requirements
```

The envelope MAY be serialized directly or mapped to compatible standards such as CloudEvents. Transport adapters MUST NOT redefine field semantics.

`message_id` identifies the immutable message occurrence. `correlation_id` groups a semantic interaction. `causation_id` points to the message that caused this message. `execution_id` identifies a concrete 2flow execution.

The payload MUST be treated as immutable after message identity is established. Any semantic mutation MUST produce a new message identifier.

## Security

Security evidence MUST bind at least the immutable identity-critical fields and payload digest. Removing a field covered by a proof invalidates that proof.

## Conformance

Round-tripping an envelope across conforming bindings MUST preserve all semantic fields even if the wire representation changes.