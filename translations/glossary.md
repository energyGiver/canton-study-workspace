# Canton Korean Translation Glossary

## Decision

Preserve Canton product names, component names, protocol terms, API names, code, identifiers, and configuration keys in English. Translate explanatory prose into natural Korean so readers can search the official English terminology and communicate with operators and developers without terminology drift.

## Terms preserved in English

- Canton Network
- Daml
- Party
- Participant Node
- Validator
- Super Validator
- Synchronizer
- Global Synchronizer
- Sequencer
- Mediator
- BFT Orderer
- Topology
- Ledger API
- JSON Ledger API
- Daml contract
- Daml package
- DAR
- Package Vetting
- Active Contract Set and ACS
- Canton Coin and CC
- Traffic Credit
- Reassignment
- External Party
- External Signing
- Command
- Transaction
- Contract ID
- Update ID

## Translation rules

1. Keep the source heading hierarchy, links, code blocks, diagrams, tables, and frontmatter structure.
2. Do not translate code, API fields, CLI commands, configuration names, filenames, package names, or identifiers.
3. Introduce a difficult English term with a short Korean explanation when needed, but continue using the English term afterward.
4. Preserve the exact meaning of authorization, privacy, trust, and failure statements. Do not strengthen or weaken guarantees.
5. Display an `Unofficial Korean translation` notice and link to the official English source.
6. Record `source_commit`, `source_sha256`, `translation_status`, and translation date in every Korean MDX file.
7. Mark a translation `stale` in the portal when the current official source hash differs from the recorded hash.

## Translation status

- `ai_draft`: AI-generated translation awaiting human review.
- `human_edited`: reviewed or edited by a team member but not finally approved.
- `approved`: accepted as the current team translation for the recorded source hash.
- `stale`: computed by the portal when the source hash changes; do not write this value manually.
