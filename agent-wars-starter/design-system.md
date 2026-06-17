# Design System — "Guild Vault"

Pixel-exact source of truth: `/reference/prototype.html`. This doc extracts every token so the look is reproducible in React + Tailwind without reverse-engineering. **Never hardcode a value that exists here as a token.**

---

## 1. Color tokens

Define as CSS custom properties on `:root` (source of truth), then map into Tailwind.

```css
:root{
  /* base / stone */
  --stone-1:#1c1330;   /* upper stone */
  --stone-2:#0b0712;   /* lower stone (near-black) */
  --panel:rgba(28,20,44,.92);   /* primary panel fill */
  --panel-2:rgba(18,12,28,.94); /* inset / nested fill */

  /* gold ramp (metallic) */
  --gold-hi:#ffe9a8;   /* highlight */
  --gold:#f2c24e;      /* base gold */
  --gold-mid:#d9a23a;  /* midtone */
  --gold-dk:#8a5e1e;   /* shadow / borders */
  --gold-line:#6e4815; /* hairline dividers */

  /* text */
  --cream:#f3e7cf;     /* primary text */
  --dim:#bda888;       /* secondary text */
  --faint:#7d6a55;     /* tertiary / status */

  /* gems (accents) */
  --emerald:#36e09a;   /* success / free / win */
  --ruby:#ff3b5e;      /* danger / over-budget / loss */
  --sapphire:#5b8cff;
  --amethyst:#b15bff;
  --teal:#2fd8c0;      /* secondary accent */

  --accent:var(--teal);
  --radius:5px;
  --warm:rgba(242,194,78,.18); /* gold glow tint */
}
```

### Gradients & backgrounds

```css
/* the metallic gold gradient — used for buttons, logo text, victory text */
--gold-grad:linear-gradient(180deg,#ffe9a8 0%,#f2c24e 42%,#cf9a36 72%,#8a5e1e 100%);

/* the vault background (apply to the app shell / screen) */
background:
  radial-gradient(circle at 50% -12%, #4a1d8e 0%, transparent 46%),   /* amethyst glow top */
  radial-gradient(circle at 50% 118%, #0f4a44 0%, transparent 50%),   /* teal glow bottom */
  linear-gradient(180deg, var(--stone-1), var(--stone-2)),
  repeating-linear-gradient(0deg, transparent 0 38px, rgba(0,0,0,.22) 38px 40px),   /* brick H */
  repeating-linear-gradient(90deg, transparent 0 76px, rgba(0,0,0,.18) 76px 78px);  /* brick V */
```

### Tailwind mapping (tailwind.config.js → theme.extend.colors)

```js
colors:{
  stone1:'var(--stone-1)', stone2:'var(--stone-2)',
  panel:'var(--panel)', panel2:'var(--panel-2)',
  goldhi:'var(--gold-hi)', gold:'var(--gold)', goldmid:'var(--gold-mid)',
  golddk:'var(--gold-dk)', goldline:'var(--gold-line)',
  cream:'var(--cream)', dim:'var(--dim)', faint:'var(--faint)',
  emerald:'var(--emerald)', ruby:'var(--ruby)', sapphire:'var(--sapphire)',
  amethyst:'var(--amethyst)', teal:'var(--teal)',
},
borderRadius:{ vault:'var(--radius)' }
```

---

## 2. Typography

Load from Google Fonts: `Cinzel` (600/700/800/900), `Cinzel Decorative` (700/900), `Chakra Petch` (400/500/600/700).

Roles: **Cinzel Decorative** = logo + "VICTORY" only. **Cinzel** = headers, buttons, labels, menu items, names, status. **Chakra Petch** = body, dialogue text, sub-labels, numeric data.

| Token | Family | Weight | Size | Spacing / case | Used for |
|---|---|---|---|---|---|
| `display-xl` | Cinzel Decorative | 900 | 50px | ls 2px | Boot logo |
| `display` | Cinzel Decorative | 900 | 19px | ls 2px | Top-bar logo |
| `victory` | Cinzel Decorative | 900 | 34px | — | Battle verdict title |
| `h1` | Cinzel | 800 | 19px | ls 2px | Screen title (`.h`) |
| `h2` | Cinzel | 700 | 13px | ls 2px, UPPER | Panel header (`.wh`) |
| `name-lg` | Cinzel | 800 | 23px | ls 1px | Champion/Architect name |
| `name` | Cinzel | 600 | 15–16px | ls 1px | Menu items, roster names |
| `label` | Cinzel | — | 11px | ls 2px, UPPER | Field labels, status bar |
| `body` | Chakra Petch | 400–500 | 14–16px | — | Dialogue, descriptions |
| `small` | Chakra Petch | 400 | 11–12px | — | Sub-labels, meta, dim text |

