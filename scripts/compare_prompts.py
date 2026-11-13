"""Compare baseline vs. specialized prompts on 5 fixed questions (and 3 playlist descriptions).

Metrics per style:
  words        mean answer length in words (RAG) / mean reason length (agent)
  cite_rate    share of answers with at least one verified citation
  review_rate  share of answers citing at least one review (RAG only)
  grounded     mean share of sentences that carry a citation (RAG) / share of reasons that mention a
               review snippet or score (agent)

Usage:
    python scripts/compare_prompts.py          # offline stub: smoke test only, styles will look identical
    python scripts/compare_prompts.py --live   # real Gemini calls; the numbers worth recording
    # Default is ~16 calls (5 RAG questions x 2 styles + 1 playlist x 2 styles). Fit a small quota with
    # --questions N and --agent-prompts N (0 skips the agent).
"""
import argparse
import re
import sys
from pathlib import Path
from typing import Callable, Dict, List

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate import AGENT_PROMPTS, stub_generate  # noqa: E402
from src import llm, prompts  # noqa: E402
from src.agent import PlaylistAgent  # noqa: E402
from src.rag import answer_question  # noqa: E402
from src.retriever import Retriever  # noqa: E402

QUESTIONS = [
    "Which lofi songs are described as good for studying?",
    "What do reviewers say about the high-energy songs?",
    "Is there a calm acoustic song for winding down?",
    "Which songs are best for a workout?",
    "What does the glossary say about the chill mood?",
]
_CITE = re.compile(r"\[(?:song|review|glossary):[a-z0-9-]+\]")


def _sentences(text: str) -> List[str]:
    return [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]


def rag_metrics(style: str, retriever, generate, questions: List[str] = QUESTIONS) -> Dict[str, float]:
    results = [answer_question(q, retriever, generate, style=style) for q in questions]
    ok = [r for r in results if r.status == "ok"]
    n = len(results)
    grounded = [sum(bool(_CITE.search(s)) for s in _sentences(r.answer)) / max(1, len(_sentences(r.answer)))
                for r in ok]
    return {
        "answered": len(ok) / n,
        "words": sum(len(r.answer.split()) for r in ok) / max(1, len(ok)),
        "cite_rate": sum(bool(r.citations) for r in ok) / n,
        "review_rate": sum(any(c.startswith("review:") for c in r.citations) for r in ok) / n,
        "grounded": sum(grounded) / max(1, len(grounded)),
    }


def agent_metrics(style: str, generate, prompts_: List[str] = AGENT_PROMPTS) -> Dict[str, float]:
    lengths: List[int] = []
    grounded: List[bool] = []
    for prompt in prompts_:
        agent = PlaylistAgent(generate=generate, trace_path=None, style=style)
        for t in agent.build_playlist(prompt).tracks:
            reason = t["reason"]
            lengths.append(len(reason.split()))
            grounded.append(bool(re.search(r"review|\"|score|\d", reason, re.IGNORECASE)))
    return {"words": sum(lengths) / max(1, len(lengths)), "grounded": sum(grounded) / max(1, len(grounded))}


def format_report(rag: Dict[str, Dict], agent: Dict[str, Dict]) -> str:
    lines = ["RAG (fixed questions)", f"{'style':<12}{'answered':>9}{'words':>8}{'cite':>7}{'review':>8}{'grounded':>10}"]
    for s, m in rag.items():
        lines.append(f"{s:<12}{m['answered']:>9.0%}{m['words']:>8.1f}{m['cite_rate']:>7.0%}"
                     f"{m['review_rate']:>8.0%}{m['grounded']:>10.0%}")
    if not agent:
        return "\n".join(lines)
    lines += ["", "Agent (track reasons)", f"{'style':<12}{'words':>8}{'grounded':>10}"]
    for s, m in agent.items():
        lines.append(f"{s:<12}{m['words']:>8.1f}{m['grounded']:>10.0%}")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--live", action="store_true", help="use real Gemini calls (needs GEMINI_API_KEY)")
    ap.add_argument("--questions", type=int, default=len(QUESTIONS), help="RAG questions per style (1 call each)")
    ap.add_argument("--agent-prompts", type=int, default=1,
                    help="playlist descriptions per style (~3 calls each; 0 skips the agent comparison)")
    args = ap.parse_args(argv)
    questions, agent_prompts = QUESTIONS[:args.questions], AGENT_PROMPTS[:args.agent_prompts]
    generate: Callable[..., str] = llm.generate if args.live else stub_generate
    retriever = Retriever.from_data()
    try:
        rag = {s: rag_metrics(s, retriever, generate, questions) for s in prompts.STYLES}
        agent = {s: agent_metrics(s, generate, agent_prompts) for s in prompts.STYLES} if agent_prompts else {}
    except llm.LLMError as e:
        print(f"LLM unavailable: {e}")
        return 1
    print(f"Mode: {'live Gemini' if args.live else 'offline stub LLM (styles are NOT distinguishable here)'}\n")
    print(format_report(rag, agent))
    return 0


if __name__ == "__main__":
    sys.exit(main())
