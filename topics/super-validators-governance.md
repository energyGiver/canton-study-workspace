# Super Validators and Governance

**Structured coverage:** definition; why it exists; actors/components; responsibilities; state/data; end-to-end mechanism; relationships with other concepts; authorization; trust; privacy; constraints; failure/exception conditions; operational implications; relevant use cases; common misconceptions; unresolved questions; official sources.

## Decision and mental model

Super Validators combine infrastructure operation with application-level governance. Ordering BFT, decentralized-party confirmation, and Daml vote contracts are distinct thresholds/layers and must not be collapsed into a generic “two-thirds vote.” [SRC-DA63952FB3 / Super Validator Components / “SV Roles and Responsibilities”](../corpus/docs/overview/reference/super-validator-components.md#sv-roles-and-responsibilities) [SRC-4FA5D0A091 / SV Governance Reference / “DSO Governance Model”](../corpus/docs/overview/reference/sv-governance-reference.md#dso-governance-model)

## Definition, purpose, components, and state

An SV runs the regular validator stack plus sequencer, mediator, ordering backend, SV App/UI, Scan App/API/UI and databases. Collectively SVs form the DSO, host a decentralized DSO party, operate the Global Synchronizer, sponsor validators, publish price preferences, vote on membership/config/economics, and expose network data. [SRC-DA63952FB3 / Super Validator Components / “Component Architecture” and “SV-Specific Applications”](../corpus/docs/overview/reference/super-validator-components.md#component-architecture)

Governance state is represented by Daml contracts: `DsoRules` for membership/config, `AmuletRules` for CC configuration schedules, `VoteRequest`/confirmations for proposals, and SV/reward/round state. The cited reference says this state is visible through Scan to parties/API users with the corresponding access. [SRC-4FA5D0A091 / SV Governance Reference / “On-Chain Governance Architecture”](../corpus/docs/overview/reference/sv-governance-reference.md#on-chain-governance-architecture)

## Decision mechanism

Any SV can create a vote request for an `ActionRequiringConfirmation`; SVs accept/reject before a deadline, optionally with a future effective time. Voted actions execute after the documented `requiredNumVotes` threshold, while routine actions can use automated confirmations. Separately, transactions authorized by the decentralized DSO party require its party-hosting confirmation threshold. [SRC-4FA5D0A091 / SV Governance Reference / “Governance Roles,” “Voting Mechanics,” and “On-Chain Governance Architecture”](../corpus/docs/overview/reference/sv-governance-reference.md#governance-roles)

Governed actions include SV admission/removal, featured-app rights, SV reward weights, DSO config, Amulet/economic config, traffic price/scaling, conversion-rate aggregation, round settings and upgrades. CIPs document proposals/standards, but on-chain adoption/execution uses the governance machinery described above. [SRC-4FA5D0A091 / SV Governance Reference / “Types of Governance Actions” and “Parameter Governance”](../corpus/docs/overview/reference/sv-governance-reference.md#types-of-governance-actions)

## Authorization, trust, privacy, and assumptions

SV namespace/party keys, DSO party topology, application vote contracts, and orderer membership each control a different authority. Participants assume no more than the documented Byzantine threshold is dishonest, cryptography/storage/network assumptions hold, and SV operators actually maintain services. The Foundation coordinates and operates one SV per the cited page but is not documented as having unilateral on-chain control. [SRC-4FA5D0A091 / SV Governance Reference / “Canton Foundation” and “BFT Guarantees”](../corpus/docs/overview/reference/sv-governance-reference.md#canton-foundation)

Governance/CC/Scan are deliberately more transparent than private application contracts. This transparency is application/topology-defined, not evidence that synchronizer nodes decrypt unrelated application views. [SRC-DA63952FB3 / Super Validator Components / “Scan API”](../corpus/docs/overview/reference/super-validator-components.md#scan-api)

## Constraints, failures, and operations

- Insufficient votes/confirmations cause rejection or expiry; faulty/absent SVs beyond thresholds can block progress.
- Coordinated upgrades, BFT peer connectivity, Scan consistency, database/key recovery, and public endpoints enlarge the SV operational surface.
- Reward weights/economic parameters are governance inputs and may change; research must cite retrieval/version time.
- Application vote thresholds and decentralized-party confirmation thresholds can differ; satisfying one does not automatically satisfy the other.
- Descriptive phrases such as “roughly two-thirds” must not replace the formulas/current topology. [SRC-4FA5D0A091 / SV Governance Reference / “DSO Governance Model” and “Voting Mechanics”](../corpus/docs/overview/reference/sv-governance-reference.md#dso-governance-model)

## Use cases, misconceptions, and unresolved questions

Governance supports shared infrastructure membership, protocol/economic configuration, scheduled upgrades, reward administration, and auditable public network operation.

- SV is not simply a more powerful stakeholder validator; it adds synchronizer and governance duties.
- Canton Foundation coordination is not equivalent to unilateral protocol control in the cited model.
- `OQ-003` asks for one authoritative matrix of orderer, mediator, DSO-party, and application-vote thresholds.
- `OQ-016` defers current membership/parameter verification to versioned network data rather than prose.

## Official sources

- [Super Validator Components](https://docs.canton.network/overview/reference/super-validator-components.md)
- [SV Governance Reference](https://docs.canton.network/overview/reference/sv-governance-reference.md)
- [The Global Synchronizer](https://docs.canton.network/overview/understand/global-synchronizer.md)
