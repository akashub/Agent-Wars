from pathlib import Path

from agentwars.fakes import FakeExecutor, FakeJudge, FakeModel
from agentwars.loader import load_agent, load_package
from agentwars.orchestrator import run_war
from agentwars.store import Store

GOOD = (
    "--- a/solution.py\n+++ b/solution.py\n@@ -1,2 +1,2 @@\n"
    " def add(a, b):\n-    raise NotImplementedError\n+    return a + b\n"
)
BAD = (
    "--- a/solution.py\n+++ b/solution.py\n@@ -1,2 +1,2 @@\n"
    " def add(a, b):\n-    raise NotImplementedError\n+    return a - b\n"
)


def _run(tmp_path):
    wp = load_package("war-packages/codegen_duel_001")
    agents = [load_agent("agents/planner.yaml"), load_agent("agents/minimalist.yaml")]
    ex = {
        "planner": FakeExecutor(diff=GOOD, final_text="return a+b"),
        "minimalist": FakeExecutor(diff=BAD, final_text="return a-b"),
    }
    st = Store(tmp_path / "store")
    st.init_db()
    res = run_war(
        wp,
        agents,
        executor_for=lambda a: ex[a.id],
        judge=FakeJudge(1.0),
        model_factory=lambda _m: FakeModel(),
        store=st,
        seed_base=1,
        work_root=tmp_path / "w",
    )
    return wp, st, res


def test_e2e_deterministic_scores(tmp_path):
    _, _, res = _run(tmp_path)
    assert [aid for aid, _ in res.ranking] == ["planner", "minimalist"]
    assert res.ranking[0][1].objective_points == 100.0
    assert res.ranking[1][1].objective_points == 0.0


def test_e2e_stable_hashes_across_runs(tmp_path):
    _, st1, _ = _run(tmp_path / "a")
    _, st2, _ = _run(tmp_path / "b")
    assert st1.get_run("wp_codegen_duel_001::planner::0")["content_hash"] == \
           st2.get_run("wp_codegen_duel_001::planner::0")["content_hash"]


def test_e2e_score_recomputable_from_store(tmp_path):
    _, st, _ = _run(tmp_path)
    rid = "wp_codegen_duel_001::planner::0"
    assert st.recompute_hash(rid) == st.get_run(rid)["content_hash"]


def test_grader_isolation_baseline_has_no_tests():
    base = Path("war-packages/codegen_duel_001/baseline")
    assert list(base.glob("test_*.py")) == []
