# Screens Spec

Six scenes, all inside `AppShell`. Each switches in the `<Viewport>`. Below: route, purpose, layout, components, content/copy, states, interactions, transitions. Copy is intentionally exact — match it.

Navigation map:
```
boot ──▶ create ──▶ hall ──┬─▶ forge ──▶ arena ──▶ battle ──▶ (Return) hall
                           ├─▶ arena ──▶ battle
                           ├─▶ hall-of-champions (stub)
                           ├─▶ chronicle (stub)
                           └─▶ create (Quarters)
back buttons: forge/arena ──▶ hall ; battle Return ──▶ hall
```
`crumb` per scene: Create→"Oath", Hall→"Guild Hall", Forge→"The Forge", Arena→"War Contracts", Battle→"The Arena".

---

## 1. Boot (`/`) — title

**Purpose:** entry / brand moment. `AppShell` is in `booting` mode (chrome hidden).

**Layout:** centered column: large `⚔` crest, glinted `display-xl` logo "AGENT WARS", tagline, blinking press-start.

**Copy:** tagline `— Forge a Champion · Plunder the Arena —`; CTA `✦ Enter the Guild ✦`.

**Interaction:** click CTA (or anywhere) → `create`. **Transition:** fade.

---

## 2. Create (`/create`) — swear in an Architect

**Purpose:** name + choose School. Gates entry to the Hall.

**Layout:** title row "Swear in an Architect". Two columns:
- Left: a `Panel` with label "Guild Name" + text input; a `Panel` (grow) "Choose a School · VI" containing a 3-col `ClassCard` grid (6 schools).
- Right: a `Panel` with the selected School `Portrait` + name; a `Panel` (grow) with the School's lore (who / description / `❖ specialty`); a primary `Button` "✦ Take the Oath" (disabled until name + school set).

**Schools (id, name, color, specialty, lore):** Artificer #e0923a (Tools & Armory), Tactician #5b8cff (Strategy & Orchestration), Beastmaster #36e09a (Sub-agents & Swarms), Loremaster #b15bff (Memory & Knowledge), Ascetic #d8d2c0 (More with less), Wanderer #2fd8c0 (Adaptability). Lore text in `data-model.md` seed / prototype.

**States:** no school → preview empty, button disabled. School selected → ring on card, preview + lore populate.

**Interaction:** select card → update preview/lore; type name; "Take the Oath" → set Architect, set StatusBar `ARCHITECT:`, go `hall`.

---

## 3. Guild Hall (`/hall`) — hub

**Purpose:** home base; pick where to go. *(This is the screen the visual direction was approved on — match it closely.)*

**Layout:** `grid 1.1fr / 1fr`.
- Left column: a `Panel` **character card** (`Portrait` + name + `ctitle` `{School} · "the Untested"` + `Badge`s + statline `Rank Bronze III · 0–0 · Treasury 1,240◈`); a `Panel` (grow, scroll) "Champions · {count}" with `RosterCard`s.
- Right column: a `Panel` (grow) "The Hall · ⚔" with a `MenuList`; a `Panel` (row) with two buttons: primary "⚔ To the Arena" + "The Forge".

**Menu items (label, sub, target):**
- The Forge — "build & equip a champion" → `forge` (default selected)
- The Arena — "take a contract · watch the raid" → `arena`
- Hall of Champions — "the ladder & standings" → stub toast
- The Chronicle — "tales of past wars" → stub toast
- Quarters — "your Architect & record" → `create`

