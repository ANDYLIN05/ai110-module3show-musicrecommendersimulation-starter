# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

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

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
  Profiles with different combinations of genre, mood, and energy levels were tested, including a user with a strong genre preference, a user with a favorite artist specified, and a user whose preferences did not closely match many songs in the catalog.

- What you looked for in the recommendations  
  The goal was to check whether the top ranked songs actually matched the user's genre and mood, and whether the scores reflected the expected weight distribution across all four factors.

- What surprised you  
  It was surprising how much the rankings shifted when the mood check was temporarily removed, songs that previously ranked near the bottom got a great increase in scoring result, showing how heavily mood was influencing results even compared to genre. The sensitivity test made it clear that small weight changes have a noticeable impact on what gets recommended.

- Any simple tests or comparisons you ran  
  A side by side comparison of the original scoring versus a modified version with mood removed and energy doubled was run to observe how the top five results changed. Individual song scores were also traced manually to confirm the formula was computing each component correctly.

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
