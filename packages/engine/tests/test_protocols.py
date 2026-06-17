from pathlib import Path

from agentwars.budget import BudgetEnforcer
from agentwars.fakes import FakeExecutor, FakeJudge, FakeModel
from agentwars.models import Budget
from agentwars.protocols import JudgeVerdict, RunArtifacts
from agentwars.resolve import ResolvedAgent


def _agent():
    return ResolvedAgent(persona="", tools=[], memory={}, strategy={}, sub_agents=[], model="m")


def test_fake_executor_returns_artifacts():
    be = BudgetEnforcer(Budget(max_tokens=1000, max_tool_calls=10, wall_clock_seconds=999))
    art = FakeExecutor(diff="DIFF", final_text="answer").run(
        _agent(), Path("."), model=FakeModel(), budget=be, seed=1)
    assert isinstance(art, RunArtifacts)
    assert art.diff == "DIFF" and art.final_text == "answer" and art.halted_reason is None


def test_fake_judge_returns_verdict():
    v = FakeJudge(overall=0.5).evaluate(evidence="x", rubric="r", criteria=["correctness"],
                                        model=FakeModel())
    assert isinstance(v, JudgeVerdict) and v.overall == 0.5
