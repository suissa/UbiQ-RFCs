# RFC-055 — Request/Response and Streaming Safety

- Status: Draft
- Category: Standards Track
- Scope: semantic, execution, trust, transport
- Created: 2026-10-13
- Requires: RFC-002, RFC-019, RFC-038, RFC-039, RFC-046, RFC-047
- Updates: RFC-038, RFC-039
- Obsoletes: —
- Threats addressed: A1, A2, A3, A5

## Abstract
This RFC defines safe reply routing, cancellation and deadline propagation, stream integrity, and resumable-stream tokens.

## Motivation
Unbound reply addresses enable reflection and exfiltration; streams need item-level integrity and resume proof when transports change.

## Terminology
A resume token authorizes continuation from a particular committed stream checkpoint. A checkpoint is durable evidence of the last accepted item.

## Specification
reply_to MUST be owned by the requesting principal and authorized for the intended response action. A responder MUST reject arbitrary reply addresses, unauthorized destinations, and mismatched audience values. Requests MUST carry an explicit deadline or a policy-bounded default. Cancellation MUST be authenticated, authorized, and correlated to the operation. Deadlines MUST NOT be extended silently across retries or transport migration.

Stream items MUST have monotonically increasing sequence numbers and integrity binding to the previous item or an equivalent authenticated batch structure. Checkpoints MUST bind stream_id, last accepted sequence, and digest. A resume token MUST be short-lived, single-use, bound to the consumer's key, and include a unique token identifier. Resume MUST verify proof of key possession, token expiry, non-reuse, and that the requested sequence equals the last committed checkpoint.

## 2flow interaction
Cancellation does not prove that a remote effect did not occur; UESP reconciliation remains mandatory.

## Security considerations
Reply capabilities MUST be scoped and non-transferable unless explicitly delegated. Resume tokens MUST NOT be reusable bearer credentials.

## Privacy considerations
Stream checkpoints SHOULD contain digests and opaque references rather than payload content.

## Backward compatibility
Older clients without bound reply/resume proofs require a separate legacy profile.

## Conformance
Tests MUST cover reply redirection, expired deadlines, cancellation races, modified stream items, token replay, key mismatch, and resume from a non-committed sequence.

## References
- RFC-038
- RFC-039
- RFC-045
- RFC-047
