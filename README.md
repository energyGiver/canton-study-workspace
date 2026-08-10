# Canton Documentation Research Workspace

## Decision and purpose

This repository is a documentation-only technical knowledge base for Canton Network. Official Canton documentation is the primary evidence source because this phase is intended to reconstruct the documented protocol and application mental model before any source-code analysis or runtime verification.

The knowledge base is useful only under three conditions: conclusions remain traceable to the corpus, inference is labeled, and unresolved documentation gaps remain open rather than being filled from model memory.

## Start here

1. Read [the concept map](maps/concept-map.md) for the learning sequence and cross-topic dependencies.
2. Follow the topic sequence in [the topic index](topics/README.md).
3. Use [the claim ledger](claims/claim-ledger.md) for classified conclusions and [the open questions registry](questions/open-questions.md) for gaps.
4. Consult [the glossary](glossary/canton-glossary.md) when terminology differs across documentation areas.
5. Use `corpus/manifest.jsonl` to resolve a source ID to its exact URL, local file, headings, retrieval time, and checksum.

## Repository layout

| Path | Purpose |
| --- | --- |
| `corpus/` | Verbatim official Markdown snapshot, official index, checksums, and retrieval metadata |
| `maps/` | Learning map and lightweight Mermaid diagrams |
| `topics/` | Cross-document mechanism notes organized by technical topic |
| `claims/` | Important conclusions classified as `EXPLICIT`, `INFERRED`, or `UNCLEAR` |
| `questions/` | Documentation gaps and the later engineering-phase backlog |
| `use-cases/` | Use cases derived from protocol and application mechanisms |
| `glossary/` | Curated terminology with ambiguity notes |
| `scripts/` | Reproducible official-document collector; it does not inspect Canton source code |

## Evidence model

- `EXPLICIT`: the cited official text directly states the conclusion.
- `INFERRED`: the conclusion follows from multiple cited facts; the reasoning is written out.
- `UNCLEAR`: the official corpus is incomplete, conflicting, or too imprecise to support one conclusion.

Topic notes use source IDs such as `SRC-A3F46FF397`. IDs are derived from source URLs and therefore remain stable if the official index is reordered. Local links support offline review; each note also lists the official URLs.

## Corpus snapshot

- Entry point: `https://docs.canton.network/llms.txt`
- Retrieved: 2026-08-10
- Documents: 804 Markdown pages
- Integrity: SHA-256 for every response body
- Coverage: Overview, App Development, Global Synchronizer, Integrations, SDKs/Tools, API/reference material linked by the official index

See [corpus/README.md](corpus/README.md) for the manifest schema and refresh procedure.

## Phase boundary

This repository does not inspect Canton source repositories, execute tests, deploy LocalNet or nodes, run runtime experiments, or verify documentation against implementation. Documentation may describe those activities, but this phase records what the documentation says rather than performing them. Items requiring those methods are explicitly deferred in the open questions registry.

## Completion standard

This snapshot establishes the research structure, full official corpus, dependency maps, topic mechanisms, classified claim ledger, curated glossary, use-case explanations, and an engineering backlog. It is a baseline knowledge base, not a claim that every one of the 804 pages has been exhaustively interpreted. Future refreshes must diff the corpus first, then revisit claims affected by changed sources.
