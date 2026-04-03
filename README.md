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

- About how recommenders turn data into predictions
  Building this system made it clear that a recommender is really just a scoring machine — it converts messy human preferences into numbers, applies a formula, and returns whatever ranks highest. The tricky part is choosing what to measure and how much each factor should matter, because those weight decisions quietly shape every result the user ever sees.

- About where bias or unfairness could show up in systems like this
  The biggest source of bias I noticed is catalog representation: genres like lofi and pop had multiple songs while jazz had only two, so users who prefer jazz will almost always get weaker recommendations through no fault of their own. The fixed weights also assume everyone cares about genre more than mood, but that assumption may not hold for every listener, meaning the system is quietly built around one type of user.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

  TuneSense 1.0

---

## 2. Intended Use

- What is this system trying to do
  TuneSense 1.0 scores every song in a 20-track catalog against a user's genre, mood, energy, and optional artist preference, then returns the top 5 matches ranked by score.

- Who is it for
  It is designed for classroom use to demonstrate how rule-based recommender systems work; it is not intended for real world deployment.


---

## 3. How It Works (Short Explanation)

- What features of each song does it consider
  Each song carries a genre label, a mood label, and a numeric energy level between 0 and 1 representing its intensity those three attributes do most of the scoring work.

- What information about the user does it use
  The user provides a preferred genre, a preferred mood, a target energy level, and an optional favorite artist.

- How does it turn those into a number
  Genre and mood are checked for an exact match and given either full or zero credit; energy is scored by how close the song's level is to the user's target; artist adds a small bonus if it matches all four pieces are multiplied by their weights and summed into a final score between 0 and 1.


---

## 4. Data

- How many songs are in `data/songs.csv`
  There are 20 songs in the catalog, each described by genre, mood, energy, tempo, valence, danceability, and acousticness.

- Did you add or remove any songs
  No songs were added or removed; the catalog was used exactly as provided in the starter files.

- What kinds of genres or moods are represented
  Genres include lofi, pop, rock, synthwave, ambient, jazz, and indie pop; moods include chill, happy, intense, relaxed, moody, and focused.

- Whose taste does this data mostly reflect
  The catalog skews toward electronic and Western pop styles, so listeners with those tastes will be served best while fans of classical, R&B, country, or world music will find nothing that matches.

---

## 5. Strengths

- Situations where the top results "felt right"
  A chill lofi listener reliably received "Library Rain," "Midnight Coding," and "Morning Stretch" at the top exactly the songs a human curator would pick for that profile.

- Particular user profiles it served well
  Users whose genre matches a well represented category like lofi or pop consistently got accurate, high-confidence recommendations because there were enough matching songs to fill the top 5.

- Simplicity or transparency benefits
  Because the formula is a straightforward weighted sum, it is easy to trace exactly why any song ranked where it did, which makes the system much easier to audit than a black-box model.

---

## 6. Limitations and Bias

- Does it ignore some genres or moods
  Yes genres like jazz and ambient appear in only a handful of songs, so users who prefer those styles receive low scores across most of the catalog and end up with weak top results.

- Does it treat all users as if they have the same taste shape
  The fixed weights assume genre always matters more than mood for every listener, but that is not true for everyone a user who prioritizes mood over genre will get results skewed away from their actual preference.

- Is it biased toward high energy or one genre by default
  Because pop has the most songs in the catalog, a user whose preferences loosely match pop will tend to see pop songs surface even when other genres might be a better fit.

- How could this be unfair if used in a real product
  Users with niche or underrepresented tastes would consistently receive lower quality recommendations, creating a worse experience for those who do not fit the mainstream mold the dataset was built around.

---

## 7. Evaluation

- You tried multiple user profiles and wrote down whether the results matched your expectations
  Multiple profiles were tested a chill lofi listener, a high-energy rock fan, a jazz enthusiast, and a user with a favorite artist set and the top 5 results were compared against what a human would intuitively choose.

- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
  Spotify tends to surface songs based on listening history and collaborative filtering, so it produces more diverse results than TuneSense, which can repeat the same artist multiple times in a single recommendation list.

- You wrote tests for your scoring logic
  Individual song scores were traced manually to confirm the formula computed each component correctly, and a side by side comparison of the original weights versus a mood removed version was run to observe how rankings shifted.


---

## 8. Future Work

- Add support for multiple users and "group vibe" recommendations
  Allowing multiple users to share a session and averaging their preferences would let the system recommend songs that fit a group rather than just one person.

- Balance diversity of songs instead of always picking the closest match
  A diversity penalty could prevent the same artist from filling multiple top-5 slots, ensuring the recommendations feel more varied and exploratory.

- Use more features, like tempo ranges or lyric themes
  Adding tempo range preferences and incorporating valence or danceability into the score would give the system a more nuanced picture of what a listener actually wants in a given moment.

---

## 9. Personal Reflection

- What surprised you about how your system behaved
  It was surprising how drastically rankings shifted when a single weight was changed removing mood from the formula caused songs that previously ranked last to jump near the top, revealing how much hidden influence one factor can carry.

- How did building this change how you think about real music recommenders
  Every Spotify or YouTube recommendation now feels like a product of deliberate weight decisions someone made, not magic the playlist reflects the designer's assumptions about what listeners prioritize just as much as it reflects actual taste.

- Where do you think human judgment still matters, even if the model seems "smart"
  Human judgment is still essential for deciding which features to measure, how to weight them, and whether the resulting recommendations are fair to users whose tastes fall outside the dataset's mainstream those choices cannot be automated.

