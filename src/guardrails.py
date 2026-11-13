"""Input validation for user questions (output checks are added in later phases)."""
import re
from typing import Tuple

MAX_QUESTION_CHARS = 500

_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")
_INJECTION_PATTERNS = [
    r"ignore (all |any |the )?(previous|prior|above|earlier)? ?(instructions|prompts?|rules)",
    r"disregard .{0,30}(instructions|rules|prompt)",
    r"(reveal|show|print|leak).{0,30}(api key|system prompt|secret|password)",
    r"you are now ",
    r"system prompt",
]
_INJECTION_RE = re.compile("|".join(_INJECTION_PATTERNS), re.IGNORECASE)


def validate_question(question: str) -> Tuple[bool, str]:
    """Return (ok, cleaned_question_or_reason). Strips control characters first."""
    if not isinstance(question, str):
        return False, "Question must be text."
    cleaned = _CONTROL_CHARS.sub("", question).strip()
    if not cleaned:
        return False, "Please enter a question."
    if len(cleaned) > MAX_QUESTION_CHARS:
        return False, f"Question is too long (max {MAX_QUESTION_CHARS} characters)."
    if _INJECTION_RE.search(cleaned):
        return False, "That request looks like an attempt to override my instructions, so I can't help with it."
    return True, cleaned


def verify_citations(citations, allowed) -> bool:
    """Output check: an answer must cite at least one source and only sources that were retrieved."""
    return bool(citations) and all(c in allowed for c in citations)
