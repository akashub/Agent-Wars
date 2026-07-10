from __future__ import annotations

import tempfile
from pathlib import Path

import typer

from .fakes import FakeExecutor, FakeJudge, FakeModel
from .loader import load_agent, load_package
from .orchestrator import run_war
from .store import Store

app = typer.Typer(help="Agent Wars engine CLI")


@app.command()
def validate(path: str) -> None:
    """Validate an agent (.yaml) or a war package (directory)."""
    if Path(path).is_dir():
        wp = load_package(path)
        typer.echo(f"valid war package: {wp.id} ({wp.format})")
    else:
        a = load_agent(path)
        typer.echo(f"valid agent: {a.id} by {a.architect}")


@app.command("run-war")
def run_war_cmd(
    package_dir: str,
    agents: list[str] = typer.Option(..., "--agents"),
    store: str = typer.Option(".aw-store", "--store"),
    work: str = typer.Option("", "--work", help="work dir; default: an isolated temp dir"),
    live: bool = typer.Option(
        False, "--live", help="run agents via strategy-driven agent loop (network)"
    ),
) -> None:
    """Run a war package against a set of agents."""
    work_dir = Path(work) if work else Path(tempfile.mkdtemp(prefix="aw-work-"))
    wp = load_package(package_dir)
    loaded = [load_agent(a) for a in agents]
    st = Store(Path(store))
    st.init_db()

    if live:
        from .live.agent_loop_executor import AgentLoopExecutor  # noqa: PLC0415
        from .live.llm_judge import LLMJudge  # noqa: PLC0415
        from .live.llm_provider import model_handle_for  # noqa: PLC0415

        model_factory = model_handle_for
        judge = LLMJudge()

        def executor_for(_a):
            return AgentLoopExecutor()

    else:
        judge = FakeJudge(0.5)

        def model_factory(_m):
            return FakeModel()

        def executor_for(a):
            return FakeExecutor(diff="", final_text=a.name)

    result = run_war(
        wp,
        loaded,
        executor_for=executor_for,
        judge=judge,
        model_factory=model_factory,
        store=st,
        seed_base=1,
        work_root=work_dir,
    )
    typer.echo("Ranking:")
    for i, (aid, score) in enumerate(result.ranking, 1):
        typer.echo(
            f"  {i}. {aid}  objective={score.objective_points}  avg_tokens={score.avg_tokens}"
        )
    typer.echo(f"Judge agreement (shadow): {result.judge_agreement}")
