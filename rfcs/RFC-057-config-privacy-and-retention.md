# RFC-057 — Secure Configuration, Privacy, and Retention

- Status: Draft
- Category: Standards Track
- Scope: trust, execution, transport
- Created: 2026-10-13
- Requires: RFC-019, RFC-021, RFC-022, RFC-028, RFC-031, RFC-046, RFC-047
- Updates: RFC-028, RFC-031
- Obsoletes: —
- Threats addressed: A2, A3, A4

## Abstract
This RFC defines strict configuration parsing, versioned activation, prevention of silent security downgrade, and privacy-preserving retention for append-only histories.

## Motivation
Ambiguous YAML parsing and mutable configuration can create downgrade paths. Immutable logs that contain plaintext personal data can conflict with deletion and minimization obligations.

## Terminology
Configuration digest identifies a canonical configuration version. Crypto-shredding makes encrypted data unrecoverable by destroying its encryption key while preserving non-sensitive audit evidence.

## Specification
A configuration profile MUST reject duplicate keys, unsupported tags, and ambiguous implicit types. YAML profiles MUST disable aliases and anchors unless explicitly bounded. Configuration MUST be schema-validated, versioned, and cryptographically authenticated when sourced across a trust boundary.

Activation MUST be atomic. Each settlement MUST record the configuration digest that governed it. A security-profile downgrade MUST be denied by default; an exception requires explicit policy approval and an auditable record. Existing in-flight executions MUST remain pinned to their approved profile unless a migration is explicitly authorized.

Append-only logs SHOULD store payload digests, opaque references, and minimal metadata rather than plaintext personal data. Sensitive payloads SHOULD be encrypted with per-subject or per-tenant data-encryption keys managed by a KMS. A deletion workflow MAY destroy the relevant key and MUST record a tombstone without retaining the deleted plaintext. The implementation MUST document backup, cache, replica, and key-retention behavior; key destruction MUST NOT be advertised as complete erasure if recoverable key copies remain.

## 2flow interaction
Execution records MUST retain enough non-sensitive evidence to explain transitions while respecting retention policy.

## Security considerations
Configuration and key rotation MUST be authenticated and audited. Secret values MUST NOT be committed to repository configuration or emitted in CI logs.

## Privacy considerations
Deployments MUST define retention periods, deletion handling, legal holds, and metadata minimization. Compliance claims require jurisdiction-specific review and cannot be inferred from crypto-shredding alone.

## Backward compatibility
Legacy configuration formats require explicit compatibility mode and MUST NOT silently downgrade security.

## Conformance
Tests MUST cover duplicate YAML keys, aliases, unsigned config, atomic activation, downgrade denial, config-digest recording, key destruction, tombstones, and backup-key retention.

## References
- RFC-028
- RFC-031
- RFC-046
- RFC-047
