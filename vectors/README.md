# UbiQ Conformance Vectors

Conformance vectors are versioned test inputs and expected outcomes. Every vector MUST include a stable ID, profile, steps, expected result, and the RFC/version it tests. Secrets and real personal data MUST NOT be included.

Suggested layout:
- vectors/RFC-047/: canonical bytes, digest, identifiers, valid/invalid semantic addresses.
- vectors/RFC-045/: crash recovery and settlement boundaries.
- vectors/RFC-044/: cross-binding semantic-equivalence corpus.
- vectors/RFC-048/: normalized 2flow AST and migration cases.

Incremental profiles:
- Core: envelope, names, canonical bytes, semantic identity.
- Secure: proof verification, authorization, replay, downgrade rejection.
- Durable: write-ahead intent, atomic settlement/outbox, fencing, reconciliation.
- Federated: peer identity, delegation, hop limits, loop rejection.

A profile MUST declare mandatory vectors and MUST NOT claim conformance when a required vector is skipped.
