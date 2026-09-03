# RFC-027 — Intent-Based Healing Protocol

- Status: Draft
- Category: Standards Track

## Abstract

Healing attempts to preserve the original semantic intent rather than blindly repeating the failed mechanism.

## Specification

A healing policy receives the intended semantic outcome, failure class, execution state, available evidence, capabilities, and constraints. It MAY select retry, alternate binding, alternate provider, transformed input, compensation, deferred execution, or Human-in-the-Healing-Loop.

Healing MUST NOT broaden authorization or weaken REQUIRED security constraints. It MUST NOT silently change the user's or caller's intent.

Each healing attempt MUST produce auditable causation evidence and remain attached to the same logical execution unless policy explicitly starts a new one.

A retry of an external effect MUST obey RFC-010 idempotency and RFC-045 settlement.

## 2flow

Healing paths SHOULD be declared in 2flow whenever predictable. Dynamic healing MAY select among declared admissible paths but MUST NOT invent an undeclared business transition.