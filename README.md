# 🎵 Music Recommender Simulation

## Project Summary

Goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This system takes a user's preferred genre, mood, and energy level and scores every song in a 20-track catalog using a weighted formula. It then returns the top 5 songs ranked by how closely they match the user's taste profile. The scoring weighs genre match most heavily, followed by mood, energy proximity, and artist preference.

---

## How The System Works

- What features does each `Song` use in your system
  Categorical: genre, mood, artist, title
  Numerical (0–1 scale): energy, valence, danceability, acousticness
  Numerical (raw): tempo_bpm

- What information does your `UserProfile` store
  genre: the genre they want matched (e.g. "lofi")
  mood: the mood they want matched (e.g. "chill")
  energy: a float (0–1) representing their desired intensity level
  artist: all music associated with that artist

- How does your `Recommender` compute a score for each song
  score = (genre match × 0.35) + (mood match  × 0.30) + (1 - |target_energy - song.energy|) × 0.25 + (artist match × 0.10)

- How do you choose which songs to recommend
  Score every song using the formula above
  Sort all songs by score descending
  Return the top k (default 5)

  [UML Design](uml_design.md)
---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried


- What happened when you changed the weight on genre from 2.0 to 0.5
  When the genre weight was lowered, songs from non-matching genres started climbing into the top results because mood and energy alone were enough to push them up. This showed how dominant genre is in shaping recommendations when it carries the most weight.

- What happened when you added tempo or valence to the score
  Adding valence caused songs with high happiness scores like "Sunrise City" and "Summer Parade" to rank higher for happy mood users. However, it also introduced noise for users whose mood preference did not map cleanly onto valence values, making some results feel less accurate.

- How did your system behave for different types of users
  A chill lofi user consistently received LoRoom and Paper Lanterns songs at the top, while an intense rock user saw Voltline tracks dominate every time. A user with niche preferences like jazz-relaxed received lower overall scores simply because fewer catalog songs matched both genre and mood simultaneously.

---

## Limitations and Risks

- It only works on a tiny catalog
  With only 20 songs, users who prefer niche genres like jazz or ambient have very few matching candidates, which means the top results may feel forced even when the scores look reasonable.

- It does not understand lyrics or language
  The system only scores songs based on numeric and categorical tags like genre, mood, and energy, so two songs can receive the same score even if they sound completely different to a real listener.

- It might over favor one genre or mood
  Because genre carries the highest weight at 35%, a user whose genre matches several songs will consistently see those songs bubble up regardless of whether the mood or energy is actually a good fit.

---

## Reflection

[**Model Card**](model_card.md)

- About how recommenders turn data into predictions
  Building this system made it clear that a recommender is really just a scoring machine, it converts messy human preferences into numbers, applies a formula, and returns whatever ranks highest. The tricky part is choosing what to measure and how much each factor should matter, because those weight decisions quietly shape every result the user ever sees.

- About where bias or unfairness could show up in systems like this
  The biggest source of bias I noticed is catalog representation: genres like lofi and pop had multiple songs while jazz had only two, so users who prefer jazz will almost always get weaker recommendations through no fault of their own. The fixed weights also assume everyone cares about genre more than mood, but that assumption may not hold for every listener, meaning the system is quietly built around one type of user.
