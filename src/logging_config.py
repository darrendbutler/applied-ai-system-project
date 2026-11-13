"""Central logging setup: console + rotating file at logs/app.log, with secrets redacted."""
import logging
import os
import re
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_FILE = LOG_DIR / "app.log"
FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"

# Google API keys look like AIza...; also catch key=... / api_key: ... patterns.
_KEY_PATTERNS = [
    re.compile(r"AIza[0-9A-Za-z_\-]{20,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret)(['\"]?\s*[=:]\s*['\"]?)[^\s'\",]+"),
]


class RedactSecretsFilter(logging.Filter):
    """Scrub API keys (and the live GEMINI_API_KEY value) from every log record."""

    def _scrub(self, text: str) -> str:
        key = os.getenv("GEMINI_API_KEY")
        if key:
            text = text.replace(key, "[REDACTED]")
        text = _KEY_PATTERNS[0].sub("[REDACTED]", text)
        return _KEY_PATTERNS[1].sub(lambda m: f"{m.group(1)}{m.group(2)}[REDACTED]", text)

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = self._scrub(record.getMessage())
        record.args = ()
        return True


def setup_logging(level: int = logging.INFO, log_file: Path = LOG_FILE) -> None:
    """Configure the root logger once (idempotent). Safe to call from every entry point."""
    root = logging.getLogger()
    if getattr(root, "_selecta_configured", False):
        return
    root.setLevel(level)
    formatter = logging.Formatter(FORMAT)
    redact = RedactSecretsFilter()

    handlers = [logging.StreamHandler()]
    try:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        handlers.append(RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3, encoding="utf-8"))
    except OSError:
        pass  # console-only logging if the file isn't writable
    for h in handlers:
        h.setFormatter(formatter)
        h.addFilter(redact)
        root.addHandler(h)
    # Quiet noisy HTTP client loggers that may include URLs with keys.
    for noisy in ("httpx", "httpcore", "google_genai"):
        logging.getLogger(noisy).setLevel(logging.WARNING)
    root._selecta_configured = True
