# RFC-016 — Multipath Delivery

- Status: Draft
- Category: Standards Track

## Abstract

Multipath allows one semantic message to traverse multiple transport paths for resilience or latency racing.

## Specification

All path copies MUST share the same canonical `message_id` and idempotency identity. A receiver MUST collapse duplicate arrivals before committing semantic effects.

Policies MAY define `race-first-valid`, `quorum`, `redundant`, or `audit-copy` modes. The selected mode MUST define when the operation is considered delivered and which acknowledgements are required.

Multipath MUST NOT weaken confidentiality by sending a protected payload across a path that fails the original security requirements.

When paths yield inconsistent results, no result may be silently preferred unless policy defines deterministic arbitration.

## Conformance

An effectively-once multipath implementation MUST prove that simultaneous arrivals cannot produce duplicate settled side effects.