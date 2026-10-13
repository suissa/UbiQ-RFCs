# RFC-000 — UbiQ RFC Process

- Status: Draft
- Category: Process
- Scope: semantic, execution, trust, transport
- Created: 2026-10-13
- Requires: RFC-049
- Updates: —
- Obsoletes: —
- Threats addressed: A3, A5

## Abstract
This RFC defines how UbiQ specifications evolve without allowing implementation convenience to silently redefine protocol semantics.

## Motivation
A protocol specification needs predictable status transitions, review rules, mandatory structure, evidence thresholds, and a clear way to resolve errors and conflicting requirements.

## Terminology
- Standards Track: normative protocol behavior.
- Process: governance and lifecycle rules.
- Informational: architecture and rationale without new normative protocol behavior.
- Exploratory: early ideas that are not yet suitable for interoperability claims.
- Independent implementation: implementation with a distinct codebase and implementation team, not a wrapper around the same protocol engine.

## Specification

### Lifecycle
An RFC progresses through Draft → Experimental → Candidate → Stable. Rejected, Withdrawn, Deprecated, and Superseded are historical or terminal states.

Promotion to Experimental requires a complete specification, threat assumptions, initial conformance vectors, and review of all blocking issues. Promotion to Candidate requires at least one implementation and passing mandatory vectors for the declared profile. Promotion to Stable MUST require two independent interoperable implementations, passing vectors, documented security review, and no unresolved P0 issues. Equivalent evidence is not a substitute for independent implementations unless maintainers document the exception and its rationale publicly.

Breaking changes to a Stable RFC require a new RFC or explicit major protocol version. Editorial corrections MAY be applied without changing semantics. Every change to a normative requirement MUST identify the owning RFC and section.

### Categories
- Standards Track: normative protocol behavior.
- Process: project governance.
- Informational: architecture and rationale.
- Exploratory: research and unproven proposals.

Status and Category are separate fields. Experimental is a lifecycle status, not a category.

### Design rule
An RFC MUST state whether its rule belongs to semantic, execution, trust, or transport scope. Transport-specific behavior MUST NOT leak into the semantic contract unless represented as an explicit capability.

### Required document structure
Every RFC MUST include Status, Category, Scope, Created, Requires, Updates, Obsoletes, Threats addressed, Abstract, Motivation, Terminology, Specification, 2flow interaction, Security considerations, Privacy considerations, Backward compatibility, Conformance, and References. Sections may explicitly state “Not applicable” with a reason; omission is not equivalent to non-applicability.

Normative terms follow RFC 2119 and RFC 8174. Each normative rule MUST have one owning RFC and section. Other RFCs MUST reference that owner instead of duplicating the rule.

### Governance and review
A proposal SHOULD remain open for public review for at least 7 calendar days before lifecycle promotion, except for urgent security fixes. Reviewers MUST disclose material conflicts of interest. Maintainers MUST record the decision, rationale, unresolved objections, and any exception to the normal evidence threshold in the RFC or its linked review record.

The project MUST publish the current editors/maintainers and the procedure for proposing changes. An RFC author MUST NOT be the sole approver of their own promotion to Candidate or Stable.

### Errata and supersession
Editorial errata MUST be recorded without changing normative meaning. A correction changing observable behavior requires a new revision with explicit Updates/Obsoletes metadata and a compatibility note. Superseded RFCs MUST link to their successor and remain available for historical review.

### Conformance and CI
The repository MUST lint required metadata and sections for every new or changed RFC. It MUST maintain versioned conformance vectors and a dependency graph from Requires, Updates, and Obsoletes. Unknown RFC references and dependency cycles MUST fail CI unless explicitly allowlisted with a documented reason.

Stable promotion MUST require two independent implementations that pass the same mandatory vector set for the claimed profile. Passing a self-authored test suite alone is insufficient.

## 2flow interaction
RFCs affecting execution MUST state their effect on pinned flow identity, transition validation, recovery, and settlement.

## Security considerations
Lifecycle status MUST NOT be presented as evidence of security review unless the required review actually occurred. Security-sensitive changes SHOULD receive review by someone other than the author.

## Privacy considerations
Review artifacts and test vectors MUST NOT contain real secrets or unnecessary personal data. Security reports MAY use a private disclosure process until remediation is available.

## Backward compatibility
Changes to the process do not retroactively promote existing Drafts. Existing RFCs are migrated to the required structure incrementally, and the CI ratchet MUST enforce the current template on changed documents.

## Conformance
A conforming repository MUST enforce this document's structure and lifecycle gates in CI and publish the required evidence before promotion.

## References
- RFC 2119
- RFC 8174
- RFC-049
