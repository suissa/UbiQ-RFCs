# RFC-029 — Federation Protocol

- Status: Draft
- Category: Standards Track

## Abstract

Federation allows independent UbiQ runtimes to exchange semantic messages while retaining separate trust and routing policies.

## Specification

Federated peers MUST negotiate supported protocol version, bindings/capabilities, trust profile, schema compatibility, and addressing scope.

No federation relationship implies transitive trust. Each peer re-authorizes semantic operations at its boundary.

Federation MUST preserve canonical message identity and SHOULD preserve end-origin proof. A forwarding peer adds hop evidence without rewriting origin identity.

Routing loops MUST be detectable using hop identity, bounded TTL/hop limits, or equivalent mechanisms.

A peer MAY refuse unsupported semantic addresses or capabilities without revealing unnecessary internal topology.

## 2flow

Cross-federation execution MUST retain the same execution identity when the remote action is part of one declared flow.