# RFC-014 — Backpressure and Flow Control

- Status: Draft
- Category: Standards Track

## Abstract

Backpressure is normalized across pull, push, stream, queue, and request/reply transports.

## Specification

Each binding MUST expose whether it supports native flow control and how pressure is observed. UbiQ normalizes pressure into capacity signals such as available credits, queue depth, consumer lag, in-flight count, and deadline risk.

The runtime MAY pause, shed, buffer, reroute, or reject work according to policy. It MUST preserve priority and security constraints during rerouting.

Unbounded buffering is non-conforming for bounded deployments. Limits MUST be explicit.

Backpressure MUST NOT cause a 2flow execution to be marked complete before the relevant settlement evidence exists.

## Security

Pressure signals are security-sensitive because forged capacity can induce denial of service or route traffic to weaker transports. Remote capacity claims SHOULD be authenticated where they influence routing.