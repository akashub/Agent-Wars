from agentwars.autocheck import GradeResult, grade_diff, parse_pytest_summary

GOOD_DIFF = """\
--- a/solution.py
+++ b/solution.py
@@ -1,2 +1,2 @@
 def add(a, b):
-    raise NotImplementedError
+    return a + b
"""

def _fixture(tmp_path):
    base = tmp_path / "baseline"
    base.mkdir()
    (base / "solution.py").write_text("def add(a, b):\n    raise NotImplementedError\n")
    grader = tmp_path / "grader"
    grader.mkdir()
    (grader / "test_solution.py").write_text(
        "from solution import add\n"
        "def test_add(): assert add(2, 3) == 5\n"
        "def test_add_neg(): assert add(-1, 1) == 0\n")
    return base, grader

def test_parse_pytest_summary():
    assert parse_pytest_summary("2 passed in 0.01s") == (2, 2)
    assert parse_pytest_summary("1 failed, 1 passed in 0.02s") == (1, 2)
    assert parse_pytest_summary("no tests ran in 0.00s") == (0, 0)

def test_good_diff_passes_hidden_tests(tmp_path):
    base, grader = _fixture(tmp_path)
    res = grade_diff(base, GOOD_DIFF, grader, tmp_path / "work")
    assert isinstance(res, GradeResult)
    assert res.passed and res.tests_passed == 2 and res.tests_total == 2

def test_grader_not_left_in_agent_view(tmp_path):
    base, grader = _fixture(tmp_path)
    assert not (base / "test_solution.py").exists()
    assert list(base.glob("test_*.py")) == []

def test_grader_ignores_public_test_in_baseline(tmp_path):
    # A public_test.py living in baseline must NOT be counted by the referee's grade.
    base = tmp_path / "baseline"
    base.mkdir()
    (base / "solution.py").write_text("def add(a, b):\n    return a + b\n")
    (base / "public_test.py").write_text(
        "from solution import add\n"
        "def test_pub1(): assert add(1, 1) == 2\n"
        "def test_pub2(): assert add(2, 2) == 4\n")
    grader = tmp_path / "grader"
    grader.mkdir()
    (grader / "test_solution.py").write_text(
        "from solution import add\ndef test_hidden(): assert add(3, 4) == 7\n")
    # identity diff (solution already correct) so we isolate the counting behavior
    diff = ""
    res = grade_diff(base, diff, grader, tmp_path / "work")
    # Only the 1 hidden test counts — not the 2 public tests.
    assert res.tests_total == 1 and res.tests_passed == 1 and res.passed


def test_grader_times_out_on_infinite_loop(tmp_path):
    # An agent solution that hangs must not hang the grader; it fails cleanly.
    base = tmp_path / "baseline"
    base.mkdir()
    (base / "solution.py").write_text("def add(a, b):\n    raise NotImplementedError\n")
    grader = tmp_path / "grader"
    grader.mkdir()
    (grader / "test_solution.py").write_text(
        "from solution import add\ndef test_add(): assert add(2, 3) == 5\n")
    hang_diff = ("--- a/solution.py\n+++ b/solution.py\n@@ -1,2 +1,2 @@\n"
                 " def add(a, b):\n-    raise NotImplementedError\n"
                 "+    while True: pass\n")
    res = grade_diff(base, hang_diff, grader, tmp_path / "work", timeout=2)
    assert not res.passed and "timed out" in res.detail
