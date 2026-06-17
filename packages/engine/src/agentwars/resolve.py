from __future__ import annotations

from dataclasses import dataclass

from .models import AgentDef, LayerRule, Ruleset


@dataclass(frozen=True)
class ResolvedAgent:
    persona: str
    tools: list[str]
    memory: dict
    strategy: dict
    sub_agents: list[dict]
    model: str


def _apply(rule: LayerRule | None, current, empty):
    if rule is None:
        return current
    if rule.frozen:
        return rule.value if rule.value is not None else empty
    return current


def resolve_agent(agent: AgentDef, ruleset: Ruleset) -> ResolvedAgent:
    layers = ruleset.layers
    persona = _apply(layers.get("persona"), agent.persona, "")
    cap = getattr(layers.get("persona"), "token_cap", None)
    if cap is not None:
        persona = " ".join(persona.split()[:cap])
    return ResolvedAgent(
        persona=persona,
        tools=_apply(layers.get("tools"), agent.tools, []),
        memory=_apply(layers.get("memory"), agent.memory, {}),
        strategy=_apply(layers.get("strategy"), agent.strategy, {}),
        sub_agents=_apply(layers.get("sub_agents"), agent.sub_agents, []),
        model=_apply(layers.get("model"), agent.model, agent.model),
    )
