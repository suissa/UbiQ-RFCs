# RFC-025 — Universal Observability Context

- Status: Draft
- Category: Standards Track

## Abstract

Observability context survives transport boundaries and must not redefine semantic identity.

## Specification

UbiQ SHOULD interoperate with W3C Trace Context using `traceparent` and `tracestate` or equivalent canonical fields. Trace identifiers are distinct from `message_id`, `correlation_id`, and `execution_id`.

Gateways MUST propagate valid trace context across protocol translation. A new span MAY be created for each transport hop while preserving the trace.

Operational metadata SHOULD include selected binding, route decision, latency, retries, failover, settlement state, and healing actions.

Sensitive payloads MUST NOT be copied into logs by default. Observability access is subject to zero-trust authorization.

## 2flow

Each node transition SHOULD be traceable so an execution graph can be reconstructed from telemetry without depending on a single broker's logs.