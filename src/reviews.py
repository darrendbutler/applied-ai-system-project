"""Song review loading and simple aggregation helpers."""
import csv
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_REVIEWS_PATH = Path(__file__).resolve().parent.parent / "data" / "reviews.csv"


def load_reviews(csv_path: str = str(DEFAULT_REVIEWS_PATH)) -> List[Dict]:
    """Load reviews from CSV, converting ids and rating to int."""
    reviews: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            reviews.append({
                "review_id": int(row["review_id"]),
                "song_id": int(row["song_id"]),
                "reviewer": row["reviewer"],
                "rating": int(row["rating"]),
                "text": row["text"],
            })
    return reviews


def reviews_for_song(song_id: int, reviews: List[Dict]) -> List[Dict]:
    """Return all reviews for one song."""
    return [r for r in reviews if r["song_id"] == song_id]


def avg_rating(song_id: int, reviews: List[Dict]) -> Optional[float]:
    """Mean rating for a song, or None if it has no reviews."""
    ratings = [r["rating"] for r in reviews if r["song_id"] == song_id]
    return sum(ratings) / len(ratings) if ratings else None
