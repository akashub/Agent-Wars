# Figures

Diagrams for the Agent Wars specs. Each diagram is stored twice:

- **`*.svg`** — the rendered image embedded in the spec docs (displays in VS Code's
  built-in Markdown preview, GitHub, etc. — no extension needed).
- **`*.mmd`** — the Mermaid source, kept so diagrams stay editable and regenerable.

## Index

| File | Used in | Shows |
|---|---|---|
| `fig2-agent-composition` | concept §4 | How a build is resolved against a ruleset before running |
| `fig3-lock-spectrum` | concept §5 | The frozen → free spectrum |
| `fig6-season-loop` | concept §8 | Ladder + marquee → Finals → medals → reset |
| `figA-components-data-flow` | technical §3 | Services + request/job data flow |
| `figB-data-model-er` | technical §5 | Entity relationships + key fields |
| `figC-run-lifecycle` | technical §6 | The 6-step agent run lifecycle |
| `figD-worktree-diff` | technical §6 | Git-worktree sandboxing for code tasks |
| `figE-referee-pipeline` | technical §7 | Auto-checks → judge → score → HITL |
| `figF-attribution-pipeline` | technical §8.1 | Layer-attribution analytics (Phase 2+) |
| `figG-end-to-end-sequence` | technical §13 | A marquee war as a sequence |
| `figH-roadmap` | technical §14 | The four build phases |

> Tables (the RPG character sheet, the Lock Matrix, the Format Atlas) live inline in
> the docs as Markdown — they render everywhere, so they aren't figures here.

## Regenerating

Requires the Mermaid CLI (`mmdc`). To re-render every diagram from its `.mmd` source:

```bash
cd docs/superpowers/specs/figures
for f in *.mmd; do mmdc -i "$f" -o "${f%.mmd}.svg" -b white; done
```

To edit a diagram: change the `.mmd`, re-run the command, done. The embed in the spec
(`![...](figures/<name>.svg)`) points at the SVG, so it updates automatically.

If you add a *new* diagram to a spec, add its Mermaid as a `.mmd` here, render it, and
embed it with `![Figure X — caption](figures/<name>.svg)`.
