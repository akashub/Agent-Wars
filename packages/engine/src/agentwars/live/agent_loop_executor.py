from __future__ import annotations

import subprocess
from pathlib import Path

from ..budget import BudgetEnforcer, BudgetExceeded
from ..protocols import ModelHandle, RunArtifacts
from ..public_check import run_public_check
from ..resolve import ResolvedAgent
from .single_turn_executor import PROMPT, _extract_code

_PLAN_SYSTEM = "{persona} Plan your approach in a few short bullets."
_RETRY_HINT = "Your previous attempt failed these checks, fix them:\n{errors}"


class AgentLoopExecutor:
    """Strategy-driven self-repair loop.

    strategy={} => one-shot (identical behaviour to SingleTurnExecutor).
    With plan_first/verify_before_final/max_retries set => full loop.
    Best candidate seen so far is returned on budget exhaustion.
    """

    def run(
        self,
        agent: ResolvedAgent,
        task_dir: Path,
        *,
        model: ModelHandle,
        budget: BudgetEnforcer,
        seed: int,
    ) -> RunArtifacts:
        work = task_dir.parent / f"_loop_{seed}"
        subprocess.run(["rm", "-rf", str(work)], check=False)
        subprocess.run(["cp", "-r", str(task_dir), str(work)], check=True)
        subprocess.run(["git", "init", "-q"], cwd=work, check=True)
        subprocess.run(["git", "add", "-A"], cwd=work, check=True)
        subprocess.run(
            ["git", "-c", "user.email=e@e", "-c", "user.name=n", "commit", "-qm", "base"],
            cwd=work,
            check=True,
        )

        stub = (work / "solution.py").read_text()
        plan_first = bool(agent.strategy.get("plan_first"))
        verify = bool(agent.strategy.get("verify_before_final"))
        max_retries = int(agent.strategy.get("max_retries", 0))
        attempts = (1 + max_retries) if verify else 1

        transcript: list[dict] = []
        tokens_used = 0
        halted: str | None = None

        # --- optional planning turn ---
        plan_text = ""
        if plan_first:
            sys_msg = _PLAN_SYSTEM.format(persona=agent.persona)
            msgs = [
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": stub},
            ]
            max_out = min(budget.remaining_tokens(), 8192)
            resp = model.complete(msgs, max_tokens=max_out)
            try:
                budget.charge(tokens=resp.tokens_in + resp.tokens_out)
            except BudgetExceeded:
                halted = "budget_exhausted"
                transcript.append({"type": "plan"})
                tokens_used += resp.tokens_in + resp.tokens_out
                return _finalize(work, None, transcript, tokens_used, halted)
            tokens_used += resp.tokens_in + resp.tokens_out
            plan_text = resp.text
            transcript.append({"type": "plan"})

        # --- generate / verify loop ---
        best_code: str | None = None
        best_n: int = -1
        last_errors: str = ""

        for i in range(attempts):
            user_parts = [f"File solution.py:\n{stub}\nReturn the full corrected file."]
            if plan_text:
                user_parts.append(f"Your plan:\n{plan_text}")
            if last_errors:
                user_parts.append(_RETRY_HINT.format(errors=last_errors))
            msgs = [
                {"role": "system", "content": PROMPT.format(persona=agent.persona)},
                {"role": "user", "content": "\n\n".join(user_parts)},
            ]
            max_out = min(budget.remaining_tokens(), 8192)
            resp = model.complete(msgs, max_tokens=max_out)
            try:
                budget.charge(tokens=resp.tokens_in + resp.tokens_out)
            except BudgetExceeded:
                halted = "budget_exhausted"
                break
            tokens_used += resp.tokens_in + resp.tokens_out

            code = _extract_code(resp.text)
            (work / "solution.py").write_text(code)
            transcript.append({"type": "generate", "attempt": i})

            if not verify:
                best_code = code
                best_n = 0
                break

            # Clear __pycache__ so the subprocess picks up the new solution.py byte-for-byte
            # rather than a stale .pyc (writes within the same second share an mtime).
            subprocess.run(["rm", "-rf", str(work / "__pycache__")], check=False)
            result = run_public_check(work)
            transcript.append(
                {
                    "type": "check",
                    "attempt": i,
                    "passed": result.passed,
                    "n_passed": result.n_passed,
                    "n_total": result.n_total,
                }
            )
            if result.n_passed > best_n:
                best_code = code
                best_n = result.n_passed
            if result.passed:
                break
            # raw errors are EPHEMERAL — fed to next prompt only, never into transcript
            last_errors = result.raw

        return _finalize(work, best_code, transcript, tokens_used, halted)


def _finalize(
    work: Path,
    best_code: str | None,
    transcript: list[dict],
    tokens_used: int,
    halted: str | None,
) -> RunArtifacts:
    final = best_code or ""
    (work / "solution.py").write_text(final)
    diff = subprocess.run(
        ["git", "diff"], cwd=work, capture_output=True, text=True
    ).stdout
    return RunArtifacts(
        diff=diff,
        final_text=final,
        transcript=transcript,
        tokens_used=tokens_used,
        halted_reason=halted,
    )