**Roster (seed):** Cartographer (hero, #5b8cff, Gold II · 14–3), Hydra (core, #ff3b8e, Gold IV · 11–7), "+ Forge new champion" (empty slot).

**Stub toast copy:** `⚜ This wing of the guild is still under construction.`

---

## 4. The Forge (`/forge`) — agent builder

**Purpose:** edit a Champion's six layers within a loadout budget.

**Layout:** title row: `◀ Hall` back button, "The Forge", a tag chip `Loadout War · Intermediate`. `grid 1.1fr / 1fr`.
- Left (scroll): six `LayerRow`s in order — Persona/Soul, Tools/Armory (clickable → reveals Armory), Memory/Grimoire, Strategy/War Tactics, Sub-agents/Party, Model/Vessel (**locked**, `🔒 SEALED`). Below: a hidden `Panel` "Armory — loadout budget" with `EquipChip`s.
- Right: a `Panel` with the Champion `Portrait` + name "Cartographer" + "the Methodical"; a `Panel` with a `StatBar` "Loadout · {spent}/100" (ruby if over) + statline `Record 14–3 · 🥇 Iron Crown`; a primary `Button` "⚔ Send to Battle" → `arena`.

**Armory items (name, cost, default-on):** Web Search 20 ✓, Code Exec 30, Calculator 5 ✓, Knowledge Pack 15 ✓, File Ops 10, Custom API 25.

**Layer icons:** 📜 ⚔️ 📖 🎯 🐺 💠.

**States:** Tools row toggles the Armory panel. Toggling chips recomputes budget; >100 turns the bar ruby and (in real build) blocks deploy. Locked Model row is non-interactive.

---

## 5. War Contracts (`/arena`) — the war board

**Purpose:** browse and enter wars (the missing screen from earlier iterations).

**Layout:** title row: `◀ Hall`, "War Contracts", tag `{n} Open`. A 2-col grid of `WarContractCard`s.

**Wars (seed) — fmt, difficulty, lockMatrix [P,T,M,S,sub,V] (1=frozen,0=free), reward, status, desc:**
1. Architect's Duel — ⚔⚔ — `[1,1,1,0,1,1]` — +25 — OPEN · 2d — "All sealed but Strategy. A test of pure cunning — same soul, same gear, different plan."
2. Loadout War — ⚔⚔⚔ — `[1,0,1,1,1,1]` — +30 — **LIVE** — "Raid the armory freely within budget. Reading the contract and picking the right gear is the whole game."
3. Iron Agent — ⚔⚔⚔⚔ — `[1,1,1,1,1,1]` — +45 — OPEN · 5d — "Minimal everything: one tool, a short oath, no party. Crack the vault with elegance, not firepower."
4. Blind War — ⚔⚔⚔⚔⚔ — `[0,0,0,0,0,1]` — +60 — OPEN · 1d — "The mark is hidden until the raid begins. Forge a generalist that survives anything."

**Card anatomy:** status (emerald LIVE / dim OPEN) + difficulty; title; description; `LockSigils`; reward (`gem-gold` + value) + `Raid ⚔` primary button → `battle`.

**Interaction:** "Raid" sets the active contract context, then go `battle`.

---

## 6. Battle (`/battle`) — the replay (signature screen)

**Purpose:** watch the agent run as a narrated fight. This is the spectacle — the agent's reasoning *is* the battle dialogue.

**Layout (full-bleed, no scene padding):**
- `Arena` (flex): a gold holographic perspective-grid floor; two `Fighter`s (left = your Champion cyan/sapphire, right = opponent magenta/ruby); an `fx` callout layer; a `Verdict` overlay (hidden until end).
- `platebar`: two `StatBar`s = each fighter's **Budget** (the MP analogue), with name + level.
- `DialogueBox`: narration; click / Space / Enter to advance turns.

**Turn script (seed) — who, text, fx{side, callout, sparks, hit?, budgetDelta}:** the prototype's `SCRIPT` array. Callouts: PLAN, RUSH, STRIKE!, BREACH, PARRY, BUDGET OUT, VAULT OPEN. Each fx spawns a `SparkBurst` (5–22) at the actor; some shake the struck fighter and drain a budget bar.

**End:** after the last line → `Verdict.show`. Verdict seed: Cartographer 92 / Hydra 81, reward `gem-gold +120 · Glicko +18 · 🥇 Giant Slayer`. Buttons: Return → `hall`, Replay → restart script.

**Real-data note:** in Phase 0 the script is replaced by a `Replay` (`ReplayEvent[]`) returned from the API (`data-model.md`, `api-spec.md`). The renderer maps event types → callouts/sparks/budget changes. Keep the seed script as the fallback/storybook.

**Reduced motion:** sparks/glint/ambient off; turns still advance, fighters don't shake.
