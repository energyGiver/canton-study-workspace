# Official documentation corpus

## Decision

The active corpus inventory follows file-backed MDX routes in the pinned official `docs.json` navigation. Official source files remain unmodified in the `upstream/cf-docs/` submodule, which makes Git diffs meaningful and keeps research prose separate from source evidence. The earlier `llms.txt` download remains as a historical 804-page snapshot.

## Files

- `llms.txt`: verbatim historical discovery index.
- `docs/`: 804 historical Markdown responses stored under their official URL paths.
- `manifest.jsonl`: one JSON object per active file-backed official navigation page, in official navigation order.
- `retrieval-metadata.json`: corpus-level retrieval details.
- `upstream/cf-docs/docs-main/`: pinned official MDX source files referenced by the active manifest.

## Manifest fields

| Field | Meaning |
| --- | --- |
| `source_id` | Stable URL-derived identifier used by notes and claims |
| `title` | Link title in official `llms.txt` |
| `source_url` | Exact official Markdown URL |
| `document_path` | Path portion of the official URL |
| `local_path` | Repository path to the pinned official MDX source file |
| `section_hierarchy` | Markdown headings with level and source line |
| `retrieval_date` / `retrieved_at` | Snapshot date and UTC timestamp |
| `sha256` / `bytes` | Integrity and size of the response body |

## Refresh procedure

Run `python3 -m portal sync` to inspect upstream changes. Use `python3 -m portal sync --update` to pin the reviewed upstream commit and regenerate `manifest.jsonl` from official file-backed navigation. Then run `python3 -m portal translations`, inspect `.generated/translation-backlog.json`, and update only translations affected by meaningful source diffs.

The Git-ignored local exclusion policy skips only exact official paths. It does not use prefix or wildcard rules, so newly added documentation cannot disappear from the translation review backlog. Changed source sections require a translation and claim review because newer documentation can invalidate an `EXPLICIT` classification or resolve an `UNCLEAR` item.

The collector fails the run if any indexed Markdown page cannot be downloaded. It does not delete pages that disappear from a later index; removals must be reviewed manually so evidence is not destroyed silently.
