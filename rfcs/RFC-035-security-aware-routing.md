# RFC-035 — Security-Aware Routing

- Status: Draft
- Category: Standards Track

## Abstract

Routing decisions include cryptographic and trust requirements as first-class capabilities.

## Specification

A route MAY be constrained by required confidentiality profile, proof-of-possession, mutually authenticated channel, jurisdiction, trusted execution boundary, PQ/hybrid cryptography, key provenance, or data-classification policy.

Security constraints are filters, not preferences, when marked REQUIRED. A fallback MUST NOT silently weaken them.

The runtime SHOULD be able to explain why a route was rejected or selected without exposing secret policy details to unauthorized principals.

Transport-local claims MUST be verified rather than trusted from configuration alone when feasible.

## 2flow

Security requirements MAY differ by node. A payment authorization step, for example, may demand stronger proof than a public notification while remaining in the same execution.