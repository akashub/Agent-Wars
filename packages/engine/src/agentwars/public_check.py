from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from .autocheck import parse_pytest_summary


@dataclass(frozen=True)
class PublicCheckResult:
    passed: bool
    n_passed: int
    n_total: int
    raw: str  # truncated stdout+stderr for the MODEL prompt only; never hash this


def run_public_check(workdir: Path, timeout: int = 30) -> PublicCheckResult:
    """Run the visible public test signal in `workdir` (a copy of baseline with the
    agent's solution.py). Uses baseline/public_test.py if present; otherwise just
    imports solution.py to surface syntax/runtime errors. NEVER runs the hidden grader."""
    pub = workdir / "public_test.py"
    if pub.exists():
        cmd = [sys.executable, "-m", "pytest", "-q", "--tb=short",
               "-p", "no:cacheprovider", str(pub)]
    else:
        # no public tests: a smoke import so the loop still gets a crash/no-crash signal
        cmd = [sys.executable, "-c", "import solution"]
    try:
        proc = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return PublicCheckResult(False, 0, 0, f"public check timed out after {timeout}s")
    out = proc.stdout + proc.stderr
    if pub.exists():
        n_passed, n_total = parse_pytest_summary(out)
        passed = n_total > 0 and n_passed == n_total
    else:
        n_total = 1
        n_passed = 1 if proc.returncode == 0 else 0
        passed = proc.returncode == 0
    return PublicCheckResult(passed=passed, n_passed=n_passed, n_total=n_total, raw=out[-1500:])
