# RFC-032 — Transport Selection Policy

- Status: Draft
- Category: Standards Track

## Abstract

Selection chooses the best eligible binding from policy and capability evidence.

## Specification

The runtime first filters transports that fail REQUIRED capability, security, availability, or policy constraints. It then ranks eligible candidates using configured objectives such as priority, latency, cost, locality, durability, or load.

Selection MUST be deterministic when the same evidence and policy require deterministic execution. Randomized selection MAY be used when explicitly declared.

The chosen transport and decisive policy inputs SHOULD be recorded for auditability.

Domain code MUST NOT branch on concrete transport names. If business meaning truly depends on a property, that property MUST be expressed as a semantic requirement or policy constraint.

## 2flow

Selection occurs at dispatch time and does not alter the declared flow graph.