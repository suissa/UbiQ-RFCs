# UbiQ Conformance Vectors

Conformance vectors are versioned test inputs and expected outcomes. Every vector MUST include a stable ID, profile, steps, expected result, and the RFC/version it tests. Secrets and real personal data MUST NOT be included.

Suggested layout:
- vectors/RFC-047/: canonical bytes, digest, identifiers, valid/invalid semantic addresses.
- vectors/RFC-045/: crash recovery and settlement boundaries.
- vectors/RFC-044/: cross-binding semantic-equivalence corpus.
- vectors/RFC-048/: normalized 2flow AST and migration cases.
- vectors/RFC-059/: cross-binding semantic-identity preservation.

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
python3 .github/scripts/test_transport_invariance.py
```

The RFC-045 JSON vectors cover an E1 crash after provider effect but before settlement, and an E3 outcome-unknown case that must be quarantined without automatic retry. The RFC-047 fixture checks deterministic-CBOR bytes and digest for a deliberately small supported value subset, one JCS-compatible JSON projection and digest, semantic-address grammar examples, and NATS/MQTT mapping examples. The RFC-059 fixture checks that the same semantic address, message ID, execution ID, and digest reference survive NATS, MQTT, HTTP, and Kafka mapping.

These scripts are reference-oracle checks for the published fixtures. They do not establish production-runtime correctness or cross-implementation interoperability. A runtime must execute the same vectors against its own persistence, adapter, provider-idempotency, and recovery implementations; independent implementations must then compare outputs before a conformance claim is justified.

## Executable runtime integration tests

The CI runs the executable reference runtime tests with only Python's standard library:

```sh
python3 -m unittest discover -s tests -v
```

Unlike the vector-oracle checks above, these tests use real SQLite databases for runtime state and a separate persistent SQLite-backed provider simulator. They cover restart recovery after an injected fault, abrupt process termination, no duplicate provider effect under enforced idempotency, E3 quarantine, fencing against stale owners, payload conflicts for reused idempotency keys, and atomic rollback when outbox persistence fails. Transport tests call the executable NATS/MQTT/HTTP/Kafka mapping functions and check round trips and invalid inputs.

This is an executable reference implementation and local provider simulation, not proof that an external production adapter or an independent UbiQ runtime conforms. Those implementations must run equivalent tests against their own systems.
