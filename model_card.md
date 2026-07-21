# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeFinder 1.0

## 2. Intended Use

A classroom simulation that suggests the top 5 songs from a small catalog for one user's taste profile, with a reason attached to every pick. It assumes the
user can describe their taste as one favorite genre, one mood, a target energy, and whether they like acoustic songs. Not for real users.

## 3. How the Model Works

Every song gets compared to the user's profile and earns points: a matching genre is worth the most (2 points), a matching mood is worth 1, up to 1 point
for how close the song's energy is to what the user wants, and half a point if the song matches their acoustic preference. Then all songs are sorted by points
and the top 5 are shown with their reasons. Compared to the starter, I implemented all the scoring from scratch and added the acoustic preference bonus using the acousticness column.

## 4. Data

18 songs (10 starter + 8 I added for diversity). Features: genre, mood, energy, tempo, valence, danceability, acousticness. Genres range from pop and lofi to metal, classical, latin, country, hiphop, and folk — but several genres have only one song, and lofi has three, so the catalog itself shapes the results.
Missing: lyrics, language, artist popularity, and anything about listening history.

## 5. Strengths

Clear-taste users get results that match intuition: the "Chill Acoustic Lofi" profile got Library Rain and Midnight Coding on top, and "Moody Synthwave" got
Night Drive Loop first by a huge margin. The energy-closeness rule works well — it rewards the right energy level instead of just louder songs, and the printed reasons make every ranking easy to sanity-check.

## 6. Limitations and Bias

Genre dominates. My adversarial "Conflicted" profile (lofi genre but 0.97 energy) still got three low-energy lofi songs on top, because a genre match (+2.0) outweighs even a near-perfect energy fit. Exact string matching makes it worse: "indie pop" earns nothing for a "pop" fan. And with only 18 songs, a user whose genre isn't in the catalog gets rankings driven almost entirely by energy, which they never asked to be the main factor.

## 7. Evaluation

I tested four profiles: High-Energy Pop, Chill Acoustic Lofi, Moody Synthwave, and the adversarial Conflicted profile. Comparing pairs: Pop vs. Lofi produce
nearly opposite lists (high-energy non-acoustic vs. low-energy acoustic), which makes sense since they differ on every feature. Synthwave only has one true
genre match, so its list is one clear winner plus energy-based filler — showing what happens when the catalog is thin. The surprise was the Conflicted profile: I expected high-energy songs to win and instead genre steamrolled everything. I
also ran a weight experiment (genre 2.0 → 0.5, energy doubled) and the top 5 flipped completely, plus the two starter pytest tests pass.

## 8. Future Work

1. Genre similarity instead of exact matching (lofi ≈ ambient ≈ jazz).
2. Normalize or expose the weights so genre can't silently dominate.
3. A diversity rule so one artist or genre can't fill the whole top 5.

## 9. Personal Reflection

The biggest thing I learned is that the "intelligence" in a recommender is mostly just weights. When I changed genre from 2.0 to 0.5 and doubled energy, the exact same user got a completely different top 5 — same data, same code structure, different opinion. That made me realize that when Spotify recommends something, a human somewhere decided what matters, and I'd never see that decision. The starter's main.py import was actually broken (it crashed with python -m src.main until we
fixed it to import from src.recommender), and I only trusted the scoring logic after running the adversarial profile and the pytest tests myself.