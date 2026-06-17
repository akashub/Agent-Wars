from __future__ import annotations

import subprocess
from pathlib import Path

from ..budget import BudgetEnforcer
from ..protocols import ModelHandle, RunArtifacts
from ..resolve import ResolvedAgent

PROMPT = ("You are competing in a code war. Edit files in the working directory to make "
          "the hidden tests pass. Persona: {persona}. When done, output only the final code.")


class AgentSdkExecutor:
    """Minimal Phase-0 adapter: one model turn that rewrites solution.py, then git diff.

    A richer Agent SDK loop (tools, sub-agents) replaces this body in Phase 1; the
    protocol signature stays identical.
    """

    def run(self, agent: ResolvedAgent, task_dir: Path, *, model: ModelHandle,
            budget: BudgetEnforcer, seed: int) -> RunArtifacts:
        work = task_dir.parent / f"_live_{seed}"
        subprocess.run(["rm", "-rf", str(work)], check=False)
        subprocess.run(["cp", "-r", str(task_dir), str(work)], check=True)
        subprocess.run(["git", "init", "-q"], cwd=work, check=True)
        subprocess.run(["git", "add", "-A"], cwd=work, check=True)
        subprocess.run(["git", "-c", "user.email=e@e", "-c", "user.name=n",
                        "commit", "-qm", "base"], cwd=work, check=True)
        stub = (work / "solution.py").read_text()
        user_msg = f"File solution.py:\n{stub}\nReturn the full corrected file."
        msgs = [
            {"role": "system", "content": PROMPT.format(persona=agent.persona)},
            {"role": "user", "content": user_msg},
        ]
        resp = model.complete(msgs, max_tokens=1024)
        budget.charge(tokens=resp.tokens_in + resp.tokens_out)
        code = resp.text
        if "```" in code:
            code = code.split("```")[1].lstrip("python").strip() + "\n"
        (work / "solution.py").write_text(code)
        diff = subprocess.run(["git", "diff"], cwd=work, capture_output=True, text=True).stdout
        return RunArtifacts(
            diff=diff, final_text=code,
            tokens_used=resp.tokens_in + resp.tokens_out, transcript=[{"final": code}],
        )
