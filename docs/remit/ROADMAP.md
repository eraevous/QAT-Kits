# Roadmap under the 2026-11-16 remit (proposed)

Author: claude:qat#01GZK2Knb8aP6VTtZ7bf5tRv · Reviewer: none yet · model=claude-opus-5-5 · Handoff: HO-QAT-20261116-Y0HJ

The earlier tool roadmap (relay-kit-private, `handoffs/outputs/HO-QAT-20261105-7RNR.md`, 2026-11-07) ranked tools for a kit limited to "chat- and thread-based cognitive tools". That limit is replaced. Its per-tool evidence still stands; its scope line doesn't.

## Now (this PR)

- README states the remit; provisional purpose record `P0@3`; CONTRIBUTING's scope line updated.
- [INVENTORY.md](INVENTORY.md): AutoEDA, MTG Deck Lab and other candidates; ChatGPT port findings recorded.
- [TOOL_CONTRACT.proposal.md](TOOL_CONTRACT.proposal.md): one source, per-runtime adapters, observed-install records.

## Next (each its own PR, eval-gated where it touches a spec)

1. Runner: `eval` exits non-success ("incomplete", proposed `3`) when any case is SKIP; regression test; lossy-coercion warnings stay visible.
2. ThreadSeed: upstream the two `verify()` fixes with three regression cases (nonexistent T2 in a T1/T3 capture; wrong quote; T1a text cited as T1a2).
3. MTG Deck Lab: relabel the §2.7 `sim()` skeleton as a non-executable design reference, unless Zach prefers pointing at a tested implementation.
4. AutoEDA: move Claude-only delivery into a runtime section; restrict `plugins/` to reviewed code; add a Parquet case once an engine is available.
5. Contract steps 3-5 (generator support for `.tool.md`, ChatGPT and paste emitters, tool-by-tool conversion), after Zach's call on the contract.

## Later

- Additional runtimes (Codex, Gemini Gems, MCP prompts) as they turn up.
- Candidates from INVENTORY §3 (chat-telemetry first), only if Zach chooses QAT-Kits as their home.
- `qat/installs/` records filled from observed tests (Abigail's install verification is the first source).
