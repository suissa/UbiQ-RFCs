# RFC-056 — Adapter ABI and Supply-Chain Verification

- Status: Draft
- Category: Standards Track
- Scope: transport, trust
- Created: 2026-10-13
- Requires: RFC-005, RFC-026, RFC-046
- Updates: RFC-005, RFC-030
- Obsoletes: —
- Threats addressed: A3, A4

## Abstract
This RFC defines the requirements for a stable adapter interface, memory ownership, error mapping, ABI versioning, and artifact verification.

## Motivation
A logical lifecycle API is not enough to load independently developed adapters safely across language and compiler boundaries.

## Terminology
ABI is the binary calling convention and data ownership contract between runtime and adapter. An artifact attestation binds a built artifact to its source and build process.

## Specification
A conforming native adapter ABI MUST define a stable versioned interface for initialization, capability reporting, send, receive/poll, health, backpressure/pressure, and close. It MUST define memory ownership, allocation/free rules, threading and callback behavior, cancellation, deadlines, error codes, and major/minor compatibility. An unknown incompatible major version MUST be rejected.

The capability manifest MUST be canonical, schema-validated, and bound to the adapter version. Runtime policy MUST distinguish self-declared capabilities from capabilities verified by a versioned conformance suite. A signed manifest SHOULD include the suite identifier, version, result, and digest.

Before loading a native adapter, the runtime MUST verify artifact identity and the configured trust policy. Deployments SHOULD use signed provenance/attestation (for example, Sigstore/cosign). Adapters MUST NOT receive runtime signing private keys; sensitive operations MUST use a constrained signing service or brokered capability.

A WASM Component Model profile MAY be offered for stronger isolation, but its host imports, resource limits, and capability access MUST be specified.

## 2flow interaction
Adapter failures MUST map to the shared failure taxonomy and MUST NOT advance a flow without required settlement evidence.

## Security considerations
Native adapters execute with process-level privileges unless sandboxed. Verification failure MUST prevent loading.

## Privacy considerations
Adapter diagnostics MUST redact payloads and secrets by default.

## Backward compatibility
ABI major versions are incompatible unless an explicit compatibility layer is provided.

## Conformance
Tests MUST cover ABI version mismatch, malformed manifests, ownership violations, timeout/cancellation, error mapping, unsigned artifacts, and attempted access to signing keys.

## References
- RFC-005
- RFC-026
- RFC-030
