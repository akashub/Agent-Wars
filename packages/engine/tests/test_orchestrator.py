from agentwars.fakes import FakeExecutor, FakeJudge, FakeModel
from agentwars.models import AgentDef, WarPackage
from agentwars.orchestrator import WarResult, run_war
from agentwars.store import Store


def _wp(tmp_path) -> WarPackage:
    base = tmp_path / "baseline"
    base.mkdir()
    (base / "solution.py").write_text("def add(a, b):\n    raise NotImplementedError\n")
    grader = tmp_path / "grader"
    grader.mkdir()
    (grader / "test_solution.py").write_text(
        "from solution import add\ndef test_add(): assert add(2,3)==5\n"
        "def test_neg(): assert add(-1,1)==0\n")
    return WarPackage.model_validate({
        "id": "wp1", "name": "Duel", "format": "architects_duel", "author": "@host",
        "task": {"baseline_path": str(base), "grader_path": str(grader)},
        "ruleset": {"layers": {layer: {"frozen": True} for layer in
                    ["persona", "tools", "memory", "sub_agents"]} |
                    {"model": {"frozen": True, "value": "m"}, "strategy": {"frozen": False}},
                    "budget": {"max_tokens": 9999, "max_tool_calls": 9, "wall_clock_seconds": 99},
                    "runs_per_agent": 2, "seed_policy": "fixed_per_run"},
        "scoring": {"base_points": 100},
    })

GOOD_DIFF = ("--- a/solution.py\n+++ b/solution.py\n@@ -1,2 +1,2 @@\n"
             " def add(a, b):\n-    raise NotImplementedError\n+    return a + b\n")
BAD_DIFF = ("--- a/solution.py\n+++ b/solution.py\n@@ -1,2 +1,2 @@\n"
            " def add(a, b):\n-    raise NotImplementedError\n+    return a - b\n")

def test_run_war_ranks_solver_above_non_solver_and_persists(tmp_path):
    wp = _wp(tmp_path)
    agents = [AgentDef(id="p", name="Planner", architect="@x", model="m"),
              AgentDef(id="m", name="Minimal", architect="@y", model="m")]
    executors = {"p": FakeExecutor(diff=GOOD_DIFF, final_text="add"),
                 "m": FakeExecutor(diff=BAD_DIFF, final_text="sub")}
    store = Store(tmp_path / "store")
    store.init_db()
    result = run_war(wp, agents, executor_for=lambda a: executors[a.id],
                     judge=FakeJudge(0.5), model=FakeModel(), store=store, seed_base=1,
                     work_root=tmp_path / "work")
    assert isinstance(result, WarResult)
    assert result.ranking[0][0] == "p"
    assert result.ranking[0][1].objective_points == 100.0
    assert result.ranking[1][1].objective_points == 0.0
    assert store.get_run("wp1::p::0")["content_hash"]
