# Official documentation corpus

## Decision

The corpus preserves the official Markdown response bodies without rewriting them. This makes Git diffs meaningful and keeps research prose separate from source evidence.

## Files

- `llms.txt`: verbatim discovery index.
- `docs/`: documents stored under their official URL paths.
- `manifest.jsonl`: one JSON object per indexed document, in official index order.
- `retrieval-metadata.json`: corpus-level retrieval details.

## Manifest fields

| Field | Meaning |
| --- | --- |
| `source_id` | Stable URL-derived identifier used by notes and claims |
| `title` | Link title in official `llms.txt` |
| `source_url` | Exact official Markdown URL |
| `document_path` | Path portion of the official URL |
| `local_path` | Repository path to the saved response body |
| `section_hierarchy` | Markdown headings with level and source line |
| `retrieval_date` / `retrieved_at` | Snapshot date and UTC timestamp |
| `sha256` / `bytes` | Integrity and size of the response body |

## Refresh procedure

Run `python3 scripts/collect_official_docs.py --root .`, inspect the Git diff, and do not update research conclusions mechanically. Changed source sections require a claim-by-claim review because newer documentation can invalidate an `EXPLICIT` classification or resolve an `UNCLEAR` item.

The collector fails the run if any indexed Markdown page cannot be downloaded. It does not delete pages that disappear from a later index; removals must be reviewed manually so evidence is not destroyed silently.
