# RFC-046 — UbiQ System and Threat Model

- Status: Draft
- Category: Standards Track
- Scope: trust, execution, transport
- Created: 2026-10-13
- Requires: RFC-000
- Updates: —
- Obsoletes: —
- Threats addressed: A1, A2, A3, A4, A5

## Abstract
This RFC defines baseline failure, storage, network, and adversary assumptions against which UbiQ guarantees are evaluated. A guarantee without its assumptions MUST NOT be advertised as unconditional.

## Motivation
Security and recovery requirements are not auditable when implementations may silently assume reliable networks, durable writes, trusted adapters, or benign federation peers.

## Terminology
- Crash-recovery node: a process may stop and restart; volatile memory is lost while committed durable state remains available under the configured durability profile.
- Durable commit: a commit acknowledged only after the storage engine's documented durability boundary has been satisfied.
- PEP: Policy Enforcement Point, enforcing an authorization decision.
- PDP: Policy Decision Point, evaluating policy.
- Fencing token: a monotonically increasing epoch used to reject operations from stale owners.

## Specification
The baseline model MUST permit message loss, duplication, delay, and reordering. A deployment claiming partition-tolerant recovery MUST document its partial-synchrony assumptions and timeout policy. Nodes use crash-recovery, not Byzantine fault tolerance, unless a profile explicitly states otherwise.

A durable write MUST NOT be acknowledged before the durability boundary named by the active profile. Implementations MUST publish whether this includes local fsync, replicated quorum, or both.

### Adversaries
- A1 — Network attacker: observes, injects, drops, delays, reorders, and replays traffic.
- A2 — Honest-but-curious intermediary: forwards traffic but may inspect metadata available to it.
- A3 — Malicious intermediary: tampers with metadata, attempts downgrade, or misroutes messages.
- A4 — Compromised adapter: executes arbitrary code inside the adapter's process boundary.
- A5 — Malicious federated peer: forges identifiers, capabilities, hop claims, or execution claims.

Compromise of a trusted policy enforcement point, host kernel, or signing key is outside the baseline model and MUST be stated as residual risk. Implementations MUST NOT imply end-to-end guarantees survive compromise of an endpoint holding plaintext or signing keys.

### Guarantee-to-assumption matrix
| Guarantee | Required assumptions | Limit |
|---|---|---|
| Transport invariance | Binding passes versioned conformance corpus; required capabilities verified | Equal timing is not implied |
| Effectively-once | Durable intent, scoped linearizable deduplication, effect class E0/E1/E2 | Not claimable for unreconcilable E3 effects |
| Proof of origin | Trusted key binding, canonical signed input, approved algorithm, key lifecycle | Does not prove truth or authorization |
| Confidentiality | Correct cryptography and endpoint key protection | Visible routing metadata may leak |
| Federation continuity | Authenticated peer identity, bounded hop path, explicit delegation | Trust is not transitively inherited |
| Durable recovery | Storage profile and fencing guarantees hold | Hardware corruption beyond profile is not covered |

Every RFC strengthening a security or recovery guarantee MUST identify relevant adversaries A1–A5, assumptions, and residual risks.

## 2flow interaction
A runtime MUST bind recovery and settlement claims to the declared execution identity and pinned contract version.

## Security considerations
Threat labels aid review but do not replace threat analysis. Implementations MUST fail closed when a required identity, proof, epoch, or policy version cannot be verified.

## Privacy considerations
Payload minimization, retention, deletion, and metadata leakage MUST be evaluated separately from integrity and durability.

## Backward compatibility
This RFC introduces a shared model and does not retroactively make Draft guarantees unconditional.

## Conformance
A conforming implementation MUST publish its storage durability profile, trust boundaries, supported adversaries, and claimed guarantees. Tests MUST include loss, duplication, reordering, restart, and stale-owner scenarios.

## References
- RFC 2119
- RFC 8174
- RFC 8949
