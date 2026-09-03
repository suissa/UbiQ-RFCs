# RFC-031 — Everything-as-Code Transport Configuration

- Status: Draft
- Category: Standards Track

## Abstract

Transport topology and policy are declarative data, allowing generated runtime configuration without embedding protocol choices in domain code.

## Specification

A deployment configuration MAY declare adapters, endpoints, credentials by reference, capability overrides, priorities, limits, routing policies, and fallback sets.

Example:

```yaml
transports:
  quic-main:
    kind: quic
    priority: 100
  nats-backup:
    kind: nats
    priority: 80
```

Secrets MUST be referenced from an authorized secret provider and SHOULD NOT appear inline.

Configuration MUST be schema-validated before activation. Changes affecting active flows SHOULD be versioned and auditable.

A 2flow contract MAY express requirements but SHOULD NOT contain environment-specific hostnames or credentials.

## Conformance

Replacing a conforming transport configuration MUST require no change to domain Action code.