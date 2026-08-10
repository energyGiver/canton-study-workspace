# Deployment and Operations

**Structured coverage:** definition; why it exists; actors/components; responsibilities; state/data; end-to-end mechanism; relationships with other concepts; authorization; trust; privacy; constraints; failure/exception conditions; operational implications; relevant use cases; common misconceptions; unresolved questions; official sources.

## Decision and mental model

Operational continuity depends on preserving participant identity and ordered state, not merely restarting containers. The minimum control set is secure keys/APIs, identity plus database backups, version-aligned upgrades, health/ACS/traffic monitoring, bounded pruning, and rehearsed recovery. [SRC-6F45F05F6D / Validator Backups](../corpus/docs/global-synchronizer/production-operations/validator-backups.md) [SRC-7C4FD68B51 / Validator Disaster Recovery](../corpus/docs/global-synchronizer/production-operations/validator-disaster-recovery.md)

## Actors, components, state, and responsibilities

The validator operator owns participant/Validator App/PQS/PostgreSQL deployment, identity and party keys, IAM/OIDC/TLS, ingress/egress, synchronizer connections, traffic funding, logs/metrics, backups, pruning, upgrades and incidents. SV/private-synchronizer operators additionally own orderer/sequencer/mediator/governance/Scan infrastructure. [SRC-DC3C1AFD58 / Validator Roles and Responsibilities / “What You Are Responsible For”](../corpus/docs/global-synchronizer/understand/validator-roles.md#what-you-are-responsible-for) [SRC-DA63952FB3 / Super Validator Components / “SV Roles and Responsibilities”](../corpus/docs/overview/reference/super-validator-components.md#sv-roles-and-responsibilities)

Recovery-critical state includes participant namespace/identity keys, participant ledger/protocol/topology databases, Validator App database, synchronizer migration position, external KMS references, and application projections/history. PQS/backups used for audit are distinct from the live participant recovery chain.

## Operational mechanisms

**Keys/security.** By default participant keys may be database-backed; an external KMS can generate/store them. The cited validator guide says migration from non-KMS to KMS or between providers is unsupported and recommends a fresh validator plus asset transfer. Session encryption keys reduce KMS cost but create a configurable in-memory plaintext-key exposure window. [SRC-9EB1F6E5A4 / Validator Security / “Using an external KMS”](../corpus/docs/global-synchronizer/production-operations/validator-security.md#using-an-external-kms-for-managing-participant-keys)

**Backup.** Back up node identities securely and outside the cluster, plus all PostgreSQL instances at least at the documented cadence. The Validator App database backup must be strictly earlier than the participant backup. Historical backups must be closer together than the pruning retention window and retained across logical synchronizer upgrades when required. [SRC-6F45F05F6D / Validator Backups / “Backup of Node Identities” and “Backups of postgres instances”](../corpus/docs/global-synchronizer/production-operations/validator-backups.md#backup-of-node-identities)

**Recovery.** Full restore requires suitable recent database state; the cited guide says backups older than 30 days may not catch up because of sequencer pruning. Identity-only recovery can re-onboard a fresh validator and recover DSO-known assets such as CC/CNS, but not necessarily all private application state. Without database/identity backup or retained KMS keys, relevant private keys and asset ownership proof may be unrecoverable. [SRC-7C4FD68B51 / Validator Disaster Recovery / opening conditions and “Restoring a validator from backups”](../corpus/docs/global-synchronizer/production-operations/validator-disaster-recovery.md#restoring-a-validator-from-backups)

**Pruning.** Automatic/manual participant pruning removes archived/history data to bound storage; take backups, choose retention against audit/downtime needs, monitor `daml_pruning_max_event_age`, and defragment PostgreSQL after deletion. Pruning is an application/API-data decision, not only storage housekeeping. [SRC-2F6E09F38B / Pruning / “Participant node pruning”](../corpus/docs/global-synchronizer/production-operations/pruning.md#participant-node-pruning)

**Monitoring/upgrades.** Monitor component health, synchronizer connectivity, ACS commitments, database/traffic/pruning age, API errors, and network-version deadlines. The monitoring page itself contains an editorial warning that its example scripts/configs are untested and not production-safe, so examples are not adopted as validated runbooks. [SRC-B85835EA73 / Monitoring Setup / introduction and “Intended Use”](../corpus/docs/global-synchronizer/production-operations/monitoring-setup.md#example-monitoring-setup) [SRC-108DB02B24 / Validator Upgrades](../corpus/docs/global-synchronizer/production-operations/validator-upgrades.md)

## Authorization, trust, privacy, constraints, and failures

Operators hold privileged Admin/API/database/backup/KMS access and therefore sit inside the party privacy/trust boundary. Backups/logs/metrics/support bundles must receive the same classification as live ledger data. OIDC rights do not protect a stolen database/identity export. [SRC-1C97EEFEFD / Trust Model Overview / “Your Validator”](../corpus/docs/overview/learn/trust-model.md#1-your-validator)

Failure conditions include lost namespace keys, inconsistent backup ordering, stale backup beyond sequencer retention, logical synchronizer migration mismatch, unsupported KMS migration, outdated network version, exhausted traffic, stuck pruning, database exhaustion, and missing historical evidence after pruning. Some recovery paths restore only public/DSO-shared assets, not every application contract.

## Use cases, misconceptions, and unresolved questions

These controls serve self-hosted validators, wallet/exchange custody, regulated/audited applications, private synchronizer operators and SVs. Exact RPO/RTO/SLA must be chosen by the operator; documentation examples are not a substitute for tests in the future engineering phase.

- Backing up a container volume is not necessarily a consistent identity/app/participant recovery point.
- Pruning does not preserve audit data unless another retained projection/backup does.
- `OQ-009` asks which monitoring/runbook pages are production-authoritative.
- `OQ-021` defers restore rehearsal, backup consistency and RPO/RTO measurement to runtime testing.

## Official sources

- [Validator Backups](https://docs.canton.network/global-synchronizer/production-operations/validator-backups.md)
- [Validator Disaster Recovery](https://docs.canton.network/global-synchronizer/production-operations/validator-disaster-recovery.md)
- [Validator Security](https://docs.canton.network/global-synchronizer/production-operations/validator-security.md)
- [Pruning](https://docs.canton.network/global-synchronizer/production-operations/pruning.md)
- [Monitoring Setup](https://docs.canton.network/global-synchronizer/production-operations/monitoring-setup.md)
