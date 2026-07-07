# Engine Status — Phase 0 (end-to-end assessment)

> **Date:** 2026-07-07 · **Branch:** `main` · **Suite:** 30 passed, 1 skipped (live smoke, gated) · ruff clean.
> Verified by running real wars via the CLI, including live OpenAI runs.

## Verdict in one line

**End-to-end as a *pipeline*: yes. End-to-end as an *agent-runner*: not yet.** The full
scoring pipeline works and is verified against real models; but the executor only
exercises 2 of the 6 agent layers, so the product thesis ("same model — the better
*build* wins") isn't demonstrable yet. That's the next engine build, not a bug.

## What is real and verified

| Capability | Status | Evidence |
|---|---|---|
| Provider/model agnostic (litellm) | ✅ | Live runs on OpenAI `gpt-4o` + `gpt-4o-mini`; any provider by model string |
| Per-competitor models + independent judge | ✅ | Open War ran `gpt-4o` vs `gpt-4o-mini`, judge on `gpt-4o-mini` |
| Ruleset resolution (freeze/free layers, strip cosmetics) | ✅ | `resolve.py` + tests |
| Sealed hidden-test grading (clean checkout; agent never sees tests) | ✅ | `autocheck.py`; grader-isolation test |
| Graduated scoring with partial credit | ✅ | Text-justify: **11/11 vs 7/11** — real spread |
| Shadow judge (recorded, never ranks) | ✅ | Agreement dropped to **0.75** on a subtle task — proves *why* it stays shadow |
| Reproducible / contestable content hashes | ✅ | SHA-256, recompute-from-store test |
| Budget enforcement + grader timeout + budget-derived output cap | ✅ | `budget.py`, `autocheck.py` timeout, executor cap fix |
| fs + SQLite store; one-command CLI (`aw run-war`) | ✅ | Runs a full war end-to-end |

## The gap (why it's not yet the full product)

**The live executor (`single_turn_executor.py`) is one model turn.** It uses only
`persona` + `model`. The other four layers — **`strategy`, `tools`, `memory`,
`sub_agents`** — are parsed and resolved but never affect the run. So today the engine
measures *"which model + which prompt wins,"* not *"which build wins."* Live results are
**capability** separation (which model), not **build** separation (how you engineered
the agent). This was a documented Phase-0 simplification, now the gating limitation.

## What the live runs actually showed

| Task | Difficulty | Result | Read |
|---|---|---|---|
| Roman numerals | easy | 100 vs 100 | too easy; token tiebreak |
| LRU cache | medium | 100 vs 100 | too easy for these models |
| Regex matching (#10) | hard | 100 vs 100 | famous problem, both know it |
| **Text justification (#68)** | hard | **gpt-4o-mini 100 · gpt-4o 63.6** | **spread + upset + judge disagreed 25%** |

Takeaway: hard *and unusual* (fiddly, edge-case-heavy) tasks separate models; well-known
algorithm problems don't. This is the **task-supply problem** (technical spec §2.3),
confirmed empirically — a real content-engineering effort, not "write a leetcode."

## Recommended next engine work (to make the build matter)

In leverage order:
1. **Strategy-loop executor** — plan → write → run tests → read failures → self-critique
   → retry, within budget. Makes `strategy` real. *Biggest lever; this is what lets a
   better-built agent beat a raw one on the same model.*
2. **Tool use** in the executor — makes `tools` real.
3. **Sub-agent orchestration** — makes `sub_agents` real (the Swarm War thesis).
4. **Memory injection** (knowledge packs / few-shots into context) — makes `memory` real.
5. Minor hygiene: executor should write to a tempdir (not next to the baseline);
   `parse_pytest_summary` should count `errored` tests; per-test (not just per-run) timeout.

## Also still ahead (known, from the plan — not engine)

Track B (Guild Vault frontend, mock-first), then convergence: FastAPI layer
(`api-spec.md`) + OpenAPI→TS `packages/contracts` + the `transcript → ReplayEvent[]`
adapter, then flip `VITE_USE_MOCK=false`.
