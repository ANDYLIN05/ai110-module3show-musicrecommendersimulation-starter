import pytest
from src.recommender import Song, UserProfile, Recommender, score_song


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_song(**overrides) -> Song:
    defaults = dict(
        id=1, title="Default Track", artist="Default Artist",
        genre="pop", mood="happy", energy=0.8,
        tempo_bpm=120, valence=0.7, danceability=0.7, acousticness=0.2,
    )
    defaults.update(overrides)
    return Song(**defaults)


def make_user(**overrides) -> UserProfile:
    defaults = dict(genre="pop", mood="happy", energy=0.8, artist="")
    defaults.update(overrides)
    return UserProfile(**defaults)


# ── Energy edge cases ─────────────────────────────────────────────────────────

def test_negative_energy_score_does_not_crash():
    """Negative energy should not raise an exception."""
    user = make_user(energy=-0.5)
    song = make_song(energy=0.8)
    result = score_song(user, song)
    assert isinstance(result, float)


def test_negative_energy_score_clamps_to_zero():
    """Energy difference > 1.0 should produce 0, not a negative contribution."""
    user = make_user(energy=-0.5)   # diff from 0.8 = 1.3 → would be negative without clamp
    song = make_song(energy=0.8)
    result = score_song(user, song)
    assert result >= 0.0


def test_energy_above_one_does_not_go_negative():
    """Energy > 1.0 should also be clamped at 0."""
    user = make_user(energy=1.8)
    song = make_song(energy=0.0)
    result = score_song(user, song)
    assert result >= 0.0


def test_energy_exact_match_gives_full_energy_weight():
    """When energy matches exactly the energy component should contribute 0.25."""
    user = make_user(genre="other", mood="other", energy=0.5, artist="")
    song = make_song(genre="other", mood="other", energy=0.5)
    result = score_song(user, song)
    # genre 0.35 + mood 0.30 + energy 0.25 + artist 0.0 = 0.90
    assert abs(result - 0.90) < 1e-9


# ── k edge cases ─────────────────────────────────────────────────────────────

def test_k_larger_than_catalog_returns_all_songs():
    """Asking for more songs than exist should return the full catalog."""
    songs = [make_song(id=i, title=f"Song {i}") for i in range(3)]
    rec = Recommender(songs)
    results = rec.recommend(make_user(), k=100)
    assert len(results) == 3


def test_k_zero_returns_empty_list():
    songs = [make_song()]
    rec = Recommender(songs)
    results = rec.recommend(make_user(), k=0)
    assert results == []


def test_empty_catalog_returns_empty_list():
    rec = Recommender([])
    results = rec.recommend(make_user(), k=5)
    assert results == []


# ── Case insensitivity ────────────────────────────────────────────────────────

def test_genre_match_is_case_insensitive():
    user = make_user(genre="POP")
    song = make_song(genre="pop")
    song2 = make_song(genre="lofi", id=2, title="Lofi Track")
    rec = Recommender([song, song2])
    results = rec.recommend(user, k=2)
    assert results[0].genre == "pop"


def test_mood_match_is_case_insensitive():
    user = make_user(mood="HAPPY")
    song = make_song(mood="happy")
    result = score_song(user, song)
    # mood component should still contribute 0.30
    assert result > 0.30


def test_artist_match_is_case_insensitive():
    user = make_user(artist="Taylor Swift")
    song = make_song(artist="taylor swift")
    result = score_song(user, song)
    # artist component should contribute 0.10
    assert result >= 0.10


# ── Artist edge cases ─────────────────────────────────────────────────────────

def test_no_artist_preference_gives_zero_artist_score():
    user = make_user(artist="")
    song = make_song(artist="Any Artist")
    result = score_song(user, song)
    # artist match should not add anything
    user_with_artist = make_user(artist="Any Artist")
    result_with_artist = score_song(user_with_artist, song)
    assert result_with_artist - result == pytest.approx(0.10)


# ── Scoring correctness ───────────────────────────────────────────────────────

def test_perfect_match_scores_one():
    user = make_user(genre="pop", mood="happy", energy=0.8, artist="Default Artist")
    song = make_song(genre="pop", mood="happy", energy=0.8, artist="Default Artist")
    result = score_song(user, song)
    assert result == pytest.approx(1.0)


def test_no_match_scores_near_zero():
    """A song that matches nothing should score close to 0."""
    user = make_user(genre="pop", mood="happy", energy=0.0, artist="Artist A")
    song = make_song(genre="jazz", mood="sad", energy=1.0, artist="Artist B")
    result = score_song(user, song)
    # energy diff = 1.0 → clamped to 0, all others miss → score = 0
    assert result == pytest.approx(0.0)


def test_ranking_order_is_correct():
    """The song that better matches the user should rank first."""
    good = make_song(id=1, title="Good Match", genre="pop", mood="happy", energy=0.8)
    bad  = make_song(id=2, title="Bad Match",  genre="jazz", mood="sad",  energy=0.0)
    rec  = Recommender([bad, good])   # intentionally reversed order
    results = rec.recommend(make_user(), k=2)
    assert results[0].title == "Good Match"


def test_ties_still_return_k_songs():
    """Songs with identical scores should still return k results."""
    songs = [make_song(id=i, title=f"Song {i}") for i in range(5)]
    rec = Recommender(songs)
    results = rec.recommend(make_user(), k=3)
    assert len(results) == 3


# ── Explanation edge cases ────────────────────────────────────────────────────

def test_explain_song_no_match_returns_general_recommendation():
    user = make_user(genre="pop", mood="happy", energy=0.0, artist="")
    song = make_song(genre="jazz", mood="sad", energy=0.5)
    rec = Recommender([song])
    explanation = rec.explain_recommendation(user, song)
    assert "general recommendation" in explanation.lower()


def test_explain_song_full_match_mentions_all_factors():
    user = make_user(genre="pop", mood="happy", energy=0.8, artist="Default Artist")
    song = make_song(genre="pop", mood="happy", energy=0.8, artist="Default Artist")
    rec = Recommender([song])
    explanation = rec.explain_recommendation(user, song)
    assert "genre" in explanation.lower()
    assert "mood" in explanation.lower()
    assert "energy" in explanation.lower()
    assert "artist" in explanation.lower()
