# Build Roadmap — Phase 0

An ordered task list for Claude Code. Work top to bottom; each milestone has acceptance criteria ("Done when…"). Keep `CLAUDE.md` guardrails in force throughout. Tackle one milestone per session where possible.

---

## M0 — Repo scaffold
- Monorepo: `apps/web` (Vite + React + TS), `apps/api` (Fastify + TS), `packages/contracts` (TS types).
- Tooling: TypeScript strict, ESLint/Prettier, a root script to run web + api together.
- **Done when:** `dev` boots an empty React app and a Fastify server with a `/api/health` route; `packages/contracts` is importable from both apps.

## M1 — Design tokens & base styles
- `styles/tokens.css` (`:root` vars from `design-system.md` verbatim), `base.css` (resets, fonts, all keyframes), Tailwind mapped to tokens.
- Fonts loaded; reduced-motion global rule in place.
- **Done when:** a throwaway page shows correct gold/stone colors, the three font families, and a working `.glint` sweep + a `Gem`.

## M2 — Contracts & seed data
- Implement all types from `data-model.md` in `packages/contracts`.
- `seed.ts`: six Schools, Armory items, four WarFormats + WarInstances (lock matrices from `screens-spec.md`), roster Champions, fallback `ReplayEvent[]` (prototype SCRIPT).
- **Done when:** seed imports type-check and contain every value the screens need.

## M3 — Primitives & app shell
- Build `AppShell, AmbientLayer, FiligreeCorner, TopBar, StatusBar` and primitives `Panel, SectionHeader, Button, Gem, Badge, StatBar, Sprite, Portrait` (`component-library.md`).
- Port `lib/sprites.ts` (renderSprite/palFor + HERO/KNIGHT/CORE grids) behind `Sprite`.
- **Done when:** a demo screen renders the shell with corners, ambient motes/twinkles, a TopBar/StatusBar, and one of each primitive matching the prototype.

## M4 — Static scenes (mock data, no API)
Build the six scenes from `screens-spec.md` against `seed`, with scene navigation:
- M4a Boot → Create (schools, name, oath) 
- M4b Guild Hall (char card, roster, menu, actions) — *match the approved look closely*
- M4c Forge (six LayerRows, Armory toggles + budget StatBar, locked Model)
- M4d Arena (WarContractCards + LockSigils)
- M4e Battle (Fighters, holo floor, DialogueBox advancing the seed replay, SparkBursts, Verdict)
- **Done when:** the full flow is clickable end-to-end and visually matches `/reference/prototype.html`; reduced-motion disables fx; keyboard works.

## M5 — API client seam (still mock)
- `lib/api.ts` exposing the `api-spec.md` functions; `USE_MOCK=true` returns seed + a simulated replay stream.
- Scenes call the seam, never `fetch` directly; store (`useGame`) orchestrates.
- **Done when:** scenes get all data through `api.ts`; flipping `USE_MOCK` is the only switch needed later.

## M6 — Backend skeleton + persistence
- Fastify routes for `architects, schools, champions, armory, formats, contracts` (`api-spec.md`), backed by the repo/store layer and seeded data.
- Domain layer: lock-matrix validation utilities; sealing helper (task content never serialized).
- **Done when:** with `USE_MOCK=false`, Boot→Create→Hall→Forge→Arena all run against the real API; `GET /contracts` provably excludes task content.

## M7 — Engine + runner seam
- `Engine` (format-agnostic) + `AgentRunner` interface (`backend-phase0.md`), in-process implementation hostile-by-default.
- `RunRequest`/`ResolvedTask`; budget ceiling; map `AgentConfig` → Anthropic request; stream output → `ReplayEvent`s.
- Stub a sealed task + deterministic/stub judge producing a `Verdict` (keep quoted-evidence shape).
- **Done when:** a script submits a champion, runs it via the Anthropic API against the stub task, and returns a persisted, reproducible replay + verdict.

## M8 — Wire Battle to real runs
- `POST /submissions` (frozen-layer validation) → `POST .../run` → consume `/runs/:id/stream` (SSE) in `Battle.tsx`; fall back to polling `/replay`.
- Handle errored runs + `FROZEN_LAYER_VIOLATION` / `BUDGET_EXCEEDED` / `CONTRACT_CLOSED` in the UI.
- **Done when:** "Raid" on a contract runs a real agent and the Battle animates from live `ReplayEvent`s, ending on a real `Verdict`.

## M9 — Polish & hardening pass
- Verify integrity guardrails (sealing, server-authoritative frozen layers, reproducibility) with tests.
- Accessibility/focus/reduced-motion audit; empty/error/loading states on every screen.
- Confirm the `Sprite` swap path and `USE_MOCK` both still work.
- **Done when:** the Phase 0 "definition of done" in `CLAUDE.md` is met and guardrails are covered by tests.

---

### Working notes for Claude Code
- Build components before screens; screens only compose.
- Keep the prototype open as the visual oracle; diff against it.
- Don't implement out-of-scope systems (ladder/seasons/sandbox/billing) — stub or display only.
- Reference the right doc per milestone: M1/M3→`design-system`+`component-library`, M4→`screens-spec`, M2/M5→`data-model`+`api-spec`, M6–M8→`backend-phase0`+`api-spec`, naming→`glossary`.
