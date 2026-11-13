import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import evaluate  # noqa: E402


def test_offline_harness_passes_all_cases():
    results = evaluate.run_all(live=False)
    failed = [(n, d) for n, (ok, d, _) in results if not ok]
    assert not failed, failed
    assert "Passed" in evaluate.format_table(results)
