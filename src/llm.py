"""Thin wrapper around the Gemini API so every LLM call goes through one mockable place."""
import logging
import os
import time
from typing import Optional

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gemini-3.8-flash"  # gemini-2.5-flash is no longer available to new users


class LLMError(RuntimeError):
    """Raised when the LLM cannot produce a response (missing key, API failure)."""


def generate(prompt: str, system: Optional[str] = None, retries: int = 2,
             timeout_s: float = 30.0) -> str:
    """Send a prompt to Gemini and return the text, retrying with backoff on failure."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise LLMError("GEMINI_API_KEY is not set")

    from google import genai
    from google.genai import types

    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=int(timeout_s * 1000)),
    )
    config = types.GenerateContentConfig(system_instruction=system, temperature=0.2)

    last_err: Optional[Exception] = None
    for attempt in range(retries + 1):
        start = time.time()
        try:
            resp = client.models.generate_content(model=model, contents=prompt, config=config)
            logger.info("llm ok model=%s latency=%.2fs", model, time.time() - start)
            return (resp.text or "").strip()
        except Exception as e:  # SDK raises various error types
            last_err = e
            logger.warning("llm error attempt=%d: %s", attempt + 1, type(e).__name__)
            if attempt < retries:
                time.sleep(2 ** attempt)
    raise LLMError(f"Gemini call failed: {type(last_err).__name__}") from last_err
