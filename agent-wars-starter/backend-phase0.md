# Backend — Phase 0

**Stack:** Node + TypeScript, Fastify. Agent runs execute via the Anthropic API. Shared types from `packages/contracts`. The goal of Phase 0 is the smallest backend that makes the frontend real *and* establishes the durable seams so later phases don't require a rewrite.

> The technical spec is the authority on the engine design, the two durable contracts, and the integrity model. This doc is the Phase 0 implementation shape that conforms to it.

---

## Layered architecture

```
HTTP (Fastify routes)         ← api-spec.md endpoints
   │
Application services          ← architect / champion / contract / run services
   │
Domain (contracts + rules)    ← packages/contracts; lock-matrix validation; sealing
   │
Engine                        ← orchestrates a run; format-agnostic core
   │
Runner  ◀── HOSTILE SEAM ──▶  ← actually executes the agent (Anthropic API + tools)
   │
Store                         ← persistence (Phase 0: SQLite/Postgres via a repo layer)
```

Keep the **Engine** standalone and UI-agnostic (it should be runnable from a script/test with no HTTP). Routes are thin; rules live in the domain layer.

---

## The orchestrator ↔ runner seam (build this hostile-by-default)

This is the single most important Phase 0 architectural decision. The **Runner** is the thing that takes an `AgentConfig` + a resolved task and actually drives the model and any tools. Treat its inputs as **untrusted** even though Phase 0 has no real sandbox.

- Define the seam as an interface, e.g. `interface AgentRunner { run(req: RunRequest): AsyncIterable<ReplayEvent> }`.
- The orchestrator passes only what the runner needs; the runner returns only `ReplayEvent`s + a result — never arbitrary host access.
- Phase 0 implementation: an in-process runner is fine, but written so it could be swapped for an out-of-process / sandboxed runner (container → microVM later) by changing only the seam implementation, not the engine.
- No task secrets, keys, or host paths cross the seam beyond the explicit `RunRequest`.

```ts
interface RunRequest {
  config: AgentConfig;          // the champion (validated against frozen layers already)
  task: ResolvedTask;           // resolved server-side from taskRef; never client-sourced
  budget: { max: number };
  seed?: number;
}
```

---

## Run lifecycle

1. `POST /submissions` → validate frozen layers against the format's lock matrix; snapshot config; persist `Submission`.
2. `POST /submissions/:id/run` → create `Run` (queued); resolve `taskRef` → `ResolvedTask` **server-side**; record the actual model+version + seed.
3. Engine drives the Runner; the Runner streams `ReplayEvent`s (narration, tool_call, subagent_spawn, retry, budget, submit).
4. Budget enforced during the run; on exhaustion the runner must stop and emit a final state (mirrors the "BUDGET OUT" beat).
5. Judging: auto-checks (objective) and/or an LLM judge that scores **from quoted evidence** in the transcript. Phase 0 may stub judging with a deterministic scorer, but keep the `JudgingSpec` shape and the quoted-evidence contract.
6. Produce a `Verdict`; persist `Run` + events + verdict for replay/contest.

---

## Integrity enforcement (must hold in Phase 0)

- **Sealing:** task content is resolved only inside the engine/runner; never serialized to any client response or client-readable log.
- **Frozen-model fairness:** the server is the authority. Any frozen layer must equal the format's shared value or the submission is rejected (`FROZEN_LAYER_VIOLATION`). Never trust the client's copy.
- **Reproducibility:** persist `configSnapshot`, resolved model+version, seed, task ref, and the full event stream so a run can be re-executed and contested.
- **Quoted-evidence judging:** judge prompts/scoring reference spans from the transcript, not free opinion.
- **Author-can't-compete / appeals / etc.:** out of Phase 0 scope, but don't design anything that blocks adding them.

---

## Persistence (Phase 0)

A simple repository layer over SQLite (local) or Postgres. Tables map to the contracts: `architects`, `champions`, `war_formats`, `war_instances`, `submissions`, `runs`, `replay_events`, `verdicts`, plus a server-only `tasks` table (sealed; never exposed). Keep the repo interface clean so the store backend can change.

---

## Anthropic API runner notes

- Keys via env only (`ANTHROPIC_API_KEY`); never in the repo or client.
- The runner maps `AgentConfig` → an Anthropic request: `persona`→system prompt, `tools`→tool definitions, `memory`→injected context/few-shots, `strategy`→the orchestration loop (plan/critique/verify/retry), `subAgents`→nested runner calls, `model`→model id.
- Stream model output and translate into `ReplayEvent`s as they arrive so the Battle screen can animate live.
- Enforce the budget as a hard ceiling on tokens/tool calls/sub-runs; stop and finalize when hit.

---

## Explicitly out of scope (Phase 0)

Hardened multi-tenant isolation (build only the seam), real sealed-task authoring pipeline, Glicko/seasons/medals as live systems, billing/accounts, appeals, casting, attribution analytics, sybil/abuse defenses. Leave seams, not implementations.

## Backend definition of done (Phase 0)

From a script or the frontend: create an architect, store a champion, list contracts (no task leakage), submit (frozen-layer validation working), run one champion against a stubbed sealed task via the Anthropic API, stream a replay, and return a verdict — all persisted and reproducible.
