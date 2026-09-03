# RFC-020 — Replay Protection

- Status: Draft
- Category: Standards Track

## Abstract

UbiQ separates legitimate redelivery from malicious replay.

## Specification

Security-sensitive messages MUST include freshness and uniqueness evidence appropriate to their threat model: nonce, issuance/expiry time, monotonic sequence, challenge, or bound idempotency key.

The receiver MUST maintain replay state for at least the acceptance window required by policy. A duplicate delivery that is valid under RFC-009 MUST be routed through idempotency handling, not executed as a new semantic operation.

Proofs SHOULD bind audience and semantic address so a captured message cannot be replayed to a different operation.

Clock-based windows MUST account for bounded skew and SHOULD avoid relying on wall-clock time alone when stronger challenge mechanisms are available.

## 2flow

Replayed transition messages MUST never advance an execution past an already settled state.