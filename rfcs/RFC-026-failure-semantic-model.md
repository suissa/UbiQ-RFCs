# RFC-026 — Failure Semantic Model

- Status: Draft
- Category: Standards Track

## Abstract

UbiQ distinguishes failures by meaning so healing and orchestration do not confuse network faults with domain rejection.

## Classes

At minimum implementations MUST distinguish:

- `transport`: bytes/path/session failure;
- `security`: identity, proof, authorization, replay, downgrade;
- `schema`: contract violation;
- `semantic`: valid message but invalid domain operation;
- `execution`: illegal or impossible 2flow transition;
- `dependency`: downstream service unavailable or rejected;
- `timeout`: required deadline exceeded;
- `internal`: runtime invariant or implementation fault.

Failures MUST retain causation and execution identity. Bindings translate native errors into this model but MUST preserve diagnostic details in namespaced metadata.

A failure is not necessarily terminal. RFC-027 policy decides retry, alternate transport, compensation, human escalation, or terminal settlement.

## Conformance

Transport errors MUST NOT be surfaced as domain validation errors and vice versa.