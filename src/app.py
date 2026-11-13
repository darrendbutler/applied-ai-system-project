"""Streamlit UI. Thin layer: all logic lives in rag.py, agent.py, reviews.py and recommender.py.

Run with: streamlit run src/app.py
"""
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st  # noqa: E402

from src.agent import PlaylistAgent  # noqa: E402
from src.logging_config import setup_logging  # noqa: E402
from src.rag import answer_question  # noqa: E402
from src.recommender import load_songs  # noqa: E402
from src.retriever import Retriever  # noqa: E402
from src.reviews import avg_rating, load_reviews, reviews_for_song  # noqa: E402

setup_logging()
logger = logging.getLogger(__name__)

DATA_DIR = ROOT / "data"
FEEDBACK_PATH = ROOT / "logs" / "feedback.jsonl"


@st.cache_data
def get_songs():
    return load_songs(str(DATA_DIR / "songs.csv"))


@st.cache_data
def get_reviews():
    return load_reviews(str(DATA_DIR / "reviews.csv"))


@st.cache_resource
def get_retriever():
    return Retriever.from_data()


def save_feedback(kind: str, query: str, rating: str) -> None:
    """Append human feedback (thumbs up/down) to logs/feedback.jsonl."""
    try:
        FEEDBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
        record = {"time": datetime.now(timezone.utc).isoformat(), "kind": kind, "query": query, "rating": rating}
        with open(FEEDBACK_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        logger.info("feedback kind=%s rating=%s", kind, rating)
    except OSError as e:
        logger.warning("could not save feedback: %s", e)


def render_library() -> None:
    songs, reviews = get_songs(), get_reviews()
    rows = [{"id": s["id"], "title": s["title"], "artist": s["artist"], "genre": s["genre"], "mood": s["mood"],
             "avg rating": round(avg_rating(s["id"], reviews), 1) if avg_rating(s["id"], reviews) else None,
             "# reviews": len(reviews_for_song(s["id"], reviews))} for s in songs]

    c1, c2 = st.columns(2)
    genres = c1.multiselect("Genre", sorted({r["genre"] for r in rows}))
    moods = c2.multiselect("Mood", sorted({r["mood"] for r in rows}))
    filtered = [r for r in rows if (not genres or r["genre"] in genres) and (not moods or r["mood"] in moods)]
    st.dataframe(filtered, use_container_width=True, hide_index=True)

    if not filtered:
        st.info("No songs match those filters.")
        return
    labels = {f"{r['title']} - {r['artist']}": r["id"] for r in filtered}
    choice = st.selectbox("Song details", list(labels))
    song_id = labels[choice]
    song = next(s for s in songs if s["id"] == song_id)
    st.markdown(f"**{song['title']}** by {song['artist']} ({song['genre']}, {song['mood']})")
    st.caption(f"energy {song['energy']} | tempo {song['tempo_bpm']:.0f} bpm | valence {song['valence']} | "
               f"danceability {song['danceability']} | acousticness {song['acousticness']}")
    for r in reviews_for_song(song_id, reviews):
        st.markdown(f"- {'★' * r['rating']}{'☆' * (5 - r['rating'])} **{r['reviewer']}**: {r['text']}")


def render_ask() -> None:
    st.caption("Ask questions about the songs and reviews. Answers are grounded in retrieved passages.")
    if "chat" not in st.session_state:
        st.session_state.chat = []
    for i, msg in enumerate(st.session_state.chat):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("meta"):
                render_rag_meta(msg["meta"], i)

    question = st.chat_input("e.g. Which lofi songs are good for studying?")
    if question:
        st.session_state.chat.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Searching the library..."):
                try:
                    res = answer_question(question, retriever=get_retriever())
                    meta = {"status": res.status, "citations": res.citations, "confidence": res.confidence,
                            "question": question,
                            "retrieved": [(d.source, d.text, round(s, 3)) for d, s in res.retrieved]}
                    answer = res.answer
                except Exception:  # never show a stack trace in the UI
                    logger.exception("rag failed in UI")
                    meta, answer = None, "Sorry, something went wrong. Please try again."
            st.markdown(answer)
            idx = len(st.session_state.chat)
            if meta:
                render_rag_meta(meta, idx)
        st.session_state.chat.append({"role": "assistant", "content": answer, "meta": meta})


def render_rag_meta(meta: dict, idx: int) -> None:
    if meta["status"] == "ok":
        st.caption(f"Confidence: {meta['confidence']:.2f} | Citations: {', '.join(meta['citations']) or 'none'}")
    elif meta["status"] != "blocked":
        st.caption(f"Status: {meta['status']}")
    if meta["retrieved"]:
        with st.expander("Retrieved passages"):
            for source, text, score in meta["retrieved"]:
                st.markdown(f"`{source}` (score {score}): {text}")
    if meta["status"] == "ok":
        feedback_buttons("rag", meta["question"], f"rag{idx}")


def feedback_buttons(kind: str, query: str, key: str) -> None:
    c1, c2, _ = st.columns([1, 1, 8])
    if c1.button("👍", key=f"{key}_up"):
        save_feedback(kind, query, "up")
        st.toast("Thanks for the feedback!")
    if c2.button("👎", key=f"{key}_down"):
        save_feedback(kind, query, "down")
        st.toast("Thanks for the feedback!")


def render_playlist() -> None:
    st.caption("Describe what you want to listen to and the agent will build a playlist.")
    with st.form("playlist_form"):
        description = st.text_area("Describe your playlist", placeholder="rainy Sunday studying, no vocals, 45 min")
        submitted = st.form_submit_button("Build playlist")
    if submitted:
        with st.spinner("Agent is planning, searching and checking..."):
            try:
                st.session_state.playlist = PlaylistAgent().build_playlist(description)
            except Exception:
                logger.exception("agent failed in UI")
                st.session_state.playlist = None
                st.error("Sorry, something went wrong. Please try again.")

    result = st.session_state.get("playlist")
    if not result:
        return
    if result.status in ("blocked", "error"):
        st.warning(result.message)
        return
    if result.status == "partial":
        st.warning(result.message)
    st.subheader("Your playlist")
    for i, t in enumerate(result.tracks, 1):
        s = t["song"]
        st.markdown(f"**{i}. {s['title']}** - {s['artist']} ({s['genre']}, {s['mood']})  \n{t['reason']}")
    st.caption(f"Confidence: {result.confidence:.2f} | Iterations: {result.iterations}")
    with st.expander("Agent trace"):
        st.json(result.trace)
    feedback_buttons("playlist", result.description, "playlist")


def main() -> None:
    st.set_page_config(page_title="Selecta", page_icon="🎵", layout="wide")
    st.title("🎵 Selecta")
    library, ask, playlist = st.tabs(["Library", "Ask", "Playlist Agent"])
    with library:
        render_library()
    with ask:
        render_ask()
    with playlist:
        render_playlist()


main()
