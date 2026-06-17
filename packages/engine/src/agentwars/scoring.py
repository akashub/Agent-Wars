from __future__ import annotations

from dataclasses import dataclass

from .autocheck import GradeResult
from .models import Scoring
from .protocols import JudgeVerdict, RunArtifacts


@dataclass(frozen=True)
class RunScore:
    objective_points: float
    tokens_used: int
    shadow_overall: float | None


@dataclass(frozen=True)
class SubmissionScore:
    objective_points: float
    avg_tokens: float
    shadow_overall: float | None


def score_run(grade: GradeResult, scoring: Scoring, artifacts: RunArtifacts,
              shadow: JudgeVerdict | None) -> RunScore:
    frac = (grade.tests_passed / grade.tests_total) if grade.tests_total else 0.0
    return RunScore(objective_points=round(frac * scoring.base_points, 4),
                    tokens_used=artifacts.tokens_used,
                    shadow_overall=(shadow.overall if shadow else None))


def aggregate(runs: list[RunScore]) -> SubmissionScore:
    n = len(runs)
    obj = sum(r.objective_points for r in runs) / n
    toks = sum(r.tokens_used for r in runs) / n
    shadows = [r.shadow_overall for r in runs if r.shadow_overall is not None]
    shadow_avg = round(sum(shadows) / len(shadows), 4) if shadows else None
    return SubmissionScore(objective_points=round(obj, 4), avg_tokens=round(toks, 4),
                           shadow_overall=shadow_avg)


def rank(submissions: dict[str, SubmissionScore]) -> list[tuple[str, SubmissionScore]]:
    return sorted(submissions.items(),
                  key=lambda kv: (-kv[1].objective_points, kv[1].avg_tokens))
