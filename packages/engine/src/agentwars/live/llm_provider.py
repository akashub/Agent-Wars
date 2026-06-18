from __future__ import annotations

from litellm import completion

from ..protocols import ModelResponse


class LiteLLMModelHandle:
    """Provider-agnostic model access via litellm. Routes to ANY provider by the model
    string (gpt-4o, claude-3-5-sonnet, gemini/gemini-1.5-pro, ...); the API key is read
    from that provider's env var (OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, ...).
    Callers receive this handle, never a key."""

    def __init__(self, model: str):
        self._model = model

    def complete(self, messages: list[dict], *, max_tokens: int) -> ModelResponse:
        resp = completion(model=self._model, messages=messages, max_tokens=max_tokens)
        text = resp.choices[0].message.content or ""
        usage = resp.usage
        return ModelResponse(
            text=text,
            tokens_in=getattr(usage, "prompt_tokens", 0) or 0,
            tokens_out=getattr(usage, "completion_tokens", 0) or 0,
        )


def model_handle_for(model: str) -> LiteLLMModelHandle:
    """Factory: a ModelHandle for any provider/model string."""
    return LiteLLMModelHandle(model)
