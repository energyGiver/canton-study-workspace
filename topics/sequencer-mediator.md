# Sequencer and Mediator

**Structured coverage:** definition; why it exists; actors/components; responsibilities; state/data; end-to-end mechanism; relationships with other concepts; authorization; trust; privacy; constraints; failure/exception conditions; operational implications; relevant use cases; common misconceptions; unresolved questions; official sources.

## Decision and mental model

The sequencer is ordered, authenticated message transport; the mediator is the confirmation-policy coordinator. Neither is the participant that stores full contract state or re-executes Daml business logic. [SRC-46FF0D4718 / Ordering Consensus / “Synchronizer Components”](../corpus/docs/overview/reference/ordering-consensus.md#synchronizer-components)

## Definitions and why they exist

The sequencer gives all recipients on a synchronizer a consistent message order/time, routes encrypted envelopes, authenticates delivery, and enforces traffic limits. This provides a deterministic position for conflict resolution and protocol deadlines without broadcasting plaintext. The mediator receives transaction confirmation metadata/responses, determines whether signatory thresholds are satisfied before deadline, and emits a commit/reject verdict. [SRC-46FF0D4718 / Ordering Consensus / “Sequencer Nodes” and “Mediator Nodes”](../corpus/docs/overview/reference/ordering-consensus.md#sequencer-nodes)

## Actors, responsibilities, and state

| Component | Receives | Maintains/observes | Emits |
| --- | --- | --- | --- |
| Sequencer | Submission batches and participant/mediator messages | Total order, timestamps, recipient/size/traffic metadata, encrypted payload retention | Addressed, signed ordered deliveries |
| BFT orderer/backend | Ordering requests from sequencer(s) | Mempool/availability/consensus/output state | Globally ordered blocks/stream for that synchronizer |
| Mediator | Informee/policy message and participant responses via sequencer | Root correlation, informees, thresholds, results, deadline | Transaction result/verdict via sequencer |

Participants and mediators communicate through sequencers rather than direct channels. A synchronizer may have multiple mediator groups and multiple sequencer endpoints/backends. [SRC-46FF0D4718 / Ordering Consensus / “Mediator Nodes”](../corpus/docs/overview/reference/ordering-consensus.md#mediator-nodes)

## End-to-end mechanism

The submitting participant sends a batch of encrypted views/root messages plus the mediator’s informee/policy message. The sequencing backend reaches an order and assigns time, then the sequencer projects the batch to each recipient. Participants validate and return signed responses through the same ordered path. The mediator tracks them against each view/signatory threshold and decision time, then submits its result for ordered delivery to affected participants. [SRC-A3F46FF397 / Transaction Lifecycle / “Submission” through “Aggregation and Commit”](../corpus/docs/overview/reference/transaction-lifecycle.md#phase-2-submission-confirmation-request)

The native BFT orderer reference describes a pipeline of mempool, availability dissemination/proofs, ISS-inspired consensus, and ordered-output reconstruction. It documents fewer-than-one-third Byzantine faults as the safety/liveness threshold, subject to its additional assumptions. The same reference also lists centralized, CometBFT, and native BFT backends; the backend changes trust/operations, not the participant-side Daml validation role. [SRC-46FF0D4718 / Ordering Consensus / “BFT Architecture” and “Centralized vs. Decentralized Options”](../corpus/docs/overview/reference/ordering-consensus.md#bft-architecture)

## Authorization, trust, and privacy boundaries

Topology authorizes synchronizer members/components and informs which participants may confirm for parties. Participant responses and delivered messages are signed; the mediator should count only topology-authorized confirmation nodes. Users trust the sequencer/operator set for order, availability, censorship resistance within its assumptions, and the mediator set for correct aggregation/verdict delivery. [SRC-1AC3D32DF2 / Topology / “Topology management”](../corpus/docs/overview/reference/topology.md#topology-management) [SRC-1C97EEFEFD / Trust Model Overview / “Synchronizer”](../corpus/docs/overview/learn/trust-model.md#3-synchronizer)

Payload privacy is cryptographic, but sequencers see routing/size/time and mediators see informee/confirmation information. Recipient sender privacy is described as stripping sender identity from delivery; that does not establish that the sequencer itself lacks sender metadata. [SRC-46FF0D4718 / Ordering Consensus / “Sequencer Nodes”](../corpus/docs/overview/reference/ordering-consensus.md#sequencer-nodes)

## Constraints, failures, and operations

- Traffic exhaustion rejects submissions before ordering.
- Sequencer unavailability/censorship blocks progress; inconsistent order violates safety.
- Mediator unavailability or missing responses reaches deadline and rejects.
- Orderer safety/liveness depends on backend quorum, network and storage assumptions.
- Multiple sequencer connections/trust thresholds can improve client resilience but add endpoint/certificate/operational complexity. [SRC-BF9D21A402 / Connecting a Validator to Multiple Synchronizers / “Connect to decentralized Sequencers”](../corpus/docs/global-synchronizer/extension-synchronizers/linking-validator-multi-sync.md#connect-to-decentralized-sequencers)

## Use cases, misconceptions, and unresolved questions

The pair supports every same-synchronizer transaction, whether the synchronizer is private or Global. Private deployments can centralize or distribute ordering trust; the Global Synchronizer distributes infrastructure across SVs.

- The sequencer is not a mempool/blockchain that stores public application state.
- The mediator is not an application validator and does not approve business logic from plaintext.
- “Synchronizer sees only ciphertext” omits mediator policy/verdict metadata; see `OQ-001`.
- The corpus alternates between native BFT and current CometBFT descriptions for Global Synchronizer components; `OQ-008` asks which backend applies by network/version.

## Official sources

- [Ordering Consensus](https://docs.canton.network/overview/reference/ordering-consensus.md)
- [Transaction Lifecycle](https://docs.canton.network/overview/reference/transaction-lifecycle.md)
- [Global Synchronizer Architecture](https://docs.canton.network/overview/learn/global-synchronizer-architecture.md)
