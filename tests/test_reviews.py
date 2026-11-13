import pytest

from src.recommender import load_songs
from src.reviews import avg_rating, load_reviews, reviews_for_song

SONGS_PATH = "data/songs.csv"
REVIEWS_PATH = "data/reviews.csv"


@pytest.fixture(scope="module")
def reviews():
    return load_reviews(REVIEWS_PATH)


def test_every_song_id_exists(reviews):
    song_ids = {s["id"] for s in load_songs(SONGS_PATH)}
    assert {r["song_id"] for r in reviews} <= song_ids


def test_every_song_has_reviews(reviews):
    for s in load_songs(SONGS_PATH):
        assert len(reviews_for_song(s["id"], reviews)) >= 3


def test_ratings_in_range(reviews):
    assert all(1 <= r["rating"] <= 5 for r in reviews)


def test_no_empty_text_or_reviewer(reviews):
    assert all(r["text"].strip() and r["reviewer"].strip() for r in reviews)


def test_review_ids_unique(reviews):
    ids = [r["review_id"] for r in reviews]
    assert len(ids) == len(set(ids))


def test_avg_rating(reviews):
    assert avg_rating(4, reviews) == pytest.approx((5 + 5 + 4) / 3)
    assert avg_rating(999, reviews) is None
