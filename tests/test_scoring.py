import pytest

from src.recommender import WEIGHTS, load_songs, recommend_songs, score_song

PROFILE = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "target_valence": 0.58,
    "target_danceability": 0.60,
    "target_acousticness": 0.75,
    "target_tempo": 0.22,
}


def make_song(**overrides):
    song = {
        "id": 1, "title": "T", "artist": "A", "genre": "lofi", "mood": "chill",
        "energy": 0.40, "tempo_bpm": 60 + 0.22 * 92, "valence": 0.58,
        "danceability": 0.60, "acousticness": 0.75,
    }
    song.update(overrides)
    return song


def test_weights_sum_to_100():
    assert sum(WEIGHTS.values()) == pytest.approx(100.0)


def test_load_songs_converts_types():
    songs = load_songs("data/songs.csv")
    assert len(songs) == 20
    first = songs[0]
    assert isinstance(first["id"], int)
    for field in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
        assert isinstance(first[field], float)
    assert len({s["id"] for s in songs}) == len(songs)


def test_perfect_match_scores_100():
    score, reasons = score_song(PROFILE, make_song())
    assert score == pytest.approx(100.0)
    assert any(r.startswith("mood match") for r in reasons)
    assert any(r.startswith("genre match") for r in reasons)


def test_mood_and_genre_mismatch_lose_their_bonus():
    full, _ = score_song(PROFILE, make_song())
    score, reasons = score_song(PROFILE, make_song(mood="happy", genre="pop"))
    assert score == pytest.approx(full - WEIGHTS["mood"] - WEIGHTS["genre"])
    assert not any("match" in r for r in reasons)


def test_closer_energy_scores_higher():
    near, _ = score_song(PROFILE, make_song(energy=0.45))
    far, _ = score_song(PROFILE, make_song(energy=0.95))
    assert near > far


def test_recommend_songs_ranked_and_limited():
    songs = load_songs("data/songs.csv")
    results = recommend_songs(PROFILE, songs, k=5)
    assert len(results) == 5
    scores = [score for _, score, _ in results]
    assert scores == sorted(scores, reverse=True)
    assert results[0][0]["genre"] == "lofi"
    assert results[0][2]  # explanation is non-empty


def test_recommend_songs_tie_breaks_on_title():
    a = make_song(id=1, title="Alpha")
    b = make_song(id=2, title="Beta")
    results = recommend_songs(PROFILE, [b, a], k=2)
    assert [r[0]["title"] for r in results] == ["Alpha", "Beta"]
