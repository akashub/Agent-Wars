# Engine Status — Phase 0 (end-to-end assessment)

> **Date:** 2026-07-10 · **Branch:** `main` · **Suite:** 39 passed, 1 skipped (live smoke, gated) · ruff clean.
> Verified by running real wars via the CLI, live OpenAI runs, and a deterministic
> end-to-end build-separation proof.

## Verdict in one line

**End-to-end as a *pipeline*: yes. As an *agent-runner*: now partially — the `strategy`
layer is real.** A self-repair agent loop (`AgentLoopExecutor`) makes `strategy`
(plan/verify/retry) materially change the outcome: a plan+verify+retry build beats a
one-shot build **on the same model** (proven — see below). `tools`, `sub_agents`, and
`memory` are still inert (the remaining executor work).

## Update 2026-07-10 — strategy layer is now real

- **`AgentLoopExecutor`** (grounded in the 2026 self-repair / harness-engineering
  paradigm — see `docs/superpowers/specs/2026-07-08-agent-loop-executor-design.md`):
  plan → generate → run **public** check → reflect on failures → retry ≤ `max_retries`
  → final. Budget-bounded; returns best-so-far on exhaustion. `strategy={}` ⇒ one-shot.
- **Sealing preserved:** the loop's feedback is a **public** signal only (visible
  `baseline/public_test.py` or a smoke import); the referee still scores on the **hidden**
  grader exactly once. Public tests are illustrative basics; hidden keeps the edge cases.
- **Build-separation proof** (real pipeline, model simulated deterministically), on the
  `wp_median_lower` gotcha task: **careful (plan+verify+retry) 100/100 vs one-shot 40/100**
  — same model, only the build differs. Transcript: plan → generate(buggy) → public 1/3 →
  generate(fixed) → public 3/3 → 100 on the hidden grader.
- **Two real bugs found + fixed end-to-end:** stale `__pycache__` serving old code to the
  check subprocess; and the executor's work dir living inside the package tree, which made
  the public-check pytest inherit the engine's `pyproject.toml` and collect 0 tests. Both
  fixed (isolated tempdir + cache clear), with regression tests.
- **Still capability-not-build** for the earlier live OpenAI runs (those used the
  one-turn executor). Re-running them live through the loop needs a fresh provider key.

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

## Recommended next engine work (to make the rest of the build matter)

In leverage order:
1. ~~Strategy-loop executor~~ — **DONE** (2026-07-10). `strategy` is now real.
2. **Tool use** in the loop — a function-calling step; makes `tools` real. *(next)*
3. **Sub-agent orchestration** — orchestrator-worker via the model factory; makes
   `sub_agents` real (the Swarm War thesis).
4. **Memory injection** (knowledge packs / few-shots into context) — makes `memory` real.
5. Minor hygiene: ~~executor tempdir~~ **DONE**; `parse_pytest_summary` should count
   `errored` tests (an errored test currently drops out of the denominator); per-test
   (not just per-run) timeout.

## Also still ahead (known, from the plan — not engine)

Track B (Guild Vault frontend, mock-first), then convergence: FastAPI layer
(`api-spec.md`) + OpenAPI→TS `packages/contracts` + the `transcript → ReplayEvent[]`
adapter, then flip `VITE_USE_MOCK=false`.
