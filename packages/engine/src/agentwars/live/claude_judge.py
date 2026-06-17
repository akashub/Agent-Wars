from __future__ import annotations

import json

from ..judge_prompt import build_judge_messages
from ..protocols import JudgeVerdict, ModelHandle


class ClaudeJudge:
    def evaluate(self, *, evidence: str, rubric: str, criteria: list[str],
                 model: ModelHandle) -> JudgeVerdict:
        msgs = build_judge_messages(evidence=evidence, rubric=rubric, criteria=criteria)
        resp = model.complete(msgs, max_tokens=1024)
        try:
            data = json.loads(resp.text[resp.text.index("{"):resp.text.rindex("}") + 1])
        except (ValueError, json.JSONDecodeError):
            data = {"scores": {}, "overall": 0.0, "rationale": "unparseable"}
        return JudgeVerdict(scores=data.get("scores", {}),
                            overall=float(data.get("overall", 0.0)),
                            rationale=str(data.get("rationale", "")))
