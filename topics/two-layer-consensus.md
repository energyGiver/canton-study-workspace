# Two-Layer Consensus

**Structured coverage:** definition; why it exists; actors/components; responsibilities; state/data; end-to-end mechanism; relationships with other concepts; authorization; trust; privacy; constraints; failure/exception conditions; operational implications; relevant use cases; common misconceptions; unresolved questions; official sources.

## Decision and mental model

Two-layer consensus separates application correctness from event ordering: stakeholder participants validate authorized Daml effects, while a synchronizer supplies common order/time and mediated finality. Neither layer alone provides the documented transaction guarantees. [SRC-D410EC0803 / Two-Layer Consensus / “The Two Layers”](../corpus/docs/overview/learn/two-layer-consensus.md#the-two-layers) [SRC-46FF0D4718 / Ordering Consensus / introductory distinction](../corpus/docs/overview/reference/ordering-consensus.md)

## Definition, purpose, actors, and state

**Smart contract consensus / Proof of Stakeholder** limits validation to participants hosting contract stakeholders. Those nodes re-execute visible Daml consequences, verify authority/signatures, check relevant ACS inputs, and send signed responses. **Ordering consensus** establishes the total order and timestamps on one synchronizer, distributes protocol messages, and enables the mediator to decide against a common sequence/deadline. [SRC-5883AA972A / Smart Contract Consensus / “Peer-to-Peer Validation”](../corpus/docs/overview/reference/smart-contract-consensus.md#peer-to-peer-validation) [SRC-46FF0D4718 / Ordering Consensus / “Sequencer Nodes”](../corpus/docs/overview/reference/ordering-consensus.md#sequencer-nodes)

| Layer | Principal actors | State/knowledge | Output |
| --- | --- | --- | --- |
| Smart contract | Submitting/confirming/observing participants | Entitled views, packages, ACS, topology | Signed approve/reject per confirmation policy |
| Ordering/mediation | Sequencers, orderer nodes, mediators | Ciphertext/metadata, total order/time, confirmation state | Ordered delivery and final transaction verdict |

## End-to-end relationship

The submitter proposes encrypted views plus confirmation metadata. Ordering makes the request and all responses part of one synchronizer sequence. Participants validate independently against their local projection and topology snapshot. The mediator counts responses per signatory/threshold and returns one verdict; participants apply that verdict to their local views. Conflicting consumes are serialized, so a later conflicting validation observes an already consumed input and rejects. [SRC-A3F46FF397 / Transaction Lifecycle / “Phase 3” through “Phase 5”](../corpus/docs/overview/reference/transaction-lifecycle.md#phase-3-sequencing-and-distribution)

## Authorization, trust, and privacy

Proof of Stakeholder’s confirmation policy is signatory-based: each required signatory’s hosting/confirmation threshold must be met. Observers receive relevant views but are not required to approve solely because they observe. Multi-hosting turns one party’s confirmation into an m-of-n hosting decision, trading availability against compromise tolerance. [SRC-5883AA972A / Smart Contract Consensus / “Confirmation Policies”](../corpus/docs/overview/reference/smart-contract-consensus.md#confirmation-policies)

Participants trust their own validator(s) and required counterparties for timely confirmation, and the synchronizer operator set for safe/live ordering and correct aggregation. The ordering layer cannot validate application semantics without plaintext; stakeholder nodes cannot establish a common synchronizer-wide order alone. Payload encryption limits the ordering layer’s content visibility but not its documented metadata. [SRC-1C97EEFEFD / Trust Model Overview / “Synchronizer”](../corpus/docs/overview/learn/trust-model.md#3-synchronizer)

For the native BFT orderer, the reference states safety/liveness under fewer than one-third Byzantine nodes, unbroken cryptography, shared fate of co-located orderer/sequencer, correct governance/onboarding, and uncorrupted storage. Those are conditions, not unconditional guarantees. [SRC-46FF0D4718 / Ordering Consensus / “BFT Trust Model”](../corpus/docs/overview/reference/ordering-consensus.md#bft-trust-model)

## Constraints and failure modes

- The total order is per synchronizer; time/order are not globally comparable across different synchronizers. [SRC-92FDECC024 / Reassignment Protocol / “Updates stream ordering”](../corpus/docs/overview/reference/reassignment-protocol.md#updates-stream-ordering)
- Any required signatory threshold not met by deadline rejects the transaction.
- Byzantine/fault assumptions differ by participant hosting topology, mediator group, and orderer backend; “2/3 honest” must identify which set and property it refers to.
- A private single-operator synchronizer centralizes ordering/availability trust even though participant validation remains stakeholder-scoped. [SRC-46FF0D4718 / Ordering Consensus / “Centralized vs. Decentralized Options”](../corpus/docs/overview/reference/ordering-consensus.md#centralized-vs-decentralized-options)

## Operational implications and use cases

Operators choose party confirmation thresholds and synchronizer backend/operator governance as separate risk decisions. Monitoring must cover participant confirmation liveness and synchronizer orderer/mediator health. This layered model supports private transactions between mutually distrustful organizations while avoiding global execution of every workflow.

## Common misconceptions and unresolved questions

- Proof of Stakeholder is not token stake or global validator voting.
- A mediator verdict does not mean the mediator re-executed Daml.
- BFT of the Global Synchronizer does not remove trust in one’s participant or contract counterparties.
- `OQ-003` tracks inconsistent wording about whether mediator infrastructure uses encrypted confirmation messages only, sees informee policies, or uses BFT state-machine replication with what exact threshold.

## Official sources

- [Two-Layer Consensus](https://docs.canton.network/overview/learn/two-layer-consensus.md)
- [Smart Contract Consensus](https://docs.canton.network/overview/reference/smart-contract-consensus.md)
- [Ordering Consensus](https://docs.canton.network/overview/reference/ordering-consensus.md)
- [Transaction Lifecycle](https://docs.canton.network/overview/reference/transaction-lifecycle.md)
