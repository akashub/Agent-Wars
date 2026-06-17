from typer.testing import CliRunner

from agentwars.cli import app

runner = CliRunner()


def test_validate_ok():
    res = runner.invoke(app, ["validate", "agents/planner.yaml"])
    assert res.exit_code == 0 and "valid" in res.stdout.lower()


def test_run_war_prints_ranking(tmp_path):
    res = runner.invoke(app, ["run-war", "war-packages/codegen_duel_001",
                              "--agents", "agents/planner.yaml",
                              "--agents", "agents/minimalist.yaml",
                              "--store", str(tmp_path / "s"),
                              "--work", str(tmp_path / "w")])
    assert res.exit_code == 0
    assert "Ranking" in res.stdout and "judge agreement" in res.stdout.lower()
