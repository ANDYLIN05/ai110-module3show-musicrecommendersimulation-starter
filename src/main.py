"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("../data/songs.csv") 

    print(f"Loaded songs: {len(songs)}")
    print() 
    
    profiles = [
        {"name": "Pop Fan",      "genre": "pop",        "mood": "happy",    "energy": 0.8},
        {"name": "Rock Head",    "genre": "rock",       "mood": "energetic","energy": 0.9},
        {"name": "Chill Vibes",  "genre": "lo-fi",      "mood": "calm",     "energy": 0.3},
        {"name": "Jazz Lover",   "genre": "jazz",       "mood": "romantic", "energy": 0.5},
    ]

    for profile in profiles:
        print(f"\n=== {profile['name']} ===")
        recommendations = recommend_songs(profile, songs, k=5)
        for song, score, explanation in recommendations:
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
