# Institutional and RWA Use Cases

**Structured coverage:** definition; why it exists; actors/components; responsibilities; state/data; end-to-end mechanism; relationships with other concepts; authorization; trust; privacy; constraints; failure/exception conditions; operational implications; relevant use cases; common misconceptions; unresolved questions; official sources.

## Decision and mental model

Canton’s institutional/RWA fit is mechanism-dependent: a use case is credible only when its party roles, contract audiences, authorization, settlement inputs, synchronizer assignation, integrations and operational trust are specified. Privacy/atomicity labels alone are not sufficient. [SRC-24BF8E1094 / Use Cases / “When Canton Fits”](../corpus/docs/overview/understand/use-cases.md#when-canton-fits)

## Mechanism-to-requirement mapping

| Requirement | Canton mechanism | Required conditions |
| --- | --- | --- |
| Confidential bilateral terms | Stakeholder/view-scoped Daml contracts | Correct observer/controller design and trusted hosting parties |
| Regulated ownership | Issuer/registry signatory plus transfer choices/eligibility data | Authoritative identity/compliance integration and package availability |
| Atomic DvP | One Daml transaction consumes/creates both legs | Inputs co-assigned to one suitable synchronizer and all authorities online |
| Auditor/regulator visibility | Observer/audit contracts or explicit disclosure | Regulator party/validator and deliberate data scope |
| Organizational autonomy | Each organization hosts party/participant/backend | Operations, keys, IAM, connectivity and upgrade capacity |
| Public/private lifecycle | Private/Global synchronizers plus reassignment | Dual connectivity, vetted packages, pending-move risk |
| Cash/token interoperability | CIP-0056/CC/USDCx or application interfaces | Registry/bridge trust, wallet/traffic/UTXO support |

## End-to-end patterns

**Tokenized securities.** An issuer/registry controls issuance and eligible-holder transitions; holders control transfer requests; regulators/auditors receive modeled views. Trades remain non-public to unrelated parties, but hosting validators and modeled observers see their data. [SRC-24BF8E1094 / Use Cases / “Tokenized Securities”](../corpus/docs/overview/understand/use-cases.md#tokenized-securities)

**Delivery versus payment.** Asset and cash contracts are brought to one synchronizer, then a single authorized transaction consumes both old holdings and creates new ones. Any missing authority, invalid input or confirmation timeout rejects both legs. If inputs start on different synchronizers, reassignment precedes the atomic transaction and is itself non-atomic. [SRC-24BF8E1094 / Use Cases / “Delivery vs. Payment”](../corpus/docs/overview/understand/use-cases.md#delivery-vs-payment-dvp) [SRC-3E385A60D2 / Cross-Synchronizer DvP Example](../corpus/docs/overview/reference/cross-sync-dvp-example.md)

**Syndicated lending.** Separate bilateral/agent-position contracts can keep each lender’s position scoped while agent/borrower workflows coordinate payments. Global aggregates are visible only if modeled for the agent/borrower/regulator. [SRC-24BF8E1094 / Use Cases / “Syndicated Loan Management”](../corpus/docs/overview/understand/use-cases.md#syndicated-loan-management)

**Cross-border payment.** Jurisdiction-local participants/backends retain customer data and each regulator observes the contracts for its scope; shared settlement actions coordinate across the chosen synchronizer. This is a design pattern, not proof that every data-residency law is satisfied. [SRC-24BF8E1094 / Use Cases / “Cross-Border Payments”](../corpus/docs/overview/understand/use-cases.md#cross-border-payments)

**Supply-chain finance.** Different audience contracts separate logistics, financing and pricing data while one transaction can create linked facts. Contract-level, not field-level, audiences are the core design constraint. [SRC-24BF8E1094 / Use Cases / “Supply Chain Finance”](../corpus/docs/overview/understand/use-cases.md#supply-chain-finance)

## Actors, authorization, trust, and privacy

Typical actors are asset issuer/registry, owner/custodian, buyer/seller, cash issuer, app provider, validators, synchronizer operators, regulator/auditor, wallet/bridge, and off-ledger KYC/oracle/settlement systems. Daml authority defines ledger consent; off-ledger identity/compliance sources and operator governance remain trusted inputs. [SRC-E077DDE543 / Canton Network Application Architecture Design / “Integrate with off-ledger systems”](../corpus/docs/appdev/deep-dives/app-architecture-design.md#integrate-with-off-ledger-systems)

The privacy boundary follows every contract/view and infrastructure copy, not the business label. A regulator added as observer sees the whole observed payload; a counterparty can leak what it legitimately learns; Global CC/Scan data may be public; a private synchronizer still exposes metadata to its operators. [SRC-5506826606 / Privacy Model Explained / “Privacy Patterns”](../corpus/docs/overview/learn/privacy-model.md#privacy-patterns)

## Constraints, failure modes, and operational implications

- Asset/cash legal enforceability, identity, oracle accuracy and bridge reserves are outside consensus unless modeled and governed.
- Co-assignment/reassignment creates latency/contention/pending risk for cross-domain DvP.
- Required issuer/regulator/counterparty participants can become liveness dependencies.
- Upgrade/package mismatches can strand in-flight multi-step workflows.
- Audit evidence must outlive pruning in PQS/ODS/backups with controlled privacy.
- Network cost/traffic/UTXO and validator operations affect product feasibility. [SRC-E077DDE543 / Canton Network Application Architecture Design / “Key Takeaways”](../corpus/docs/appdev/deep-dives/app-architecture-design.md#4-key-takeaways) [SRC-2F6E09F38B / Pruning / “Participant node pruning”](../corpus/docs/global-synchronizer/production-operations/pruning.md#participant-node-pruning)

## Common misconceptions and unresolved questions

- Atomic ledger settlement does not establish legal finality or reserve sufficiency.
- Selective disclosure does not automatically satisfy every regulator or residency rule.
- RWA token interfaces do not define the off-ledger asset’s legal/control framework.
- `OQ-020` tracks bridge/reserve verification; `OQ-022` tracks legal/oracle/control assumptions; `OQ-023` defers end-to-end DvP contention/failure measurement.

## Official sources

- [Use Cases](https://docs.canton.network/overview/understand/use-cases.md)
- [Cross-Synchronizer DvP Example](https://docs.canton.network/overview/reference/cross-sync-dvp-example.md)
- [Privacy Model Explained](https://docs.canton.network/overview/learn/privacy-model.md)
- [Canton Network Application Architecture Design](https://docs.canton.network/appdev/deep-dives/app-architecture-design.md)
