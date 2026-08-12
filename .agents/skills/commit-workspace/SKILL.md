---
name: commit-workspace
description: Create, amend, or review Git commits in this repository using focused one-line Conventional Commit messages. Use when Codex is asked to commit changes, prepare a commit, amend a commit, write a commit message, or verify commit authorship. Do not use for read-only Git history questions that require no commit operation.
---

# Commit Workspace

Create a focused commit with a single clear Conventional Commit subject and human-only authorship.

## Workflow

1. Read `AGENTS.md` and inspect `git status`, the relevant diff, and recent commit history.
2. Preserve unrelated user changes. Stage only files that belong to the requested change unless the user explicitly requests all changes.
3. Run checks appropriate to the changed files. Do not claim checks that were not run.
4. Select the narrowest accurate type and scope.
5. Create the commit with exactly one subject line and no body or trailers.
6. Verify the final subject, author, committer, changed files, and clean or expected worktree state.

## Message Format

Use exactly:

```text
type(scope): clear and well summarized comment
```

Allowed types:

- `feat`: add user-visible capability or a substantial workspace feature.
- `fix`: correct faulty behavior or incorrect content.
- `docs`: change documentation only.
- `refactor`: restructure without changing behavior.
- `test`: add or update tests only.
- `build`: change build tooling or dependencies.
- `ci`: change continuous integration.
- `chore`: perform repository maintenance not covered above.
- `revert`: revert a specific earlier commit using `git revert`.

Choose a short module or domain for `scope`, such as `portal`, `research`, `corpus`, or `workspace`. Write the summary in imperative mood, keep it specific, omit the final period, and target 72 characters or fewer for the full subject.

Examples:

```text
feat(portal): define the local research workspace architecture
docs(research): clarify source and storage ownership
fix(corpus): preserve removed pages during refresh
```

## Authorship Rules

- Use the repository-configured human `user.name` and `user.email` for both author and committer.
- Never add `Co-authored-by` or similar attribution for Codex, Claude Code, ChatGPT, Copilot, or any other AI agent.
- Never identify an AI agent as author, committer, signer, or contributor.
- Do not add generated-by notices to the commit message.
- Do not change human authorship unless the user explicitly requests it.

## Rewrite and Revert Safety

- Amend only when the user explicitly asks to redo the latest commit and the target commit is verified.
- Use `git revert` only when the user explicitly wants the content of an earlier commit reversed.
- Do not use `git reset`, interactive rebase, force push, or other history rewrites without explicit authorization and an exact target.
- If the word "revert" could mean either undoing content or redoing a commit, inspect the history and choose the non-destructive interpretation unless the requested target is unambiguous.

## Verification

After committing, verify:

- The subject matches `type(scope): summary` and contains one line.
- The author and committer match the repository-configured human identity.
- No AI attribution or `Co-authored-by` trailer exists.
- The commit contains only intended files.
- Remaining worktree changes are reported clearly.
