from __future__ import annotations

import os

from anthropic import Anthropic

from ..protocols import ModelResponse


class AnthropicModelHandle:
    """Holds the API key. Callers receive this object, never the key itself."""

    def __init__(self, model: str = "claude-haiku-4-5-20251001"):
        self._client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self._model = model

    def complete(self, messages: list[dict], *, max_tokens: int) -> ModelResponse:
        system = next((m["content"] for m in messages if m["role"] == "system"), "")
        convo = [m for m in messages if m["role"] != "system"]
        resp = self._client.messages.create(model=self._model, max_tokens=max_tokens,
                                             system=system, messages=convo)
        text = "".join(b.text for b in resp.content if b.type == "text")
        return ModelResponse(text=text, tokens_in=resp.usage.input_tokens,
                             tokens_out=resp.usage.output_tokens)
