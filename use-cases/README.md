# Canton Mechanism-Based Use Cases

## Decision

These use cases are accepted as documented design patterns only when their required parties, participant trust, contract audiences, synchronizer topology, external systems and failure handling are stated. This avoids turning product examples into unsupported protocol guarantees.

## Pattern matrix

| Pattern | Core mechanism | Privacy/trust conditions | Main failure/constraint | Deep dive |
| --- | --- | --- | --- | --- |
| Atomic DvP | One Daml transaction consumes cash/asset inputs and creates both outputs | All stakeholders/authorizers on one suitable synchronizer; cash/asset app trust remains | Cross-sync inputs require prior non-atomic reassignment; timeout rejects both legs | [Institutional/RWA](../topics/institutional-rwa-use-cases.md#end-to-end-patterns) |
| Tokenized security | Issuer/registry signatory, holder-controlled choices, eligibility/reference contracts | Issuer/regulator/holder visibility is explicitly modeled | Off-ledger legal identity/title and package/participant availability | [Daml model](../topics/daml-application-model.md) |
| Syndicated lending | Separate lender-position contracts plus agent/borrower coordination | Each lender receives only its position views; agent scope is deliberate | Agent/required participant becomes liveness/information hub | [Official use case](../corpus/docs/overview/understand/use-cases.md#syndicated-loan-management) |
| Cross-border payment | Jurisdiction-local hosting and regulator observers plus atomic settlement | Data residency depends on every participant/backend/backup, not synchronizer encryption alone | Legal/KYC/FX/correspondent systems are off-ledger dependencies | [Privacy](../topics/privacy-visibility.md) |
| Supply-chain finance | Separate audience-specific logistics/finance contracts created atomically | Contract-level audience design; shared reference must not leak terms | Composition/fetch/disclosure can widen visibility | [Official use case](../corpus/docs/overview/understand/use-cases.md#supply-chain-finance) |
| Hybrid private processing / Global settlement | Lifecycle-based assignation and reassignment | Both operator sets and dual-connected participants are trusted for their phases | Pending reassignment, contention, package/topology eligibility | [Private vs Global](../topics/private-vs-global-synchronizer.md) |
| Custodial exchange | Vault party, hosting validator, memo-tag deposit allocation, durable proof data | Operator safeguards keys plus private ledger state and backend mappings | Memo mismatch, traffic/UTXO/pruning/upgrade failures | [Wallet/exchange integrations](../topics/wallet-exchange-integrations.md) |
| External-custody dApp wallet | Prepare/review/sign/execute with Wallet Gateway/CIP-0103 | Custody holds keys; gateway/validator still see/host relevant data | Incorrect effect presentation, session/network binding, unavailable signer | [Wallet Gateway source](../corpus/docs/integrations/wallet-gateway/overview.md#transaction-lifecycle) |
| USDCx bridge use | Standard-token holdings plus bridge agreement/attestation mint/burn workflows | Depends on bridge operators, reserve/attestation/admin controls outside generic Canton consensus | Reserve/chain reorg/pause/recovery assumptions unverified | `OQ-020` |

## End-to-end DvP dependency chain

1. Identity/topology establishes issuer, owner, buyer, seller, cash provider and hosting/confirmation nodes.
2. Daml templates/interfaces encode ownership, eligibility, transfer and settlement authority.
3. Applications obtain current asset/cash inputs and external compliance/reference data.
4. The router finds one admissible synchronizer and completes any required reassignments.
5. One transaction tree contains both payment and delivery consequences.
6. Stakeholder participants validate their views; the mediator returns one verdict.
7. Backends retain completion/audit evidence and handle retries, integration updates and exceptions.

This chain is supported across [identity](../topics/identity-authorization.md), [Daml](../topics/daml-application-model.md), [reassignment](../topics/synchronizers-reassignment.md), [transaction](../topics/transaction-lifecycle.md), and [application architecture](../topics/ledger-api-app-architecture.md) notes. The inference that cross-synchronizer DvP is atomic only after co-assignment is recorded as `CLM-040`.

## Fit and non-fit tests

A Canton design is a strong documented fit when multiple organizations need shared state transitions, explicit authority, selective contract/view distribution and atomic composition. It may be a poor fit when global transparency is desired, EVM-native execution is mandatory, anonymous participation is essential, or a simple single-party database solves the problem with less trust/operations overhead. [SRC-24BF8E1094 / Use Cases / “When Canton Fits” and “When Canton May Not Fit”](../corpus/docs/overview/understand/use-cases.md#when-canton-fits)

## Later verification backlog

- Measure multi-reassignment DvP latency/contention/failure behavior (`OQ-023`).
- Verify package/runtime upgrade behavior for in-flight workflows (`OQ-010`).
- Verify exact view/disclosure boundaries (`OQ-001`, `OQ-002`, `OQ-006`, `OQ-011`).
- Analyze bridge/reserve/admin controls (`OQ-020`).
- Build use-case-specific legal/oracle/control models (`OQ-022`).
