# RFC-007 — Cross-Protocol Event Translation

- Status: Draft
- Category: Standards Track

## Abstract

Cross-protocol bridges translate wire representation while preserving semantic identity.

## Specification

Translation is a two-stage operation:

```text
Transport A wire -> canonical UbiQ envelope -> Transport B wire
```

Direct protocol-to-protocol transformations that bypass canonical validation are non-conforming when they can change semantic meaning.

Translation MUST preserve message identity, canonical address, correlation, causation, execution identity, schema identity, trace context, security evidence where portable, and payload bytes or canonical payload value.

Transport metadata that cannot be represented by the target MAY be retained under a namespaced diagnostics field. It MUST NOT be promoted into domain semantics.

When a required property cannot be preserved, translation MUST fail before dispatch or route through a declared healing policy.

## Conformance

For a supported pair `A,B`, decoding the translated message MUST produce a canonical envelope semantically equivalent to decoding the original message.