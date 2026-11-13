import pytest

from src import prompts
from src.agent import PlaylistAgent
from src.rag import answer_question, build_prompt
from src.retriever import Retriever


@pytest.fixture(scope="module")
def retriever():
    return Retriever.from_data()


def test_specialized_adds_persona_and_examples():
    assert len(prompts.rag_system("specialized")) > len(prompts.rag_system("baseline"))
    assert prompts.rag_fewshot("baseline") == ""
    assert prompts.rag_fewshot("specialized")
    assert "music librarian" in prompts.rag_system("specialized")  # contract the eval stub relies on


def test_unknown_style_rejected():
    with pytest.raises(ValueError):
        prompts.rag_system("weird")
    with pytest.raises(ValueError):
        PlaylistAgent(style="weird", generate=lambda *a, **k: "")


def test_rag_passes_style_to_llm(retriever):
    seen = {}

    def gen(prompt, system=None, **_):
        seen[system is not None and "at most 3 sentences" in system] = prompt
        return "Answer [song:1]."

    for style in ("baseline", "specialized"):
        answer_question("Which lofi songs are good for studying?", retriever, gen, style=style)
    assert set(seen) == {True, False}
    assert "Examples of the expected style" in seen[True]
    assert "Examples of the expected style" not in seen[False]


def test_build_prompt_baseline_has_no_examples(retriever):
    docs = retriever.search("lofi", k=2)
    assert "Examples" not in build_prompt("q", docs, "baseline")
    assert "Examples" in build_prompt("q", docs, "specialized")
