# Agent-Loop Executor — Design (grounded in current practice)

> **Date:** 2026-07-08 · **Status:** design → build. Replaces the Phase-0 `SingleTurnExecutor`
> (one model turn, only `persona`+`model`) with a configurable agent loop where the
> competitor's six-layer build actually drives execution.

## Why this is the build that matters (the research)

Current (2026) agentic-coding research converges on a few load-bearing points, and they
line up exactly with the Agent Wars thesis:

- **Loop structure is the binding constraint, not model size.** Harness-engineering work
  reports local models going from 2/10 → 10/10 on a SWE-bench subset purely by fixing the
  loop/tool space; harness ablations localize gains to **tools, middleware, and long-term
  memory — not the system prompt.** *(This is the empirical case for "same model, the
  better build wins" — and it also says our persona-only executor exercises the least
  impactful layer.)*
- **Self-repair is the converged paradigm.** Generate → run tests → feed the failing
  output/traceback back → regenerate. Reported gains of **+5 to +30 pp** pass rate
  (HumanEval/MBPP). Lineage: Self-Refine, Reflexion (verbal reinforcement across
  attempts), and the "iterative generate–validate–repair" loop every modern coding agent
  (Aider, SWE-agent, OpenHands) now uses.
- **Orchestrator–worker is the converged multi-agent pattern.** A lead agent decomposes a
  task and dispatches specialist workers (researcher/coder/tester/reviewer), then merges —
  Anthropic's *Building Effective Agents* "orchestrator-workers," ~70% of production
  multi-agent deployments in 2026.

Sources: see the "References" section.

## The core idea: the executor is a *configurable harness*, the build is its config

Agent Wars is a harness that runs someone else's agent. So the competitor's six-layer
build **is a harness spec**, and the executor interprets it into a real loop:

| Layer | Becomes, in the loop |
|---|---|
| `persona` | system prompt |
| `model` | the brain (via the provider-agnostic factory) |
| **`strategy`** | **the loop shape**: `plan_first`, `verify_before_final`, `max_retries` (self-repair) |
| `tools` | capabilities offered to the model and executed each turn |
| `memory` | knowledge/few-shots injected into context |
| `sub_agents` | orchestrator-worker: spawn + coordinate specialists |

## Integrity landmine (and how we defuse it): sealing MUST hold

A self-repair loop feeds test results back to the agent. **The agent must never see the
SEALED grader** — that is the anti-overfitting guarantee. We mirror the industry
public-vs-hidden split (SWE-bench `PASS_TO_PASS`/`FAIL_TO_PASS` are hidden from the agent):

- **The agent's loop uses PUBLIC signals only:** it executes its own code and, if the task
  author bundles them, runs **public example tests** in `baseline/` (visible, and *distinct*
  from the hidden grader). It sees stdout / exceptions / public-test failures.
- **The referee runs the HIDDEN grader exactly once, at the end,** for the score
  (unchanged). The hidden grader is never in the agent's workspace (already enforced).
- Task authors write both: a small public smoke set (teaches the loop) + the sealed grader
  (scores). No overlap required; the public set can be a subset or entirely different.

This keeps the sealed-task guarantee intact *and* gives the strategy loop a real feedback
signal — the same separation real benchmarks use.

## Staged build (leverage order — this session ships #1)

1. **Strategy self-repair loop** ← *this increment.* plan? → generate → apply → public
   check → if failing and retries remain: reflect on the errors → regenerate → … → final.
   Budget-bounded (each model call charges tokens; the loop halts on exhaustion).
2. **Tool use** — a function-calling loop; `tools` offered + executed.
3. **Sub-agents** — orchestrator-worker via the model factory (spawn specialists, merge).
4. **Memory** — inject knowledge packs / few-shots into context.

The `Executor` protocol signature is unchanged, so each stage is a drop-in; the CLI's
`--live` path picks the loop executor.

## This increment — concrete shape

- New `live/agent_loop_executor.py` → `AgentLoopExecutor` implementing `Executor.run(...)`.
  Keep `SingleTurnExecutor` as the trivial baseline (useful as a "no-strategy" control).
- Reads `resolved.strategy`: `plan_first: bool`, `verify_before_final: bool`,
  `max_retries: int` (default 0 → behaves like one-shot).
- **Feedback source** = a public check helper: run the candidate `solution.py` plus any
  `baseline/public_test.py`, capture pass/fail + truncated errors. Never touches `grader/`.
- Loop (budget-bounded, `max_retries` cap):
  1. if `plan_first`: one planning turn (short plan, charged to budget).
  2. generate full `solution.py`.
  3. if `verify_before_final` and retries remain: run public check; if failing, feed the
     errors back and regenerate (reflect step); repeat until pass, retries exhausted, or
     budget hit.
  4. return the final diff + a transcript of the turns (so the Battle replay is real).
- **Tests (mocked model, no network):** a scripted model that returns a broken solution
  first then a correct one → assert a `max_retries>=1, verify=True` build converges while a
  `max_retries=0` build does not; assert budget exhaustion halts gracefully; assert the
  public check never reads `grader/`.
- **Demo task** with a `public_test.py` + a distinct hidden grader.
- **Live proof:** same model, a plan+verify+retry build vs a one-shot build → the former
  wins. *This is build separation, not capability separation* — the thing that was missing.

## References

- Harness engineering / loop-is-the-constraint: arxiv.org/abs/2604.25850, arxiv.org/pdf/2604.03515, github.com/ai-boost/awesome-harness-engineering
- Self-repair / reflexion / iterative repair: arxiv.org/html/2604.10508, emergentmind.com/topics/self-debugging-agent, arxiv.org/html/2510.18327v1
- Orchestrator-workers / multi-agent: anthropic.com/engineering/multi-agent-research-system, resources.anthropic.com/building-effective-ai-agents
