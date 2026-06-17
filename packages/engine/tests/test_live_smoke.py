import os

import pytest

pytestmark = pytest.mark.skipif("ANTHROPIC_API_KEY" not in os.environ,
                                reason="live smoke needs ANTHROPIC_API_KEY")


def test_live_war_runs_with_shadow_judge(tmp_path):
    from agentwars.live.agentsdk_executor import AgentSdkExecutor
    from agentwars.live.claude_judge import ClaudeJudge
    from agentwars.live.model_broker import AnthropicModelHandle
    from agentwars.loader import load_agent, load_package
    from agentwars.orchestrator import run_war
    from agentwars.store import Store

    wp = load_package("war-packages/codegen_duel_001")
    agents = [load_agent("agents/planner.yaml")]
    st = Store(tmp_path / "s")
    st.init_db()
    res = run_war(wp, agents, executor_for=lambda a: AgentSdkExecutor(),
                  judge=ClaudeJudge(), model=AnthropicModelHandle(),
                  store=st, seed_base=1, work_root=tmp_path / "w")
    assert res.ranking and res.judge_agreement is not None
