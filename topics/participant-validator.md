# Participant and Validator

**Structured coverage:** definition; why it exists; actors/components; responsibilities; state/data; end-to-end mechanism; relationships with other concepts; authorization; trust; privacy; constraints; failure/exception conditions; operational implications; relevant use cases; common misconceptions; unresolved questions; official sources.

## Decision and mental model

A participant node is the privacy-sensitive Canton runtime; a Canton Network validator is the operational product stack that embeds a participant and adds Splice/network services. Keeping the distinction explicit prevents wallet automation, traffic management, and Scan access from being mistaken for protocol-engine responsibilities. [SRC-E183CD5ECF / Validator Node Components / “How the Layers Relate”](../corpus/docs/overview/reference/validator-node-components.md#how-the-layers-relate)

## Definition, purpose, components, and state

The participant hosts parties, exposes Ledger/Admin APIs, interprets Daml, maintains the local ACS and history, stores topology/package information, and participates in preparation/validation/confirmation. The validator layer adds a Validator App, Splice/Token Standard DARs, wallet/CNS interfaces, JSON API exposure, Scan proxy, traffic top-up, onboarding, and application automation. [SRC-E183CD5ECF / Validator Node Components / “Canton Participant” and “Splice Layer”](../corpus/docs/overview/reference/validator-node-components.md#canton-participant)

| Component | Responsibility | Persistent/operational state |
| --- | --- | --- |
| Daml engine | Interpret commands and validate received views | Packages and deterministic execution inputs |
| ACS/ledger store | Local active state and retained history | Contracts visible to hosted parties, transactions/offsets |
| Protocol layer | Prepare, encrypt, submit, validate, confirm, apply verdicts | Sequencer client messages, locks, protocol state |
| Topology/package store | Resolve keys/hosting/permissions and vetted code | Sequenced topology snapshots and vetting state |
| Validator App | Onboarding, party/user management, wallet/reward/traffic automation | App DB, configuration, network migration state |
| PQS | Optional read-side SQL projection | Denormalized active and historical data |

## End-to-end responsibilities

On submission, the participant interprets the command, builds the transaction/view structure, and submits encrypted protocol messages. On receipt, it decrypts the entitled views, checks Daml conformance, authorization, ACS consistency, time bounds, and root-hash binding, then sends its confirmation through the sequencer. It changes its ACS only after an approve verdict. [SRC-A3F46FF397 / Transaction Lifecycle / “Phase 1,” “Phase 4,” and “Phase 5”](../corpus/docs/overview/reference/transaction-lifecycle.md#phase-1-preparation)

On reads, the Ledger API exposes party-filtered streams/state and PQS can maintain an SQL projection. PQS is passive and does not submit ledger writes. App backends should preserve offset consistency, retry whole tasks against current projections, and make submissions idempotent. [SRC-E183CD5ECF / Validator Node Components / “PQS”](../corpus/docs/overview/reference/validator-node-components.md#pqs-participant-query-store) [SRC-E077DDE543 / Canton Network Application Architecture Design / “Provision higher-level APIs” and “Automate on-ledger workflows”](../corpus/docs/appdev/deep-dives/app-architecture-design.md#provision-higher-level-apis)

## Authorization, trust, and privacy

The operator controls API exposure, IAM, package vetting, keys for local parties, database access, pruning, backup, and synchronizer connections. A hosted party therefore trusts the operator for confidentiality, availability, correct state, and confirmation; external signing can retain transaction-signing authority outside the validator. [SRC-1C97EEFEFD / Trust Model Overview / “Your Validator”](../corpus/docs/overview/learn/trust-model.md#1-your-validator)

The participant stores contract data when hosted parties are stakeholders and may learn additional material through transaction visibility/disclosure rules. It does not hold a global ledger replica. A validator hosting many parties is a shared privacy/traffic/operational boundary because all those parties use the same infrastructure and, on the Global Synchronizer, share a participant-level traffic balance. [SRC-E183CD5ECF / Validator Node Components / “Active Contract Set” and “Traffic Management”](../corpus/docs/overview/reference/validator-node-components.md#active-contract-set-acs)

## Constraints and failure conditions

- Offline/unreachable required participant: commands may not progress and mediated confirmation can time out. [SRC-A3F46FF397 / Transaction Lifecycle / “Timeout”](../corpus/docs/overview/reference/transaction-lifecycle.md#failure-modes)
- Missing/unvetted packages, stale topology, inconsistent ACS, or invalid authorization: preparation or validation rejects. [SRC-A3F46FF397 / Transaction Lifecycle / “Validation and Confirmation”](../corpus/docs/overview/reference/transaction-lifecycle.md#phase-4-validation-and-confirmation)
- Lost identity keys without usable identity/database backup or retained KMS keys can prevent asset recovery. [SRC-7C4FD68B51 / Validator Disaster Recovery / introductory recovery conditions](../corpus/docs/global-synchronizer/production-operations/validator-disaster-recovery.md)
- Pruning bounds history but removes Ledger API-visible events; audit/proof systems must retain their own required history. [SRC-2F6E09F38B / Pruning / “Participant node pruning”](../corpus/docs/global-synchronizer/production-operations/pruning.md#participant-node-pruning)
- Traffic exhaustion can reject Global Synchronizer submissions; the Validator App can automate top-ups but those top-ups also need reserved traffic. [SRC-E183CD5ECF / Validator Node Components / “Traffic Management”](../corpus/docs/overview/reference/validator-node-components.md#traffic-management)

## Operational implications and use cases

Operators must secure APIs/databases/keys, monitor health and ACS commitments, back up identity plus ordered databases, test/coordinate upgrades, size history and pruning, and maintain all network environments required by their integration model. Wallet/exchange operators additionally become custodians of customer-private ledger data even when end users retain signing keys. [SRC-DC3C1AFD58 / Validator Roles and Responsibilities / “Infrastructure Operations” and “Security Responsibilities”](../corpus/docs/global-synchronizer/understand/validator-roles.md#infrastructure-operations) [SRC-A1E2F651DD / Canton Network Overview / “Implications for Wallet Providers”](../corpus/docs/integrations/wallets-and-exchanges/canton-network-overview.md#implications-for-wallet-providers)

## Common misconceptions and unresolved questions

- A participant is not a stateless RPC gateway; its local state is essential.
- A validator does not join the Global Synchronizer’s BFT orderer merely by validating stakeholder transactions.
- External keys do not eliminate validator data custody.
- The overview corpus contains unfinished participant/monitoring text, so `OQ-009` tracks which operational guidance is production-authoritative.

## Official sources

- [Validator Node Components](https://docs.canton.network/overview/reference/validator-node-components.md)
- [Transaction Lifecycle](https://docs.canton.network/overview/reference/transaction-lifecycle.md)
- [Validator Roles and Responsibilities](https://docs.canton.network/global-synchronizer/understand/validator-roles.md)
- [Validator Disaster Recovery](https://docs.canton.network/global-synchronizer/production-operations/validator-disaster-recovery.md)
