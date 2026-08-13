# Shared Inline Comments

This directory stores comments explicitly published from the local documentation portal. Official English MDX and translated MDX remain unchanged.

## Layout

```text
research/comments/
└── <source_id>/
    └── <comment_id>.md
```

One file per comment reduces Git merge conflicts. The portal creates, updates, and deletes these files with optimistic hash checks. Review the resulting Markdown diff before committing it.

## Anchor data

Each comment records:

- Stable `source_id`, official path, pinned source commit, and official source SHA-256.
- Language and rendered-language document SHA-256.
- Exact selected quote, bounded prefix/suffix context, and start/end text offsets.
- Nearest heading, author label, created time, and updated time.
- Shared resolve state, resolver label, and resolved time.
- Escaped plain-text comment content under `## Comment`.

The selector follows the [W3C Web Annotation Data Model](https://www.w3.org/TR/annotation-model/). The portal restores a saved position only when the exact quote still matches, or restores a quote fallback only when prefix/suffix context identifies one unique candidate. Ambiguous or missing anchors are left unresolved rather than guessed.

Incomplete drafts are not stored here. They remain in the local ignored SQLite database at `data/local/research.sqlite` until the researcher selects **Publish to Git**.
