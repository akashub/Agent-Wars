from types import SimpleNamespace

import agentwars.live.llm_provider as prov
from agentwars.protocols import ModelResponse


def test_litellm_handle_maps_openai_shaped_response(monkeypatch):
    def fake_completion(model, messages, max_tokens):
        assert model == "gpt-4o-mini"
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="hello"))],
            usage=SimpleNamespace(prompt_tokens=12, completion_tokens=7),
        )
    monkeypatch.setattr(prov, "completion", fake_completion)
    r = prov.model_handle_for("gpt-4o-mini").complete(
        [{"role": "user", "content": "hi"}], max_tokens=50
    )
    assert isinstance(r, ModelResponse)
    assert r.text == "hello" and r.tokens_in == 12 and r.tokens_out == 7
