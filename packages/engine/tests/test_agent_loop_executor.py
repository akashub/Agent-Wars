from __future__ import annotations

import json

from agentwars.budget import BudgetEnforcer
from agentwars.fakes import ScriptedModel
from agentwars.live.agent_loop_executor import AgentLoopExecutor
from agentwars.models import Budget
from agentwars.protocols import RunArtifacts
from agentwars.resolve import ResolvedAgent

STUB = "def add(a, b):\n    raise NotImplementedError\n"
PUBLIC = (
    "from solution import add\n"
    "def test_a(): assert add(2, 3) == 5\n"
    "def test_b(): assert add(1, 1) == 2\n"
)
BROKEN = "def add(a, b):\n    return a - b\n"
FIXED = "def add(a, b):\n    return a + b\n"


def _task(tmp_path):
    d = tmp_path / "task"
    d.mkdir(parents=True)
    (d / "solution.py").write_text(STUB)
    (d / "public_test.py").write_text(PUBLIC)
    return d


def _agent(strategy):
    return ResolvedAgent(
        persona="p", tools=[], memory={}, strategy=strategy, sub_agents=[], model="m"
    )


def _budget(tokens=100000):
    return BudgetEnforcer(Budget(max_tokens=tokens, max_tool_calls=10, wall_clock_seconds=999))


def test_verify_retry_build_recovers_from_a_bad_first_attempt(tmp_path):
    ex = AgentLoopExecutor()
    art = ex.run(
        _agent({"verify_before_final": True, "max_retries": 1}),
        _task(tmp_path),
        model=ScriptedModel([BROKEN, FIXED]),
        budget=_budget(),
        seed=1,
    )
    assert isinstance(art, RunArtifacts)
    assert "a + b" in art.final_text
    kinds = [t["type"] for t in art.transcript]
    assert kinds.count("generate") == 2 and "check" in kinds


def test_one_shot_build_keeps_the_bad_first_attempt(tmp_path):
    ex = AgentLoopExecutor()
    art = ex.run(
        _agent({}),
        _task(tmp_path),
        model=ScriptedModel([BROKEN, FIXED]),
        budget=_budget(),
        seed=1,
    )
    assert "a - b" in art.final_text
    assert [t["type"] for t in art.transcript].count("generate") == 1


def test_transcript_is_deterministic_and_has_no_raw_paths(tmp_path):
    ex = AgentLoopExecutor()
    a1 = ex.run(
        _agent({"verify_before_final": True, "max_retries": 1}),
        _task(tmp_path / "a"),
        model=ScriptedModel([BROKEN, FIXED]),
        budget=_budget(),
        seed=1,
    )
    a2 = ex.run(
        _agent({"verify_before_final": True, "max_retries": 1}),
        _task(tmp_path / "b"),
        model=ScriptedModel([BROKEN, FIXED]),
        budget=_budget(),
        seed=1,
    )
    assert json.dumps(a1.transcript, sort_keys=True) == json.dumps(a2.transcript, sort_keys=True)
    blob = json.dumps(a1.transcript)
    assert "/" not in blob and "0x" not in blob
    for t in a1.transcript:
        assert "raw" not in t


def test_budget_exhaustion_returns_best_so_far(tmp_path):
    ex = AgentLoopExecutor()
    art = ex.run(
        _agent({"verify_before_final": True, "max_retries": 3}),
        _task(tmp_path),
        model=ScriptedModel([BROKEN, FIXED]),
        budget=_budget(tokens=2),
        seed=1,
    )
    assert art.final_text.strip() != ""
    assert art.halted_reason == "budget_exhausted"


def test_public_check_works_when_task_nested_in_a_pytest_package(tmp_path):
    # Regression: the executor's work dir must be isolated so the public-check pytest
    # does NOT inherit a surrounding pyproject.toml (which would collect 0 tests).
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "pyproject.toml").write_text(
        '[tool.pytest.ini_options]\nfilterwarnings = ["error"]\ntestpaths = ["tests"]\n')
    d = pkg / "task"
    d.mkdir()
    (d / "solution.py").write_text(STUB)
    (d / "public_test.py").write_text(PUBLIC)
    ex = AgentLoopExecutor()
    art = ex.run(
        _agent({"verify_before_final": True, "max_retries": 1}),
        d,
        model=ScriptedModel([BROKEN, FIXED]),
        budget=_budget(),
        seed=1,
    )
    checks = [t for t in art.transcript if t["type"] == "check"]
    assert checks and all(c["n_total"] == 2 for c in checks)   # public tests were collected
    assert "a + b" in art.final_text                           # loop still recovers
    assert list(pkg.glob("_loop_*")) == []                     # no work dir leaked into the pkg
