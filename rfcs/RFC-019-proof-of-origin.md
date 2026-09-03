# RFC-019 — Proof-of-Origin Message

- Status: Draft
- Category: Standards Track

## Abstract

Proof-of-origin cryptographically binds a message to an authorized origin independent of the transport path.

## Specification

A proof SHOULD cover a canonical digest of identity-critical envelope fields, semantic address, payload digest, intended audience, issuance time, and anti-replay material.

Intermediate gateways MUST NOT invalidate end-origin proof when only transport metadata changes. If a gateway transforms semantic content, it MUST emit a new message and establish a new causal relation rather than pretending the original signature still covers it.

Proof algorithms are negotiated by policy and MUST be algorithm-agile. Implementations SHOULD support key rotation and multiple concurrent verification keys.

A proof is evidence, not authorization by itself. The receiver MUST still evaluate current policy.

## Conformance

Any modification of a proof-covered semantic field MUST cause verification failure.