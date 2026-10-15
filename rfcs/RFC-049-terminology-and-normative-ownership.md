# RFC-049 — UbiQ Terminology and Normative Ownership

- Status: Draft
- Category: Process
- Scope: semantic, execution, trust, transport
- Created: 2026-10-13
- Requires: RFC-000, RFC-002, RFC-026, RFC-044, RFC-045
- Updates: —
- Obsoletes: —
- Threats addressed: A3, A5

## Abstract
This RFC defines shared terms and the ownership rule for normative requirements so that duplicated wording does not drift across the specification.

## Motivation
Terms used across multiple RFCs need a single definition. Repeating normative rules creates ambiguity when one copy changes and another does not.

## Terminology
- Action: a declared operation that may produce an effect and has an explicit effect class.
- Actor: a runtime identity that owns or processes a declared execution role.
- Agent: an implementation component acting for a principal under explicit policy.
- Principal: an authenticated identity to which authorization decisions apply.
- 2flow contract: a versioned execution definition with canonical digest and explicit transition semantics.
- Settlement: durable evidence that an attempted semantic operation reached a known outcome under its effect class.
- Effect-unknown: dispatch may have produced an external effect, but evidence does not prove success or non-application.
- Capability: a typed property a binding can satisfy, with explicit scope and comparison semantics.
- Requirement: a property demanded by a message, flow, policy, or conformance profile.
- Binding: an implementation mapping the UbiQ envelope to a concrete transport.
- Fencing token: a monotonic epoch used to reject writes from an older owner.
- Human-in-the-Healing-Loop (HITL): an explicit human decision required when safe automated recovery cannot determine a unique outcome.

## Specification
Each normative rule MUST have one owning RFC and section. Other RFCs MUST reference the owner instead of paraphrasing the requirement. RFC-044 owns transport invariance; RFC-045 owns settlement and recovery; RFC-046 owns baseline system/threat assumptions; RFC-047 owns canonical serialization and identifier grammar; RFC-048 owns 2flow identity and migration.

The repository MUST maintain a dependency graph generated from Requires, Updates, and Obsoletes metadata. CI MUST flag unknown references and cycles in normative Requires dependencies.

## 2flow interaction
Flow and settlement terminology MUST follow the definitions owned by RFC-048 and RFC-045 respectively.

## Security considerations
Ambiguous ownership can create policy bypasses and incompatible implementations. Duplicate normative definitions MUST be treated as a correctness risk.

## Privacy considerations
Terminology and logs SHOULD avoid encoding personal data into identifiers or traces.

## Backward compatibility
This glossary supplements existing Drafts; conflicts MUST be resolved before any affected RFC advances to Candidate.

## Conformance
The linter MUST validate metadata and required sections for changed RFCs. Dependency checks MUST flag unknown references and cycles.

## References
- RFC-000
- RFC-044
- RFC-045
- RFC-046
- RFC-047
- RFC-048
