from agentwars.autocheck import GradeResult
from agentwars.models import Scoring
from agentwars.protocols import JudgeVerdict, RunArtifacts
from agentwars.scoring import RunScore, SubmissionScore, aggregate, rank, score_run


def _art(tokens):
    return RunArtifacts(diff="d", final_text="f", tokens_used=tokens)


def test_objective_points_scale_with_tests_and_record_shadow_judge():
    g = GradeResult(passed=False, tests_passed=1, tests_total=2, detail="")
    rs = score_run(g, Scoring(base_points=100), _art(20),
                   shadow=JudgeVerdict(scores={}, overall=0.9, rationale=""))
    assert rs.objective_points == 50.0
    assert rs.shadow_overall == 0.9
    rs2 = score_run(g, Scoring(base_points=100), _art(20), shadow=None)
    assert rs2.objective_points == rs.objective_points


def test_aggregate_averages_and_rank_orders_by_objective_then_tiebreak():
    a = aggregate([RunScore(80.0, 30, 0.1), RunScore(100.0, 10, 0.2)])
    assert a.objective_points == 90.0
    ranking = rank({"A": SubmissionScore(90.0, 20.0, None),
                    "B": SubmissionScore(90.0, 10.0, None)})
    assert ranking[0][0] == "B"
