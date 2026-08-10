# Party, Identity, and Authorization

**Structured coverage:** definition; why it exists; actors/components; responsibilities; state/data; end-to-end mechanism; relationships with other concepts; authorization; trust; privacy; constraints; failure/exception conditions; operational implications; relevant use cases; common misconceptions; unresolved questions; official sources.

## Decision and mental model

Treat identity and authorization as three linked layers: cryptographic/topology authority says who may represent a party, Daml authority says which parties must authorize ledger actions, and API authorization says which clients may ask a participant to read or act. A secure explanation requires all three. [SRC-1AC3D32DF2 / Topology / “Topology management”](../corpus/docs/overview/reference/topology.md#topology-management) [SRC-70BD5CED78 / Authorization Model / “Daml’s authorization model”](../corpus/docs/appdev/modules/m3-authorization.md#damls-authorization-model) [SRC-4CA0A3A918 / Authorization / “Basic interaction”](../corpus/docs/appdev/deep-dives/authorization.md#basic-interaction)

## Definition, purpose, actors, and state

A party is a stable on-ledger identity within a cryptographic namespace. Party-to-participant topology maps the party to hosting nodes and their submission/confirmation/observation permissions; signing keys and thresholds may define externally signed authority. Topology state is sequenced and deterministically validated by nodes on a synchronizer so protocol messages can rely on a shared view of identities and keys. [SRC-1AC3D32DF2 / Topology / “Topology management” and `PartyToParticipant`](../corpus/docs/overview/reference/topology.md#topology-management)

| Layer | Principal actors | Authoritative state |
| --- | --- | --- |
| Topology | Namespace/key owners, parties, participants, synchronizer nodes | Namespace delegations, keys, party hosting, permissions, thresholds, package vetting |
| Daml | Submitters, signatories, observers, choice controllers/actors | Templates, active contracts, transaction action tree |
| Ledger API | Users/apps, identity provider, participant | JWT/user rights such as `canReadAs`, `canActAs`, `canExecuteAs` |

## Mechanism

For local parties, a submission-permission participant controls the party’s submission keys and can prepare/submit on its behalf. For external parties, the party controls signing keys: a preparing participant turns a command into transaction data/hash, the owner reviews/signs, and an executing participant forwards the signed transaction; confirming participants still validate and record state. [SRC-5BD308B0DF / Local and External Parties / “Local party,” “External party,” and “Submission Flow”](../corpus/docs/overview/reference/external-party.md#submission-flow)

Within a Daml transaction, every action has required authorizers and every parent transaction/subtransaction supplies authorizers. Creates require contract signatories; exercises require choice controllers; exercise consequences gain the actors and the exercised contract’s signatories. A transaction is authorized only when each action’s required authorizers are a subset of its parent’s authorizers. Authority is not automatically transitive through nested exercises. [SRC-70BD5CED78 / Authorization Model / “Daml’s authorization model”](../corpus/docs/appdev/modules/m3-authorization.md#damls-authorization-model)

Before a participant serves an API request, it validates the access token issuer/signature/expiry and rights. `canReadAs(p)` gates data visible to party `p`; `canActAs(p)` adds ordinary command submission; `canExecuteAs(p)` permits prepare/execute without implicit read access. Node capability plus Daml validity plus client rights are all required. [SRC-4CA0A3A918 / Authorization / “Access Tokens and Rights”](../corpus/docs/appdev/deep-dives/authorization.md#access-tokens-and-rights)

## Trust and privacy boundaries

- A local party delegates submission authority and typically its namespace governance to the hosting submission participant; it therefore trusts that operator not to act contrary to its intent. [SRC-5BD308B0DF / Local and External Parties / “Local party”](../corpus/docs/overview/reference/external-party.md#local-party)
- External signing prevents a hosting participant from authorizing submissions without the party signature, but the party still needs at least one confirming participant for validation/state and may use preparing/executing participants for service. [SRC-5BD308B0DF / Local and External Parties / “External party”](../corpus/docs/overview/reference/external-party.md#external-party)
- Hosting participants see the data of hosted parties; a topology permission is not a content-blinding mechanism. Multi-hosting can distribute confirmation availability/trust but enlarges the set of infrastructure holding relevant data. [SRC-1C97EEFEFD / Trust Model Overview / “Your Validator”](../corpus/docs/overview/learn/trust-model.md#1-your-validator)
- API users and end users are off-ledger identities; a party is the on-ledger authority/visibility identity. Mapping many humans to one organizational party therefore requires backend IAM controls in addition to Daml rules. [SRC-E077DDE543 / Canton Network Application Architecture Design / “Architecture Options”](../corpus/docs/appdev/deep-dives/app-architecture-design.md#3-architecture-options)

## Constraints, failures, and operational implications

- A multi-hosted party has a confirmation threshold; higher thresholds strengthen compromise resistance but reduce availability. [SRC-5883AA972A / Smart Contract Consensus / “Multi-Hosted Parties and Thresholds”](../corpus/docs/overview/reference/smart-contract-consensus.md#multi-hosted-parties-and-thresholds)
- Documented external-party limitations include one root node and one submitting party, plus node-local completion/deduplication behavior. [SRC-5BD308B0DF / Local and External Parties / “Limitations”](../corpus/docs/overview/reference/external-party.md#limitations)
- Invalid/expired/insufficient JWTs fail at the API layer; absent Daml authority fails interpretation/validation; stale or unauthorized topology fails representation/confirmation. These failures must be diagnosed by layer rather than called a generic permission error. [SRC-4CA0A3A918 / Authorization / “Acquire and Use Access Tokens”](../corpus/docs/appdev/deep-dives/authorization.md#acquire-and-use-access-tokens) [SRC-A3F46FF397 / Transaction Lifecycle / “Failure Modes”](../corpus/docs/overview/reference/transaction-lifecycle.md#failure-modes)
- Namespace/root keys and identity backups are recovery-critical; loss can make proof of asset ownership unrecoverable. [SRC-7C4FD68B51 / Validator Disaster Recovery](../corpus/docs/global-synchronizer/production-operations/validator-disaster-recovery.md)

## Use cases, misconceptions, and unresolved questions

External parties suit wallet/custody models requiring user-held signing; local parties suit trusted automation; multi-hosted/decentralized parties suit threshold confirmation/governance. Proposal/accept and role-contract patterns express one-time versus continuing authorization in Daml. [SRC-70BD5CED78 / Authorization Model / “Use Propose-Accept” and “Use role contracts”](../corpus/docs/appdev/modules/m3-authorization.md#use-propose-accept-workflow-for-one-off-authorization)

- Party is not synonymous with human user, wallet UI, API account, or validator.
- Observer grants visibility, not choice authority unless the same party is also a controller.
- External signing reduces submission trust; it does not make the hosting participant unnecessary or blind.
- `OQ-005` tracks the exact portability/interoperability of a party identity across independently governed synchronizers; some overview wording is broader than the detailed topology model establishes.

## Official sources

- [Topology](https://docs.canton.network/overview/reference/topology.md)
- [Local and External Parties](https://docs.canton.network/overview/reference/external-party.md)
- [Authorization Model](https://docs.canton.network/appdev/modules/m3-authorization.md)
- [Ledger API Authorization](https://docs.canton.network/appdev/deep-dives/authorization.md)
