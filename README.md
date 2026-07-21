# 🎵 Music Recommender Simulation

## Project Summary

My version is a content-based recommender: 18 songs with features like genre, mood, energy, and acousticness are each scored against one user's taste profile, then ranked. Every recommendation comes with the reasons for its score, and I tested it with four different profiles including one designed to break it.

---

## How The System Works

Real platforms like Spotify mix collaborative filtering (what similar users played, skipped, and playlisted) with content-based filtering (matching song attributes to your known taste). My simulation is purely content-based: no other users, just song features versus one taste profile.

- Each `Song` uses: genre, mood, energy (0-1) tempo_bpm, valence, danceability, and acousticness.
- The `UserProfile` stores: favorite_genre, favorite_mood, target_energy, and likes_acoustic.
- Scoring recipe (per song): +2.0 for a genre match, +1.0 for a mood match, up to +1.0 for energy closeness (1 minus the gap between song energy and target energy, so closeness is rewarded, not just "high"), and +0.5 if the song's acousticness matches the user's acoustic preference.
- Ranking: every song in the CSV gets scored, then `sorted()` orders them by score (highest first) and the top k are returned with their reasons.
Expected bias: genre is worth double anything else, so the system will likely recommend a weak genre match over a great song from a neighboring genre — a
small filter bubble.

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

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

- Weight shift: I dropped genre from 2.0 to 0.5 and doubled the energy weight, then re-ran the "Conflicted" profile (lofi genre, energy 0.97). The top 5 completely flipped: originally three lofi songs led despite terrible energy fits; after the shift, high-energy metal/rock/edm (Steel Horizon, Gym Hero, Storm Runner) took over and no lofi song survived. Same data, same user- he weights alone decided the "taste."
- Adversarial profile: giving a user conflicting preferences (chill genre + max energy) exposed that genre dominates ties; the system picks the genre side of the conflict every time under default weights.

---

## Limitations and Risks

- Tiny catalog (18 songs): rankings are decided by what happens to exist in the file. Lofi has 3 songs; several genres have exactly 1.
- Exact-string genre matching: "indie pop" and "pop" score zero for each other even though they're neighbors.
- Genre weight dominates: a mediocre genre match usually beats an excellent energy + mood fit, creating a filter bubble.
- No lyrics, language, artist popularity, or listening history — real taste has dimensions this data can't see.

---

## Reflection

The biggest thing I learned is that the "intelligence" in a recommender is mostly just weights. When I changed genre from 2.0 to 0.5 and doubled energy, the exact same user got a completely different top 5 — same data, same code structure, different opinion. That made me realize that when Spotify recommends something, a human somewhere decided what matters, and I'd never see that decision. The starter's main.py import was actually broken (it crashed with python -m src.main until we
fixed it to import from src.recommender), and I only trusted the scoring logic after running the adversarial profile and the pytest tests myself.





