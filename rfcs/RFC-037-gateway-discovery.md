# RFC-037 — UbiQ Gateway Discovery

- Status: Draft
- Category: Standards Track

## Abstract

Discovery finds candidate UbiQ gateways without making discovery itself an authorization mechanism.

## Specification

Discovery MAY use static configuration, DNS, service registries, local manifests, federation exchange, or other mechanisms. Results SHOULD include endpoint references, supported UbiQ version, advertised capabilities, and identity hints.

A discovered endpoint is untrusted until RFC-018/RFC-021 verification succeeds. Discovery metadata MUST NOT override security policy.

Clients SHOULD support multiple candidates and MAY rank them using RFC-032 policies.

Cached discovery records MUST have bounded freshness. Stale records MAY be attempted but require full re-verification.

## Privacy

Discovery SHOULD reveal only the minimum topology and capabilities needed for connection establishment.