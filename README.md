# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This system takes a user's preferred genre, mood, and energy level and scores every song in a 20-track catalog using a weighted formula. It then returns the top 5 songs ranked by how closely they match the user's taste profile. The scoring weighs genre match most heavily, followed by mood, energy proximity, and artist preference.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  Categorical: genre, mood, artist, title
  Numerical (0–1 scale): energy, valence, danceability, acousticness
  Numerical (raw): tempo_bpm

- What information does your `UserProfile` store
  genre: the genre they want matched (e.g. "lofi")
  mood: the mood they want matched (e.g. "chill")
  target_energy: a float (0–1) representing their desired intensity level
  artist: all music associated with that artist

- How does your `Recommender` compute a score for each song
  score = (genre match × 0.35) + (mood match  × 0.30) + (1 - |target_energy - song.energy|) × 0.25 + (artist match × 0.10)

- How do you choose which songs to recommend
  Score every song using the formula above
  Sort all songs by score descending
  Return the top k (default 5)

You can include a simple diagram or bullet list if helpful.
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
  Adding valence caused songs with high happiness scores like "Sunrise City" and "Summer Parade" to rank higher for happy-mood users. However, it also introduced noise for users whose mood preference did not map cleanly onto valence values, making some results feel less accurate.

- How did your system behave for different types of users
  A chill lofi user consistently received LoRoom and Paper Lanterns songs at the top, while an intense rock user saw Voltline tracks dominate every time. A user with niche preferences like jazz-relaxed received lower overall scores simply because fewer catalog songs matched both genre and mood simultaneously.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
  With only 20 songs, users who prefer niche genres like jazz or ambient have very few matching candidates, which means the top results may feel forced even when the scores look reasonable.

- It does not understand lyrics or language
  The system only scores songs based on numeric and categorical tags like genre, mood, and energy, so two songs can receive the same score even if they sound completely different to a real listener.

- It might over favor one genre or mood
  Because genre carries the highest weight at 35%, a user whose genre matches several songs will consistently see those songs bubble up regardless of whether the mood or energy is actually a good fit.

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
  Building this system made it clear that a recommender is really just a scoring machine — it converts messy human preferences into numbers, applies a formula, and returns whatever ranks highest. The tricky part is choosing what to measure and how much each factor should matter, because those weight decisions quietly shape every result the user ever sees.

- about where bias or unfairness could show up in systems like this
  The biggest source of bias I noticed is catalog representation: genres like lofi and pop had multiple songs while jazz had only two, so users who prefer jazz will almost always get weaker recommendations through no fault of their own. The fixed weights also assume everyone cares about genre more than mood, but that assumption may not hold for every listener, meaning the system is quietly built around one type of user.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

