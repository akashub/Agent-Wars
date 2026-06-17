# API Spec (Phase 0)

REST over JSON, served by `apps/api` (Fastify). Types reference `data-model.md` (`packages/contracts`). **Mock-first:** the frontend hits a single `api/` client module that returns seed data until these endpoints exist, then flips to live with no screen changes.

Base path: `/api`. All responses JSON. Errors: `{ error: { code, message } }` with appropriate HTTP status.

---

## Architect

### `POST /api/architects`
Create the local Architect (Phase 0 = single player, no real auth).
- Body: `{ name: string; school: SchoolId }`
- 201 → `Architect`

### `GET /api/architects/:id`
- 200 → `Architect`

### `GET /api/schools`
- 200 → `School[]` (the six)

---

## Champions

### `GET /api/architects/:id/champions`
- 200 → `Champion[]`

### `POST /api/architects/:id/champions`
- Body: `{ name; epithet?; spriteKind; color; config: AgentConfig }`
- 201 → `Champion`

### `GET /api/champions/:id` → `Champion`
### `PATCH /api/champions/:id`
Edit layers. Server validates against any constraints (and later, against the format if building *for* a specific contract).
- Body: `Partial<{ name; epithet; config: Partial<AgentConfig> }>`
- 200 → `Champion` | 422 if an edit violates an invariant.

### `GET /api/armory`
The catalog of equippable tools + loadout rules.
- 200 → `{ items: ArmoryItem[]; defaultBudget: number }`

---

## War formats & contracts

### `GET /api/formats` → `WarFormat[]`
### `GET /api/contracts`
Open/live wars for the board.
- Query: `?status=open|live|all`
- 200 → `WarInstance[]` (with `formatId`; client joins to format for display). **Never includes task content.**

### `GET /api/contracts/:id` → `WarInstance`

---

## Submission & run lifecycle

### `POST /api/contracts/:id/submissions`
Enter a Champion into a war. Server snapshots the config and **validates frozen layers** against the format; rejects mismatches.
- Body: `{ architectId; championId }`
- 201 → `Submission` | 422 `{ error.code: "FROZEN_LAYER_VIOLATION" }`

### `POST /api/submissions/:id/run`
Start the run (executes the agent against the sealed task via Anthropic API). Async.
- 202 → `Run` (status `queued`/`running`)

### `GET /api/runs/:id`
Poll status. (Or use SSE/websocket; see below.)
- 200 → `Run`

### `GET /api/runs/:id/replay`
The watchable event stream once available.
- 200 → `{ run: Run; events: ReplayEvent[]; verdict?: Verdict }`

### Streaming (preferred for Battle)
`GET /api/runs/:id/stream` (SSE): emits `ReplayEvent`s as they're produced, then a final `verdict` event. The Battle screen consumes this to animate turns live; falls back to polling `/replay`.

---

## Ladder & treasury (Phase 0: mock)

### `GET /api/ladder?season=current` → `{ entries: { architectId; name; rank; record }[] }`
### `GET /api/architects/:id/treasury` → `{ gold: number }`

These may return static/seed data in Phase 0 — keep the shape so they can become real later.

---

## Cross-cutting rules

- **Sealing:** no endpoint ever returns task prompts or answer keys to the client. The runner resolves `taskRef` server-side only.
- **Authority:** all layer-lock validation is server-side. The client treats frozen layers as read-only but must not be trusted to enforce them.
- **Reproducibility:** `POST /run` records the resolved model+version and a seed on the `Run`.
- **Idempotency:** `POST .../run` on an already-running submission returns the existing `Run`, not a new one.
- **Errors to handle in UI:** `FROZEN_LAYER_VIOLATION` (Forge/Deploy), `BUDGET_EXCEEDED` (Forge), `CONTRACT_CLOSED` (Arena), generic 500 on run failure (Battle shows an errored state).
