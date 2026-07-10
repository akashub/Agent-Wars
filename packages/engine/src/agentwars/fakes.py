from __future__ import annotations

from pathlib import Path

from .budget import BudgetEnforcer
from .protocols import JudgeVerdict, ModelResponse, RunArtifacts
from .resolve import ResolvedAgent


class FakeModel:
    def __init__(self, text: str = "ok"):
        self._text = text

    def complete(self, messages: list[dict], *, max_tokens: int) -> ModelResponse:
        return ModelResponse(text=self._text, tokens_in=1, tokens_out=1)


class FakeExecutor:
    def __init__(self, diff: str = "", final_text: str = "", tokens: int = 10):
        self._diff, self._final, self._tokens = diff, final_text, tokens

    def run(
        self,
        agent: ResolvedAgent,
        task_dir: Path,
        *,
        model,
        budget: BudgetEnforcer,
        seed: int,
    ) -> RunArtifacts:
        budget.charge(tokens=self._tokens)
        return RunArtifacts(
            diff=self._diff,
            final_text=self._final,
            transcript=[{"step": "fake", "seed": seed}],
            tokens_used=self._tokens,
        )


class FakeJudge:
    def __init__(self, overall: float = 1.0):
        self._overall = overall

    def evaluate(
        self, *, evidence: str, rubric: str, criteria: list[str], model
    ) -> JudgeVerdict:
        return JudgeVerdict(
            scores={c: self._overall for c in criteria},
            overall=self._overall,
            rationale="fake",
        )


class ScriptedModel:
    """Returns a fixed sequence of responses (for testing multi-turn loops)."""

    def __init__(self, texts: list[str]):
        self._texts = list(texts)
        self._i = 0

    def complete(self, messages: list[dict], *, max_tokens: int) -> ModelResponse:
        text = self._texts[min(self._i, len(self._texts) - 1)]
        self._i += 1
        return ModelResponse(text=text, tokens_in=1, tokens_out=1)
