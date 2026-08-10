# Synchronizers and Reassignment

**Structured coverage:** definition; why it exists; actors/components; responsibilities; state/data; end-to-end mechanism; relationships with other concepts; authorization; trust; privacy; constraints; failure/exception conditions; operational implications; relevant use cases; common misconceptions; unresolved questions; official sources.

## Decision and mental model

A synchronizer is a selectable coordination/trust domain for contract changes. A contract’s stakeholders agree on one current assignation, and a Daml transaction’s inputs must be co-assigned to one suitable synchronizer; moving a contract is a two-request unassignment/assignment protocol with a pending interval. [SRC-CB6BCAA81A / Multi-Synchronizer Architecture / “Assignation” and “Reassignment protocol”](../corpus/docs/overview/learn/multi-synchronizer.md#reassignment-protocol)

## Definition and purpose

Synchronizers offer ordered confidential delivery and mediated confirmation under a particular governance, performance, cost, access, and failure model. Reassignment exists so shared state can move to a synchronizer trusted/reachable by all transaction stakeholders and compatible with all input packages. The contract payload remains on stakeholder participants; assignation identifies which synchronizer coordinates its next changes. [SRC-92FDECC024 / Reassignment Protocol / “Why reassignments exist”](../corpus/docs/overview/reference/reassignment-protocol.md#why-reassignments-exist)

## Actors, state, and responsibilities

| Actor/state | Responsibility |
| --- | --- |
| Stakeholders/signatories | Agree through confirmation on moving the contract |
| Submitting participant/router | Choose target, obtain time proof, submit unassign/assign |
| Reassigning participant | Connected/hosting appropriately on source and target; checks continuity/double-spend protections |
| Source synchronizer | Coordinate unassignment and make contract inactive there |
| Target synchronizer | Supply topology time proof and coordinate assignment |
| Reassignment counter/unassign ID | Correlate lifecycle and prevent replay/duplication |
| Assignment exclusivity | Temporary right for initiator to finish before others may do so |

## End-to-end mechanism

1. Determine an admissible target: relevant stakeholders are hosted, required packages vetted, and confirmation thresholds satisfiable at a fixed target topology timestamp.
2. Obtain a target time proof.
3. Submit unassignment on the source. Source-side signatory unassigning participants validate/confirm; on commit the contract becomes inactive and pending assignment, and its counter increments.
4. Submit assignment on the target using the unassign ID. Target-side signatory assigning participants validate the source proof/counter/topology conditions.
5. On commit the same contract becomes active on the target; an assigned event can carry contract data to participants whose visibility begins on the target. [SRC-92FDECC024 / Reassignment Protocol / “Two-step process,” “Key definitions,” and “Ledger API data”](../corpus/docs/overview/reference/reassignment-protocol.md#two-step-process-unassignment-and-assignment)

Automatic routing selects an admissible synchronizer by priority, then fewest reassignments, then lowest synchronizer ID; explicit Ledger API commands allow prescribed routing. A prescribed but unsuitable target fails. [SRC-92FDECC024 / Reassignment Protocol / “Automatic vs. explicit reassignment”](../corpus/docs/overview/reference/reassignment-protocol.md#automatic-vs-explicit-reassignment)

## Authorization, trust, and privacy

Signatories confirm reassignment because they can authorize the contract’s destruction/recreation semantics; observer confirmation adds no equivalent safety according to the detailed page. Hosting permissions and thresholds are evaluated separately on source and target topology snapshots. [SRC-CB6BCAA81A / Multi-Synchronizer Architecture / “Confirmation policies”](../corpus/docs/overview/learn/multi-synchronizer.md#confirmation-policies)

Stakeholders must trust both synchronizers during the move and at least some dual-connected reassigning participants to protect continuity. The assignment can make a contract enter or leave a participant’s visibility because hosting differs between synchronizers; the target assigned event supplies payload to newly informed participants. [SRC-92FDECC024 / Reassignment Protocol / “Contracts entering and leaving visibility”](../corpus/docs/overview/reference/reassignment-protocol.md#contracts-entering-and-leaving-visibility)

## Constraints, failures, and operational implications

- The detailed documentation explicitly calls the procedure non-atomic across two confirmation requests. Between them the contract is inactive/pending; topology changes can make completion impossible and may require topology repair/manual repair service. [SRC-CB6BCAA81A / Multi-Synchronizer Architecture / “Overview” under “Reassignment protocol”](../corpus/docs/overview/learn/multi-synchronizer.md#overview-1) [SRC-92FDECC024 / Reassignment Protocol / warning under “Validation rules”](../corpus/docs/overview/reference/reassignment-protocol.md#validation-rules)
- Reassignment competes with exercises, including some read-only transaction workflows, because the contract is locked.
- All inputs of a transaction must ultimately be on one suitable synchronizer; there is no single atomic commit spanning independently ordered synchronizers in the described flow.
- Updates from different synchronizers have no global comparable time/order and can be merged differently at participants. [SRC-92FDECC024 / Reassignment Protocol / “Updates stream ordering”](../corpus/docs/overview/reference/reassignment-protocol.md#updates-stream-ordering)

## Use cases, misconceptions, and unresolved questions

Reassignment enables private-to-global settlement, jurisdiction/governance changes, bringing asset and cash inputs together for DvP, and lifecycle-based cost/performance routing.

- “Atomic from stakeholders’ perspective” appears earlier on the multi-synchronizer page, while the detailed section says “non-atomic”; `OQ-012` records the contradiction and uses the detailed two-step/pending description as the working model.
- “Cross-synchronizer transaction” is shorthand for routing/reassigning inputs then executing on one synchronizer, not a documented simultaneous two-synchronizer Daml commit.

## Official sources

- [Multi-Synchronizer Architecture](https://docs.canton.network/overview/learn/multi-synchronizer.md)
- [Reassignment Protocol](https://docs.canton.network/overview/reference/reassignment-protocol.md)
