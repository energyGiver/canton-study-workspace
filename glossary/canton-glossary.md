# Curated Canton Glossary

## Decision

Definitions below preserve official Canton terminology while adding scope where the corpus uses terms inconsistently. They are working research definitions, not replacements for the source glossaries. Conflicts are linked to the open-question registry.

| Term | Working definition | Source / note |
| --- | --- | --- |
| Active Contract Set (ACS) | Contracts currently active in one participant’s ledger projection for its hosted parties. | [Official glossary](../corpus/docs/overview/understand/glossary.md#active-contract-set-acs), [Participant](../topics/participant-validator.md) |
| Actor | Party whose authority is used for an exercised choice in the transaction authorization context. | [Authorization model](../corpus/docs/appdev/modules/m3-authorization.md#damls-authorization-model) |
| Admin API | Privileged node-operations API for topology, packages, parties, connections and related administration. | [Validator components](../corpus/docs/overview/reference/validator-node-components.md#admin-api) |
| Amulet | Daml/application name for the code and logic implementing Canton Coin; some contract/type names retain it. | [Splice glossary](../corpus/docs/global-synchronizer/splice-fundamentals/glossary.md) |
| Assignation | Stakeholders’ agreement about the one synchronizer that coordinates changes to a contract at a given time. | [Multi-synchronizer](../corpus/docs/overview/learn/multi-synchronizer.md#motivation) |
| Assignment | Second reassignment request, making a pending contract active on the target synchronizer. | [Reassignment](../corpus/docs/overview/reference/reassignment-protocol.md#two-step-process-unassignment-and-assignment) |
| Assignment exclusivity | Target-time window in which the unassignment submitter has exclusive right to initiate assignment. | [Reassignment](../corpus/docs/overview/reference/reassignment-protocol.md#assignment-exclusivity) |
| Canton | Protocol/software for privacy-preserving distributed ledgers; distinguish it from the public Canton Network deployment. | [Official glossary](../corpus/docs/overview/understand/glossary.md#canton) |
| Canton Coin (CC) | Utility token/application of the Global Synchronizer, used for extra traffic purchase and governed rewards. | [Tokenomics](../topics/fees-rewards-economics.md) |
| Canton Foundation (CF) | Linux Foundation-hosted body coordinating/supporting Global Synchronizer governance and growth; cited governance says it lacks unilateral on-chain control. | [Governance](../topics/super-validators-governance.md) |
| Canton Network | Public network using Canton and the Global Synchronizer, validators, SVs and Splice services. | [Official glossary](../corpus/docs/overview/understand/glossary.md#canton-network) |
| Choice | Daml action declared on a template and controlled by specified parties; consuming by default unless declared non-consuming. | [Choices](../corpus/docs/appdev/modules/m3-choices.md) |
| Command | Application request to create/exercise ledger actions; interpretation may fail before protocol submission. | [Transaction lifecycle](../topics/transaction-lifecycle.md) |
| Confirming Participant Node (CPN) | Participant authorized by topology to confirm for a hosted party; thresholds can require several CPNs. | [External parties](../corpus/docs/overview/reference/external-party.md) |
| Contract | Immutable instance of a Daml template, active from committed creation until archival. | [Contract templates](../corpus/docs/appdev/modules/m3-contract-templates.md#daml-ledger-basics) |
| Controller | Party whose authority is required to exercise a specific choice. It need not be a signatory/observer outside that action. | [Authorization model](../corpus/docs/appdev/modules/m3-authorization.md#damls-authorization-model) |
| DAR | Archive containing compiled Daml packages for deployment/vetting on participants. | [Official glossary](../corpus/docs/overview/understand/glossary.md#dar-daml-archive) |
| Daml | Functional smart-contract/workflow language compiled to Daml-LF and interpreted by participants. | [Development stack](../corpus/docs/appdev/modules/m1-development-stack.md#daml) |
| Decision time | Sequencing time plus synchronizer decision timeout, after which insufficient confirmation rejects. | [Transaction lifecycle](../corpus/docs/overview/reference/transaction-lifecycle.md#timing-and-deadlines) |
| Divulgence / disclosure | Contract information made available beyond original stakeholder visibility through documented transaction/disclosure mechanisms. Exact witness scope needs clarification. | [Privacy](../topics/privacy-visibility.md), `OQ-006` |
| DSO | Decentralized Synchronizer Operator, the SV collective operating/governing the Global Synchronizer. | [Governance](../topics/super-validators-governance.md) |
| DSO party | Decentralized Daml party hosted by SV participants with a confirmation threshold, used for collective on-ledger authority. | [SV governance reference](../corpus/docs/overview/reference/sv-governance-reference.md#on-chain-governance-architecture) |
| Executing Participant Node (EPN) | For external parties, participant that forwards signed transaction data to the chosen synchronizer and provides completion. | [External party submission](../corpus/docs/overview/reference/external-party.md#submission-flow) |
| Explicit disclosure | Out-of-band contract disclosure supplied with submission so a party can use a reference contract without permanent stakeholder visibility. | [App architecture](../corpus/docs/appdev/deep-dives/app-architecture-design.md#serve-reference-data-contracts) |
| External party | Party with no submission-permission participant and externally controlled signing keys; still needs confirming/observing hosting for state. | [External party](../corpus/docs/overview/reference/external-party.md#external-party) |
| Global Synchronizer | Public/common SV-operated synchronizer plus Splice network services; not a full-state storage layer. | [Global Synchronizer](../topics/global-synchronizer.md) |
| Hosting | Topology relationship by which a participant represents, confirms and/or observes for a party according to permissions. | [Topology](../corpus/docs/overview/reference/topology.md) |
| Informee | Party entitled to information about a transaction action/view and included in protocol confirmation metadata. | [Transaction lifecycle](../corpus/docs/overview/reference/transaction-lifecycle.md#phase-1-preparation) |
| Ledger API | Participant application API for commands, completions, updates, ACS/state and user/rights-controlled access. | [Validator components](../corpus/docs/overview/reference/validator-node-components.md#ledger-api-grpc) |
| Local party | Party whose submission authority/namespace is delegated to a submission participant, suitable for trusted automation. | [External parties](../corpus/docs/overview/reference/external-party.md#local-party) |
| Mediator | Synchronizer component that tracks confirmation policy/responses and issues the transaction verdict; it does not re-run Daml payload logic. | [Sequencer and Mediator](../topics/sequencer-mediator.md) |
| Mining round | Governed Canton Coin accounting period used for fee/price snapshots and rewards; values/behavior are versioned. | [Tokenomics](../corpus/docs/overview/reference/tokenomics-of-gs.md#fee-schedules-and-round-snapshots) |
| Namespace | Cryptographic identity scope rooted in a signing-key fingerprint and used to authorize topology entities/changes. | [Topology](../corpus/docs/overview/reference/topology.md#namespace) |
| Observer | Contract stakeholder with persistent visibility but no choice authority unless separately a controller. | [Core concepts](../corpus/docs/overview/understand/core-concepts.md#party-roles-in-contracts) |
| Observing Participant Node (OPN) | Participant that receives relevant party data/verdicts but does not confirm on the party’s behalf. | [External parties](../corpus/docs/overview/reference/external-party.md) |
| Ordering consensus | Per-synchronizer mechanism establishing a common order/time for protocol messages without validating Daml business logic. | [Ordering consensus](../corpus/docs/overview/reference/ordering-consensus.md) |
| Participant node | Canton runtime hosting parties, Daml engine, local ledger state, APIs and transaction protocol. In some prose it is called validator, but the validator product stack is broader. | [Participant and Validator](../topics/participant-validator.md), `OQ-004` |
| Party | Stable on-ledger identity for authority/visibility, hosted through topology and distinct from a human/API user. | [Identity](../topics/identity-authorization.md) |
| Party-to-participant mapping | Topology mapping of a party to hosting participants, permissions, thresholds and optionally external signing keys. | [Topology](../corpus/docs/overview/reference/topology.md) |
| Preparing Participant Node (PPN) | Participant that turns an external party’s command into reviewable transaction data/hash for signing. | [External party submission](../corpus/docs/overview/reference/external-party.md#submission-flow) |
| Private / extension synchronizer | Dedicated synchronizer with restricted operators/members and operator-defined infrastructure/governance, usable beside Global. | [Private vs Global](../topics/private-vs-global-synchronizer.md) |
| Proof of Stakeholder | Canton smart-contract consensus in which participant nodes hosting affected stakeholders validate/confirm; unrelated global nodes do not. | [Smart contract consensus](../corpus/docs/overview/reference/smart-contract-consensus.md#proof-of-stakeholder) |
| PQS | Participant Query Store, a passive SQL read projection of Ledger API data for queries/history/automation. | [App architecture](../topics/ledger-api-app-architecture.md) |
| Reassigning participant | Participant connected/hosting a stakeholder appropriately on both source and target so it can validate continuity. | [Reassignment](../corpus/docs/overview/reference/reassignment-protocol.md#reassigning-participant) |
| Reassignment | Non-atomic working-model process of source unassignment followed by target assignment. The overview contains contradictory atomic wording. | [Reassignment note](../topics/synchronizers-reassignment.md), `OQ-012` |
| Reassignment counter | Contract counter incremented on unassignment and shared by its matching assignment event. | [Reassignment](../corpus/docs/overview/reference/reassignment-protocol.md#reassignment-counter) |
| Root hash | Cryptographic commitment binding the transaction view tree and correlating confirmation responses. | [Transaction lifecycle](../corpus/docs/overview/reference/transaction-lifecycle.md#phase-1-preparation) |
| Scan | SV-operated application/API indexing public/DSO-visible Global Synchronizer application/governance/economic data. It is not a query endpoint for all private Canton state. | [SV components](../corpus/docs/overview/reference/super-validator-components.md#scan-app) |
| Sequencer | Synchronizer component providing authenticated, timestamped, addressed total-order delivery of encrypted messages on one synchronizer. | [Ordering consensus](../corpus/docs/overview/reference/ordering-consensus.md#sequencer-nodes) |
| Sequencing time | Timestamp/order reference assigned when a sequencer orders a request batch. | [Transaction lifecycle](../corpus/docs/overview/reference/transaction-lifecycle.md#timing-and-deadlines) |
| Signatory | Contract stakeholder whose authority is required for creation and which participates in signatory-based confirmation policy. | [Contract templates](../corpus/docs/appdev/modules/m3-contract-templates.md#signatories) |
| Splice | Project/application suite implementing CC, DSO governance, validator/SV apps, wallets, CNS and related Global services. | [Validator components](../corpus/docs/overview/reference/validator-node-components.md#splice-layer) |
| Stakeholder | Contract signatory or observer; persistent contract visibility/storage follows this role, though transaction witness rules can add views. | [Core concepts](../corpus/docs/overview/understand/core-concepts.md#party-roles-in-contracts) |
| Submission Participant Node (SPN) | Participant with submission permission for a local party; threshold greater than one has restrictions in cited external-party docs. | [External parties](../corpus/docs/overview/reference/external-party.md) |
| Sub-transaction privacy | Merkle/view-based, encrypted distribution of only entitled transaction portions to relevant participants. | [Privacy](../topics/privacy-visibility.md) |
| Super Validator (SV) | Institution/node stack operating validator, synchronizer order/mediation, governance and Scan services for Global. | [SV components](../corpus/docs/overview/reference/super-validator-components.md) |
| Synchronizer | Coordination/trust/order domain consisting of sequencer/mediator infrastructure; it does not hold full contract payload state. | [Sequencer and Mediator](../topics/sequencer-mediator.md) |
| Target timestamp | Fixed target-synchronizer topology time proof used during unassignment validation. | [Reassignment](../corpus/docs/overview/reference/reassignment-protocol.md#target-timestamp) |
| Template | Daml definition of contract payload, signatories/observers and choices; contracts are its instances. | [Contract templates](../corpus/docs/appdev/modules/m3-contract-templates.md#templates) |
| Topology transaction | Signed/sequenced change to identity, key, hosting, package or synchronizer-related topology state. | [Topology](../corpus/docs/overview/reference/topology.md#topology-management) |
| Traffic | Byte-denominated synchronizer capacity/accounting; Global participants get base allocation and burn CC for extra traffic. | [Economics](../topics/fees-rewards-economics.md) |
| Transaction | Atomic Daml action tree coordinated on one synchronizer and committed/rejected by one mediated verdict. | [Transaction lifecycle](../topics/transaction-lifecycle.md) |
| Unassignment | First reassignment request, making a contract inactive on the source and pending assignment. | [Reassignment](../corpus/docs/overview/reference/reassignment-protocol.md#two-step-process-unassignment-and-assignment) |
| Validator | Canton Network operational stack containing a participant plus Validator App/Splice services; ordinary validators do not operate Global orderer/mediator infrastructure. | [Validator components](../corpus/docs/overview/reference/validator-node-components.md) |
| Vetting | Topology approval of a Daml package for use by/on a participant/synchronizer context. | [Official glossary](../corpus/docs/overview/understand/glossary.md#vetting) |
| View | Privacy-scoped portion/projection of a transaction that entitled participants can decrypt/validate. Exact decomposition details are deferred in `OQ-011`. | [Transaction lifecycle](../corpus/docs/overview/reference/transaction-lifecycle.md#subtransaction-privacy) |

## Terminology cautions

- The Splice glossary contains older fee/reward wording that conflicts with post-CIP-0078/CIP-0104 pages; use [the economics note](../topics/fees-rewards-economics.md), not an isolated glossary bullet, for current research.
- “Domain” appears in older names and code/config examples where newer prose says “synchronizer.” Preserve source terminology when quoting identifiers, but use “synchronizer” in analysis.
- “Internal party” appears in some integration prose where protocol/reference pages use “local party.” This workspace uses “local party.”
- “Validator” may refer loosely to a participant in conceptual prose; component/operations notes use the broader validator stack definition.
