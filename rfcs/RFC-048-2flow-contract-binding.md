# RFC-048 — 2flow Contract Binding

- Status: Draft
- Category: Standards Track
- Scope: execution, semantic
- Created: 2026-10-13
- Requires: RFC-004, RFC-017, RFC-027, RFC-045, RFC-046, RFC-047
- Updates: RFC-004, RFC-017, RFC-027, RFC-045
- Obsoletes: —
- Threats addressed: A3, A4, A5

## Abstract
This RFC defines how an execution is pinned to a versioned 2flow contract, how contract identity is computed, and when an in-flight execution may migrate to a new contract.

## Motivation
Orchestration guarantees depend on a declared graph and transition rules. If graph digests depend on formatting or a flow can change mid-execution, independent runtimes cannot agree on allowed transitions.

## Terminology
A normalized AST is a parsed abstract syntax tree with a versioned, deterministic normalization algorithm. A pinned execution is bound to one flow digest until an explicit migration is committed.

## Specification
A 2flow implementation MUST expose a versioned parser and normalized AST. Normalization MUST define node identifiers, operator representation, ordering of unordered collections, literal encoding, and rejection of duplicate or ambiguous node IDs.

The Draft v1 flow digest is SHA-256 over the domain prefix UbiQ/2flow/v1 concatenated with deterministic-CBOR encoding of normalize(AST). This formula MUST NOT be treated as Stable until test vectors and independent implementations are published.

Each execution MUST pin flow_id, flow_digest, and language/profile version at creation. A running execution MUST NOT silently adopt a changed definition.

Every operator MUST define enabled transitions, causality behavior, join rules, cancellation behavior, and settlement requirements. Parallel joins MUST preserve all causation identifiers. A runtime MUST reject any transition not declared by the pinned contract.

Migration to a different digest is denied by default. It MAY proceed only when an authorized, versioned migration map identifies old-to-new nodes and every settled node has an unambiguous equivalent. The runtime MUST append a durable migration record containing old digest, new digest, mapping digest, approver, timestamp, and fencing epoch before any new side effect. If safe mapping cannot be proven, execution MUST remain pinned or enter explicit operator-controlled quarantine. Rewriting history is prohibited.

## 2flow interaction
This RFC defines contract identity and migration; RFC-045 remains the owner of settlement state and effect recovery.

## Security considerations
Contract digests MUST be domain-separated and verified against the authenticated source of the flow. An untrusted peer MUST NOT replace a pinned contract by supplying a new digest.

## Privacy considerations
Flow definitions and node names may expose business logic. Logs SHOULD use access controls and avoid recording sensitive literals unnecessarily.

## Backward compatibility
Existing executions remain pinned to their original definition. Migration to this Draft profile requires an explicit operator-approved mapping.

## Conformance
Tests MUST cover formatting-invariant digests, different digests for semantically different flows, invalid-transition rejection, join causality, and migration denial/approval.

## References
- RFC-004
- RFC-017
- RFC-027
- RFC-045
- RFC-046
- RFC-047
