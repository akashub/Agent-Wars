from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from .autocheck import grade_diff
from .budget import BudgetEnforcer, BudgetExceeded
from .models import AgentDef, WarPackage
from .protocols import Executor, Judge, ModelHandle, RunArtifacts
from .resolve import resolve_agent
from .scoring import SubmissionScore, aggregate, rank, score_run
from .store import Store


@dataclass(frozen=True)
class WarResult:
    ranking: list[tuple[str, SubmissionScore]]
    judge_agreement: float | None

def _criteria() -> list[str]:
    return ["correctness", "elegance"]

def run_war(package: WarPackage, agents: list[AgentDef], *,
            executor_for: Callable[[AgentDef], Executor], judge: Judge,
            model: ModelHandle, store: Store, seed_base: int, work_root: Path) -> WarResult:
    baseline = Path(package.task.baseline_path)
    grader = Path(package.task.grader_path)
    submissions: dict[str, SubmissionScore] = {}
    agreements: list[float] = []

    for agent in agents:
        resolved = resolve_agent(agent, package.ruleset)
        run_scores = []
        for i in range(package.ruleset.runs_per_agent):
            seed = seed_base + i
            be = BudgetEnforcer(package.ruleset.budget)
            try:
                art = executor_for(agent).run(resolved, baseline, model=model, budget=be, seed=seed)
            except BudgetExceeded:
                art = RunArtifacts(diff="", final_text="", halted_reason="budget_exhausted")
            grade = grade_diff(baseline, art.diff, grader, work_root / f"{agent.id}_{i}")
            shadow = judge.evaluate(evidence=art.final_text, rubric="reward correct, simple code",
                                    criteria=_criteria(), model=model)
            rs = score_run(grade, package.scoring, art, shadow)
            run_scores.append(rs)
            agreements.append(1.0 if (shadow.overall >= 0.5) == grade.passed else 0.0)
            run_id = f"{package.id}::{agent.id}::{i}"
            payload = json.dumps({"transcript": art.transcript, "grade": grade.__dict__},
                                 sort_keys=True).encode()
            h = store.put_transcript(run_id, payload)
            store.record_run(run_id=run_id, war_id=package.id,
                             agent_version=f"{agent.id}@1", seed=seed,
                             tokens_used=art.tokens_used, content_hash=h,
                             transcript_ref=f"{run_id}.json")
        submissions[agent.id] = aggregate(run_scores)

    agreement = round(sum(agreements) / len(agreements), 4) if agreements else None
    return WarResult(ranking=rank(submissions), judge_agreement=agreement)
