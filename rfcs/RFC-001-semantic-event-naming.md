# RFC-001 — Universal Semantic Event Naming

- Status: Draft
- Category: Standards Track

## Abstract

UbiQ defines a transport-independent canonical event name so domain meaning is stable across protocols.

## Specification

The canonical form is:

```text
<Entity>.<intent-or-action>.<state>
```

Examples:

```text
Order.create.requested
Order.create.completed
Payment.authorize.failed
```

`Entity` identifies the semantic owner. The middle segment expresses an intent or action. The final segment expresses the observable state/result. Names MUST be stable under transport substitution and MUST NOT contain broker-specific partitions, hostnames, URLs, queue names, or protocol verbs.

Case and character normalization MUST be deterministic. Implementations SHOULD use ASCII identifiers for interoperable wire names while allowing localized human labels as metadata.

A binding MAY transform separators where a transport requires it, but MUST preserve a reversible mapping to the canonical name.

## Invariant

```text
canonical(bind(name, T)) = name
```

for every conforming transport binding `T`.

## Conformance

A receiver MUST be able to recover the exact canonical semantic name regardless of ingress transport.