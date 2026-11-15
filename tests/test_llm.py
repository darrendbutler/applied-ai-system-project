"""Tests for the Gemini wrapper's error handling and throttling (no network)."""
import sys
import types

import pytest

from src import llm


class FakeErr(Exception):
    def __init__(self, code):
        super().__init__(f"err {code}")
        self.code = code


def _install_fake_genai(monkeypatch, codes):
    calls = {"n": 0}

    class Models:
        def generate_content(self, **_):
            i = calls["n"]
            calls["n"] += 1
            if i < len(codes):
                raise FakeErr(codes[i])
            return types.SimpleNamespace(text=" ok ")

    class Client:
        def __init__(self, **_):
            self.models = Models()

    genai = types.ModuleType("google.genai")
    genai.Client = Client
    genai.types = types.SimpleNamespace(
        HttpOptions=lambda **k: None, GenerateContentConfig=lambda **k: None)
    google = types.ModuleType("google")
    google.genai = genai
    monkeypatch.setitem(sys.modules, "google", google)
    monkeypatch.setitem(sys.modules, "google.genai", genai)
    monkeypatch.setitem(sys.modules, "google.genai.types", genai.types)
    monkeypatch.setenv("GEMINI_API_KEY", "k")
    monkeypatch.setattr(llm, "load_dotenv", lambda: None)
    monkeypatch.setattr(llm.time, "sleep", lambda s: None)
    return calls


def test_non_retryable_error_fails_fast(monkeypatch):
    calls = _install_fake_genai(monkeypatch, [404, 404, 404])
    with pytest.raises(llm.LLMError):
        llm.generate("x", retries=2)
    assert calls["n"] == 1


def test_rate_limit_is_retried(monkeypatch):
    calls = _install_fake_genai(monkeypatch, [429])
    assert llm.generate("x", retries=2) == "ok"
    assert calls["n"] == 2
