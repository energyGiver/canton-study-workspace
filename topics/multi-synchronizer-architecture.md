# Multi-Synchronizer Architecture

**Structured coverage:** definition; why it exists; actors/components; responsibilities; state/data; end-to-end mechanism; relationships with other concepts; authorization; trust; privacy; constraints; failure/exception conditions; operational implications; relevant use cases; common misconceptions; unresolved questions; official sources.

## Decision and mental model

Multi-synchronizer Canton is a federation of independent coordination/order domains joined by participants and contract reassignment, not one global total order. Application composability requires finding a common eligible synchronizer for each transaction. [SRC-CB6BCAA81A / Multi-Synchronizer Architecture / “Multiple Synchronizers”](../corpus/docs/overview/learn/multi-synchronizer.md#multiple-synchronizers) [SRC-92FDECC024 / Reassignment Protocol / “Updates stream ordering”](../corpus/docs/overview/reference/reassignment-protocol.md#updates-stream-ordering)

## Definition and why it exists

A participant can connect to several synchronizers with different regulation, locality, latency/throughput, governance, cost, and application-access characteristics. Each active contract has one current assignation. Horizontal/federated deployment lets workflows choose an appropriate domain without moving full ledger state to that domain. [SRC-CB6BCAA81A / Multi-Synchronizer Architecture / “Motivation”](../corpus/docs/overview/learn/multi-synchronizer.md#motivation)

## Actors, topology, and state

- Participant connections have aliases, priorities, sequencer endpoints/trust thresholds, packages, and party-hosting topology per synchronizer.
- Contract state has an assignation and reassignment counter in addition to its Daml lifecycle.
- Stakeholders may be hosted differently on each synchronizer, producing inhomogeneous eligibility and visibility.
- The synchronizer router evaluates all input contracts and candidate synchronizers; explicit disclosure/package vetting/party topology can influence eligibility. [SRC-CB6BCAA81A / Multi-Synchronizer Architecture / “Automatic selection of the Synchronizer”](../corpus/docs/overview/learn/multi-synchronizer.md#automatic-selection-of-the-synchronizer)

## Mechanism and data flow

For a multi-input transaction, the router finds candidate synchronizers to which all contracts can validly move and on which all stakeholders/packages/submitter conditions hold. It prefers connection priority, minimizes moves, and uses synchronizer ID as a tie-breaker. It completes required two-step reassignments, then submits the Daml transaction to the selected synchronizer. Outputs may later be reassigned for their next lifecycle stage. [SRC-CB6BCAA81A / Multi-Synchronizer Architecture / “Transactions with Multiple Synchronizers”](../corpus/docs/overview/learn/multi-synchronizer.md#transactions-with-multiple-synchronizers)

The Ledger API updates stream merges multiple per-synchronizer streams without a global cross-synchronizer causality order. Applications needing cross-domain sequencing must rely on contract/workflow causality and offsets rather than comparing synchronizer timestamps as a universal clock. [SRC-92FDECC024 / Reassignment Protocol / “Updates stream ordering”](../corpus/docs/overview/reference/reassignment-protocol.md#updates-stream-ordering) [SRC-0436AE8A3D / Causality and Time](../corpus/docs/overview/reference/ledger-causality.md)

## Authorization, trust, and privacy boundaries

Each synchronizer has its own operator/governance/trust and topology state. A transaction requires all relevant stakeholders to accept one common synchronizer for that state transition. Moving to a target can change which hosting participants receive contract data; private infrastructure may reduce operator/metadata exposure but does not change stakeholder visibility encoded by Daml. [SRC-E1B2C8D5F7 / Private Synchronizers / “Why Private Synchronizers”](../corpus/docs/global-synchronizer/extension-synchronizers/private-synchronizers.md#why-private-synchronizers)

The Global Synchronizer is documented as the common default trusted by broad participants, improving interoperability. A private synchronizer narrows operators/access and can tune policy/performance, but participants must trust/operate it and may pay reassignment latency/availability costs when composing with Global contracts. [SRC-CB6BCAA81A / Multi-Synchronizer Architecture / “Importance of the Global Synchronizer”](../corpus/docs/overview/learn/multi-synchronizer.md#importance-of-the-global-synchronizer)

## Constraints, failures, and operations

- No admissible common synchronizer means submission fails.
- Stakeholder connectivity, permissions, confirmation thresholds, and package vetting must align on the candidate target.
- Non-atomic reassignment introduces a pending window and repair risk.
- Each additional synchronizer adds endpoints/TLS, topology/package management, monitoring, upgrades, traffic/cost policy, and incident response.
- Different per-domain ordering and connection priority can produce surprising routing/stream observations if applications assume one chain. [SRC-BF9D21A402 / Connecting a Validator to Multiple Synchronizers / “Synchronizer connections” and “Synchronizer priority”](../corpus/docs/global-synchronizer/extension-synchronizers/linking-validator-multi-sync.md#synchronizer-connections)

## Relevant use cases

Hybrid private processing/global settlement, jurisdiction-specific processing, consortium workflows, latency-sensitive bilateral flow, cost isolation, and common-network DvP are explicit motivations. [SRC-99E06BD97E / Hybrid Synchronizer Pattern / “Why use a hybrid setup”](../corpus/docs/global-synchronizer/extension-synchronizers/hybrid-synchronizer-pattern.md#why-use-a-hybrid-setup)

## Common misconceptions and unresolved questions

- Multiple synchronizers do not create one total order across all Canton state.
- Connecting a participant to two synchronizers does not make every hosted party/package eligible on both.
- Global Synchronizer is a common coordination choice, not a mandatory home for every application contract.
- `OQ-005` tracks identity/topology portability wording; `OQ-012` tracks reassignment atomicity; `OQ-013` defers router behavior under concurrent reassignment/failure to engineering verification.

## Official sources

- [Multi-Synchronizer Architecture](https://docs.canton.network/overview/learn/multi-synchronizer.md)
- [Reassignment Protocol](https://docs.canton.network/overview/reference/reassignment-protocol.md)
- [Connecting a Validator to Multiple Synchronizers](https://docs.canton.network/global-synchronizer/extension-synchronizers/linking-validator-multi-sync.md)
