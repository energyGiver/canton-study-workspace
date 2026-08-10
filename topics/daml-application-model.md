# Daml Application Model

**Structured coverage:** definition; why it exists; actors/components; responsibilities; state/data; end-to-end mechanism; relationships with other concepts; authorization; trust; privacy; constraints; failure/exception conditions; operational implications; relevant use cases; common misconceptions; unresolved questions; official sources.

## Decision and mental model

Daml models shared multi-party facts and rights, not autonomous mutable objects. Contracts are immutable template instances; external actors advance workflows by creating contracts or exercising choices, which produces an atomic transaction tree. [SRC-09A4FB7F13 / Contract Templates / “Daml ledger basics”](../corpus/docs/appdev/modules/m3-contract-templates.md#daml-ledger-basics) [SRC-E077DDE543 / Canton Network Application Architecture Design / “Automate on-ledger workflows”](../corpus/docs/appdev/deep-dives/app-architecture-design.md#automate-on-ledger-workflows)

## Definition and why it exists

A Daml template defines contract data, signatories, observers, and choices. A contract is active from its committed creation until committed archival; it cannot be mutated in place. This makes state transitions explicit and lets stakeholders independently verify the same permitted workflow while retaining audience-scoped visibility. [SRC-258861A679 / Core Concepts / “Smart Contracts (Templates)”](../corpus/docs/overview/understand/core-concepts.md#smart-contracts-templates)

## Actors, components, state, and responsibilities

| Construct/actor | Responsibility | State/data effect |
| --- | --- | --- |
| Template | Defines a contract type and its authorization/visibility surface | Compiles through Daml-LF into a DAR/package |
| Contract | Immutable instance/fact | Enters/leaves the ACS through create/archive |
| Signatory | Authorizes contract creation and sees the contract | Required authorizer for create |
| Observer | Receives contract visibility | No authority unless also a controller |
| Choice/controller | Declares a permitted action and required actor | Consuming choice archives; non-consuming choice retains |
| Daml engine | Interprets commands and re-validates transaction consequences | Deterministic transaction/action tree |
| Backend/automation | Supplies time/events/integration and submits commands | Off-ledger task/IAM/integration state |

## End-to-end mechanism

1. A client submits create/exercise commands as one or more parties.
2. The Daml engine evaluates templates/choices against known active contracts and produces an action tree containing creates, exercises, fetches, and consequences.
3. Authorization is checked structurally at every action boundary: required authorizers must be provided by the parent context.
4. Canton decomposes the tree into views, coordinates stakeholder validation, and commits all actions or none.
5. Consumed contracts leave the ACS and created contracts enter it; application readers observe only events visible to their requested parties. [SRC-7A10561336 / Choices / “Choices in the ledger model”](../corpus/docs/appdev/modules/m3-choices.md#choices-in-the-ledger-model) [SRC-70BD5CED78 / Authorization Model / “Daml’s authorization model”](../corpus/docs/appdev/modules/m3-authorization.md#damls-authorization-model)

Proposal/accept is the documented pattern when a future signatory has not yet authorized a contract. Role contracts can encode continuing delegation. Atomic composition lets one choice exercise/fetch/create across application packages when all required packages, contracts, parties, and authorization are available. [SRC-70BD5CED78 / Authorization Model / “Use Propose-Accept” and “Use role contracts”](../corpus/docs/appdev/modules/m3-authorization.md#use-propose-accept-workflow-for-one-off-authorization)

## Authorization, trust, and privacy boundaries

Signatories/observers define contract stakeholders and persistent visibility; controllers define choice authority. Transaction witnesses can receive additional views needed to validate consequences, so privacy must be designed across the entire composed transaction rather than template fields in isolation. Daml authorization protects ledger transitions, but off-ledger authentication, business checks, data sources, and user permissions remain backend responsibilities. [SRC-5506826606 / Privacy Model Explained / “Stakeholder Visibility Rules” and “Divulgence”](../corpus/docs/overview/learn/privacy-model.md#stakeholder-visibility-rules) [SRC-E077DDE543 / Canton Network Application Architecture Design / “Integrate with off-ledger systems”](../corpus/docs/appdev/deep-dives/app-architecture-design.md#integrate-with-off-ledger-systems)

Application users trust deployed/vetted package logic and the organizations controlling signatory/automation parties. Participant nodes re-execute visible Daml consequences, but documentation-only research has not verified compiler/runtime behavior or package implementation. [SRC-5883AA972A / Smart Contract Consensus / “What Each Confirming Participant Does”](../corpus/docs/overview/reference/smart-contract-consensus.md#what-each-confirming-participant-does)

## Constraints, failures, and operations

- Daml has no independent execution thread or external API access; backends must trigger time/state/external workflows. [SRC-E077DDE543 / Canton Network Application Architecture Design / “Automate on-ledger workflows”](../corpus/docs/appdev/deep-dives/app-architecture-design.md#automate-on-ledger-workflows)
- Missing authority, inactive inputs, failed assertions, missing/vetting-incompatible packages, time-bound violations, and disclosure errors can reject before or during confirmation. [SRC-A3F46FF397 / Transaction Lifecycle / “Failure Modes”](../corpus/docs/overview/reference/transaction-lifecycle.md#failure-modes)
- Active “event log” contracts can cause unbounded ACS growth; the architecture guide recommends historical PQS events for completed workflow history where suitable. [SRC-E077DDE543 / Canton Network Application Architecture Design / “Provision higher-level APIs”](../corpus/docs/appdev/deep-dives/app-architecture-design.md#provision-higher-level-apis)
- Upgrades require package compatibility and coordinated deployment across participants that may validate the workflows; exact upgrade mechanics are outside this topic but are part of operations planning.

## Relevant use cases

The model fits bilateral agreements, regulated token ownership, proposals/acceptance, payment instructions, delivery-versus-payment, workflow delegation, audit-observer patterns, and cross-application atomic composition. Field-level secrecy must be modeled with separate contracts/views for distinct audiences; observers see the contract payload they observe. [SRC-24BF8E1094 / Use Cases / “Supply Chain Finance”](../corpus/docs/overview/understand/use-cases.md#supply-chain-finance)

## Common misconceptions and unresolved questions

- A Daml contract is not mutable storage with methods; consuming transitions archive/create facts.
- A controller is not automatically a signatory or persistent observer.
- Backend access control cannot replace Daml authorization for shared ledger guarantees.
- `OQ-006` tracks conflicting/over-broad descriptions of who receives fetched or divulged contract data.
- `OQ-010` defers runtime/package-upgrade behavior verification to the later engineering phase.

## Official sources

- [Contract Templates](https://docs.canton.network/appdev/modules/m3-contract-templates.md)
- [Choices](https://docs.canton.network/appdev/modules/m3-choices.md)
- [Authorization Model](https://docs.canton.network/appdev/modules/m3-authorization.md)
- [Canton Network Application Architecture Design](https://docs.canton.network/appdev/deep-dives/app-architecture-design.md)
