# Frontend Architecture

**Stack:** React + TypeScript + Vite. Styling via CSS custom properties (the `design-system.md` tokens) with Tailwind mapped onto them. Client state via Zustand. Shared types from `packages/contracts`.

---

## Project structure

```
apps/web/
  index.html
  src/
    main.tsx
    App.tsx                 # AppShell + scene router
    styles/
      tokens.css            # :root design tokens (source of truth)
      base.css              # resets, fonts, keyframes (glint, rise, tw, sparkfly, pop, shake)
    lib/
      api.ts                # the ONE server seam (mock ↔ live)
      sprites.ts            # code-grid sprite renderer (Sprite abstraction)
      sound.ts              # optional blips (off by default)
    store/
      useGame.ts            # architect, champions, active contract, scene
    components/             # everything in component-library.md
      shell/ (AppShell, TopBar, StatusBar, FiligreeCorner, AmbientLayer)
      primitives/ (Panel, Button, Gem, Badge, StatBar, Sprite, Portrait, SectionHeader)
      composite/ (MenuList, RosterCard, ClassCard, LayerRow, EquipChip,
                  WarContractCard, LockSigils, DialogueBox, Verdict, Fighter)
      fx/ (Glint, Mote, Twinkle, SparkBurst)
    scenes/
      Boot.tsx  Create.tsx  Hall.tsx  Forge.tsx  Arena.tsx  Battle.tsx
```

---

## Scene management

Phase 0 is a single-surface flow, not deep linking — a simple scene state is enough (matches the prototype). Use a `scene` value in the store and render the active scene in `<Viewport>`; keep URL sync optional (React Router can be added later for shareable replay links). Transitions: the `fade` keyframe on scene mount; respect reduced motion.

```ts
type Scene = 'boot'|'create'|'hall'|'forge'|'arena'|'battle';
```

Set `AppShell.crumb` from a `scene → label` map; toggle `booting` only for `boot`.

---

## State (Zustand store `useGame`)

```ts
interface GameState {
  scene: Scene; setScene(s: Scene): void;
  architect?: Architect;
  champions: Champion[];
  activeChampionId?: string;
  activeContractId?: string;
  // actions
  createArchitect(name: string, school: SchoolId): Promise<void>;
  loadChampions(): Promise<void>;
  updateChampion(id: string, patch: Partial<AgentConfig>): Promise<void>;
  enterContract(contractId: string, championId: string): Promise<RunHandle>;
}
```

Domain truth lives on the server; the store caches and orchestrates. Derived UI values (budget spent, frozen-layer flags) computed in selectors, not stored.

---

## Tokens → code

- `styles/tokens.css` holds the `:root` variables verbatim from `design-system.md` — **the** source of truth.
- `tailwind.config.js` maps color/radius tokens (see `design-system.md §1`) so utilities like `bg-panel border-golddk text-cream rounded-vault` resolve to the vars.
- Keyframes (`glint`, `rise`, `tw`, `sparkfly`, `pop`, `shake`, `fade`, `blink`) live in `base.css`; expose as Tailwind `animate-*` or apply via component classes.
- Fonts loaded in `index.html` (`Cinzel`, `Cinzel Decorative`, `Chakra Petch`).
- Global: `@media (prefers-reduced-motion:reduce){ *{animation:none!important} }` plus skip mounting `AmbientLayer`/`SparkBurst` work.

---

## Sprite abstraction (`lib/sprites.ts` + `Sprite` component)

Phase 0 renders sprites from the code grids (`HERO`/`KNIGHT`/`CORE`) via the prototype's `renderSprite`/`palFor` functions, output as inline SVG. The `Sprite` component takes `{ kind, color, size }` and hides this. When real art arrives, swap the internals to draw a PNG/sheet frame — **no call sites change**. See `assets-spec.md`.

---

## The API seam (`lib/api.ts`)

Every server call goes through this module. It exposes typed functions matching `api-spec.md` (`getSchools`, `createArchitect`, `listContracts`, `submit`, `startRun`, `streamReplay`, …). A `USE_MOCK` flag (env) returns `packages/contracts/seed` data and a simulated replay stream in mock mode; live mode `fetch`es the API. Scenes never `fetch` directly.

---

## Battle rendering

`Battle.tsx` consumes a replay source — mock (the seed `ReplayEvent[]`) or live (SSE from `/runs/:id/stream`). A reducer maps each `ReplayEvent` → DialogueBox content + side effects (`SparkBurst` at the actor, `Fighter.hit` recoil, `StatBar` budget delta). Advance is user-driven (click/Space) in mock/replay mode and time/stream-driven in live mode; support both. End → mount `Verdict`.

---

## Quality bar

- Keyboard: menus arrow+Enter; all interactive elements focusable with visible focus.
- No `localStorage`/`sessionStorage` reliance for core flow (fine to add later for prefs).
- Components are pure/presentational where possible; data fetching in scenes/store.
- Type-safe end to end via `packages/contracts`.
