# Component Library

Every reusable piece of the Guild Vault UI. Build these as React + TypeScript components styled with the tokens from `design-system.md`. Each entry: purpose, anatomy, variants/states, and a props sketch. The prototype's CSS classes are noted in `(parens)` as the visual reference.

> Rule: if a pattern appears on two screens, it's a component here. Screens (`screens-spec.md`) only compose these.

---

## App shell

### `AppShell` (`#screen`)
The vault frame that wraps every screen. Contains the ambient layer, four filigree corners, the TopBar, a `<Viewport>` for the active scene, and the StatusBar.
- Props: `{ crumb: string; booting?: boolean; children }`
- `booting` hides TopBar + StatusBar (used by the Boot scene).

### `AmbientLayer` (`.ambient`)
Absolutely-positioned, behind content. Renders ~22 `Mote`s + ~10 `Twinkle`s at random positions. Pure decoration; `pointer-events:none`.

### `FiligreeCorner` (`.orn`)
The gold SVG flourish. One component, rotated/flipped via a `position` prop for the four corners.
- Props: `{ position: 'tl'|'tr'|'bl'|'br'; size?: number }`
- SVG (reuse verbatim):
```html
<svg viewBox="0 0 64 64">
 <g fill="none" stroke="var(--gold)" stroke-width="2.4" stroke-linecap="round">
  <path d="M5 42 L5 15 Q5 5 15 5 L42 5"/><path d="M13 35 L13 21 Q13 13 21 13 L35 13"/>
  <path d="M5 42 Q16 40 18 29"/><path d="M42 5 Q40 16 29 18"/></g>
 <circle cx="13" cy="13" r="4" fill="var(--gold)"/></svg>
```

### `TopBar` (`.topbar`)
Left: brand (`⚔` + glinted logo). Center: breadcrumb (`crumb`). Right: `Treasury`.
- Props: `{ crumb: string; treasury: number }`

### `StatusBar` (`.statusbar`)
Cinzel, uppercase, faint. Left: `⚜ GUILD ACTIVE`. Then `ARCHITECT: {name}`. Spacer. Right: `VESSEL: {model}`, `SEASON {n}`.
- Props: `{ architectName?: string; model: string; season: string }`

---

## Primitives

### `Panel` (`.win`)
The dark gold-edged container. Optional header.
- Props: `{ title?: string; headerRight?: ReactNode; scroll?: boolean; grow?: boolean; children }`
- Renders `SectionHeader` when `title` given.

### `SectionHeader` (`.wh`)
Cinzel uppercase gold, `◈` prefix, hairline `--gold-line` underline, optional right slot (`.x`, faint).

### `Button` (`.btn`)
- Variants: `default` (gold-outlined, warm hover) | `primary` (gold-gradient fill, dark text, **built-in glint sweep**).
- Sizes: `md` | `sm`.
- Props: `{ variant?, size?, onClick, disabled?, children }`
- States: hover (warm glow), active (translateY 1px), disabled (opacity .4).

### `GemBadge` / `Gem` (`.gem`)
A faceted gem chip; optionally with a value.
- Props: `{ kind: 'emerald'|'ruby'|'sapphire'|'amethyst'|'gold'; value?: string|number; size?: number }`

### `Badge` (`.badge`)
A gem-colored pill for archetype/type tags (Pokémon-style). `◈` prefix, dark text on a gradient of the gem color.
- Props: `{ label: string; color: string }`

### `StatBar` (`.bar` + `i`)
Gold-fill progress bar with label row.
- Props: `{ label: string; value: number; max: number; danger?: boolean }`
- `danger` (e.g. over budget) switches the fill to ruby.

### `Sprite` (`.spr`) and `Portrait` (`.port`)
- `Sprite` renders a Champion/Architect sprite. **Abstraction over the art source** — Phase 0 uses the code-grid renderer; later swaps to a PNG/sheet. See `assets-spec.md`. Props: `{ kind: 'hero'|'knight'|'core'; color: string; size: number }`.
- `Portrait` is the ornate gold-ringed frame (`◆` node on top) that wraps a `Sprite`. Props: `{ size: number; children }`.

---

## Composite components

### `MenuList` / `MenuItem` (`.menu li`)
Cinzel rows with a glowing `⚔` cursor on hover/selected, a `sub` line, gold left-border on active.
- Item props: `{ label, sub, selected?, onSelect }`
- Keyboard: arrow to move, Enter to select; cursor blinks on focused/selected.

### `RosterCard` (`.rcard`)
A Champion in the roster list: `Portrait` (small) + name + record + rank (gold, right). Selectable.
- Props: `{ champion: ChampionSummary; selected?; onClick }`

### `ClassCard` (`.ccard`)
A School option in Create: small `Portrait` + name. Selectable (gold ring when chosen).
- Props: `{ school: School; selected?; onClick }`

### `LayerRow` (`.layer`)
A Champion layer in the Forge: icon tile + name with RPG subtitle + current value summary; locked variant shows a `🔒 SEALED` tag and is non-interactive.
- Props: `{ icon, name, rpgName, summary, locked?, onClick? }`

### `EquipChip` (`.chip`)
A toggleable Armory item with a gold cost. On = warm fill + gold border + `✓`.
- Props: `{ name: string; cost: number; on: boolean; onToggle }`

### `WarContractCard` (`.warcard`)
A war on the board: status row (`● LIVE` emerald / `○ OPEN · {window}` dim) + difficulty (`⚔`×n), title, description, `LockSigils`, reward (gem + value) and a `Raid ⚔` primary button.
- Props: `{ contract: WarInstance; onDeploy }`

### `LockSigils` (`.sigils`)
Six small tiles `P T M S ◊ V`; `free` = gold/outlined + glow, `frozen` = dark/muted. Renders from a `LockMatrix`.
- Props: `{ lockMatrix: LockMatrix }`

### `DialogueBox` (`.dlg`)
Battle narration box: gold top-border, uppercase gold `who`, body text, blinking `▼` advance arrow. Click or Space/Enter advances.
- Props: `{ who: string; text: string; onAdvance }`

### `Verdict` (`.verdict`)
Battle end overlay: "VICTORY" (gold-gradient Cinzel Decorative), two `scoreline`s, a `reward` row (gem + Glicko + medal), Return + Replay buttons.
- Props: `{ result: Verdict; onReturn; onReplay }`

### `Fighter` + `SparkBurst` (battle)
- `Fighter`: nameplate + `Sprite`, with a `hit` shake animation trigger.
- `SparkBurst`: imperative helper that spawns N `.spark` elements at a screen point with random vectors. Props/args: `{ origin: {x,y}; count: number }`.

---

## Utility wrappers

- `Glint` (`.glint`) — wrap any element to add the sweep (logo, gold frames).
- `Mote`, `Twinkle` — ambient particles (used only inside `AmbientLayer`).

## Component inventory checklist

App shell: AppShell, AmbientLayer, FiligreeCorner, TopBar, StatusBar •
Primitives: Panel, SectionHeader, Button, Gem/GemBadge, Badge, StatBar, Sprite, Portrait •
Composite: MenuList/MenuItem, RosterCard, ClassCard, LayerRow, EquipChip, WarContractCard, LockSigils, DialogueBox, Verdict, Fighter, SparkBurst •
Utility: Glint, Mote, Twinkle.
