# RFC-002 — Universal Message Envelope

- Status: Draft
- Category: Standards Track
- Scope: semantic, trust, transport
- Created: 2026-10-13
- Requires: RFC-001, RFC-003, RFC-019, RFC-020, RFC-022, RFC-047
- Updates: —
- Obsoletes: —
- Threats addressed: A1, A2, A3, A5

## Abstract
This RFC defines the transport-neutral UbiQ message envelope and its required semantics. The exact canonical encoding is specified by RFC-047.

## Motivation
The envelope must contain or unambiguously reference every field required by routing, security, federation, retries, deadlines, streaming, and settlement. A single causal parent cannot represent joins in a parallel flow.

## Terminology
A message is an immutable semantic occurrence. A delivery attempt is a transport-level attempt to deliver that occurrence. A settlement records the known outcome of an execution attempt; it is not equivalent to a transport acknowledgement.

## Specification

### Required fields
A v1 message MUST carry or resolve the following fields:
- ubiq_ver: protocol envelope version; integer.
- message_id: UUIDv7, immutable across redelivery and multipath.
- semantic_address: canonical address as defined by RFC-047.
- created_at: RFC 3339 timestamp; informational and not an ordering authority.
- payload: typed content or encrypted payload envelope.

A message that can cause an effect MUST carry expires_at or be governed by an explicitly named policy that bounds validity. When proof is present, audience MUST be bound to the intended recipient or service. A federated message MUST carry bounded hop information. The following fields MUST be present when their feature is used: causation_ids for causal parents; correlation_id for interaction grouping; flow and execution identity for 2flow execution; sequence for declared ordering; deadline for deadline-governed operations; priority for priority-aware routing; reply_to for request/response; schema_ref for schema-governed payloads; proof for proof-of-origin; encryption metadata for encrypted payloads; attempt metadata for delivery/settlement records.

The canonical field registry, field types, optionality, and CBOR tags MUST be maintained alongside the versioned envelope schema. Unknown critical fields MUST cause rejection; unknown non-critical extension fields MAY be preserved and ignored according to the profile.

### Causality and retries
causation_ids is a set of zero or more message identifiers and MUST preserve every causal parent of a join. A message identifier MUST remain stable for redelivery and multipath. A new semantic message caused by a retry decision MUST use a new message identifier and refer to the prior message through causation_ids.

Transport attempt identifiers and attempt counts are not semantic message identity. They MUST be recorded as delivery or settlement metadata and MUST NOT change message_id.

### Deadlines and cancellation
Deadlines MUST use a single documented representation per profile and MUST NOT be extended silently during failover. Cancellation MUST identify the operation being cancelled and be authorized independently. Expiration and cancellation do not prove that an external effect did not occur; RFC-045 governs reconciliation.

### Payload and proof
Payload mutation after identity establishment MUST create a new message. Security proof MUST cover the canonical identity-critical fields and payload representation required by RFC-019 and RFC-022. Field absence and explicit null MUST be distinguishable.

### Canonical encoding
RFC-047 owns canonical serialization, identifier grammar, and transport mappings. This RFC does not define an alternative encoding.

## 2flow interaction
Flow and execution identity MUST be pinned as defined by RFC-048. Joins MUST preserve all causal parent identifiers. A transport ACK MUST NOT advance a flow without settlement evidence required by RFC-045.

## Security considerations
The receiver MUST validate protocol version, expiration, audience, proof, authorization, and replay controls before processing an effect. It MUST reject malformed or ambiguous addresses.

## Privacy considerations
Implementations SHOULD minimize exposed routing metadata and MUST NOT place secrets or unnecessary personal data in identifiers, traces, or public digests.

## Backward compatibility
An envelope version MUST identify its schema. A receiver MUST reject unsupported major versions rather than silently downgrade. Additive fields are compatible only when the active profile defines them as non-critical extensions.

## Conformance
Vectors MUST test field presence, null-versus-absent encoding, multiple causal parents, stable identity under redelivery, expiration, audience validation, and round-trip preservation across bindings.

## References
- RFC-047
- RFC-048
- RFC-045
- RFC-019
- RFC-020
- RFC-022
