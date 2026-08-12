# Local Canton Research Portal Development Design

## Decision

Build the workspace as a local **Canton official documentation mirror with a team research overlay**. Official content remains read-only, team knowledge is stored as Git-tracked Markdown or MDX, and personal or derived state is stored in a local SQLite database.

This separation is required to keep official evidence intact, make shared research reviewable through Git, and prevent personal UI state or generated indexes from creating repository conflicts.

The December 2026 public testnet launch scope covers Canton and its services. MultiVM development remains a future workstream and is not part of the December 2026 public launch documentation scope.

## Product goals

The local portal must:

1. Render the official Canton documentation locally with the same information architecture and styling as closely as the official toolchain permits.
2. Provide English and unofficial Korean views without modifying the official English source.
3. Help each researcher track personal reading progress.
4. Publish AI-generated and human-edited summaries as shared, reviewable files.
5. Connect source pages to claims, open questions, topics, maps, and use cases.
6. Detect upstream changes and identify research artifacts that require review.
7. Allow official documentation updates without merging custom features into upstream files.

## Non-goals

- Modifying or contributing changes directly to the official Canton documentation repository.
- Inspecting Canton implementation source code or verifying documentation through runtime experiments.
- Running Canton nodes, LocalNet, tests, or protocol experiments.
- Providing real-time multi-user editing through a shared SQLite file.
- Launching MultiVM as part of the December 2026 public testnet.

## Four data layers

| Layer | Location | Authority | Mutability | Git policy |
| --- | --- | --- | --- | --- |
| Official authoring source | `upstream/cf-docs/` | Official `cf-docs` commit | Read-only | Git submodule, parent tracks the pinned commit |
| Published evidence snapshot | `corpus/` | Content served by `docs.canton.network` at retrieval time | Append or refresh through the collector | Tracked in the parent repository |
| Shared research overlay | `translations/`, `research/`, existing knowledge directories | Team-reviewed research | Editable through branches and review | Tracked in the parent repository |
| Personal and derived state | `data/local/research.sqlite`, `.generated/` | Individual user or rebuildable process | Freely mutable | Never tracked |

### Official authoring source

