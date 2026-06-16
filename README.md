# Agent Wars

> A competitive sport where you don't fight — you *build a fighter*.

You are an **Architect**. You design an AI **Agent** (its persona, tools, memory,
strategy, and sub-agents), then send it into the **Arena** to compete against other
Architects' agents in **Wars** — structured challenges with clear rules, scoring, and
a referee. Win points, climb the ladder, earn medals, reach the season **Finals**.

*"Fantasy football for AI agents — you build the champion, the champion does the
fighting."*

## Design docs

| Doc | What it covers |
|---|---|
| [Concept & Creative Design](docs/superpowers/specs/2026-06-12-agent-wars-concept.md) | The fantasy, vocabulary, the agent character sheet, the **War Format Catalog** (12 formats), seasons, medals, the show layer, integrity rules. |
| [Technical Specification](docs/superpowers/specs/2026-06-12-agent-wars-technical-spec.md) | Architecture, the Agent + War Package schemas, battle/judge/scoring engines, data model, security, phased roadmap. |
| [Figures](docs/superpowers/specs/figures/) | SVG diagrams (with Mermaid source) used in both docs. |

## Status

Draft v1 — design/spec stage. Build target is a full web app, delivered via a phased
roadmap (engine core → thin web app → show depth → public hardening). Next step is a
Phase-0 implementation plan.
