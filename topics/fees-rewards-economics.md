# Fees, Rewards, and Economics

**Structured coverage:** definition; why it exists; actors/components; responsibilities; state/data; end-to-end mechanism; relationships with other concepts; authorization; trust; privacy; constraints; failure/exception conditions; operational implications; relevant use cases; common misconceptions; unresolved questions; official sources.

## Decision and mental model

Canton Coin economics separates synchronizer traffic purchase/burn from governed minting/reward allocation. The corpus contains a current traffic-based app-reward page alongside older marker-based descriptions, so exact current reward behavior is `UNCLEAR` until version/network activation is reconciled. [SRC-B246B6729B / Tokenomics of the Global Synchronizer / “Burn-Mint Equilibrium”](../corpus/docs/overview/reference/tokenomics-of-gs.md#burn-mint-equilibrium) [SRC-66FC36138B / Traffic-Based App Rewards / “Overview” and “Activation”](../corpus/docs/global-synchronizer/splice-fundamentals/traffic-based-app-rewards.md#overview)

## Definition and why it exists

CC is the Global Synchronizer utility token. Validators receive a regenerating base traffic allocation and burn CC to purchase extra byte-denominated traffic. Governed issuance lets SVs, validators, applications and a development fund mint within configured curves/rounds in exchange for infrastructure/activity. The model intends to relate network utility burn to contributor issuance. [SRC-B246B6729B / Tokenomics of the Global Synchronizer / “Traffic Economics” and “Issuance Curve and Minting Schedule”](../corpus/docs/overview/reference/tokenomics-of-gs.md#traffic-economics)

## Actors, contracts, and state

| Actor/mechanism | Role/state |
| --- | --- |
| Sending validator | Shares traffic balance across hosted parties; base allowance then paid credits |
| SV/DSO governance | Sets traffic price, scaling, issuance/reward configuration and conversion-rate process |
| `AmuletRules` / round contracts | Fee/issuance schedule and per-round snapshots/calculations |
| SV | Infrastructure reward coupons/weights and governance participation |
| Validator | Activity reward tied to documented burns; former liveness reward discontinued in cited page |
| Featured application | Eligible app reward under current configured reward scheme |
| Scan/SV Apps | Measure/agree/expand traffic-based reward commitments in CIP-0104 description |

## Traffic mechanism

The sender, not each recipient, is charged. Base traffic regenerates up to a burst limit/window and is consumed before paid traffic. Extra credits are bought by burning CC at the governed USD/MB price and current CC/USD conversion; cost scales with payload bytes and recipient delivery factor. Traffic is participant/validator-level, so hosted users share capacity and external parties rely on their host to buy it. [SRC-B246B6729B / Tokenomics of the Global Synchronizer / “Traffic Economics”](../corpus/docs/overview/reference/tokenomics-of-gs.md#traffic-economics)

Each SV publishes a preferred conversion rate and the cited page says the round uses the median, recorded in `OpenMiningRound`. Fee parameters are snapshotted by round to make transactions in the round use consistent values. [SRC-B246B6729B / Tokenomics of the Global Synchronizer / “Fee Schedules and Round Snapshots” and “CC-USD Conversion Rate”](../corpus/docs/overview/reference/tokenomics-of-gs.md#fee-schedules-and-round-snapshots)

## Reward mechanism and documentation conflict

The overview tokenomics page describes `FeaturedAppActivityMarker`/`AppRewardCoupon` as active accounting. The newer dedicated page says CIP-0104 replaces markers with off-ledger, sequencer-traffic-based computation: Scan aggregates per featured provider/round into a Merkle commitment, a supermajority of SVs confirms the root on ledger, and the SV App creates `RewardCouponV2` leaves, one per eligible party/round with TTL and beneficiary support. Activation is governed by `rewardConfigMintingVersion` and can be dry-run first. [SRC-B246B6729B / Tokenomics of the Global Synchronizer / “Reward Distribution”](../corpus/docs/overview/reference/tokenomics-of-gs.md#reward-distribution) [SRC-66FC36138B / Traffic-Based App Rewards / “How It Works” and “Activation”](../corpus/docs/global-synchronizer/splice-fundamentals/traffic-based-app-rewards.md#how-it-works)

The cited tokenomics page also says CIP-0078 removed nearly all CC transfer/lock fees, retaining per-UTXO holding-fee/dust-expiry behavior, and CIP-0096 reduced validator liveness reward to zero effective 2026-04-30. These statements supersede older glossary wording but remain versioned documentation claims rather than implementation verification. [SRC-6472F63A2D / Canton Coin Tokenomics / “Transfer and Lock Fees,” “UTXO Model and Dust Expiry,” and “Burn-Mint Equilibrium”](../corpus/docs/overview/reference/canton-coin-tokenomics.md#transfer-and-lock-fees-post-cip-0078)

## Authorization, trust, privacy, constraints, and failures

Economic configuration and featured-app rights are governed through DSO votes; round/reward automation relies on SV agreement and Scan-derived data in the traffic-based design. Users trust that price inputs, traffic measurement, reward roots and governance are correct under the SV threshold. Public Scan/CC visibility is broader than generic private contracts. [SRC-4FA5D0A091 / SV Governance Reference / “Parameter Governance”](../corpus/docs/overview/reference/sv-governance-reference.md#parameter-governance) [SRC-66FC36138B / Traffic-Based App Rewards / “How It Works”](../corpus/docs/global-synchronizer/splice-fundamentals/traffic-based-app-rewards.md#how-it-works)

- Insufficient traffic rejects submissions; operators need automatic/manual top-up and reserve planning.
- Reward coupons/rounds/TTLs can expire, and external-party minting needs delegation or custom signed automation.
- CC UTXO fragmentation creates holding-fee/dust management exposure.
- Configuration/activation/network version changes can invalidate fixed fee/reward assumptions.
- The burn-mint page describes an aim/equilibrium, not a guaranteed market-price peg. [SRC-D3F9087E37 / Minting Delegations](../corpus/docs/global-synchronizer/splice-fundamentals/rewards-minting.md) [SRC-B246B6729B / Tokenomics of the Global Synchronizer / “Burn-Mint Equilibrium”](../corpus/docs/overview/reference/tokenomics-of-gs.md#burn-mint-equilibrium)

## Use cases, misconceptions, and unresolved questions

Traffic funds shared infrastructure and rate-limits abuse; rewards incentivize infrastructure, usage and featured applications; holding fees discourage dust.

- “Every Canton transaction pays CC” is false for private synchronizers and may be false within Global base allocation.
- “CC transfers still charge legacy admin fees” conflicts with post-CIP-0078 pages.
- `OQ-017` asks which app reward scheme is active per network/snapshot and which older pages are historical.
- `OQ-018` asks for authoritative formulas/current values rather than descriptive examples.

## Official sources

- [Tokenomics of the Global Synchronizer](https://docs.canton.network/overview/reference/tokenomics-of-gs.md)
- [Canton Coin Tokenomics](https://docs.canton.network/overview/reference/canton-coin-tokenomics.md)
- [Traffic-Based App Rewards](https://docs.canton.network/global-synchronizer/splice-fundamentals/traffic-based-app-rewards.md)
- [SV Governance Reference](https://docs.canton.network/overview/reference/sv-governance-reference.md)
