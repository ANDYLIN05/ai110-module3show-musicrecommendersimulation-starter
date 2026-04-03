# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**TuneSense 1.0**

---

## 2. Intended Use  

- What kind of recommendations does it generate  
  It generates a ranked list of up to 5 songs from a 20-track catalog based on how closely each song matches the user's genre, mood, energy, and optionally their favorite artist.

- What assumptions does it make about the user  
  It assumes the user can clearly express a single preferred genre, mood, and a target energy level between 0 and 1, and that these preferences are stable and equally weighted across all listeners.

- Is this for real users or classroom exploration  
  This is strictly for classroom exploration to illustrate how real-world recommender systems work; it is not intended for deployment with actual users.  

---

## 3. How the Model Works  
 
- What features of each song are used (genre, energy, mood, etc.)  
  Each song is described by its genre, mood, energy level (a number from 0 to 1 representing intensity), tempo, and additional feel attributes like valence and danceability.

- What user preferences are considered  
  The user tells the system their preferred genre, preferred mood, and a target energy level; they can also optionally name a favorite artist to give that factor a small bonus.

- How does the model turn those into a score  
  The model checks whether the song's genre and mood match the user's preferences (earning full credit or none), then calculates how close the song's energy is to the user's target, and adds a small bonus if the artist matches — each piece is multiplied by its weight and added together to produce a final score between 0 and 1.

- What changes did you make from the starter logic  
  Artist preference was added as a fourth scoring factor with a 10% weight, and the remaining weights were tuned so genre (35%), mood (30%), and energy (25%) reflect how most listeners prioritize those qualities.  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

- How many songs are in the catalog  
  The catalog contains 20 songs stored in `data/songs.csv`, each with fields for genre, mood, energy, tempo, valence, danceability, and acousticness.

- What genres or moods are represented  
  Genres include lofi, pop, rock, synthwave, ambient, jazz, and indie pop; moods include chill, happy, intense, relaxed, moody, and focused.

- Did you add or remove data  
  No songs were added or removed from the original starter dataset; the catalog was used as-is for all experiments.

- Are there parts of musical taste missing in the dataset  
  The dataset skews toward electronic and Western pop styles, with no representation of classical, country, R&B, or world music, meaning users with those tastes would receive no useful recommendations.  

---

## 5. Strengths  

- User types for which it gives reasonable results  
  The system works best for users whose preferences align with well-represented genres like lofi or pop, consistently surfacing accurate top results for those profiles.

- Any patterns you think your scoring captures correctly  
  The energy proximity component does a good job of separating high-intensity songs like Voltline tracks from low-energy ambient or lofi tracks, so users who care deeply about energy level tend to get sensible results.

- Cases where the recommendations matched your intuition  
  A user profiled as a chill lofi listener reliably received "Library Rain," "Midnight Coding," and "Morning Stretch" at the top, which are exactly the songs a human curator would select for that mood.  

---

## 6. Limitations and Bias 

- Features it does not consider  
  The system does not account for listening history, song popularity, or tempo preferences beyond what is stored in the user profile. It also ignores attributes like danceability, valence, and acousticness even though they are present in the dataset, meaning two very different sounding songs can receive identical scores.

- Genres or moods that are underrepresented  
  If the dataset contains far more songs in certain genres like Pop or Hip-Hop, users who prefer niche genres like Jazz or Classical may receive lower-quality recommendations simply because there are fewer candidates to choose from. Similarly, moods that appear less frequently in the catalog will produce results that rely more on genre and energy matches, which may not feel accurate.

- Cases where the system overfits to one preference  
  A user who specifies a favorite artist can see their top results dominated almost entirely by that artist, even when other songs would be a better overall fit. During our sensitivity test, doubling the energy weight caused rankings to shift heavily toward energy matches while ignoring whether the songs fit the user's genre or mood.

- Ways the scoring might unintentionally favor some users  
  Users whose preferences align with the most common genre and mood combinations in the dataset will consistently receive higher scoring recommendations than users with less common tastes. The fixed weights also assume that genre is always more important than mood, which may not reflect how every listener actually prioritizes their preferences.

---

## 7. Evaluation  

- Which user profiles you tested  
  Profiles with different combinations of genre, mood, and energy levels were tested, including a user with a strong genre preference, a user with a favorite artist specified, and a user whose preferences did not closely match many songs in the catalog.

- What you looked for in the recommendations  
  The goal was to check whether the top ranked songs actually matched the user's genre and mood, and whether the scores reflected the expected weight distribution across all four factors.

- What surprised you  
  It was surprising how much the rankings shifted when the mood check was temporarily removed, songs that previously ranked near the bottom got a great increase in scoring result, showing how heavily mood was influencing results even compared to genre. The sensitivity test made it clear that small weight changes have a noticeable impact on what gets recommended.

- Any simple tests or comparisons you ran  
  A side by side comparison of the original scoring versus a modified version with mood removed and energy doubled was run to observe how the top five results changed. Individual song scores were also traced manually to confirm the formula was computing each component correctly.


---

## 8. Future Work  

- Additional features or preferences  
  Adding tempo range preferences would let users specify whether they want slow background music or fast workout tracks, making the energy score more precise.

- Better ways to explain recommendations  
  Each recommended song could display a short breakdown showing exactly how many points came from genre, mood, energy, and artist so the user understands why it was chosen.

- Improving diversity among the top results  
  A diversity penalty could be applied to prevent the same artist from occupying multiple spots in the top 5, ensuring users see a wider range of options.

- Handling more complex user tastes  
  Allowing users to rate songs and adjusting weights over time based on those ratings would move the system closer to how real personalized recommenders like Spotify actually learn from behavior.  

---

## 9. Personal Reflection  


- What you learned about recommender systems  
  I learned that recommender systems are fundamentally about translating human preferences into math, and that the hard part is not the calculation itself but deciding which features matter and how much weight each one deserves.

- Something unexpected or interesting you discovered  
  It was surprising how dramatically the rankings shifted when even one weight was adjusted — removing mood entirely caused songs that previously ranked last to jump into the top results, which showed how much hidden influence a single factor can carry.

- How this changed the way you think about music recommendation apps  
  I now realize that every playlist Spotify or YouTube generates reflects someone's decisions about what to measure and prioritize, meaning the recommendations I receive say as much about the system's design choices as they do about my actual taste.  
