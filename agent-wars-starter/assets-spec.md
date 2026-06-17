# Assets Spec

How art and icons plug into the build. Phase 0 ships with **code-drawn placeholder sprites**; this doc defines the slot system so real pixel art drops in later with zero call-site changes.

---

## The Sprite abstraction

All character art goes through one component: `Sprite({ kind, color, size })` (see `frontend-architecture.md`). Today it renders an inline SVG from a string-grid (`lib/sprites.ts`). Tomorrow it renders a frame from a PNG/sprite-sheet. **Nothing else in the app may reference art directly** — always go through `Sprite`/`Portrait`.

`kind` values (current placeholders): `hero` (robed Architect/champion), `knight` (armored), `core` (arcane construct = agent). `color` is the character's identity hex; the placeholder renderer derives shading from it.

### Swapping in real art (later)
- Provide a sheet per `kind` (and per state if animated): idle, and optionally attack/hit/cast for the Battle screen.
- Recommended frame size: **64×64** or **96×96**, transparent PNG, nearest-neighbor (`image-rendering:pixelated`).
- Naming: `sprites/{kind}/{state}.png` (+ a JSON frame map if multi-frame).
- `Sprite` chooses art by `kind`; `color` becomes a tint/recolor or selects a palette variant. Keep the `{kind,color,size}` signature stable.

---

## Required art slots (when commissioning a set)

Matching your reference set's quality means a cohesive pixel pack. Minimum slots for the current screens:
- **Architect heroes** — one figure per School (6), or one base recolored per School color. Used: Boot crest, Create preview, Hall character card.
- **Champion/agent bodies** — at least 2–3 distinct silhouettes (e.g. hero, knight, construct) for roster + battle, recolored per Champion identity color.
- **Battle states** (nice-to-have) — idle + attack/hit/cast for the two fighters to make the spark beats land.

Until then, the three code-grid sprites recolored by identity color are the placeholders and read fine inside the ornate `Portrait` frames.

---

## Fonts

Loaded via Google Fonts in `index.html`:
- **Cinzel** (600/700/800/900) — headers, buttons, names, labels.
- **Cinzel Decorative** (700/900) — logo + "VICTORY" only.
- **Chakra Petch** (400/500/600/700) — body, dialogue, numeric/data.

Keep weights minimal for load; self-host later if needed.

---

## Icon & ornament inventory

These are glyphs/SVG, not raster assets — no files needed:
- **Gems:** CSS `Gem` component (emerald/ruby/sapphire/amethyst/gold). Treasury, rewards, rank.
- **`⚔`** crossed swords: brand mark, difficulty, menu cursor, primary-action accent.
- **`⚜`** fleur (status bar "GUILD ACTIVE").
- **`◈ ◆ ✦ ❖ ▼`** ornamental bullets / sparkles / advance arrow.
- **Filigree corner:** the gold SVG in `component-library.md → FiligreeCorner` (reuse verbatim).
- **Layer icons (Forge):** emoji placeholders `📜 ⚔️ 📖 🎯 🐺 💠` — replace with custom gold line-icons when art is produced (keep one-to-one with the six layers).

---

## Audio (optional, off by default)

The prototype has none, but a tiny WebAudio "blip" on select/confirm and a soft "chime" on Victory suit the vibe. Gate behind a user-initiated mute toggle; never autoplay. Keep optional for Phase 0.
