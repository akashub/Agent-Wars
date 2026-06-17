from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from .budget import BudgetEnforcer
from .resolve import ResolvedAgent


@dataclass(frozen=True)
class ModelResponse:
    text: str
    tokens_in: int
    tokens_out: int


class ModelHandle(Protocol):
    """Brokered model access. Implementations hold the key; callers never see it."""

    def complete(self, messages: list[dict], *, max_tokens: int) -> ModelResponse: ...


@dataclass(frozen=True)
class RunArtifacts:
    diff: str
    final_text: str
    transcript: list[dict] = field(default_factory=list)
    tokens_used: int = 0
    tool_calls: int = 0
    halted_reason: str | None = None


class Executor(Protocol):
    def run(
        self,
        agent: ResolvedAgent,
        task_dir: Path,
        *,
        model: ModelHandle,
        budget: BudgetEnforcer,
        seed: int,
    ) -> RunArtifacts: ...


@dataclass(frozen=True)
class JudgeVerdict:
    scores: dict[str, float]
    overall: float
    rationale: str


class Judge(Protocol):
    def evaluate(
        self,
        *,
        evidence: str,
        rubric: str,
        criteria: list[str],
        model: ModelHandle,
    ) -> JudgeVerdict: ...
