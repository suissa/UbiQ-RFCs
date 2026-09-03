# UbiQ RFCs

UbiQ is an **eXtreme Zero Trust semantic messaging layer, transport-independent by design, with verifiable orchestration through 2flow execution contracts**.

The protocol separates four concerns that are commonly coupled by messaging stacks:

1. **Semantics** — what a message means.
2. **Execution** — how a declared 2flow contract advances.
3. **Trust** — what evidence is required before every operation.
4. **Transport** — how bytes move between endpoints.

A conforming UbiQ application MUST NOT require domain code to know whether a message crossed QUIC, NATS, HTTP, WebSocket, SSE, Kafka, MQTT, RabbitMQ, Redpanda, or another binding.

The core invariant is:

```text
SemanticEffect(deliver(M, T1)) ≡ SemanticEffect(deliver(M, T2))
```

when both transports satisfy the capabilities required by `M`.

UbiQ additionally guarantees **orchestration integrity**: when an execution is bound to a 2flow contract, the runtime MUST be able to identify the current execution state, allowed transitions, evidence already settled, and the deterministic recovery point. UbiQ does not guarantee that external systems always succeed; it guarantees that execution remains auditable, resumable, and governed by the declared contract.

## Normative language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, and **MAY** are to be interpreted as described by RFC 2119 and RFC 8174.

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

All RFCs are initially **Draft** until an implementation and interoperability evidence promote them through the process defined by RFC-000.
