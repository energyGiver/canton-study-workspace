# Canton Concept and Documentation Map

## Decision

The recommended learning path starts with party authority and participant-local state, then adds contract lifecycle/privacy, then ordering/mediation, and only afterward introduces multi-synchronizer routing, Global governance/economics, integrations and operations. This order prevents public-blockchain analogies from assigning the wrong responsibilities to synchronizers or validators.

## Dependency map

| Learn first | Why it is prerequisite | Concepts that depend on it | Research note |
| --- | --- | --- | --- |
| Party, topology, hosting | Establishes identity, authority, storage and confirmation location | Daml roles, privacy, consensus, external signing, reassignment | [Identity and Authorization](../topics/identity-authorization.md) |
| Participant vs validator | Establishes local state/API/operational boundary | Transaction validation, PQS, wallet custody, recovery | [Participant and Validator](../topics/participant-validator.md) |
| Daml contract/action model | Establishes immutable state, action trees and structural authorization | Transaction views, composition, DvP, application architecture | [Daml Application Model](../topics/daml-application-model.md) |
| Transaction lifecycle | Establishes preparation, messages, validation and finality | Privacy, Proof of Stakeholder, mediator failures | [Transaction Lifecycle](../topics/transaction-lifecycle.md) |
| Visibility/trust model | Establishes who sees payload/metadata and whom users trust | Institutional privacy, wallets, private-vs-Global choice | [Privacy and Visibility](../topics/privacy-visibility.md) |
| Two-layer consensus | Establishes correctness vs ordering roles | Sequencer/mediator and Global BFT/governance | [Two-Layer Consensus](../topics/two-layer-consensus.md) |
| Synchronizer assignation | Establishes one order domain per transaction | Multi-synchronizer routing, hybrid architecture, cross-domain DvP | [Synchronizers and Reassignment](../topics/synchronizers-reassignment.md) |
| Application stack | Establishes read/write/automation/IAM boundaries | Integrations and operational architecture | [Ledger API and Application Architecture](../topics/ledger-api-app-architecture.md) |
| Global/SV governance | Establishes shared infrastructure and governed network services | CC traffic/rewards, validator onboarding, Scan, upgrades | [Global Synchronizer](../topics/global-synchronizer.md) |

## Major domains and cross-links

| Domain | Central question | Primary concepts/components | Related notes |
| --- | --- | --- | --- |
| Ledger/application model | What state exists and who can change it? | Templates, contracts, choices, signatories, controllers, ACS | Daml model, identity, transactions |
| Privacy | Who receives which payload and metadata? | Stakeholders, witnesses/views, encryption, hosting, Scan | Privacy, participant, integrations |
| Smart-contract consensus | Who validates correctness? | Proof of Stakeholder, CPN threshold, Daml conformance | Consensus, transactions |
| Ordering/mediation | How is conflict order/finality coordinated? | Orderer, sequencer, mediator, deadline/verdict | Sequencer/mediator, Global |
| Multi-synchronizer | How does state move between trust/order domains? | Assignation, router, unassign/assign, time proof | Reassignment, private-vs-Global |
| Global network services | How is public infrastructure operated/governed/funded? | SV, DSO party, Scan, CC, traffic, rewards | Global, governance, economics |
| Application/integrations | How do users and enterprise systems interact? | Ledger API, PQS, backend, wallet, custody, token standards | App architecture, wallets/exchanges |
| Operations | What preserves confidentiality/availability/recovery? | Keys/KMS, backup, pruning, upgrade, monitoring | Operations, participant |
| Institutional/RWA | Which mechanisms satisfy business constraints? | Regulated ownership, DvP, auditor views, off-ledger controls | Institutional/RWA, privacy, multi-sync |

## Diagram index

- [Concept prerequisites](prerequisites.mmd) references the topic learning order.
- [System architecture](architecture.mmd) references architecture, participant and synchronizer notes.
- [Actor/component relationships](actor-relationships.mmd) references identity, application and governance notes.
- [Transaction lifecycle](transaction-flow.mmd) references the five-phase protocol note.
- [Trust boundaries](trust-boundaries.mmd) references the selective trust analysis.
- [Privacy boundaries](privacy-boundaries.mmd) references payload/metadata visibility.
- [Synchronizer architecture](synchronizer-architecture.mmd) references ordering and multi-synchronizer notes.
- [Application stack](application-stack.mmd) references Ledger API/PQS/backend design.
- [Governance/economics](governance-economics.mmd) references SV, traffic and reward notes.

## Documentation authority map

The Overview `learn` pages establish accessible mental models; Overview `reference` pages are preferred when they give more precise protocol behavior; App Development pages define Daml/API/application patterns; Global Synchronizer pages define network operations/Splice/private synchronizers; Integrations pages define wallet/exchange requirements. When these conflict, the claim remains `UNCLEAR` regardless of navigation hierarchy. Exact source IDs, paths, headings, timestamps and checksums are in `corpus/manifest.jsonl`.

## Known cross-domain tension points

- Privacy overview vs protocol metadata: [CLM-017](../claims/claim-ledger.md) / `OQ-001`.
- Reassignment atomic vs non-atomic wording: [CLM-024](../claims/claim-ledger.md) / `OQ-012`.
- Global current ordering backend: [CLM-030](../claims/claim-ledger.md) / `OQ-008`.
- Marker vs traffic-based app rewards: [CLM-033](../claims/claim-ledger.md) / `OQ-017`.
- Encrypted Global protocol vs public CC/Scan data: `OQ-007`.
