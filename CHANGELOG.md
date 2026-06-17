# Changelog

All notable changes to Agent Wars are recorded here. Format follows
[Keep a Changelog](https://keepachangelog.com/); the project pre-1.0 tracks work by
date rather than semantic version until the first release.

## [Unreleased]

### Shipped — Phase 0 Track A: engine core (branch `phase0/engine-core`)
Built subagent-driven (TDD per task) in `packages/engine/` (Python/uv): schemas, ruleset
resolution, fs+sqlite store with SHA-256 hashing, inline budget enforcer, executor/judge
protocols + fakes (brokered handle, no keys), the objective grader (clean checkout + diff
+ hidden tests, isolated from the agent worktree), injection-safe quoted-evidence judge
prompt, objective scoring with **shadow-mode** judge, the orchestrator (`run_war`), Typer
CLI (`aw validate` / `aw run-war`), example Architect's Duel war package + agents, a
deterministic e2e gate, and live Anthropic adapters (gated smoke). **27 tests + 1 gated
skip, ruff clean.** Fixed a content-hash determinism bug (excluded nondeterministic pytest
timing from the hash). Known minor: live fence-parse uses `lstrip("python")` (B005 footgun)
— harmless in Phase 0's gated live path, switch to `removeprefix` in Phase 1.

### Added
- `CLAUDE.md` — project operating manual: hard rules (incl. spec-derived integrity
  rules), Python engine stack, mandatory dev workflow, directory layout, phasing.
- `CHANGELOG.md`, `plans/README.md` — development scaffolding.
- Technical spec §1.1 **Compute economics & fairness levers** and §2.3 **Task Supply**
  (content pipeline) sections.
- `agent-wars-starter/` — adopted the **"Guild Vault" frontend** (design-system,
  component-library, screens-spec, data-model, api-spec, build-roadmap + a
  `prototype.html` visual oracle) as the UI source of truth.

### Adopted / reconciled (from the Guild Vault starter)
- **Frontend = React + TS + Vite, Guild Vault aesthetic** (mock-first, one `api.ts`
  seam). Replaces the earlier Next.js placeholder.
- **Stack kept Python** for engine + FastAPI (per the earlier deliberate choice);
  declined the starter's Node/Fastify assumption. Stack is therefore **polyglot**.
- **Contract seam locked:** Pydantic (engine) is the source of truth → TS
  `packages/contracts` generated from FastAPI's OpenAPI; engine transcript →
  frontend `ReplayEvent[]`/`Verdict` via an adapter.
- **Phase 0 is now two parallel tracks** (engine + Guild Vault frontend) converging
  at the typed FastAPI seam; the frontend moved into Phase-0 scope.

### Changed
- Reframed intent across both specs: **general public product, friends-first as a
  beachhead** (not the endpoint); stated what the friend phase does/doesn't validate.
- Promoted **task supply** from open-question to a first-order risk + designed
  subsystem. Added **format grading tiers** (ranked leans objective; LLM-judged is
  exhibition until calibrated), **hostile-by-design runner seam**, **sybil/collusion
  seam**, and graceful low-population ladder behavior.
- Show layer: **recap is now the headline**, replay the box score.
- Differentiated Mirror Match vs Architect's Duel; flagged Draft War as a
  synchronous/live-event format.

### Decided
- **Compute: platform-controlled models** (platform owns keys + per-war budgets;
  no BYO-key in fair formats) — preserves the model-frozen + budget-enforcer fairness
  levers. Funding (subscription/credits) is a downstream, fairness-neutral choice.

## 2026-06-16

### Added
- Project scaffolding (`CLAUDE.md`, `CHANGELOG.md`, `plans/`) modelled on the
  FarmerChat Agentic and Nexus conventions.

### Decided
- Engine core language: **Python** (uv + pytest + ruff). Web app (Phase 1) in
  Next.js + TypeScript with a FastAPI backend.

## 2026-06-13

### Added
- Embedded **SVG figures** (11) into both specs, replacing Mermaid code blocks so they
  render in VS Code's built-in Markdown preview. Mermaid sources kept in `figures/`.
- Integrated four reviewed upgrades into the specs: git-worktree sandboxing, SHA-256
  transcript hashing, the Bounty Hunt format (uniqueness-weighted scoring), and
  layer-attribution analytics (gated to Phase 2).

### Changed
- Created GitHub repo `akashub/Agent-Wars` (private); pushed initial specs + figures.

## 2026-06-12

### Added
- Initial design: **concept/creative spec** (vision, vocabulary, the agent character
  sheet, the 12-format War Catalog, seasons, integrity rules) and **technical spec**
  (architecture, Agent + War Package schemas, battle/judge/scoring engines, data
  model, phased roadmap).
