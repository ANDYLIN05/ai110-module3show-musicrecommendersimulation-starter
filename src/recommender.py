import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    genre: str
    mood: str
    energy: float
    artist: str = ""

def explain_song(user_prefs: UserProfile, song: Song) -> str:
    parts = []
    if song.genre.lower() == user_prefs.genre.lower():
        parts.append(f"matches your genre ({song.genre})")
    if song.mood.lower() == user_prefs.mood.lower():
        parts.append(f"matches your mood ({song.mood})")
    if abs(user_prefs.energy - song.energy) <= 0.2:
        parts.append(f"energy level is close to your target ({song.energy:.2f})")
    if user_prefs.artist and song.artist.lower() == user_prefs.artist.lower():
        parts.append(f"by your artist ({song.artist})")
    if not parts:
        return f"'{song.title}' by {song.artist} is a general recommendation."
    return f"'{song.title}' by {song.artist}: {', '.join(parts)}."


def score_song(user_prefs: UserProfile, song: Song) -> float:
    """
    Scores a song against user preferences.
    score = (genre match × 0.35) + (mood match × 0.30)
          + (1 - |target_energy - song.energy|) × 0.25
          + (artist match × 0.10)
    """
    genre_match = 1.0 if song.genre.lower() == user_prefs.genre.lower() else 0.0
    mood_match = 1.0 if song.mood.lower() == user_prefs.mood.lower() else 0.0
    energy_score = max(0.0, 1.0 - abs(user_prefs.energy - song.energy))
    artist_match = 1.0 if user_prefs.artist and song.artist.lower() == user_prefs.artist.lower() else 0.0

    return (genre_match * 0.35) + (mood_match * 0.30) + (energy_score * 0.25) + (artist_match * 0.10)


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = sorted(self.songs, key=lambda s: score_song(user, s), reverse=True)
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        return explain_song(user, song)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    user = UserProfile(
        genre=user_prefs.get("genre", ""),
        mood=user_prefs.get("mood", ""),
        energy=float(user_prefs.get("energy", 0.5)),
        artist=user_prefs.get("artist", ""),
    )
    song_objects = [
        Song(
            id=int(s.get("id", 0)),
            title=s.get("title", ""),
            artist=s.get("artist", ""),
            genre=s.get("genre", ""),
            mood=s.get("mood", ""),
            energy=float(s.get("energy", 0.5)),
            tempo_bpm=float(s.get("tempo_bpm", 0)),
            valence=float(s.get("valence", 0)),
            danceability=float(s.get("danceability", 0)),
            acousticness=float(s.get("acousticness", 0)),
        )
        for s in songs
    ]
    scored = sorted(
        ((orig, s, score_song(user, s)) for orig, s in zip(songs, song_objects)),
        key=lambda t: t[2],
        reverse=True,
    )
    return [(orig, sc, explain_song(user, s)) for orig, s, sc in scored[:k]]
