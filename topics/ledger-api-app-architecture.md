# Ledger API and Application Architecture

**Structured coverage:** definition; why it exists; actors/components; responsibilities; state/data; end-to-end mechanism; relationships with other concepts; authorization; trust; privacy; constraints; failure/exception conditions; operational implications; relevant use cases; common misconceptions; unresolved questions; official sources.

## Decision and mental model

A Canton application is a distributed enterprise application whose shared state/rights live in Daml, whose commands and party-filtered updates flow through a participant’s Ledger API, and whose automation/IAM/integrations live in off-ledger services. PQS is a read projection, not an alternate write path. [SRC-E077DDE543 / Canton Network Application Architecture Design / “Canton Network application components”](../corpus/docs/appdev/deep-dives/app-architecture-design.md#canton-network-application-components) [SRC-E183CD5ECF / Validator Node Components / “PQS”](../corpus/docs/overview/reference/validator-node-components.md#pqs-participant-query-store)

## Definition, purpose, actors, and state

| Layer | Responsibility | State/data |
| --- | --- | --- |
| Daml model | Shared contracts, choices, authorization and visibility | DAR/package plus on-ledger contracts |
| Participant/Ledger API | Command submission/preparation/execution, completions, updates and ACS | Party-filtered ledger projection, users/rights |
| PQS | Queryable SQL projection for reads, reporting and automation | Active/historical denormalized PostgreSQL data |
| Backend | Higher-level API, IAM, retries, automation, external integration | Sessions, tasks, idempotency keys, integration state |
| Frontend/wallet | Human interaction and approval | UI/session state; normally no authoritative ledger state |
| App provider/user | Build/operate components and hold parties | Organizational infrastructure and policy |

The architecture exists because Daml deliberately has no independent execution thread or external I/O. External services must initiate commands and bridge KYC, pricing, reporting, messaging, and other systems while preserving ledger-level authorization. [SRC-E077DDE543 / Canton Network Application Architecture Design / “Automate on-ledger workflows” and “Integrate with off-ledger systems”](../corpus/docs/appdev/deep-dives/app-architecture-design.md#automate-on-ledger-workflows)

## End-to-end data flow

1. An end user authenticates to a frontend/backend; the backend maps that session to Ledger API rights/parties.
2. For writes, the backend submits a Daml command through gRPC or JSON Ledger API, tracks completion, and uses consuming inputs or command deduplication to make retries safe.
3. For reads, it consumes party-filtered Ledger API updates/ACS or queries a PQS projection at a known ledger offset.
4. Automation discovers a current on-ledger task, consults external systems if required, then submits an idempotent command. On retry it repeats the whole query/decision block against current state.
5. Downstream integrations receive ledger events through backend-controlled queues/webhooks/databases rather than direct write access. [SRC-E077DDE543 / Canton Network Application Architecture Design / “Provision higher-level APIs,” “Automate on-ledger workflows,” and “Integrate with off-ledger systems”](../corpus/docs/appdev/deep-dives/app-architecture-design.md#provision-higher-level-apis)

## Architecture choices

The detailed guide describes a continuum: provider-operated backend, user-operated provider backend, or each organization’s own backend. More user-local infrastructure increases self-sovereign queries, integration flexibility, and fine-grained organizational IAM, but increases operating cost, multi-version support, supply-chain coordination, and upgrade complexity. The simpler fully mediated frontend-to-backend model is the overview default; CQRS/direct frontend command submission is an alternative when exposing ledger concepts is justified. [SRC-E077DDE543 / Canton Network Application Architecture Design / “Architecture Options”](../corpus/docs/appdev/deep-dives/app-architecture-design.md#3-architecture-options) [SRC-B058EFC467 / Application Architecture / “Choosing an Architecture Style”](../corpus/docs/appdev/modules/m4-app-architecture.md#choosing-an-architecture-style)

## Authorization, trust, and privacy

API JWT rights gate which party data/actions a client can request; Daml rules still decide whether the resulting transaction is valid. A centralized backend becomes a censorship, credential, privacy, and availability trust point even when the ledger prevents it from forging missing party authority. User-run backends reduce that dependency but do not remove participant/synchronizer trust. [SRC-4CA0A3A918 / Authorization / “Access Tokens and Rights”](../corpus/docs/appdev/deep-dives/authorization.md#access-tokens-and-rights) [SRC-1C97EEFEFD / Trust Model Overview / “Application Provider”](../corpus/docs/overview/learn/trust-model.md#4-application-provider)

PQS/backends see only subscribed party data but may retain and combine it beyond participant pruning. Explicit disclosure can provide a non-stakeholder submitter with a reference contract for one transaction; it must not be confused with permanent observer visibility. [SRC-E077DDE543 / Canton Network Application Architecture Design / “Serve reference data contracts”](../corpus/docs/appdev/deep-dives/app-architecture-design.md#serve-reference-data-contracts)

## Constraints, failures, and operations

- Read-after-write/projection lag and inconsistent offsets can make automation act on stale data.
- Retrying only the final submission can repeat an outdated business decision; rerun the task against current state.
- Daml package/version differences across participant/app deployments can block workflows.
- PQS is not a recovery source for participant keys/consensus state; it is an application projection.
- Direct browser Ledger API access expands token/party-ID exposure and requires a deliberate security model.
- Off-ledger checks are not automatically consensus facts unless their result/authority is represented in the Daml transaction. [SRC-E077DDE543 / Canton Network Application Architecture Design / “Write” and “Automate on-ledger workflows”](../corpus/docs/appdev/deep-dives/app-architecture-design.md#automate-on-ledger-workflows)

## Use cases, misconceptions, and unresolved questions

The pattern supports regulated onboarding, oracle/reference data, trade processing, accounting/reporting, payments, and workflows spanning organization-local systems. “Smart contract application” does not imply every application needs custom Daml; applications may compose with existing models/APIs.

- Ledger API authentication is not Daml authorization.
- PQS does not create global visibility or submit state changes.
- `OQ-015` asks which API surface/version is normative where overview and reference naming differ.
- Upgrade/runtime compatibility verification remains deferred under `OQ-010`.

## Official sources

- [Canton Network Application Architecture Design](https://docs.canton.network/appdev/deep-dives/app-architecture-design.md)
- [Application Architecture](https://docs.canton.network/appdev/modules/m4-app-architecture.md)
- [Validator Node Components](https://docs.canton.network/overview/reference/validator-node-components.md)
- [Authorization](https://docs.canton.network/appdev/deep-dives/authorization.md)
