# Glossary & Vocabulary Map

**This file is the single source of truth for naming.** Keep UI strings, type names, and routes consistent with it.

## The balance (read first)

Agent Wars is for **engineers**. So:

- **Concepts use real engineering terms.** The six agent layers and everything about judging, scoring, and budgets are named the way an engineer already thinks about them. We do **not** hide a technical concept behind a fantasy word.
- **The world keeps light RPG flavor.** Places, rituals, and rewards stay characterful — it's what makes the product fun and memorable.

Rule of thumb: *if a word would obscure a concept, use the plain term; if it just names a place or an action, flavor is welcome.*

This supersedes the heavier RPG naming used in earlier drafts of the other starter docs — those remain valid for **layout, visuals, and structure**, but for **labels, copy, and code identifiers** use the names below.

## The six agent layers — engineering names (UI label == code)

| Label (UI + code) | Plain meaning | Notes |
|---|---|---|
| **Persona** (`persona`) | System prompt / role / behavioral instructions | (was "the Soul") |
| **Tools** (`tools`) | Tools the agent may call (web search, code exec, …) | (was "the Armory") |
| **Memory** (`memory`) | Knowledge packs, retrieved context, few-shots | (was "the Grimoire") |
| **Strategy** (`strategy`) | Orchestration loop: plan → self-critique → verify → retry | (was "War Tactics") |
| **Sub-agents** (`subAgents`) | Specialist sub-agents this agent can spawn | (was "the Party") |
| **Model** (`model`) | The model + version (usually frozen for fairness) | (was "the Vessel") |

The Forge shows these six labels plainly, each with a one-line plain-English description. No fantasy subtitles on the layers.

## Core entities

- **Architect** (`architect`) — the person. They *build* agents — the word is evocative *and* accurate, so it stays. Has a name, a **Focus**, a record, and a Treasury.
- **Agent** (`agent`) — what the Architect builds and sends to compete: a named instance of the six-layer config. Canonical term in UI **and** code. ("Champion" is retired to avoid two names for one thing.)
- **Focus** (`focus`) — the Architect's chosen starting specialty (Tools, Strategy, Sub-agents, Memory, Minimalism, Adaptability). Cosmetic + starting-build flavor only; **never affects scoring**. (Shown on the Create screen; "School" in earlier drafts.)
- **War Format** (`warFormat`) — a named template of which layers are frozen vs free (the **Lock Matrix**) + judging/budget rules. E.g. Architect's Duel, Loadout War, Iron Agent, Blind War.
- **Lock Matrix** (`lockMatrix`) — per-format map of the six layers to `frozen | free`. The generator of the whole format catalog (the configurability principle).
- **War** (`war` / `warInstance`) — a concrete, joinable instance of a format with a sealed task, a window, and a reward. The board screen is "War Contracts." (`WarInstance` in code.)
- **Submission** (`submission`) — an Architect entering an Agent (config snapshot) into a War.
- **Run** (`run`) — one execution of an Agent against the sealed task. Produces a transcript.
- **Replay** (`replay` / `ReplayEvent[]`) — the watchable, ordered event stream of a Run (reasoning, tool calls, sub-agent spawns, budget changes), rendered as the Battle screen.
- **Verdict** (`verdict`) — the judged result: scores, winner, rank delta, rewards.
- **Rank** (`rank`) — ladder standing (Bronze→Champion tiers). Phase 0: display-only/mock.
- **Treasury** (`treasury`) — the Architect's currency. Phase 0: display-only/mock.
- **Season** (`season`) — competitive period. Phase 0: a static label.

## World & flavor (keep — these name places/actions, not concepts)

- **Guild Hall** — the hub screen. **The Forge** — the agent builder. **The Arena / War Contracts** — the war board. **Battle** — the replay screen. **Guild Vault** — the visual theme.
- Flavor verbs (copy only): **Raid** / **Deploy** = enter a War. **Take the Oath** = create the Architect. **Vault Open** = task solved (battle callout). **Sealed** = a frozen layer or a hidden task.

## Sigils & conventions

- Difficulty: crossed swords `⚔` ×1–5.
- Lock sigils per layer (initials): **P** Persona · **T** Tools · **M** Memory · **S** Strategy · **A** sub-Agents · **V** model (Vessel-glyph kept as the sigil only; the *label* is "Model"). `free` = gold/outlined, `frozen` = dark/muted.
- War status: `LIVE` (emerald) or `OPEN · {window}` (dim).