`upstream/cf-docs/` is a Git submodule pointing to a specific commit of the official [canton-network/cf-docs](https://github.com/canton-network/cf-docs) repository. It provides the MDX source, navigation configuration, assets, and styling inputs used to render the documentation.

The parent repository stores only the selected submodule commit. Local research features must not be committed inside the submodule.

### Published evidence snapshot

`corpus/` is the immutable-at-retrieval Markdown snapshot discovered through the official `llms.txt`. It records what the public documentation site served on a specific date, including URL, headings, retrieval time, and SHA-256.

The snapshot and the submodule are complementary. The snapshot supports evidence traceability to a deployed version, while the submodule supports local rendering and upstream history. A GitHub commit must not be assumed to be the exact deployed version unless that relationship is separately verified.

### Shared research overlay

Anything intended to be reused, reviewed, cited, or understood by another team member belongs in Markdown, MDX, Mermaid, or another text file tracked by Git. Shared material must not exist only in SQLite.

### Personal and derived state

Personal progress, UI preferences, drafts, browsing history, and rebuildable indexes belong in local SQLite or ignored generated directories. The SQLite database must never be shared over a network filesystem or committed to Git.

## Storage classification

### Git-tracked Markdown or MDX

| Item | Proposed path | Reason |
| --- | --- | --- |
| Korean translations | `translations/ko/<official-path>.mdx` | Shared content requiring diff, review, and source-version tracking |
| Three-line page summaries | `research/pages/<official-path>.md` | Shared AI draft and human edits |
| Page-level research analysis | `research/pages/<official-path>.md` | Cross-person knowledge linked to the source page |
| Default launch-scope profile | `research/scope/public-testnet.json` | Applies one reviewable decision consistently across the official corpus |
| Page-specific scope override | Page research frontmatter | Records an intentional exception to the default profile |
| Summary approval state | Page research frontmatter | Shared review state such as `ai_draft`, `human_edited`, or `approved` |
| Claims and open questions | Existing `claims/` and `questions/` | Shared evidence and engineering backlog |
| Topics, maps, glossary, use cases | Existing directories | Shared knowledge base |
| Translation terminology policy | `translations/glossary.md` | Consistent handling of Canton terms across translators |
| Upstream sync review notes | `research/sync/` when a durable report is needed | Shared record of source changes that affect conclusions |

One research file per official page is preferred over one large registry. This reduces Git merge conflicts and makes ownership and review boundaries clear.

### Local SQLite

| Item | Reason |
| --- | --- |
| Personal page status: `unreviewed`, `complete` | Applies to one researcher and changes frequently |
| Personal Favorites | Applies to one researcher and changes frequently |
| Last visited page and recent-history list | Personal navigation state |
| Preferred language, theme, and collapsed panels | Personal UI settings |
| Bookmarks and private highlights | Personal until deliberately published |
| Summary or translation autosave drafts | Prevents work loss before publishing a shared file |
| AI chat sessions and temporary prompts | Potentially large and usually personal |
| Full-text search index and parsed-document cache | Rebuildable and potentially large |
| Upstream file hash cache and stale-comparison cache | Derived data that can be regenerated |
| Pending local write queue | Supports safe autosave and retry behavior |

### Generated and ignored data

| Item | Proposed path |
| --- | --- |
| Composed local Mintlify site | `.generated/site/` |
| Build cache | `.generated/cache/` |
| Search index exports | `.generated/index/` |
| Temporary sync reports | `.generated/sync/` |

## Shared page research format

Each source page can have a matching research file:

```yaml
---
source_id: SRC-A3F46FF397
source_path: overview/understand/what-is-canton
source_commit: <cf-docs-commit>
source_sha256: <source-file-sha256>
scope: included
scope_reason: "Required for the public testnet foundation"
summary_status: ai_draft
updated_at: 2026-08-12
updated_by: team-member
---
```

```markdown
## Three-line summary

1. First summary line.
2. Second summary line.
3. Third summary line.

## Research notes

Page-specific mechanism analysis and links to related topics.

## Related records

- Claims: CLM-...
- Open questions: OQ-...
```

The initial summary may be generated by AI, but it must remain labeled `ai_draft` until a team member edits or approves it. The UI renders this section as collapsed by default and allows edits through the local portal.

An edit is first autosaved to SQLite. Selecting **Publish to workspace** writes the corresponding Markdown file after checking that its Git blob or filesystem version has not changed since editing began. If it changed, the UI shows a conflict instead of overwriting the file.

## Korean translation versioning

Korean pages mirror the official source path under `translations/ko/`. Each translated file records:

```yaml
---
source_path: overview/understand/what-is-canton
source_commit: <cf-docs-commit>
source_sha256: <source-file-sha256>
translation_status: ai_draft
translated_at: 2026-08-12
reviewed_by: null
---
```

The portal compares `source_sha256` with the current upstream file. A mismatch displays `Translation update required`; it does not silently overwrite the translation. Updated translations are committed through the normal branch and review workflow.

The translation glossary must preserve Canton component names, API names, protocol terms, code, identifiers, and product names in English. Every Korean page must display an `Unofficial Korean translation` notice and link to the official English page.

Mintlify supports locale-based routing and a language switcher through `docs.json`. The generated site configuration must partition the complete English and Korean navigation under `navigation.languages`; `navigation.global.languages` is only a global link switcher and does not establish locale-aware document navigation. The overlay also rewrites internal document links inside a Korean article to the corresponding `/ko/` route when that translation exists. Explicit ENG controls remain unchanged, and untranslated targets fall back to the official English page. See the official [Mintlify internationalization guide](https://www.mintlify.com/docs/guides/internationalization).

## Local web architecture

```text
Browser
  -> Mintlify local documentation site
       -> Official MDX and navigation from upstream/cf-docs
       -> Korean MDX and shared research files from the parent repository
       -> Research Overlay JavaScript and CSS
  -> Local research API
       -> SQLite for personal and derived state
       -> Controlled file writer for shared Markdown and MDX
```

The build process composes an ignored `.generated/site/` directory from the pinned upstream source and the parent repository overlay. It then runs the official local documentation toolchain from that generated directory. The upstream submodule remains unchanged.

Mintlify supports local preview with `mint dev` and globally included JavaScript and CSS. The overlay can therefore add sidebar status controls and the summary panel while preserving the official navigation and article layout. Mintlify warns that styling selectors can change, so upstream updates require browser smoke tests. See [local preview](https://www.mintlify.com/docs/cli/preview) and [custom scripts](https://www.mintlify.com/docs/customize/custom-scripts).

## Sidebar page-state UX

Each page row keeps two compact controls with distinct ownership and meaning:

| Position | Display | State | Storage |
| --- | --- | --- | --- |
| Left | Gray `☆` | Not a Favorite | Local SQLite |
| Left | Filled purple `★` | Favorite | Local SQLite |
| Right | Empty box | `unreviewed` and in scope | Local SQLite |
| Right | Green `✓` box | `complete` and in scope | Local SQLite |
| Right | Gray `✕` box | Excluded from the launch scope | Git-tracked page research metadata |

The left star toggles Favorite independently of review and scope, so an excluded page can still be saved for later reference. The right control advances `empty → complete → excluded → empty`. Moving from complete to excluded asks for a reason because that transition changes shared launch-scope metadata. Moving from excluded to empty creates an explicit include override and resets personal progress to `unreviewed`.

Progress and Favorites are stored by stable `source_id`, not by page title. Renaming a title therefore does not lose personal state. Legacy `in_progress` rows are migrated to `unreviewed`; the UI no longer exposes an intermediate progress state.

## Scope exclusion UX

Scope remains independent from personal Favorites and is shared rather than personal. The Git-tracked profile at `research/scope/public-testnet.json` defines the conservative default for the current standalone private Synchronizer public testnet. It excludes only documentation that clearly depends on historical releases, Global Synchronizer economics and rewards, Super Validator-only operations, or existing Global network services. Core protocol, Daml, APIs, topology, onboarding, security, monitoring, wallet, custody, traffic, and private Synchronizer material remains included.

A page-level action named **Exclude from current scope** or **Include in scope** writes an explicit override and reason to the shared page research file. A summary publish does not create a scope override by itself, so later profile updates continue to apply unless a team member deliberately made a page-specific decision.

Excluded pages show a gray `X` in the right-side status box. Activating that box includes the page and returns it to the empty `unreviewed` state. The left Favorite star remains independently available.

The `/research/scope` view lists only X-marked pages. It shows the active profile and conditions, exclusion counts, search, documentation-area and reason filters, per-page rationale, and ENG/KOR links when a Korean translation exists.

Because exclusion changes the team's research and launch coverage, it must be committed and reviewed through Git rather than stored only in SQLite.

## Summary, claims, and questions rendering

Each official document page contains a collapsed **Research summary** panel above the article body. It displays:

- The three-line summary and its `ai_draft`, `human_edited`, or `approved` state.
- Source commit and stale status.
- Links to related claims, open questions, topics, and maps.
- Edit and publish actions.

The portal also exposes dedicated pages:

- `/research/claims`
- `/research/questions`
- `/research/progress`
- `/research/scope`
- `/research/changes`

Claims and questions remain stored in their existing Markdown registries for the first implementation. A build-time parser produces the indexes and page backlinks. They can later move to one-file-per-record storage if concurrent editing of the registries becomes a frequent conflict.

## Suggested SQLite schema

```sql
page_progress(
  source_id TEXT PRIMARY KEY,
  status TEXT NOT NULL,
  updated_at TEXT NOT NULL
)

user_settings(
  key TEXT PRIMARY KEY,
  value_json TEXT NOT NULL,
  updated_at TEXT NOT NULL
)

drafts(
  source_id TEXT NOT NULL,
  kind TEXT NOT NULL,
  content TEXT NOT NULL,
  base_file_sha256 TEXT,
  version INTEGER NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY(source_id, kind)
)

bookmarks(
  source_id TEXT NOT NULL,
  anchor TEXT,
  note TEXT,
  created_at TEXT NOT NULL
)

document_cache(
  source_id TEXT PRIMARY KEY,
  source_sha256 TEXT NOT NULL,
  parsed_json TEXT,
  indexed_at TEXT NOT NULL
)
```

Use SQLite WAL mode, short write transactions, a busy timeout, and optimistic version checks for drafts. One portal process should own database writes. SQLite remains local to each clone.

Use SQLite FTS5 for English, Korean, and research-note full-text search in the first implementation. A vector database is not required for the initial corpus size and can be added only if citation-backed semantic retrieval is demonstrably inadequate.

## Upstream synchronization workflow

1. Fetch the official `cf-docs` submodule remote.
2. Select and pin the intended upstream commit in a dedicated branch.
3. Refresh `corpus/` separately when a new deployed-site evidence snapshot is required.
4. Rebuild the source manifest and hashes.
5. Compare summary and translation `source_sha256` values with the new source.
6. Display stale summaries and translations in the portal.
7. Rebuild the generated site and full-text index.
8. Run link validation and overlay browser smoke tests.
9. Review and merge the upstream-sync change as a dedicated pull request.

The sync process must never rewrite shared summaries or translations automatically. It may generate a review queue and proposed AI drafts, but publishing remains an explicit workspace change.

## Git collaboration workflow

1. Pull the parent repository and initialize the pinned submodule.
2. Create a short-lived branch for translation, summary, analysis, or scope changes.
3. Edit through the portal or directly in Markdown/MDX.
4. Review the file diff, source hash, classification, and links.
5. Commit and submit the change for review.
6. Resolve conflicts at the per-page file level.

Personal progress and drafts remain available locally across branch changes but never appear in commits.

## Recommended repository layout

```text
canton-research-workspace/
├── upstream/
│   └── cf-docs/                    # Read-only Git submodule
├── corpus/                         # Published-site evidence snapshots
├── translations/
│   ├── glossary.md
│   └── ko/                         # Korean MDX mirroring official paths
├── research/
│   ├── pages/                      # Shared summary and analysis per page
│   └── sync/                       # Durable upstream review reports
├── claims/
├── questions/
├── topics/
├── maps/
├── glossary/
├── use-cases/
├── portal/                         # Future local portal source
├── data/local/                     # SQLite, ignored
└── .generated/                     # Composed site and caches, ignored
```

## Implementation phases

### Phase 1: faithful local mirror

- Add the pinned `cf-docs` submodule.
- Generate and run the local Mintlify site.
- Preserve official English navigation and styling.
- Add the ignored composition directory.

### Phase 2: research overlay MVP

- Add the local API and SQLite migrations.
- Add tri-state personal progress and scope-exclusion badges.
- Render and edit collapsed three-line summaries.
- Render claims, questions, and page backlinks.

### Phase 3: Korean documentation

- Generate English and Korean navigation.
- Add translation glossary and source-version metadata.
- Add stale translation detection and side-by-side comparison.

### Phase 4: research quality tools

- Add unified English, Korean, and research-note search.
- Add source-section selection for creating claims and questions.
- Add progress, scope, and upstream-change dashboards.
- Add citation-constrained document Q&A only after source linkage is enforced.

## MVP completion criteria

The first usable portal is complete when:

- The pinned official English MDX renders locally without editing the submodule.
- English and available Korean pages can be selected through the language UI.
- Personal progress survives restarts but does not appear in Git.
- Team scope exclusions render as an `X` badge and are Git-reviewable.
- Every page can display, edit, and publish its shared three-line summary.
- Claims and open questions render globally and link back to relevant source pages.
- An upstream source change makes affected translations and summaries visibly stale.
- Upstream sync, local build, and research publishing are documented and reproducible.
- The official source, deployed snapshot, shared research, and local data remain distinguishable in both the filesystem and the UI.

## Implementation status

The local portal MVP was implemented on 2026-08-12. Phases 1 and 2 are complete, and the Phase 3 workflow now validates and renders complete Korean translation batches in a dedicated navigation product. Translation coverage remains incremental team research work and is recorded in `translations/STATUS.md`.

Phase 4 currently includes English/Korean/research full-text search, source-linked evidence capture for claim or question drafts, claims/questions backlinks, and progress/scope/upstream-change dashboards. Generative document Q&A remains intentionally deferred until a model provider, credential policy, citation validation, and fail-closed behavior are approved. This prevents uncited model output from entering a documentation-only evidence workflow.

## Required conditions

The design remains valid only if official files stay read-only, every shared conclusion is stored in a reviewable text artifact, local SQLite files are ignored, and source commit or hash metadata is preserved for every translation and summary.
