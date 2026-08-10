# Transactions and Contract Lifecycle

**Structured coverage:** definition; why it exists; actors/components; responsibilities; state/data; end-to-end mechanism; relationships with other concepts; authorization; trust; privacy; constraints; failure/exception conditions; operational implications; relevant use cases; common misconceptions; unresolved questions; official sources.

## Decision and mental model

A Canton transaction is a privacy-partitioned, atomically decided action tree. Contract state changes only after sequenced stakeholder validation and a mediator verdict; preparation and confirmation failures leave the ACS unchanged. [SRC-A3F46FF397 / Transaction Lifecycle / “Transaction Lifecycle” and “Failure Modes”](../corpus/docs/overview/reference/transaction-lifecycle.md)

## Definition and purpose

Contracts are immutable active facts. A create adds a contract; a consuming exercise archives its target and can create successors; a non-consuming exercise leaves its target active; fetch reads a contract inside interpretation. A transaction groups those actions and consequences so the result is all-or-nothing. [SRC-AE0BEF4683 / The Ledger Model / “Contracts as UTXOs” and “Transaction Structure”](../corpus/docs/overview/learn/ledger-model.md#contracts-as-utxos)

The protocol exists to let independent participants agree on valid changes to their shared contract projections without revealing unrelated transaction subtrees. It binds partial views to one transaction with cryptographic hashes and combines participant confirmation with synchronizer ordering. [SRC-A3F46FF397 / Transaction Lifecycle / “Subtransaction Privacy”](../corpus/docs/overview/reference/transaction-lifecycle.md#subtransaction-privacy)

## Actors, state, and responsibilities

| Actor | Responsibility | State/data |
| --- | --- | --- |
| Application | Submit command and observe completion/update | Command ID, workflow context |
| Submitting participant | Interpret full command context available to it; determine informees; build views/root hash | ACS inputs, transaction tree, encrypted view batch |
| Sequencer | Assign order/time and deliver addressed messages | Envelopes and ordering metadata |
| Confirming participant | Validate entitled views and respond | Local ACS/topology/packages, decrypted views |
| Mediator | Evaluate responses against per-view policy | Root hash, informees, thresholds, responses/deadline |
| Informee participant | Apply/discard its local projection after verdict | Committed transaction/history and ACS |

## Five-phase mechanism

1. **Preparation:** the submitting participant interprets the command, determines informees, decomposes actions into Merkle-linked views, encrypts them for recipient groups, and computes a root hash.
2. **Submission:** it sends one sequencer batch containing encrypted views, recipient root-hash messages, and mediator informee/confirmation-policy messages.
3. **Sequencing/distribution:** the sequencer gives the batch a position/timestamp and delivers only addressed material; the mediator starts the decision deadline.
4. **Validation/confirmation:** receiving participants check decryption/structure, Daml conformance, authorization, input activity/consistency, time bounds, and root-hash binding, then send approve/reject responses through the sequencer.
5. **Aggregation/commit:** the mediator applies signatory/hosting thresholds. It sends a verdict through the sequencer; participants atomically apply creates/archives or discard the proposal. [SRC-A3F46FF397 / Transaction Lifecycle / “Phase 1” through “Phase 5”](../corpus/docs/overview/reference/transaction-lifecycle.md#phase-1-preparation)

The sequenced approve/reject result is documented as final, with no forks or reorganizations. Within one synchronizer, ordering plus local ACS conflict checks ensures that two attempts to consume the same contract cannot both commit. [SRC-A3F46FF397 / Transaction Lifecycle / “Local commit or discard”](../corpus/docs/overview/reference/transaction-lifecycle.md#phase-5-aggregation-and-commit) [SRC-5883AA972A / Smart Contract Consensus / “Consistency”](../corpus/docs/overview/reference/smart-contract-consensus.md#security-properties)

## Authorization, trust, and privacy boundaries

Create/exercise authorization comes from Daml signatories/controllers and the transaction authority context; topology resolves which participants can confirm for those parties. Confirming participants must trust their own execution/state and the synchronizer’s ordered delivery, while counterparties cannot cause an invalid change involving an honest required confirmer. [SRC-70BD5CED78 / Authorization Model / “Daml’s authorization model”](../corpus/docs/appdev/modules/m3-authorization.md#damls-authorization-model) [SRC-5883AA972A / Smart Contract Consensus / “Security Properties”](../corpus/docs/overview/reference/smart-contract-consensus.md#security-properties)

Payload visibility is view-scoped, but protocol infrastructure retains/observes metadata. The detailed lifecycle states that participants persist sequencer messages they receive and the sequencer may persist encrypted views for a limited period; the mediator receives informee lists and outcomes. Therefore “no full payload access” must not be rewritten as “no observable metadata.” [SRC-A3F46FF397 / Transaction Lifecycle / “Subtransaction Privacy” and “Submission”](../corpus/docs/overview/reference/transaction-lifecycle.md#subtransaction-privacy)

## Constraints, failures, and operations

- Preparation can fail synchronously for missing contracts, authorization, assertions, package or interpretation problems.
- A participant rejects malformed/nonconformant views, inactive inputs, bad time bounds, inconsistent roots, or unauthorized actions.
- A required threshold not reached before `decisionTimeout` rejects the whole transaction.
- Participants or synchronizer services being offline/overloaded reduce liveness, not atomicity; rejected work applies no state.
- Inputs assigned to different synchronizers must first be brought to one admissible synchronizer through reassignment. [SRC-A3F46FF397 / Transaction Lifecycle / “Timing and Deadlines” and “Failure Modes”](../corpus/docs/overview/reference/transaction-lifecycle.md#timing-and-deadlines) [SRC-CB6BCAA81A / Multi-Synchronizer Architecture / “Transactions with Multiple Synchronizers”](../corpus/docs/overview/learn/multi-synchronizer.md#transactions-with-multiple-synchronizers)

Applications need idempotent retry and command-deduplication strategies because a client can lose the completion response even when the ledger outcome is final. Read/automation loops should re-query current state rather than replaying only the failed submission step. [SRC-E077DDE543 / Canton Network Application Architecture Design / “Write” and “Automate on-ledger workflows”](../corpus/docs/appdev/deep-dives/app-architecture-design.md#automate-on-ledger-workflows)

## Use cases, misconceptions, and unresolved questions

Atomic DvP, multi-party approval, token transfer, and cross-application composition use the same mechanism: all required consequences and authorizations are one tree/verdict. “Two-layer consensus” does not mean two independent commits; ordering supports one mediated transaction decision.

- “No single node sees the full transaction” conflicts with preparation wording that the submitting participant produces a full transaction tree from the command/context it can interpret. `OQ-002` requests a precise visibility statement.
- The simplified view model says each action node becomes a view; detailed protocol semantics may be more nuanced. Runtime/source verification is deferred in `OQ-011`.

## Official sources

- [Transaction Lifecycle](https://docs.canton.network/overview/reference/transaction-lifecycle.md)
- [Smart Contract Consensus](https://docs.canton.network/overview/reference/smart-contract-consensus.md)
- [The Ledger Model](https://docs.canton.network/overview/learn/ledger-model.md)
