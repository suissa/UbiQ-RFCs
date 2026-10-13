# UbiQ RFCs

UbiQ is an **eXtreme Zero Trust semantic messaging layer, transport-independent by design, with verifiable orchestration through 2flow execution contracts**.

The protocol separates four concerns commonly coupled by messaging stacks:

1. **Semantics** — what a message means.
2. **Execution** — how a declared 2flow contract advances.
3. **Trust** — what evidence is required before an operation.
4. **Transport** — how bytes move between endpoints.

A conforming UbiQ application MUST NOT require domain code to know whether a message crossed QUIC, NATS, HTTP, WebSocket, SSE, Kafka, MQTT, RabbitMQ, Redpanda, or another binding.

The central invariant is:

```text
SemanticEffect(deliver(M, T1)) ≡ SemanticEffect(deliver(M, T2))
```

when both transports satisfy the capabilities required by M. RFC-044 is the normative owner of transport invariance; RFC-047 defines the canonical serialization profile, and RFC-045 defines effect settlement. These are Drafts and their guarantees remain conditional on their stated assumptions.

UbiQ does not promise that external systems always succeed or that network delivery is exactly-once. A transport ACK is not business completion, and an unknown external effect must be reconciled rather than blindly retried.

## Normative language

The key words MUST, MUST NOT, REQUIRED, SHOULD, SHOULD NOT, and MAY are interpreted as described by RFC 2119 and RFC 8174.

## RFC index

| RFC | Title |
|---|---|
| 000 | UbiQ RFC Process |
| 001 | Universal Semantic Event Naming |
| 002 | Universal Message Envelope |
| 003 | Universal Semantic Addressing |
| 004 | 2flow Orchestration Assurance |
| 005 | Transport Binding Model |
| 006 | Transport Capability Negotiation |
| 007 | Cross-Protocol Event Translation |
| 008 | Transport Equivalence Contract |
| 009 | Universal Delivery Semantics |
| 010 | Universal Idempotency |
| 011 | Ordering and Causality |
| 012 | Universal Correlation |
| 013 | Subscription Model |
| 014 | Backpressure and Flow Control |
| 015 | Multi-Transport Failover |
| 016 | Multipath Delivery |
| 017 | Cross-Protocol Execution Continuity |
| 018 | Universal Zero-Trust Identity |
| 019 | Proof-of-Origin Message |
| 020 | Replay Protection |
| 021 | eXtreme Zero Trust Transport |
| 022 | Message Confidentiality Envelope |
| 023 | Schema Contract |
| 024 | Schema Evolution |
| 025 | Universal Observability Context |
| 026 | Failure Semantic Model |
| 027 | Intent-Based Healing Protocol |
| 028 | Persistent Event Semantics |
| 029 | Federation Protocol |
| 030 | Adapter ABI |
| 031 | Everything-as-Code Transport Configuration |
| 032 | Transport Selection Policy |
| 033 | Cost-Aware Routing |
| 034 | Latency-Aware Routing |
| 035 | Security-Aware Routing |
| 036 | Semantic Routing |
| 037 | UbiQ Gateway Discovery |
| 038 | Universal Request/Response |
| 039 | Universal Streaming |
| 040 | Universal Pub/Sub |
| 041 | Universal Queue |
| 042 | Protocolless Application Contract |
| 043 | Transportless Actor Model |
| 044 | UbiQ Transport Invariance Principle |
| 045 | UbiQ Execution Settlement Protocol (UESP) |
| 046 | UbiQ System and Threat Model |
| 047 | Canonical Serialization and Wire Identifiers |
| 048 | 2flow Contract Binding |
| 049 | UbiQ Terminology and Normative Ownership |
| 050 | Delivery and Effect Profiles |
| 051 | Authorization Enforcement and Delegation |
| 052 | Federation Identity and Multipath Coordination |
| 053 | Proof Profiles and Resource Budgets |
| 054 | Deterministic and Privacy-Aware Semantic Routing |
| 055 | Request/Response and Streaming Safety |
| 056 | Adapter ABI and Supply-Chain Verification |
| 057 | Secure Configuration, Privacy, and Retention |
| 058 | Typed Capability Registry |
| 059 | Formal Transport Invariance and Equivalence Oracle |

## Conformance and maturity

All RFCs remain Draft until promoted under RFC-000. The repository includes a structural linter, an initial crash-recovery vector, and a profile layout for Core, Secure, Durable, and Federated conformance. Passing structural lint is not proof of protocol interoperability. Stable promotion requires independent implementations and shared passing vectors.

## Repository map

- `rfcs/`: protocol and process specifications.
- `RFC-TEMPLATE.md`: required document structure.
- `vectors/`: versioned conformance vectors.
- `.github/scripts/lint_rfc.py`: RFC metadata/structure lint.
- `.github/workflows/rfc-lint.yml`: pull-request and main-branch validation.

## Licensing note

The existing LICENSE remains unchanged. LICENSE-SPEC, LICENSE-CODE, and PATENTS.md are proposals for clearer separation of specification, reference-code, and patent policy; they do not automatically relicense existing files or establish a patent grant.
