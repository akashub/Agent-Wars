from __future__ import annotations

import time
from collections.abc import Callable

from .models import Budget


class BudgetExceeded(Exception):
    pass


class BudgetEnforcer:
    def __init__(self, budget: Budget, now: Callable[[], float] = time.monotonic):
        self._b = budget
        self._now = now
        self._start = now()
        self.used = {"tokens": 0, "tool_calls": 0}

    def charge(self, *, tokens: int = 0, tool_calls: int = 0) -> None:
        if self.used["tokens"] + tokens > self._b.max_tokens:
            raise BudgetExceeded("token budget exhausted")
        if self.used["tool_calls"] + tool_calls > self._b.max_tool_calls:
            raise BudgetExceeded("tool-call budget exhausted")
        self.check_time()
        self.used["tokens"] += tokens
        self.used["tool_calls"] += tool_calls

    def check_time(self) -> None:
        if self._now() - self._start > self._b.wall_clock_seconds:
            raise BudgetExceeded("wall-clock budget exhausted")
