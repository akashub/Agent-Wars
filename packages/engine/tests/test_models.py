import pytest
from pydantic import ValidationError

from agentwars.models import AgentDef, Budget, LayerRule, Ruleset, WarPackage


def test_agent_requires_architect():
    with pytest.raises(ValidationError):
        AgentDef(id="a1", name="A", architect="", model="claude-haiku-4-5-20251001")


def test_agent_roundtrip_defaults():
    a = AgentDef(id="a1", name="A", architect="@x", model="claude-haiku-4-5-20251001")
    assert a.tools == [] and a.strategy == {} and a.cosmetics == {}


def test_warpackage_author_required_and_layers_complete():
    wp = WarPackage.model_validate({
        "id": "wp1", "name": "Duel", "format": "architects_duel", "author": "@host",
        "task": {"baseline_path": "baseline", "grader_path": "grader"},
        "ruleset": {
            "layers": {layer: {"frozen": True} for layer in
                       ["persona", "tools", "memory", "sub_agents", "model"]}
            | {"strategy": {"frozen": False}},
            "budget": {"max_tokens": 50000, "max_tool_calls": 10, "wall_clock_seconds": 300},
            "runs_per_agent": 3, "seed_policy": "fixed_per_run",
        },
        "scoring": {"base_points": 100},
    })
    assert wp.ruleset.layers["model"].frozen is True
    assert wp.ruleset.runs_per_agent == 3


def test_warpackage_rejects_unknown_layer():
    with pytest.raises(ValidationError):
        Ruleset(layers={"persona": LayerRule(frozen=True), "bogus": LayerRule(frozen=True)},
                budget=Budget(max_tokens=1, max_tool_calls=1, wall_clock_seconds=1),
                runs_per_agent=1, seed_policy="fixed_per_run")
