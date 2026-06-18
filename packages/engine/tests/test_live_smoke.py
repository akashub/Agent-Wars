import os

import pytest

pytestmark = pytest.mark.skipif(
    not (os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")),
    reason="live smoke needs an LLM provider key",
)


def test_live_war_runs_with_shadow_judge(tmp_path):
    from agentwars.live.llm_judge import LLMJudge
    from agentwars.live.llm_provider import model_handle_for
    from agentwars.live.single_turn_executor import SingleTurnExecutor
    from agentwars.loader import load_agent, load_package
    from agentwars.orchestrator import run_war
    from agentwars.store import Store

    wp = load_package("war-packages/codegen_duel_001")
    agents = [load_agent("agents/planner.yaml")]
    st = Store(tmp_path / "s")
    st.init_db()
    res = run_war(
        wp,
        agents,
        executor_for=lambda a: SingleTurnExecutor(),
        judge=LLMJudge(),
        model_factory=model_handle_for,
        store=st,
        seed_base=1,
        work_root=tmp_path / "w",
    )
    assert res.ranking and res.judge_agreement is not None
