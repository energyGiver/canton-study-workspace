# Core Architecture

**Structured coverage:** definition; why it exists; actors/components; responsibilities; state/data; end-to-end mechanism; relationships with other concepts; authorization; trust; privacy; constraints; failure/exception conditions; operational implications; relevant use cases; common misconceptions; unresolved questions; official sources.

## Decision and mental model

Canton should be understood as private participant-maintained ledger projections coordinated through one or more synchronizers. This framing is necessary because treating the synchronizer as a globally replicated chain incorrectly assigns storage and business validation to the ordering layer. [SRC-4125FC3B33 / Architecture Overview / “The Big Picture”](../corpus/docs/overview/learn/architecture.md#the-big-picture)

## Definition and why it exists

A participant node hosts parties, interprets Daml, stores the contracts relevant to those parties, and validates affected transaction views. A synchronizer orders encrypted messages and coordinates confirmation without becoming the authoritative store of full contract state. This separation is designed to combine multi-party integrity with need-to-know data distribution. [SRC-258861A679 / Core Concepts / “Validators” and “Synchronizers”](../corpus/docs/overview/understand/core-concepts.md#validators-participant-nodes) [SRC-5883AA972A / Smart Contract Consensus / “Proof of Stakeholder”](../corpus/docs/overview/reference/smart-contract-consensus.md#proof-of-stakeholder)

## Actors, responsibilities, and state

| Actor/component | Responsibility | State or data involved |
| --- | --- | --- |
| Party | On-ledger identity; acts as signatory, observer, or controller | Party identifier, authority, visibility rights |
| Participant node | Hosts parties, executes Daml, prepares and validates views | Local ACS, transaction history, packages, topology, keys |
| Validator | Canton Network operational bundle containing a participant plus Splice services | Participant state plus wallet, traffic, automation, and app state |
| Sequencer | Authenticated, timestamped, ordered multicast | Encrypted envelopes, routing/size metadata, ordering state |
| Mediator | Aggregates required confirmations and emits verdicts | Informee/confirmation-policy metadata, responses, verdict state |
| Application | Submits commands, reads projections, integrates external systems | Off-ledger identity/session, workflow and integration state |

The validator/participant distinction matters: the participant is the Canton protocol runtime, while the Canton Network validator adds Splice applications such as Canton Coin/wallet automation and network management. [SRC-E183CD5ECF / Validator Node Components / “How the Layers Relate”](../corpus/docs/overview/reference/validator-node-components.md#how-the-layers-relate)

## End-to-end mechanism

1. An application submits a Daml command through a participant’s Ledger API.
2. The submitting participant interprets the command against its available state and constructs a transaction tree and privacy-preserving views.
3. It sends encrypted confirmation material through a synchronizer.
4. The sequencer orders and distributes the material; entitled participants decrypt and validate their views.
5. The mediator evaluates confirmations against the policy and returns a commit/reject verdict through the sequencer.
6. Each involved participant independently updates its local projection on commit or discards the proposed change on rejection. [SRC-A3F46FF397 / Transaction Lifecycle / “Phase 1” through “Phase 5”](../corpus/docs/overview/reference/transaction-lifecycle.md#phase-1-preparation)

## Authorization, trust, and privacy boundaries

Daml contract structure defines required signatories and choice controllers; topology determines which participant nodes may represent or confirm for each party; Ledger API rights determine which authenticated clients may request reads, preparation, or execution. These layers are complementary and must not be conflated. [SRC-70BD5CED78 / Authorization Model / “Daml’s authorization model”](../corpus/docs/appdev/modules/m3-authorization.md#damls-authorization-model) [SRC-1AC3D32DF2 / Topology / “Topology management”](../corpus/docs/overview/reference/topology.md#topology-management) [SRC-4CA0A3A918 / Authorization / “Access Tokens and Rights”](../corpus/docs/appdev/deep-dives/authorization.md#access-tokens-and-rights)

The party owner trusts hosting participants for confidentiality, availability, correct local storage, and confirmation; external signing can remove the hosting node’s unilateral submission authority but not its data/validation role. Synchronizer operators are trusted for ordering, delivery, availability, and correct verdict aggregation, while encryption prevents them from reading transaction payloads under the documented cryptographic assumptions. [SRC-1C97EEFEFD / Trust Model Overview / “Five Trust Domains”](../corpus/docs/overview/learn/trust-model.md#five-trust-domains) [SRC-5BD308B0DF / Local and External Parties / “Trust model”](../corpus/docs/overview/reference/external-party.md#trust-model)

## Constraints, failures, and operations

- A party cannot transact when the required hosting/confirming threshold or synchronizer infrastructure is unavailable; transaction timeouts reject without applying state. [SRC-A3F46FF397 / Transaction Lifecycle / “Failure Modes”](../corpus/docs/overview/reference/transaction-lifecycle.md#failure-modes)
- Data access is localized: applications query a hosting participant or an application/public projection, not a universal RPC containing private network state. [SRC-A1E2F651DD / Canton Network Overview / “Reading Data and Validator State”](../corpus/docs/integrations/wallets-and-exchanges/canton-network-overview.md#reading-data-and-validator-state)
- Multi-synchronizer use requires common eligible topology/package state and may require two-step reassignment before a transaction can execute. [SRC-CB6BCAA81A / Multi-Synchronizer Architecture / “Transactions with Multiple Synchronizers”](../corpus/docs/overview/learn/multi-synchronizer.md#transactions-with-multiple-synchronizers)
- Operational correctness depends on identity backup, database backup, key protection, upgrades, monitoring, traffic capacity, and pruning policy. [SRC-DC3C1AFD58 / Validator Roles and Responsibilities / “What You Are Responsible For”](../corpus/docs/global-synchronizer/understand/validator-roles.md#what-you-are-responsible-for)

## Relationships and use cases

Core architecture supplies the base for sub-transaction privacy, Proof of Stakeholder validation, multi-synchronizer routing, private/global hybrid deployments, Daml application composition, and atomic multi-party settlement. The use-case fit comes from selecting stakeholders and synchronizers so each component sees and controls only what its role requires. [SRC-24BF8E1094 / Use Cases / “When Canton Fits”](../corpus/docs/overview/understand/use-cases.md#when-canton-fits)

## Common misconceptions and unresolved questions

- “The synchronizer is the ledger database” is false; contract payload/state resides with relevant participant nodes.
- “Every validator validates everything” is false; documented validation is stakeholder-scoped.
- “Encrypted payload means no metadata exists” is unsupported: protocol references document routing, timing, size, informee, and verdict metadata. See `OQ-001`.
- “Validator” and “participant” are always interchangeable is imprecise in operations documentation. See `OQ-004`.

## Official sources

- [Architecture Overview](https://docs.canton.network/overview/learn/architecture.md)
- [Core Concepts](https://docs.canton.network/overview/understand/core-concepts.md)
- [Transaction Lifecycle](https://docs.canton.network/overview/reference/transaction-lifecycle.md)
- [Validator Node Components](https://docs.canton.network/overview/reference/validator-node-components.md)
