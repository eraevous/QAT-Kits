# .aec: purpose and justification records (Telosmith, formerly AEC)

- `records.jsonl`: append-only reasoning records (purpose, requirements, claims, evidence, decisions,
  authorities). Never edit a line; append a new version. Vocabulary:
  https://github.com/eraevous/Telosmith/blob/main/docs/reasoning-vocabulary.md
- `edges.jsonl`: the structural snapshot of the code (`aec edges`). Generated, so it is git-ignored
  (`.aec/.gitignore`): regenerate it rather than committing or hand-editing it.
- `snippets/`: the Claude Code hook and CI job as `aec init` generated them. Both are installed: the hook
  at `.claude/settings.json` (identical) and the CI job at `.github/workflows/telosmith.yml` (renamed
  `telosmith`, with a header comment; otherwise identical).

The purpose stub `P0` has been replaced (`P0@2`, `"epistemic": "provisional"`). It becomes
`"committed"` once Zach decides changes to it need his authorization.

All Telosmith results are structural: they show what changed and what relied on it, not whether the
remaining evidence is good enough. That stays a review question.
