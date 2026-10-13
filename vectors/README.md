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

## Executable reference checks

Run the standard-library checks from the repository root:

```sh
python3 .github/scripts/test_conformance.py
python3 .github/scripts/test_uesp_e3.py
```

The RFC-045 JSON vectors cover an E1 crash after provider effect but before settlement, and an E3 outcome-unknown case that must be quarantined without automatic retry. The RFC-047 fixture checks one JCS-compatible JSON projection, its SHA-256 digest, semantic-address grammar examples, and NATS/MQTT mapping examples.

These scripts are reference-oracle checks for the published fixtures. They do not establish production-runtime correctness or cross-implementation interoperability. A runtime must execute the same vectors against its own persistence, adapter, provider-idempotency, and recovery implementations; independent implementations must then compare outputs before a conformance claim is justified.
