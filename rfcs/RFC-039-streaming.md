# RFC-039 — Universal Streaming

- Status: Draft
- Category: Standards Track

## Abstract

UbiQ models a logical stream independently of QUIC streams, WebSocket sessions, SSE, broker streams, or chunked HTTP.

## Specification

A stream has stable semantic identity, producer/consumer principals, ordered or unordered mode, lifecycle, flow-control policy, and item schema.

Transport migration MAY continue the same logical stream if continuity evidence proves the last accepted item/sequence. The new transport MUST NOT silently duplicate already settled items.

End, cancel, error, and resume are semantic lifecycle events and MUST be distinguishable from a transient transport disconnect.

Backpressure follows RFC-014. Security re-verification is required when binding a logical stream to a new transport session.

## Conformance

A resumable implementation MUST demonstrate disconnection and continuation without changing the logical stream identifier.