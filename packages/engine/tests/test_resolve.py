from agentwars.models import AgentDef, Budget, LayerRule, Ruleset
from agentwars.resolve import ResolvedAgent, resolve_agent


def _duel_ruleset(model="claude-haiku-4-5-20251001"):
    frozen = {
        layer: LayerRule(frozen=True)
        for layer in ("persona", "tools", "memory", "sub_agents")
    }
    frozen["model"] = LayerRule(frozen=True, value=model)
    frozen["strategy"] = LayerRule(frozen=False)
    budget = Budget(max_tokens=1, max_tool_calls=1, wall_clock_seconds=1)
    return Ruleset(
        layers=frozen, budget=budget, runs_per_agent=1, seed_policy="fixed_per_run"
    )


def test_duel_forces_model_and_strips_cosmetics_and_keeps_strategy():
    agent = AgentDef(id="a", name="A", architect="@x", model="claude-opus-4-8",
                     persona="hi", tools=["web"], strategy={"plan_first": True},
                     cosmetics={"title": "the Bold"})
    r = resolve_agent(agent, _duel_ruleset())
    assert isinstance(r, ResolvedAgent)
    assert r.model == "claude-haiku-4-5-20251001"
    assert r.strategy == {"plan_first": True}
    assert r.persona == "" and r.tools == []
    assert not hasattr(r, "cosmetics")


def test_token_cap_truncates_persona():
    rs = _duel_ruleset()
    rs.layers["persona"] = LayerRule(frozen=False, token_cap=3)
    agent = AgentDef(id="a", name="A", architect="@x", model="m",
                     persona="one two three four five")
    r = resolve_agent(agent, rs)
    assert len(r.persona.split()) <= 3
