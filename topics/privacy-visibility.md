# Privacy and Information Visibility

**Structured coverage:** definition; why it exists; actors/components; responsibilities; state/data; end-to-end mechanism; relationships with other concepts; authorization; trust; privacy; constraints; failure/exception conditions; operational implications; relevant use cases; common misconceptions; unresolved questions; official sources.

## Decision and mental model

Canton provides stakeholder/view-scoped payload distribution, not an absolute absence of metadata. Privacy analysis must enumerate application parties, hosting participants, sequencer metadata, mediator metadata, public application projections, and off-ledger systems separately. [SRC-5506826606 / Privacy Model Explained / “Canton’s Approach”](../corpus/docs/overview/learn/privacy-model.md#cantons-approach-sub-transaction-privacy) [SRC-46FF0D4718 / Ordering Consensus / “Synchronizer Components”](../corpus/docs/overview/reference/ordering-consensus.md#synchronizer-components)

## Definition and purpose

Sub-transaction privacy decomposes an action tree into cryptographically linked views and distributes each view to participants hosting entitled parties. Signatories and observers are stakeholders; controllers/actors and witnesses may gain action/consequence visibility according to transaction semantics. Hashes preserve structural consistency where content is hidden. [SRC-A3F46FF397 / Transaction Lifecycle / “Subtransaction Privacy”](../corpus/docs/overview/reference/transaction-lifecycle.md#subtransaction-privacy)

This exists so affected parties can validate their portion and detect conflicts without global state/compute replication. Privacy and scalability follow from limiting validation/storage to the stakeholder set rather than all network nodes. [SRC-5883AA972A / Smart Contract Consensus / “Proof of Stakeholder”](../corpus/docs/overview/reference/smart-contract-consensus.md#proof-of-stakeholder)

## Visibility matrix

| Boundary | Documented visibility | Documented exclusions/limits |
| --- | --- | --- |
| Party | Contracts/actions/views it is entitled to by Daml transaction semantics | Unrelated views and parties |
| Hosting participant | Data/views for parties it hosts; local history/ACS; received sequencer messages | No global ledger projection |
| Sequencer | Ciphertext, recipients/routing, sender request, size, timing/ordering, traffic usage | Decrypted transaction payload and participant decryption keys |
| Mediator | Informee lists, confirmation policy/outcomes, deadlines/root correlation | Decrypted contract/action payload |
| Counterparty | Shared contract/view data | Data outside the shared visibility graph; cannot be prevented from leaking data it legitimately learns |
| Application/PQS | Data authorized to queried parties and retained by its backend | No automatic network-wide private query |
| Scan/CC services | Public/application-defined data described by the relevant Splice contracts/APIs | Not evidence that all Canton application data is public |

The infrastructure rows are supported by the ordering reference, which says sequencers see recipient lists/message sizes and mediators see informee lists/confirmation outcomes. [SRC-46FF0D4718 / Ordering Consensus / “Sequencer Nodes” and “Mediator Nodes”](../corpus/docs/overview/reference/ordering-consensus.md#sequencer-nodes)

## Mechanism

The submitting participant creates a short-lived symmetric key per recipient informee group, encrypts each view, and encrypts the session key to eligible participant public keys. Parent-view material can carry child-view hashes/keys needed by witnesses. The sequencer routes the encrypted envelopes, entitled participants reconstruct their projection, and root-hash checks bind their visible content to the same committed tree. [SRC-A3F46FF397 / Transaction Lifecycle / “Subtransaction Privacy”](../corpus/docs/overview/reference/transaction-lifecycle.md#subtransaction-privacy)

Contract-level audience is designed with signatories/observers; transaction-level audience expands through choice actors, consequences, fetches/disclosure, and composition. Separate contracts are needed when different audiences must see different fields because an observer of a contract receives its payload. [SRC-5506826606 / Privacy Model Explained / “Stakeholder Visibility Rules” and “Privacy Patterns”](../corpus/docs/overview/learn/privacy-model.md#stakeholder-visibility-rules) [SRC-24BF8E1094 / Use Cases / “Supply Chain Finance”](../corpus/docs/overview/understand/use-cases.md#supply-chain-finance)

## Authorization and trust assumptions

Cryptography and topology restrict envelope decryption to intended hosting infrastructure under the stated key assumptions. Daml defines entitlement, but any entitled party/validator/app can disclose plaintext after receipt; Canton cannot cryptographically force a legitimate recipient to keep it secret. The party therefore trusts hosting operators and counterparties for confidentiality beyond protocol delivery. [SRC-1C97EEFEFD / Trust Model Overview / “Your Validator” and “Contract Counterparties”](../corpus/docs/overview/learn/trust-model.md#1-your-validator)

External KMS reduces long-term key exposure but session-key caching creates a documented memory compromise window (one hour by default in the cited validator configuration). This is an operational privacy/security tradeoff, not a change to Daml visibility. [SRC-9EB1F6E5A4 / Validator Security / “Using an external KMS”](../corpus/docs/global-synchronizer/production-operations/validator-security.md#using-an-external-kms-for-managing-participant-keys)

## Constraints, exceptions, and operations

- Timing, message size, routing/informee, traffic, and verdict metadata exist; traffic analysis is not ruled out.
- Observer overuse and composed fetch/disclosure can reveal more data than intended.
- A regulator/auditor sees data only if modeled or disclosed to its party; privacy does not itself produce regulatory access.
- Backends, logs, PQS, backups, support dumps, and public APIs can expand retention/access beyond the participant protocol boundary.
- Pruning removes participant query history but does not erase copies already disclosed or retained elsewhere. [SRC-5506826606 / Privacy Model Explained / “Common Privacy Mistakes”](../corpus/docs/overview/learn/privacy-model.md#common-privacy-mistakes) [SRC-2F6E09F38B / Pruning / “Participant node pruning”](../corpus/docs/global-synchronizer/production-operations/pruning.md#participant-node-pruning)

## Use cases, misconceptions, and unresolved questions

Privacy-aware DvP, bilateral agreements, confidential positions, jurisdiction-specific regulator views, and supply-chain compartmentalization come from contract/view design plus appropriate participant/synchronizer operations. They are not a blanket property of putting data on Canton.

- “The synchronizer sees none of this” is too broad when “this” includes metadata; `OQ-001` preserves the conflict.
- The corpus says CC transactions/balances are public through Scan while generic GS pages emphasize encrypted payloads; `OQ-007` asks which contract stakeholders/projections create that visibility.
- Divulgence descriptions are not fully consistent about affected parties; `OQ-006` requires specification-level clarification.

## Official sources

- [Privacy Model Explained](https://docs.canton.network/overview/learn/privacy-model.md)
- [Transaction Lifecycle](https://docs.canton.network/overview/reference/transaction-lifecycle.md)
- [Ordering Consensus](https://docs.canton.network/overview/reference/ordering-consensus.md)
- [Trust Model Overview](https://docs.canton.network/overview/learn/trust-model.md)
