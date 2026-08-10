# Topic index and learning order

## Decision

Read the topics in dependency order rather than page order. Canton separates identity, private state validation, and ordering infrastructure, so later mechanisms are hard to reason about until those foundations are explicit.

### Foundation

1. [Core Architecture](core-architecture.md)
2. [Party, Identity, and Authorization](identity-authorization.md)
3. [Participant and Validator](participant-validator.md)
4. [Daml Application Model](daml-application-model.md)

### Protocol mechanisms

5. [Transactions and Contract Lifecycle](transaction-lifecycle.md)
6. [Privacy and Information Visibility](privacy-visibility.md)
7. [Two-Layer Consensus](two-layer-consensus.md)
8. [Sequencer and Mediator](sequencer-mediator.md)
9. [Synchronizers and Reassignment](synchronizers-reassignment.md)
10. [Multi-Synchronizer Architecture](multi-synchronizer-architecture.md)
11. [Private vs Global Synchronizer](private-vs-global-synchronizer.md)

### Application and network services

12. [Ledger API and Application Architecture](ledger-api-app-architecture.md)
13. [Global Synchronizer](global-synchronizer.md)
14. [Super Validators and Governance](super-validators-governance.md)
15. [Fees, Rewards, and Economics](fees-rewards-economics.md)
16. [Wallet and Exchange Integrations](wallet-exchange-integrations.md)
17. [Deployment and Operations](deployment-operations.md)
18. [Institutional and RWA Use Cases](institutional-rwa-use-cases.md)

Each note covers definition/purpose, actors, state, mechanism, relationships, authorization, trust, privacy, constraints, failures, operations, use cases, misconceptions, unresolved questions, and official sources. A section may combine closely related fields when that better exposes the mechanism.
