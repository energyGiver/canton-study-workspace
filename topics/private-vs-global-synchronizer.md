# Private vs Global Synchronizer

**Structured coverage:** definition; why it exists; actors/components; responsibilities; state/data; end-to-end mechanism; relationships with other concepts; authorization; trust; privacy; constraints; failure/exception conditions; operational implications; relevant use cases; common misconceptions; unresolved questions; official sources.

## Decision and mental model

Choose a synchronizer by operator/governance trust, membership, metadata exposure, availability/performance, cost, and interoperability. Daml stakeholder privacy remains relevant on both, while the Global Synchronizer adds public network services/economics and a distributed SV operator set. [SRC-E1B2C8D5F7 / Private Synchronizers / “Why Private Synchronizers”](../corpus/docs/global-synchronizer/extension-synchronizers/private-synchronizers.md#why-private-synchronizers) [SRC-E9749732A0 / The Global Synchronizer / “What It Is”](../corpus/docs/overview/understand/global-synchronizer.md#what-it-is)

## Comparison

| Dimension | Global Synchronizer | Private/extension synchronizer |
| --- | --- | --- |
| Operators/governance | SV collective/DSO and Canton Foundation governance | One operator, third party, or private BFT consortium |
| Interoperability | Broad default common synchronizer; CC/CNS/governance services | Limited to connected/authorized participants; compose through reassignment |
| Economics | Traffic allocation/purchase in CC; network reward/governance mechanisms | Documentation says private traffic does not consume CC credits; operator-defined economics |
| Infrastructure | Distributed sequencers/mediators/orderer across SVs | Dedicated sequencer/mediator, centralized or BFT |
| Control | Shared network parameters/upgrades/onboarding | Operator controls access, parameters, upgrade schedule and locality |
| Privacy | Encrypted payload transport plus application-specific public Splice/Scan visibility | Encrypted payload transport; narrower operator/member set and potentially private metadata |
| Operations | Validator maintains connection/version/traffic; SVs operate sync | Private participants/operators also own synchronizer availability/backups/upgrades |

These are documented characteristics, not performance/SLA measurements; no runtime comparison was performed. [SRC-E1B2C8D5F7 / Private Synchronizers / “Deployment Models”](../corpus/docs/global-synchronizer/extension-synchronizers/private-synchronizers.md#deployment-models)

## Mechanisms and relationships

Both synchronizer types provide sequencing and mediation. Participants can connect to both and assign contracts by lifecycle. A hybrid workflow can create/process on private infrastructure, reassign the settlement inputs to the Global Synchronizer, execute with CC/other public contracts, and optionally move outputs later. The move uses the same non-atomic unassignment/assignment protocol and requires common stakeholder connectivity/package vetting. [SRC-99E06BD97E / Hybrid Synchronizer Pattern / “Contract assignment strategies” and “Cross-synchronizer reassignment”](../corpus/docs/global-synchronizer/extension-synchronizers/hybrid-synchronizer-pattern.md#contract-assignment-strategies)

## Authorization, trust, and privacy boundaries

Daml parties/signatories/controllers determine transaction content visibility/authority on either synchronizer. The synchronizer choice determines who operates ordering/mediation and may see traffic/routing/informee metadata. A single-operator private synchronizer concentrates censorship/availability/order trust; private BFT distributes it. The Global Synchronizer distributes that trust across SVs under its documented BFT/governance assumptions. [SRC-46FF0D4718 / Ordering Consensus / “Centralized vs. Decentralized Options”](../corpus/docs/overview/reference/ordering-consensus.md#centralized-vs-decentralized-options)

“Private” should not be read as “no operator metadata” or “only one party sees data.” It means a restricted/dedicated coordination domain; stakeholder participants still receive the views Daml entitles them to. Conversely “Global” does not make generic application payload public, but built-in CC/governance/Scan applications can deliberately expose data. [SRC-E1B2C8D5F7 / Private Synchronizers / “How They Work”](../corpus/docs/global-synchronizer/extension-synchronizers/private-synchronizers.md#how-they-work) [SRC-91BB5B75AB / Glossary / “Canton Coin”](../corpus/docs/global-synchronizer/splice-fundamentals/glossary.md)

## Constraints, failures, and operational implications

- CC operations are documented as requiring the Global Synchronizer; private flow must move to Global to interact atomically with CC.
- Parties/validators absent from a private synchronizer cannot use contracts assigned there.
- Reassignment adds unavailable/pending time and target topology/package prerequisites.
- Private operation adds sequencing/mediation database, key, BFT (if used), monitoring, backup, capacity, and upgrade duties.
- Public-network integration adds sponsorship/onboarding, frequent version alignment, and traffic funding. [SRC-E1B2C8D5F7 / Private Synchronizers / “When to Use a Private Synchronizer” and “Relationship with the Global Synchronizer”](../corpus/docs/global-synchronizer/extension-synchronizers/private-synchronizers.md#when-to-use-a-private-synchronizer)

## Use cases, misconceptions, and unresolved questions

Use private for controlled high-volume, jurisdiction-bound, consortium, latency-sensitive, or metadata-sensitive workflow stages. Use Global for broad composability, CC settlement, public network services, and reduced synchronizer-operation burden. Use hybrid when both conditions apply.

- “Private synchronizer transactions have zero cost” is not established; only absence of Global CC traffic credits is documented.
- “Global is always more decentralized/secure” ignores the chosen private operator/BFT design and participant trust.
- `OQ-007` tracks the exact boundary between encrypted Global traffic and public Splice/Scan data; `OQ-014` requests authoritative production support/SLA status for private synchronizer backends.

## Official sources

- [Private Synchronizers](https://docs.canton.network/global-synchronizer/extension-synchronizers/private-synchronizers.md)
- [Hybrid Synchronizer Pattern](https://docs.canton.network/global-synchronizer/extension-synchronizers/hybrid-synchronizer-pattern.md)
- [The Global Synchronizer](https://docs.canton.network/overview/understand/global-synchronizer.md)
