# Agent Wars

A competitive sport where you don't fight — you *build a fighter*. Architects design AI **Agents** (persona, tools, memory, strategy, sub-agents) that battle in configurable **Wars**, judged by a referee, scored, and ranked across seasons. Design source of truth: `docs/superpowers/specs/` (concept + technical spec).

## Hard rules
- Every file <= 200 LOC. Refactor, never bypass.
- pytest for everything. Warnings are errors. No skipped tests without a linked issue.
- No secrets in code. Load from env.
- Prefer editing existing files over creating new ones.
- No emoji in code or dev docs unless the user asks. (Creative flavor lives only in `docs/superpowers/specs/`.)
- **The two schemas are durable contracts.** Agent definition + War Package (technical spec §2) are validated on load; changes are versioned, never silently broken.
- **Reproducibility.** Every run logs a full transcript + a SHA-256 `content_hash`. No scoring path that isn't recomputable from stored inputs.
- **Judge isolation.** Agent output reaches the LLM judge only as *quoted evidence* — never concatenated into judge instructions. Rubric + scale stay outside the agent-controllable region.
- **Sealed tasks.** Never commit task answers/solutions (or fixtures an agent could read) into the repo. Tasks are revealed at run time only.
- **No leakage to the judge/engine.** Cosmetics are stripped before an agent is resolved; they never reach engine or referee.
- **Author-can't-compete.** A War Package's author may not enter it. Enforce in code, not policy.
- **Inline budgets.** Every model/tool call decrements token/tool-call/time budgets; halt gracefully on exhaustion.

## Stack
- **Monorepo**: uv workspace. `packages/` (Python engine), `apps/` (Phase 1 web), `infra/`, `war-packages/`, `plans/`, `docs/`.
- **Engine core (Phase 0)**: Python 3.12+. uv, pytest, ruff. CLI via Typer (Phase 0 is CLI-triggered, no UI).
- **Agent runtime**: provider-neutral battle runner — composes the resolved agent, runs the loop, enforces budgets, and drives whatever model the layer specifies through the generic `ModelHandle` seam (no provider hardcoded in the executor/judge).
- **LLM — provider & model agnostic (core requirement)**: any model of any provider, via **litellm**. The Model layer value is a litellm model string (`gpt-4o`, `claude-3-5-sonnet`, `gemini/...`); the provider is inferred from the string and the API key is read from that provider's env var (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, ...). All routing lives in litellm behind `live/llm_provider.py` (`LiteLLMModelHandle` + `model_handle_for`). Each competitor runs on its own model; the judge runs on `WarPackage.referee.judge_model`, independent of competitors **by default** — caveat: when a format *frees* the Model layer, a competitor could choose the judge's model, so the judge stays in **shadow mode** (never affects rank) in Phase 0.
- **Code-task sandbox**: git worktree off a baseline branch; correctness = apply diff + run tests (technical spec §6). Worktree isolates state, inside a container later.
- **Storage (Phase 0)**: local filesystem for transcripts/artifacts + SQLite for run/score records. Schema designed to port to **PostgreSQL + object store** in Phase 1.
- **Frontend (Phase 0, Track B)**: **React + TypeScript + Vite**, "Guild Vault" design system. Adopted wholesale from `agent-wars-starter/` (the approved UI). Mock-first: every screen runs on seed data behind one `lib/api.ts` seam before the API exists. CSS-custom-property tokens + Tailwind mapped to them; Zustand for client state. **Not Next.js** — the loved prototype is Vite/SPA.
- **API + workers (Phase 1)**: **FastAPI** (Python, async) wrapping the engine + Python workers (queue: Redis + arq/RQ). Polyglot-by-choice: Python engine/API + TS web (see contract seam below). BYO-Node is the alternative we declined (engine plan + your stack are Python).
- **Contract seam (source-of-truth = Python)**: Pydantic models in `packages/engine` are the authority; the frontend's `packages/contracts` TS types are **generated from FastAPI's OpenAPI** so they can't drift. The engine's run transcript maps to the frontend's typed `ReplayEvent[]` + `Verdict` via a dedicated adapter — lock this contract before either track wires to the other.
- **Deployment (Phase 1+)**: Railway, Docker only. Migrations run during deploy, never in app startup. Phase 0 stays local.
- **Memory**: Eagle Mem for session + long-term state. **Docs**: design specs in `docs/superpowers/specs/`; decisions + outcomes captured in Eagle Mem and `CHANGELOG.md`.
- **Phase planning**: Superpowers skill (brainstorming -> writing-plans). One plan per session, in `plans/`.

## Core vocabulary
**Balance:** engineering terms for what you build/tune (the six layers — Persona, Tools, Memory, Strategy, Sub-agents, Model — and all judging/scoring/budget concepts); light RPG flavor for the world (Guild Hall, the Forge, the Arena, Wars, Raids, Treasury, Seasons). Never hide a concept behind a fantasy word; flavor is for places/actions only. Canonical entity is the **Agent** (not "Champion"). **Authoritative naming: `agent-wars-starter/glossary.md`.**

