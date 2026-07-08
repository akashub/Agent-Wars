from agentwars.public_check import PublicCheckResult, run_public_check


def _mk(tmp_path, solution_src, public_src=None):
    wd = tmp_path / "wd"
    wd.mkdir(parents=True)
    (wd / "solution.py").write_text(solution_src)
    if public_src is not None:
        (wd / "public_test.py").write_text(public_src)
    return wd


PUB = ("from solution import add\n"
       "def test_a(): assert add(2, 3) == 5\n"
       "def test_b(): assert add(0, 0) == 0\n")


def test_public_check_passes_with_correct_solution(tmp_path):
    wd = _mk(tmp_path, "def add(a, b): return a + b\n", PUB)
    r = run_public_check(wd)
    assert isinstance(r, PublicCheckResult)
    assert r.passed and r.n_passed == 2 and r.n_total == 2


def test_public_check_reports_failures_with_raw_for_model(tmp_path):
    wd = _mk(tmp_path, "def add(a, b): return a - b\n", PUB)   # wrong
    r = run_public_check(wd)
    assert not r.passed and r.n_passed < r.n_total
    assert r.raw   # non-empty text to feed back to the model


def test_public_check_smoke_import_when_no_public_tests(tmp_path):
    wd = _mk(tmp_path, "def add(a, b): return a + b\n")  # no public_test.py
    assert run_public_check(wd).passed          # imports cleanly
    wd2 = _mk(tmp_path / "x", "def add(a, b):\n    return\n import broken\n")  # syntax error
    assert not run_public_check(wd2).passed
