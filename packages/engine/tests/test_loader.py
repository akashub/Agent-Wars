from agentwars.loader import load_agent, load_package


def test_load_example_package_and_agents():
    wp = load_package("war-packages/codegen_duel_001")
    assert wp.format == "architects_duel"
    assert wp.ruleset.layers["model"].frozen is True
    a = load_agent("agents/planner.yaml")
    assert a.architect.startswith("@")
