import pytest

from agentwars.budget import BudgetEnforcer, BudgetExceeded
from agentwars.models import Budget


def test_token_budget_raises_when_exceeded():
    be = BudgetEnforcer(Budget(max_tokens=100, max_tool_calls=5, wall_clock_seconds=999))
    be.charge(tokens=60)
    with pytest.raises(BudgetExceeded):
        be.charge(tokens=50)
    assert be.used["tokens"] == 60

def test_tool_calls_and_time():
    clock = iter([0.0, 0.0, 10.0])
    be = BudgetEnforcer(Budget(max_tokens=99, max_tool_calls=1, wall_clock_seconds=5),
                        now=lambda: next(clock))
    be.charge(tool_calls=1)
    with pytest.raises(BudgetExceeded):
        be.charge(tool_calls=1)
    with pytest.raises(BudgetExceeded):
        be.check_time()

def test_remaining_tokens_tracks_usage():
    be = BudgetEnforcer(Budget(max_tokens=1000, max_tool_calls=5, wall_clock_seconds=999))
    assert be.remaining_tokens() == 1000
    be.charge(tokens=300)
    assert be.remaining_tokens() == 700
