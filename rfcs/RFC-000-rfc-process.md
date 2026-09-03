# RFC-000 — UbiQ RFC Process

- Status: Draft
- Category: Process

## Abstract

This RFC defines how UbiQ specifications evolve without allowing implementation convenience to silently redefine protocol semantics.

## Lifecycle

An RFC progresses through `Draft -> Experimental -> Candidate -> Stable`. `Rejected`, `Withdrawn`, `Deprecated`, and `Superseded` are terminal or historical states.

A Standards Track RFC MUST define observable conformance requirements. Promotion to Candidate requires at least one implementation. Promotion to Stable SHOULD require two independent interoperable implementations or equivalent evidence.

Breaking changes to a Stable RFC require a new RFC or explicit major protocol version. Editorial corrections MAY be applied without changing semantics.

## Categories

- **Standards Track**: normative protocol behavior.
- **Process**: project governance.
- **Informational**: architecture and rationale.
- **Experimental**: behavior not yet proven interoperable.

## Design rule

An RFC MUST state whether its rule belongs to semantic, execution, trust, or transport scope. Transport-specific behavior MUST NOT leak into the semantic contract unless represented as an explicit capability.

## Conformance

Every RFC MUST contain status, category, abstract, specification, security considerations, and conformance criteria. Normative terms follow RFC 2119/RFC 8174.