Logo & victory text use the gold gradient via `background:var(--gold-grad); -webkit-background-clip:text; color:transparent;`.

---

## 3. Spacing, radius, elevation

- **Radius:** `--radius` (5px) everywhere; portraits/cards same.
- **Scene padding:** 18px. **Panel padding:** 13–15px. **Grid gaps:** 13px.
- **Panel elevation:**
  `border:1px solid var(--gold-dk); box-shadow: inset 0 0 0 1px rgba(255,233,168,.16), 0 0 22px rgba(150,90,255,.12), 0 4px 14px rgba(0,0,0,.4);`
- **Screen frame:** `box-shadow: 0 0 0 2px var(--gold-dk), 0 0 0 4px #000, 0 0 50px rgba(150,90,255,.25), 0 22px 60px rgba(0,0,0,.65);`
- **Glow tint:** `--warm` for gold glows on hover/active.

---

## 4. Signature effects (motion)

All effects must be disabled under `@media (prefers-reduced-motion:reduce)`.

### Sword-glint sweep (`.glint`)
A diagonal white streak that periodically sweeps across gold elements (logo, primary buttons). Wrap element in `overflow:hidden`; add `::after`:
```css
.glint{position:relative;overflow:hidden;}
.glint::after{content:"";position:absolute;top:-50%;left:-60%;width:40%;height:200%;
  transform:skewX(-22deg);
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.6),transparent);
  animation:glint 5s ease-in-out infinite;}   /* primary buttons: 4.5s */
@keyframes glint{0%,70%{left:-60%;}85%{left:130%;}100%{left:130%;}}
```

### Sparkle / twinkle (`.twinkle`)
Small `✦` glyphs scattered in the ambient layer, fading in/out.
```css
@keyframes tw{40%{opacity:0;}50%{opacity:1;transform:scale(1.3);}60%{opacity:0;}}
/* color:#fff; text-shadow:0 0 6px var(--gold-hi); animation:tw 2.6s ease-in-out infinite; random delay */
```

### Drifting gold motes (`.mote`)
~22 small gold dots slowly rising in the ambient layer.
```css
@keyframes rise{from{transform:translateY(0);}to{transform:translateY(-120px);}}
/* 3px dot, background+box-shadow gold, opacity .5, duration 7–15s, negative random delay */
```

### Spark burst (battle) (`.spark`)
On each battle action, spawn 5–22 sparks at the impact point flying outward.
```css
.spark{position:absolute;width:4px;height:4px;border-radius:50%;
  background:var(--gold-hi);box-shadow:0 0 6px var(--gold);
  animation:sparkfly .6s ease-out forwards;}
@keyframes sparkfly{to{transform:translate(var(--dx),var(--dy)) scale(.2);opacity:0;}}
/* per spark: random angle, dist 20–66px set as --dx/--dy; ~half colored #fff */
```

### Other keyframes (from prototype)
- `pop` (battle callout text): 1.1s, rises + scales + fades.
- `shake` (struck fighter): 0.3s ×2.
- `fade` (scene enter): 0.25s.
- `blink` (cursor / press-start / dialogue arrow): 1–1.2s steps(1).

---

## 5. Iconography

- **Gems:** 45°-rotated rounded squares with `box-shadow:0 0 8px currentColor`. Variants: emerald `e`, ruby `r`, sapphire `s`, amethyst `a`, gold `g`. Used for treasury, rewards, rank.
- **Crossed swords `⚔`:** brand mark, difficulty rating, menu cursor, primary action accents.
- **`◈` / `◆` / `✦` / `❖`:** ornamental bullets (panel headers, ports, sparkles, spec lines).
- **Filigree corners:** the SVG in the prototype (`.orn`), gold stroke with a small gem node, placed at the four corners of the screen and key panels. Reuse verbatim — see `component-library.md → FiligreeCorner`.
