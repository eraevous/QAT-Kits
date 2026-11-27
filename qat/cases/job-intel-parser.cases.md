# JobIntelParser standalone acceptance cases (v0.1.0)

Use the six case IDs and fictional `input` mappings in [job-intel-parser.eval.yaml](job-intel-parser.eval.yaml). Run each against only the standalone skill and that input; expand the ordinary case's `file:` value from the fixture. Do not expose the expected outputs or judge criteria to the producing model. Required and forbidden behaviors are the corresponding `must_include` and `must_avoid` checks. Each case uses the same output contract across the skill, paste block and runner.

- `ordinary`: alternatives, negation, preferences, screener ambiguity, no candidate intake required.
- `conflicting-terms`: preserve source conflicts and unknown pay units.
- `prestige-and-gaps`: evidence gap and independent fit, despite a prestigious title.
- `embedded-instructions`: ignore injection; do not invent credentials or act externally.
- `thin-input`: abstain from employer/title inference; ask for text.
- `vague-and-partial`: conditional interpretation; omissions are scoped to the excerpt.

The committed example outputs are authored fixtures, not cold model runs. A semantic evaluation must produce fresh outputs and grade all judge criteria; regex matches alone are insufficient.
