# RFC-018 — Universal Zero-Trust Identity

- Status: Draft
- Category: Standards Track

## Abstract

UbiQ identity is independent of IP address, connection, broker account, or transport session.

## Specification

Every privileged semantic operation MUST resolve an authenticated principal and authorization context. Identity MAY be human, service, agent, actor, device, workload, or delegated capability.

A trusted connection MUST NOT imply trusted messages. Identity and authorization MUST be re-evaluable at every trust boundary.

Principal identity SHOULD be represented by stable identifiers while credentials and proof keys remain rotatable and short-lived.

Delegation MUST be explicit, bounded by audience, capability, time, and semantic scope.

Transport authentication such as mTLS MAY contribute evidence but MUST NOT become the sole semantic identity model.

## Conformance

The same principal communicating over two different transports MUST resolve to the same semantic identity when equivalent proof is presented.