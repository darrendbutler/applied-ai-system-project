"""TF-IDF retriever over songs, reviews and a genre/mood glossary."""
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.recommender import load_songs
from src.reviews import load_reviews

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@dataclass(frozen=True)
class Document:
    """A retrievable passage. `source` is the citation id, e.g. song:12, review:34, glossary:lofi."""
    source: str
    kind: str
    text: str


def song_to_text(song: Dict) -> str:
    """Render a song's metadata and features as natural-language sentences."""
    return (
        f"{song['title']} by {song['artist']} is a {song['mood']} {song['genre']} song. "
        f"Energy {song['energy']:.2f}, valence {song['valence']:.2f}, "
        f"danceability {song['danceability']:.2f}, acousticness {song['acousticness']:.2f}, "
        f"tempo {song['tempo_bpm']:.0f} BPM."
    )


def load_glossary(path: Path) -> List[Document]:
    """Split a markdown glossary into one document per '## heading' section."""
    docs: List[Document] = []
    text = Path(path).read_text(encoding="utf-8")
    for block in re.split(r"^## ", text, flags=re.MULTILINE)[1:]:
        heading, _, body = block.partition("\n")
        heading, body = heading.strip(), body.strip()
        if not body:
            continue
        slug = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")
        docs.append(Document(f"glossary:{slug}", "glossary", f"{heading}. {body}"))
    return docs


def build_documents(songs: List[Dict], reviews: List[Dict], glossary: List[Document]) -> List[Document]:
    """Build the multi-source corpus. Review text is prefixed with its song title for context."""
    titles = {s["id"]: s["title"] for s in songs}
    docs = [Document(f"song:{s['id']}", "song", song_to_text(s)) for s in songs]
    for r in reviews:
        text = (f"Review of {titles.get(r['song_id'], 'unknown song')} "
                f"(rated {r['rating']}/5 by {r['reviewer']}): {r['text']}")
        docs.append(Document(f"review:{r['review_id']}", "review", text))
    return docs + glossary


class Retriever:
    """TF-IDF + cosine similarity search. Swap this class for an embedding retriever with the same API."""

    def __init__(self, documents: List[Document]):
        if not documents:
            raise ValueError("Retriever needs at least one document")
        self.documents = documents
        self._vectorizer = TfidfVectorizer(stop_words="english", sublinear_tf=True, ngram_range=(1, 2))
        self._matrix = self._vectorizer.fit_transform(d.text for d in documents)

    @classmethod
    def from_data(cls, data_dir: Optional[Path] = None) -> "Retriever":
        d = Path(data_dir) if data_dir else DATA_DIR
        songs = load_songs(str(d / "songs.csv"))
        reviews = load_reviews(str(d / "reviews.csv"))
        glossary = load_glossary(d / "glossary.md")
        return cls(build_documents(songs, reviews, glossary))

    def search(self, query: str, k: int = 5) -> List[Tuple[Document, float]]:
        """Return up to k (document, score) pairs, best first, excluding zero-score matches."""
        scores = cosine_similarity(self._vectorizer.transform([query]), self._matrix)[0]
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [(self.documents[i], float(scores[i])) for i in ranked if scores[i] > 0]
