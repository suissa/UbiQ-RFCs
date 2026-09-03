# RFC-023 — Schema Contract

- Status: Draft
- Category: Standards Track

## Abstract

Every semantic message type may reference a machine-verifiable payload contract independent of implementation language.

## Specification

`schema_ref` SHOULD identify an immutable or content-addressed schema version. UbiQ RECOMMENDS JSON Schema compatible representations and MAY express source schemas in YAML.

Validation occurs against the canonical payload, not transport framing. A binding MUST NOT weaken schema constraints.

Schemas SHOULD define semantic fields, constraints, examples, and compatibility metadata. Secret values MUST NOT be embedded in schemas.

A schema failure is an RFC-026 semantic validation failure and may enter RFC-027 healing; it is not automatically a transport failure.

## 2flow

A 2flow edge MAY declare the output schema of one node and required input schema of the next. The runtime SHOULD verify compatibility before execution when possible.