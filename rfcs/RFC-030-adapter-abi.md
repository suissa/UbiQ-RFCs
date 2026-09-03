# RFC-030 — Adapter ABI

- Status: Draft
- Category: Standards Track

## Abstract

The Adapter ABI allows transports to be added or replaced without recompiling domain logic.

## Required surface

An adapter MUST expose lifecycle, capability description, endpoint configuration validation, send, receive/subscription, health, backpressure signals, and error normalization.

The ABI MUST exchange canonical UbiQ envelope values or a stable binary representation, not transport-native domain types.

Adapters MUST be isolated from application authorization decisions. A compromised adapter SHOULD have the minimum capability necessary to move already-authorized messages.

Version negotiation MUST prevent loading an adapter with an incompatible ABI.

Implementations MAY provide language-specific ABIs, including Zig, Rust, Go, and TypeScript, provided conformance tests prove equivalent behavior.

## Dynamic loading

Runtime-loaded modules MUST be authenticated/verified according to deployment policy before execution.