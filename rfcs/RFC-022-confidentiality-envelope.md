# RFC-022 — Message Confidentiality Envelope

- Status: Draft
- Category: Standards Track

## Abstract

End-to-end payload confidentiality MUST survive broker and transport changes.

## Specification

A message MAY carry an encrypted payload envelope whose cryptographic scope is independent of transport encryption. The envelope SHOULD identify algorithm suite, recipient/key reference, nonce, ciphertext, and authenticated associated-data policy.

Identity-critical cleartext metadata that influences authorization SHOULD be authenticated as associated data.

Intermediaries that do not possess decryption capability MAY route using authorized metadata but MUST NOT require plaintext payload access.

Key rotation MUST NOT require renaming semantic events. Re-encryption by a trusted gateway produces auditable cryptographic evidence and MUST preserve message semantics.

## Security

Nonce reuse under algorithms that prohibit it is catastrophic and MUST be prevented. Metadata leakage should be minimized according to deployment threat model.