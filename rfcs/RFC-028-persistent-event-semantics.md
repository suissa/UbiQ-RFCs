# RFC-028 — Persistent Event Semantics

- Status: Draft
- Category: Standards Track

## Abstract

Persistence is defined by semantic history, not by a particular broker's retention feature.

## Specification

Persisted records SHOULD store the canonical envelope, settlement status, schema identity, security evidence references, and sufficient metadata to rebuild causality and execution state.

Append-only event history is preferred for audit-critical transitions. Corrections SHOULD be new causally linked records rather than mutation of settled history.

Snapshots MAY accelerate recovery but MUST be derivable or verifiable against authoritative history. Snapshot cadence is deployment policy.

Retention MUST account for idempotency, replay protection, legal requirements, privacy, and recovery guarantees.

A broker's acknowledgement is not automatically equivalent to semantic settlement.

## 2flow

A restarted runtime MUST be able to reconstruct the last settled node and resume according to RFC-004.