Architect (player) · Agent (the competitor; 6 layers above) · War (a match) · War Package (task + ruleset + referee + scoring) · Ruleset / Lock Matrix (which layers are frozen/free) · Referee (auto-checks + LLM judge + optional HITL) · Ladder · Season -> Finals.

## Development workflow (mandatory)
Every change follows this pipeline. No shortcuts.

1. **Requirement** — understand the ask, clarify ambiguities.
2. **Plan** — create `plans/<YYYY-MM-DD>-<HHMM>-<slug>.md` with Objective, Acceptance criteria, Steps. One plan per session.
3. **Tasks + Acceptance criteria + Test cases** — break the plan into discrete tasks, each with measurable criteria and test cases.
4. **Implement** — follow the plan; keep files <= 200 LOC.
5. **Run tests** — all green: no linter, type, or build errors, no warnings (`uv run pytest -q`).
6. **Run anti-slop** — `/eagle-anti-slop` on changed files.
7. **Run spectral agents** — clear all severities (critical, high, medium, low, nits).
8. **Lint** — `uv run ruff check` (and `pnpm lint` / `vitest` for Phase 1 web). Zero warnings.
9. **Commit** — Conventional Commits (`feat()`, `fix()`, `docs()`, `test()`, `refactor()`), bisectable, end the message with `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
10. **Push** — to `akashub/Agent-Wars` via the `github-personal` SSH remote (`git@github-personal:akashub/Agent-Wars.git`). NOT plain `github.com` (that is the work account). Commit identity is akashub's GitHub noreply.
11. **Post-push** — update Eagle Mem memories, `CHANGELOG.md`, and the task list. Move to the next task.

## Directory layout
```
docs/superpowers/specs/  Design specs (concept + technical) + figures    [exists]
plans/                   Session plans <YYYY-MM-DD>-<HHMM>-<slug>.md      [exists]
agent-wars-starter/      Guild Vault UI source-of-truth (design-system,
                         component-library, screens-spec, data-model, ...)
                         + reference/prototype.html (visual oracle)       [exists]
packages/
  engine/                Python engine (agentwars pkg) — Track A          [Phase 0]
    models.py            Agent + War Package Pydantic schemas (contract source of truth)
    resolve.py budget.py store.py autocheck.py protocols.py
    judge_prompt.py scoring.py orchestrator.py cli.py
    adapters/            transcript -> ReplayEvent[]; AgentConfig <-> AgentDef
    live/                Claude Agent SDK executor + judge (brokered key)
  contracts/             TS types for the web, GENERATED from OpenAPI       [Phase 0/1]
apps/
  web/                   React + TS + Vite (Guild Vault) — Track B         [Phase 0]
  api/                   FastAPI thin layer over the engine (api-spec.md)   [Phase 1]
war-packages/            Authored packages (task + ruleset + referee + scoring) [Phase 0]
agents/                  Example agent definitions                          [Phase 0]
infra/                   Docker, CI, Railway deploy                          [Phase 1]
```

## Plan convention
`plans/<YYYY-MM-DD>-<HHMM>-<objective-slug>.md`. Each plan begins with **Objective**, **Acceptance criteria**, **Steps/Tasks** (each task carries test cases). Progress + outcomes captured in Eagle Mem and `CHANGELOG.md`. See `plans/README.md`.

## Phasing
Phase 0 runs as **two parallel tracks that converge at the typed contract:**
- **Track A — Engine core (Python)**: schemas, resolve, budget, store/hashing, worktree grader, shadow judge, scoring, orchestrator, CLI. A full war runs end-to-end with reproducible scores. First war: a code-gen task in an Architect's Duel ruleset. Plan: `plans/2026-06-16-1119-phase-0-engine-core.md`.
- **Track B — Guild Vault frontend (React/Vite)**: the six screens (Boot → Create → Hall → Forge → Arena → Battle) built **mock-first** on seed data, matching `agent-wars-starter/reference/prototype.html`. Plan: forthcoming.
- **Convergence**: a thin **FastAPI** layer (`apps/api`, matching `agent-wars-starter/api-spec.md`) + the `transcript → ReplayEvent[]` adapter; flip the frontend's `USE_MOCK` to live; Battle renders real runs.

Later: **Phase 1** — Postgres + object store, queue, real ladder/season, deploy on Railway. **Phase 2** — more formats (Swarm, Gauntlet, Boss Raid, Bounty Hunt), casting/recaps, Glicko, attribution analytics. **Phase 3** — microVM isolation, community authoring, abuse limits, sign-up.

## Out of scope (Phase 0)
Auth/multi-user, Postgres/object store, real queue, hardened sandboxing (build only the hostile *seam*), community War Package authoring, billing, real ladder/seasons/medals (display as mock/seed). Phase 0 = one trusted operator; the engine runs from the CLI and the frontend runs mock-first, meeting at the FastAPI seam.
