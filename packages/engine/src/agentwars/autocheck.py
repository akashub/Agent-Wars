from __future__ import annotations

import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GradeResult:
    passed: bool
    tests_passed: int
    tests_total: int
    detail: str


def parse_pytest_summary(text: str) -> tuple[int, int]:
    failed = passed = 0
    for line in text.splitlines():
        m = re.search(r"(\d+) failed", line)
        if m:
            failed = int(m.group(1))
        m = re.search(r"(\d+) passed", line)
        if m:
            passed = int(m.group(1))
    return passed, passed + failed


def grade_diff(baseline_dir: Path, diff_text: str, grader_dir: Path, workdir: Path,
               timeout: int = 60) -> GradeResult:
    if workdir.exists():
        shutil.rmtree(workdir)
    shutil.copytree(baseline_dir, workdir)
    subprocess.run(["git", "init", "-q"], cwd=workdir, check=True)
    subprocess.run(["git", "add", "-A"], cwd=workdir, check=True)
    subprocess.run(["git", "-c", "user.email=e@e", "-c", "user.name=n",
                    "commit", "-qm", "base"], cwd=workdir, check=True)
    if diff_text.strip():
        (workdir / "_agent.diff").write_text(diff_text)
        applied = subprocess.run(["git", "apply", "_agent.diff"], cwd=workdir,
                                 capture_output=True, text=True)
        (workdir / "_agent.diff").unlink()
        if applied.returncode != 0:
            return GradeResult(False, 0, 0, f"diff did not apply: {applied.stderr.strip()}")
    copied = []
    for t in grader_dir.glob("test_*.py"):
        shutil.copy(t, workdir / t.name)
        copied.append(t.name)
    try:
        proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "--tb=no",
                               "-p", "no:cacheprovider", *copied],
                              cwd=workdir, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return GradeResult(False, 0, 0, f"grader timed out after {timeout}s")
    passed, total = parse_pytest_summary(proc.stdout + proc.stderr)
    return GradeResult(passed=(total > 0 and passed == total),
                       tests_passed=passed, tests_total=total, detail=proc.stdout[-500:])
