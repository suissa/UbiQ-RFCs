# RFC-045 — UbiQ Execution Settlement Protocol (UESP)

- Status: Draft
- Category: Standards Track
- Scope: execution
- Created: 2026-10-13
- Requires: RFC-002, RFC-004, RFC-009, RFC-010, RFC-017, RFC-026, RFC-028, RFC-041, RFC-046, RFC-048
- Updates: RFC-004, RFC-009, RFC-010, RFC-017, RFC-028, RFC-041
- Obsoletes: —
- Threats addressed: A3, A4, A5

## Abstract
UESP defines when a UbiQ execution step is considered irreversibly known by the orchestration runtime, enabling deterministic recovery without confusing transport acknowledgement with business completion.

## Motivation
Without durable intent before dispatch, atomic settlement/output persistence, and fencing, a crash or stale execution owner can cause an irreversible external effect to be repeated or incorrectly reported as complete.

## Terminology
- Intent: durable record that an effect attempt is about to be invoked.
- Settlement: durable record of a known attempt outcome.
- Effect class: the recovery capabilities available for an action.
- Fencing epoch: monotonic owner generation used to reject stale writes.
- Transactional outbox: atomic persistence of settlement evidence and resulting output messages.

## Specification

### Write-ahead intent
Before invoking an adapter that may produce an external effect, the runtime MUST durably append an Intent containing execution_id, flow_digest, node_id, attempt_id, idempotency scope/key, input_message_id, and fencing epoch. The adapter MUST NOT be invoked until the intent crosses the configured durability boundary.

After dispatch, the runtime MUST persist Settlement and any resulting OutputMessage atomically, using a transactional outbox or an equivalent atomic commit mechanism. A transport ACK MUST NOT be sent before the required settlement/output commit has succeeded.

On recovery, an Intent without a matching Settlement MUST be classified as effect-unknown. The runtime MUST reconcile it using provider evidence, idempotency lookup, or an explicitly authorized human decision; it MUST NOT blindly re-invoke an effect whose outcome is unknown.

### Fencing and ownership
At most one active incarnation may commit state for an execution_id at a time. Each ownership acquisition MUST receive a monotonically increasing epoch. Every log append MUST include the epoch and expected log version; the storage layer MUST reject stale epochs and version conflicts atomically.

The epoch MUST be passed to effect adapters as a fencing token. Where a provider supports fencing, the provider MUST reject operations carrying an older epoch. If the provider does not support fencing, the runtime MUST rely on idempotency/reconciliation and MUST NOT claim stale external writes are fully prevented.

Loss of a lease MUST prevent the old owner from starting new effects. A lease timeout alone does not prove that an already-dispatched effect did not occur.

### Effect classes and effectively-once
Actions MUST declare one effect class:
- E0: pure computation, no external effect.
- E1: external effect deduplicated by a provider-enforced idempotency key.
- E2: external effect with a reliable reconciliation query that can prove applied or not applied.
- E3: irreversible or non-reconcilable effect.

UbiQ MAY claim effectively-once only for E0–E2 when all required storage, deduplication, and provider assumptions hold. E3 MUST NOT be automatically retried after effect-unknown; it requires an explicit human/domain decision or quarantine.

### State machine
Implementations MUST expose equivalent states and valid transitions:
NOT_STARTED → INTENT_PERSISTED → DISPATCHED → SETTLED_SUCCESS | SETTLED_FAILURE
DISPATCHED → EFFECT_UNKNOWN → reconciliation → SETTLED_SUCCESS | SETTLED_FAILURE | NOT_APPLIED
SETTLED_FAILURE → COMPENSATED | QUARANTINED

An unresolved EFFECT_UNKNOWN MUST transition to QUARANTINED after a configured resolution deadline and emit an alert. It MUST NOT silently retry. Compensation is a new declared effect, not deletion or rewriting of prior settlement history.

### Idempotency
Idempotency scope MUST use unambiguous, domain-separated encoding and MUST bind principal, operation, and key. A reused key with a different canonical payload digest MUST be rejected as a conflict. Returning a prior outcome MUST require current authentication and authorization and MUST NOT leak the result to an unauthorized requester. Deduplication retention MUST be at least the maximum redelivery/replay horizon. After expiry, the runtime MUST fail closed rather than assume a key is new. Idempotency keys MUST NOT be used as replay nonces.

### Delivery and settlement
Delivery guarantees and effect guarantees are independent dimensions. A delivery ACK indicates only the transport-defined receipt. A settlement indicates a known execution outcome under the declared effect class. Implementations MUST document both dimensions separately.

## 2flow interaction
A node advances only from valid settlement evidence bound to the pinned flow digest and fencing epoch. Recovery MUST resume at the first unsettled semantic step.

## Security considerations
Settlement records MUST bind execution identity, action, attempt, outcome, input digest, flow digest, and epoch. Authorization MUST be checked before returning stored outcomes. Storage and provider assumptions MUST be visible in the claimed conformance profile.

## Privacy considerations
Settlement records SHOULD store payload digests and references instead of plaintext personal data. Sensitive payload retention and deletion MUST follow the configured privacy policy.

## Backward compatibility
Existing implementations that lack write-ahead intent or fencing MUST NOT claim Durable profile conformance. Rollout requires explicit profile negotiation and migration of in-flight executions.

## Conformance
The crash harness MUST test pre-intent, post-intent, post-dispatch, post-effect/pre-settlement, post-settlement/pre-ACK, and post-ACK boundaries. For E1/E2 test providers, recovery MUST reconcile without duplicating the provider effect. E3 tests MUST prove no blind automatic retry occurs.

## References
- RFC-009
- RFC-010
- RFC-026
- RFC-046
- RFC-048
