# RFC-042 — Protocolless Application Contract

- Status: Draft
- Category: Standards Track

## Abstract

Domain code communicates with UbiQ semantics and MUST NOT depend on concrete messaging protocols.

## Rule

Application Actions SHOULD express operations such as:

```text
emit(Order.create.requested, payload)
request(Payment.authorize.requested, payload)
subscribe(Order.create.completed)
```

They SHOULD NOT call `nats.publish`, `http.post`, `quic.send`, or equivalent protocol APIs as part of domain behavior.

Protocol choice, endpoint, credentials, retry transport, and physical topology belong to runtime configuration and policy.

If application meaning depends on a transport property, that property MUST be modeled as a requirement (for example ordered streaming), not a concrete product name.

## Value

This rule enables one Action implementation to execute locally, remotely, synchronously, asynchronously, or over different protocols without source modification.

## Conformance

A reference conformance test SHOULD switch at least two bindings using configuration only and observe equivalent domain behavior.