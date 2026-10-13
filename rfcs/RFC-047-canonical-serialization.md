# RFC-047 — Canonical Serialization and Wire Identifiers

- Status: Draft
- Category: Standards Track
- Scope: semantic, trust, transport
- Created: 2026-10-13
- Requires: RFC-001, RFC-003, RFC-019, RFC-022, RFC-046
- Updates: RFC-001, RFC-002, RFC-003, RFC-019
- Obsoletes: —
- Threats addressed: A1, A3, A5

## Abstract
This RFC proposes deterministic byte-level representation for UbiQ protocol objects, stable message identifiers, semantic-address grammar, and explicit mapping rules for transport identifiers.

## Motivation
Terms such as deterministic, reversible, and canonical digest are not interoperable unless implementations agree on exact bytes, field presence, identifier syntax, and escaping.

## Terminology
Canonical serialization is a single byte representation for a logical object. A projection is a human-readable representation that is not automatically authoritative for signatures.

## Specification
The initial Draft profile MUST use deterministic CBOR as defined by RFC 8949 §4.2 for signed or hashed protocol objects. Parsers MUST reject duplicate map keys, invalid UTF-8, and values outside the schema. Missing fields and explicit null values MUST remain distinguishable.

JSON MAY be used as a human-readable projection. Where a textual JSON digest is required, implementations MUST use JCS (RFC 8785). The active profile MUST identify the representation used for each digest and signature. Canonicalization profile and version MUST be domain-separated in digest and signature inputs.

For profile v1, message_id MUST be UUIDv7 as specified by RFC 9562. It remains immutable across redelivery and multipath copies. Semantic mutation MUST create a new message identifier and preserve causal references. execution_id MUST be issuer-qualified as issuer-id/uuidv7, with issuer bound to an authenticated principal or explicit delegation.

### Semantic address grammar
The v1 address is ASCII-only: entity.action.state. Entity uses PascalCase ASCII letters and digits; action uses lowercase letters, digits, and hyphens; state is requested, accepted, completed, failed, rejected, cancelled, or an extension beginning x-. Each component MUST be 1–64 characters and the full address MUST NOT exceed 192 octets. Wildcards and separators with special meaning in common transports, including *, >, +, #, slash, backslash, and whitespace, are prohibited. Private states MUST use the x- prefix.

### Transport mapping
| Binding | Mapping | Reversibility |
|---|---|---|
| NATS | Subject equals canonical address | Exact |
| MQTT | Replace dot with slash | Exact because slash is prohibited in the address |
| HTTP | POST /v1/events/{semantic-address} using standard path-segment encoding | Exact after one decoding pass |
| Kafka | Carry canonical address in ubiq-name header; topic is binding configuration | Exact in header |

Adapters MUST reject invalid or ambiguous mappings and MUST NOT normalize malformed input into a different semantic address.

### Local substrate framing
A runtime MAY use a compact local log header for storage efficiency. It is not the interoperable envelope. The mapping from local fields to canonical envelope MUST be documented and round-trip tested. Local sequence numbers or status bits MUST NOT be confused with global message identity.

## 2flow interaction
Canonical execution and flow digests MUST use the serialization profile selected by the pinned contract.

## Security considerations
Signatures and digests MUST cover canonical bytes with a domain/version prefix. Parsers MUST limit object size, nesting depth, and collection lengths.

## Privacy considerations
Digesting low-entropy plaintext can leak equality or enable confirmation attacks. Encrypted payload profiles SHOULD hash ciphertext or use an explicitly specified salted commitment.

## Backward compatibility
This Draft profile does not silently redefine existing encodings. A binding MUST negotiate or explicitly configure the profile version.

## Conformance
Versioned vectors MUST cover canonical bytes, invalid names, digests, and per-binding round trips. Independent implementations MUST produce identical canonical bytes and digests.

## References
- RFC 8949
- RFC 8785
- RFC 9562
