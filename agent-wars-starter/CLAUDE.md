# Agent Wars — Project Brief (read me first)

This is the root context for building **Agent Wars**. Read this file fully before writing any code, then consult the other docs in the order given under "Reading order."

---

## What Agent Wars is

A competitive platform where people don't fight directly — they **build an AI agent ("Champion") and send it into the Arena** to compete against other people's agents on sealed tasks. Everyone has access to the same underlying models, so the skill is entirely in *how you build and direct the agent*.

The product is wrapped in a light RPG metaphor: the player is an **Architect** who forges **Champions**. Each Champion is a **six-layer character sheet**:

| Layer | RPG name | What it is |
|---|---|---|
| Persona | the Soul | system prompt / role |
| Tools | the Armory | which tools the agent may use |
| Memory | the Grimoire | knowledge packs, few-shots |
| Strategy | War Tactics | plan/critique/verify/retry loop |
| Sub-agents | the Party | specialist sub-agents |
| Model | the Vessel | the model (usually frozen for fairness) |

**The configurability principle:** every layer can be independently *frozen* (locked to a shared value) or *free*. A "war format" is just a named pattern of which layers are frozen vs free. This one rule generates the entire format catalog and is the heart of the game — keep it central in the data model and UI.

Matches are **watchable**: the agent narrates its reasoning as it runs, which we render as a turn-by-turn battle. See `screens-spec.md` → Battle.

> The full product rationale lives in the two source docs you already have: **`2026-06-12-agent-wars-concept.md`** (concept) and **`2026-06-12-agent-wars-technical-spec.md`** (technical spec). Those are the authority for *why*; the docs in this folder are the authority for *what to build now*. If they ever conflict, the technical spec wins on architecture/integrity and these docs win on this specific build/UI.

---

## Visual identity: "Guild Vault"

The approved look is a dark thieves'-guild treasure vault: amethyst-and-teal stone lit by **metallic gold** ornament, faceted **gems** as accents, and martial energy (sword glints, sparkle, spark bursts in battle). The pixel-exact source of truth is the prototype committed at **`/reference/prototype.html`** (the file `agent-wars-guild-vault.html`). When in doubt about a visual detail, open that file — the docs extract from it, but it is the ground truth.

All tokens, components, and screens are specified in `design-system.md`, `component-library.md`, and `screens-spec.md`.

---

## Stack (decided)

- **Frontend:** React + TypeScript + Vite. Styling via CSS custom properties (the design tokens) with Tailwind mapped to those tokens. No CSS-in-JS.
- **Backend:** Node + TypeScript, Fastify. Agent runs execute through the Anthropic API.
- **Monorepo:** `apps/web` (frontend), `apps/api` (backend), `packages/contracts` (shared TS types from `data-model.md`).
- **State:** lightweight store (Zustand) for client state; server is source of truth for domain data.

Rationale and structure: `frontend-architecture.md`, `backend-phase0.md`.

---

## Non-negotiable guardrails

These come from the technical spec and must hold from day one, even in Phase 0:

1. **Sealed tasks.** Task content is never sent to the client and never logged in a recoverable place before run time. The frontend never receives the answer key.
2. **Frozen-model fairness.** When a layer (especially Model) is frozen by a format, the backend enforces it — the client cannot override a frozen layer. Validation is server-side and authoritative.
3. **Hostile-by-default runner seam.** The boundary between the orchestrator and the code that actually runs an agent is designed as if the agent config is untrusted. Phase 0 doesn't need full sandboxing, but the *seam* must assume hostility so isolation can be hardened later without a rewrite. See `backend-phase0.md`.
4. **Reproducibility.** Every run records enough (config snapshot, seeds, model + version, inputs) to be replayed and contested.
5. **Quoted-evidence judging.** Any LLM-judge step scores from quoted evidence in the transcript, never free-floating opinion. (Phase 0 judging can be stubbed, but keep the shape.)
6. **No secrets in the repo.** API keys via env only. Never commit keys, never hardcode them in client code.

If a task would violate one of these, stop and flag it rather than working around it.

---

## Phase 0 scope

**In scope (build this):**
- The full frontend flow in Guild Vault style: Boot → Create → Guild Hall → Forge → War Contracts → Battle, navigable, matching the prototype.
- Shared TS contracts (`packages/contracts`) per `data-model.md`.
- A backend that can: register an Architect, store Champions (six-layer configs), list war formats/contracts, accept a submission, run a single agent against a (stubbed) sealed task via the Anthropic API, and return a replay + verdict.
- The orchestrator↔runner seam, built hostile-by-default.
- Mock-first: every screen works against mock data before the API exists, then swaps to the real API behind one client module.

**Explicitly out of scope for Phase 0 (do NOT build yet):**
- Hardened multi-tenant sandboxing (microVMs). Build the *seam*, not the isolation.
- Glicko ladder, seasons, medals as real systems (display them as static/mock).
- Billing / payments / accounts beyond a single local Architect.
- Real sealed-task authoring pipeline, appeals, casting, attribution analytics.
- Real pixel-art assets (use the placeholder sprite system; see `assets-spec.md`).

---

## Reading order for the rest of the docs

1. `glossary.md` — vocabulary; keep code and copy consistent with it.
2. `design-system.md` — tokens + effects (source of truth for the look).
3. `component-library.md` — reusable components built from those tokens.
4. `screens-spec.md` — assemble components into the six screens.
5. `data-model.md` — shared TS types.
6. `api-spec.md` — endpoints the screens call.
7. `frontend-architecture.md` — how the web app is structured.
8. `backend-phase0.md` — how the API + runner are structured.
9. `assets-spec.md` — sprite/asset slots for later real art.
10. `build-roadmap.md` — the ordered task list; use it as your running checklist.

---

## Conventions

- **Vocabulary:** use the RPG names in user-facing copy, technical names in code identifiers (see `glossary.md`). E.g. UI says "Armory," the type is `tools`.
- **Tokens, not literals:** never hardcode a hex or px that exists as a token. Reference the CSS var / Tailwind token.
- **Components, not copies:** if a visual pattern appears twice, it's a component in `component-library.md`.
- **Mock-first, one seam:** all server access goes through a single `api/` client module so mock ↔ real is a one-line swap.
- **Accessibility:** keyboard-navigable menus, focus states, `prefers-reduced-motion` disables the ambient/glint/spark animations (the prototype already does this).

## Definition of done (Phase 0)

A user can boot the app, create an Architect, see the Guild Hall, open the Forge and edit a Champion's six layers within a loadout budget, open War Contracts, deploy into a war, watch a narrated battle render from real run data, and see a verdict — all in the Guild Vault aesthetic, with the backend enforcing frozen layers and sealing the task.
