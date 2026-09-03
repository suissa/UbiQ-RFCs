# RFC-024 — Schema Evolution

- Status: Draft
- Category: Standards Track

## Abstract

Schema evolution allows independent components to change without silently changing message meaning.

## Specification

Schema versions MUST be identifiable. Compatibility SHOULD be classified as backward, forward, full, or breaking under explicit rules.

A producer MUST NOT advertise compatibility it does not satisfy. A consumer MUST validate the actual referenced schema/version rather than assuming the newest version.

Semantic changes that alter the meaning of an existing field SHOULD use a new field or new semantic event version rather than reinterpret historical data.

Adapters MUST NOT perform undocumented schema coercion. Any transformation is a semantic transformation and SHOULD be represented as an explicit Action with causation evidence.

## 2flow

Flow deployment SHOULD validate schema compatibility across connected nodes before activation.