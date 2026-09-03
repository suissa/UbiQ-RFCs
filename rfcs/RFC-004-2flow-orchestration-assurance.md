# RFC-004 — 2flow Orchestration Assurance

- Status: Draft
- Category: Standards Track

## Abstract

UbiQ provides verifiable orchestration assurance by binding message execution to a declared 2flow contract.

## Contract

A flow execution MUST have a stable `flow_id`, concrete `execution_id`, current node/state, and a version or digest of the 2flow definition. The runtime MUST only accept transitions allowed by that contract.

2flow operators define execution semantics independently of transport, including sequential flow (`->`, `<-`), call/called relations (`->>`, `<<-`), parallel composition, and declared error/healing paths.

UbiQ does **not** guarantee that external effects succeed. It guarantees orchestration integrity: after interruption the runtime can determine what was requested, what was settled, which evidence exists, and which transition may legally occur next.

A transport change MUST NOT create a new logical execution.

## Recovery invariant

If execution stops after settled step `N`, recovery MUST NOT re-run settled side effects unless the step contract explicitly permits replay. The runtime resumes from the first unsettled transition or invokes a declared healing/compensation path.

## Security

The 2flow digest, execution identity, and transition evidence SHOULD be cryptographically bound to settlement records.

## Conformance

A conforming runtime MUST reject undeclared transitions and expose deterministic execution state after restart.