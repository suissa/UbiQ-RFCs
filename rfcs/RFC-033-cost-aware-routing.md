# RFC-033 — Cost-Aware Routing

- Status: Draft
- Category: Standards Track

## Abstract

Cost may influence routing after correctness and security requirements are satisfied.

## Specification

Cost models MAY include network egress, broker operations, CPU, memory, energy, provider fees, or organizational chargeback. Units and freshness MUST be explicit.

A cheaper transport that violates a REQUIRED capability or security constraint is ineligible regardless of cost.

Policies MAY set budgets per message, principal, flow, tenant, or time window. Budget exhaustion MAY trigger defer, alternate route, or semantic failure according to 2flow policy.

Cost evidence SHOULD be observable and settlement records MAY include actual cost for later optimization.

## Security

Untrusted remote cost claims MUST NOT control routing without validation; manipulated prices can force denial of service or downgrade.