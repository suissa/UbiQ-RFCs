# RFC-021 — eXtreme Zero Trust Transport

- Status: Draft
- Category: Standards Track

## Abstract

This RFC defines UbiQ's transport security posture: transport encryption is necessary evidence but never sufficient trust.

## Requirements

Bindings SHOULD use authenticated encryption in transit. Deployments MAY combine mTLS, DPoP-like proof of possession, ephemeral keys, hardware-backed keys, and post-quantum or hybrid key establishment according to policy.

Security context MUST be bound to semantic identity and audience. Reconnection requires re-verification; an old connection's trust state MUST NOT be blindly copied to a new path.

The runtime MUST prevent silent downgrade from a stronger required security profile to a weaker fallback transport.

Long-lived bearer secrets SHOULD be avoided. Proof-of-possession and short-lived credentials are preferred.

Cryptographic algorithms MUST be replaceable without changing domain event names or 2flow contracts.

## Principle

Trust is continuously evidenced at semantic boundaries; it is not inherited merely because bytes arrived through a previously authenticated channel.