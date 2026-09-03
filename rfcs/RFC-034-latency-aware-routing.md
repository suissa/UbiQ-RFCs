# RFC-034 — Latency-Aware Routing

- Status: Draft
- Category: Standards Track

## Abstract

Latency-aware routing selects among eligible transports using measured deadline risk.

## Specification

Measurements SHOULD distinguish connection setup, queue wait, dispatch, acknowledgement, and end-to-end semantic settlement latency.

Policies MAY use rolling percentiles, deadlines, or service-level objectives. A single transient sample SHOULD NOT cause unstable route flapping; implementations SHOULD use hysteresis or equivalent stabilization.

Deadline requirements belong to message/flow policy. If no eligible route can meet a hard deadline, the runtime SHOULD fail or heal before launching an effect whose late result would be invalid.

Latency optimization MUST occur after security and semantic capability filtering.

## Multipath

RFC-016 race-first-valid mode MAY be used for strict latency goals when duplicate effects are safely suppressed.