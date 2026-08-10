# Global Synchronizer

**Structured coverage:** definition; why it exists; actors/components; responsibilities; state/data; end-to-end mechanism; relationships with other concepts; authorization; trust; privacy; constraints; failure/exception conditions; operational implications; relevant use cases; common misconceptions; unresolved questions; official sources.

## Decision and mental model

The Global Synchronizer is Canton Network’s broadly shared, SV-operated coordination and economic/governance domain. It is not a separate state-replicating blockchain and is not mandatory for every private Canton workflow, but it is the common home for Canton Coin and broad cross-application interoperability. [SRC-E9749732A0 / The Global Synchronizer / “What It Is”](../corpus/docs/overview/understand/global-synchronizer.md#what-it-is)

## Definition and why it exists

The official corpus describes it as a BFT configuration of distributed sequencer and mediator infrastructure operated by independent Super Validators under DSO/Canton Foundation governance. It supplies a common synchronizer that many validators/parties can trust, avoiding pairwise creation of private coordination infrastructure for every cross-organization transaction. [SRC-7FF79A1051 / Global Synchronizer Architecture / “Components”](../corpus/docs/overview/learn/global-synchronizer-architecture.md#components) [SRC-CB6BCAA81A / Multi-Synchronizer Architecture / “Importance of the Global Synchronizer”](../corpus/docs/overview/learn/multi-synchronizer.md#importance-of-the-global-synchronizer)

## Actors, components, and state

| Actor/component | Responsibility/state |
| --- | --- |
| Regular validator | Host parties/contracts, connect as client, validate stakeholder views, fund traffic |
| Super Validator | Run validator stack plus sequencer, mediator/orderer, Scan and governance applications |
| DSO/decentralized party | Collective operator/governance identity with threshold confirmation |
| Canton Foundation | Coordination, policy/transparency, code/featured-app processes; one SV vote per cited reference |
| Sequencer/mediator | Ordered encrypted delivery and confirmation verdicts |
| Splice apps | Canton Coin, traffic/rewards, wallet, CNS, governance and Scan projections |

The Global Synchronizer does not hold each application’s full contract state; its databases store synchronization/order/mediation/service data, while participants retain their stakeholder projections. [SRC-DA63952FB3 / Super Validator Components / “Synchronizer Infrastructure”](../corpus/docs/overview/reference/super-validator-components.md#synchronizer-infrastructure) [SRC-4125FC3B33 / Architecture Overview / “The Big Picture”](../corpus/docs/overview/learn/architecture.md#the-big-picture)

## Mechanism

Regular validators connect to multiple SV sequencer endpoints, submit encrypted confirmation batches, receive entitled views, and confirm through the mediator path. SV orderer nodes establish the common sequence; mediators aggregate stakeholder confirmations. Splice Daml/apps run network economics/governance, and independently operated Scan instances expose public/network information and BFT-read mechanisms. [SRC-7FF79A1051 / Global Synchronizer Architecture / “Transaction flow through the synchronizer”](../corpus/docs/overview/learn/global-synchronizer-architecture.md#transaction-flow-through-the-synchronizer) [SRC-DA63952FB3 / Super Validator Components / “Scan App”](../corpus/docs/overview/reference/super-validator-components.md#scan-app)

Canton Coin is burned to purchase extra synchronizer traffic and minted according to governed reward mechanisms. Validator onboarding requires SV sponsorship and network/version configuration. Private synchronizers may coexist; contracts are reassigned when a workflow needs Global services or counterparties. [SRC-B246B6729B / Tokenomics of the Global Synchronizer / “Traffic Economics”](../corpus/docs/overview/reference/tokenomics-of-gs.md#traffic-economics) [SRC-E9749732A0 / The Global Synchronizer / “Becoming a Validator”](../corpus/docs/overview/understand/global-synchronizer.md#becoming-a-validator)

## Authorization, trust, and privacy

Stakeholder participants still enforce Daml correctness and retain payload state. Users trust the SV set for safe/live ordering, mediation, availability, topology/economic/governance operations under the documented BFT thresholds, and they trust their own validator separately. The Foundation/DSO governs parameters and membership but, per the governance reference, no single CF vote unilaterally changes on-chain state. [SRC-4FA5D0A091 / SV Governance Reference / “Canton Foundation” and “On-Chain Governance Architecture”](../corpus/docs/overview/reference/sv-governance-reference.md#canton-foundation)

Encrypted protocol payload does not imply all Splice application data is private. The corpus explicitly describes public CC/Scan visibility while generic application payloads remain stakeholder-scoped; the contract/projection mechanism establishing that boundary needs clearer authoritative documentation. [SRC-91BB5B75AB / Glossary / “Canton Coin”](../corpus/docs/global-synchronizer/splice-fundamentals/glossary.md) [SRC-DA63952FB3 / Super Validator Components / “Scan API”](../corpus/docs/overview/reference/super-validator-components.md#scan-api)

## Constraints, failures, and operations

- Progress depends on orderer/mediator BFT thresholds and enough stakeholder participants; failures beyond assumptions stop/reject processing.
- Validators must maintain compatible versions, network connectivity, keys/backups, and traffic.
- Governance can change protocol/economic parameters and schedules.
- A logical synchronizer upgrade may require validator recovery/migration procedures.
- Overview pages include unfinished TODO text and rapidly changing upgrade/reward descriptions; operational truth must be version-scoped. [SRC-E9749732A0 / The Global Synchronizer / “Upgrade Considerations”](../corpus/docs/overview/understand/global-synchronizer.md#upgrade-considerations) [SRC-7C4FD68B51 / Validator Disaster Recovery](../corpus/docs/global-synchronizer/production-operations/validator-disaster-recovery.md)

## Use cases, misconceptions, and unresolved questions

Global is the default venue for broad interoperability, CC settlement, network services, and applications that prefer shared decentralized synchronizer operations. It is not the only synchronizer and does not eliminate application/participant trust.

- `OQ-008`: current Global ordering backend differs across official pages (CometBFT vs native BFT descriptions).
- `OQ-007`: exact public/private data boundary for CC, DSO and Scan.
- `OQ-016`: authoritative current SV/operator count, thresholds and network-specific parameters are intentionally not frozen from descriptive prose.

## Official sources

- [The Global Synchronizer](https://docs.canton.network/overview/understand/global-synchronizer.md)
- [Global Synchronizer Architecture](https://docs.canton.network/overview/learn/global-synchronizer-architecture.md)
- [Super Validator Components](https://docs.canton.network/overview/reference/super-validator-components.md)
- [SV Governance Reference](https://docs.canton.network/overview/reference/sv-governance-reference.md)
