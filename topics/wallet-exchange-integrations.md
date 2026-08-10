# Wallet and Exchange Integrations

**Structured coverage:** definition; why it exists; actors/components; responsibilities; state/data; end-to-end mechanism; relationships with other concepts; authorization; trust; privacy; constraints; failure/exception conditions; operational implications; relevant use cases; common misconceptions; unresolved questions; official sources.

## Decision and mental model

A Canton wallet/exchange integration is a validator-backed private-data and signing system, not only a key/address UI. It must support party hosting, token-standard transactions, transaction approval/signing, traffic/UTXO operations, and durable transaction evidence. [SRC-A1E2F651DD / Canton Network Overview / “Implications for Wallet Providers”](../corpus/docs/integrations/wallets-and-exchanges/canton-network-overview.md#implications-for-wallet-providers) [SRC-32A6E1A868 / Integrating with the Canton Network / “Necessary Features”](../corpus/docs/integrations/wallets-and-exchanges/integrating-with-canton.md#necessary-features)

## Actors, components, responsibilities, and state

| Actor/component | Responsibility/state |
| --- | --- |
| Wallet/exchange operator | Run/use validator, protect hosted ledger data, fund traffic, maintain environments |
| Party/account | On-ledger ownership/authority identity; local or externally signed |
| Custody/signing provider | Hold keys and approve/sign prepared transaction hashes |
| Wallet Gateway/dApp API | Authenticate users/dApps, prepare/approve/sign/execute, manage wallets/networks |
| Token registry/standard | CIP-0056 holdings, transfers, instructions and metadata |
| Exchange ledger | Map memo tags/deposits to internal customer accounts |
| Wallet backend | Retain transfer object/update ID, history/proofs and UTXO state |

## Core integration flow

The necessary-feature guide calls for CIP-0056, CC and USDCx support, memo tags, and UTXO management; preapprovals and CIP-0103 dApp support are recommended additions. For external parties, the system prepares a transaction on a validator, presents the effects for approval, obtains a custody signature, executes through a participant, and tracks completion. [SRC-32A6E1A868 / Integrating with the Canton Network / “Necessary Features” and “Optional Features”](../corpus/docs/integrations/wallets-and-exchanges/integrating-with-canton.md#necessary-features) [SRC-D7D9BB46E9 / Overview / “Transaction lifecycle”](../corpus/docs/integrations/wallet-gateway/overview.md#transaction-lifecycle)

Wallet Gateway is a self-hosted adapter between CIP-0103 dApps, user sessions/UI, one or more validator networks, and configurable participant/external custody signing providers. Each wallet maps to a Canton party, network and signing provider; dApp sessions are bound per dApp. [SRC-D7D9BB46E9 / Overview / “Core concepts”](../corpus/docs/integrations/wallet-gateway/overview.md#core-concepts)

For exchange deposits, the docs recommend one/few vault parties rather than ephemeral parties and use `splice.lfdecentralizedtrust.org/reason` metadata as a memo/tag to map an incoming transfer to an internal account. Registries should preserve the transfer specification/metadata through multi-step flows. [SRC-A1E2F651DD / Canton Network Overview / “Advice on using Parties”](../corpus/docs/integrations/wallets-and-exchanges/canton-network-overview.md#advice-on-using-parties-for-wallet-providers) [SRC-AEA7294230 / Memo Tags](../corpus/docs/integrations/wallets-and-exchanges/memo-tags.md)

The proof-of-transfer guide requires wallets to expose/copy the latest UpdateID and Transfer Object and persist them in their own backend because participant pruning can make historical event queries fail. Two-step transfers must update the proof reference from offer to accepted transfer. [SRC-0E62E3CD99 / Proof of Transfer / “Exposing the Transfer Object and UpdateID” and “Data Persistence and Pruning”](../corpus/docs/integrations/wallets-and-exchanges/proof-of-transfer.md#exposing-the-transfer-object-and-updateid)

USDCx support ranges from CIP-0056 hold/transfer, through bridge onboarding and mint/burn API choices, to direct Ethereum xReserve UI/transaction integration. Documentation describes USDC locked on Ethereum and represented as a Canton standard token; this phase does not verify bridge contracts or reserves. [SRC-5E39404A6B / USDCx Support / “Overview” and “Supporting xReserve Deposits and Withdrawals”](../corpus/docs/integrations/wallets-and-exchanges/usdcx-support.md#overview)

## Authorization, trust, privacy, constraints, and failures

Externally signed parties retain key authority, but the validator still hosts private data/confirms state and Wallet Gateway/backend handles user authentication, transaction presentation and submission. Users trust it not to alter/misrepresent prepared effects, censor submissions, leak data, or bind the wrong wallet/network/provider. [SRC-D7D9BB46E9 / Overview / “How it fits together”](../corpus/docs/integrations/wallet-gateway/overview.md#how-it-fits-together) [SRC-1C97EEFEFD / Trust Model Overview / “Application Provider”](../corpus/docs/overview/learn/trust-model.md#4-application-provider)

- Party creation has state/cost, so Ethereum-style unique deposit address patterns should not be copied blindly.
- Memo omission/mismatch causes allocation exceptions even if ledger transfer succeeds.
- UTXO fragmentation, locked two-step funds, traffic exhaustion and expired instructions need recovery/UI handling.
- Pruned data breaks proof lookup unless retained off-ledger.
- Multi-environment upgrades and validator state make a wallet integration operationally heavier than a stateless RPC client.

## Use cases, misconceptions, and unresolved questions

The documented patterns cover custodial exchanges, self-custody/external custody, dApp connection, CC/standard tokens, deposit attribution, independent transfer proofing, and USDCx bridge flows.

- A party is not a cheap disposable deposit address.
- Key custody alone is not the full custody/privacy responsibility on Canton.
- `OQ-019` asks for a single normative matrix of current CIP-0056/CIP-0103 versions and backward compatibility.
- `OQ-020` defers USDCx reserve/bridge security and failure recovery to later external/code/runtime verification.

## Official sources

- [Canton Network Overview for Wallets and Exchanges](https://docs.canton.network/integrations/wallets-and-exchanges/canton-network-overview.md)
- [Integrating with Canton](https://docs.canton.network/integrations/wallets-and-exchanges/integrating-with-canton.md)
- [Memo Tags](https://docs.canton.network/integrations/wallets-and-exchanges/memo-tags.md)
- [Proof of Transfer](https://docs.canton.network/integrations/wallets-and-exchanges/proof-of-transfer.md)
- [Wallet Gateway Overview](https://docs.canton.network/integrations/wallet-gateway/overview.md)
