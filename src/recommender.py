import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

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
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _prefs_dict(self, user: UserProfile) -> Dict:
        """Convert a UserProfile into the prefs dict used by score_song."""
        return {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score every song against the user and return the top k, best first."""
        prefs = self._prefs_dict(user)
        ranked = sorted(
            self.songs,
            key=lambda song: score_song(prefs, asdict(song))[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of a song's score for this user."""
        score, reasons = score_song(self._prefs_dict(user), asdict(song))
        reason_text = ", ".join(reasons) if reasons else "no matching preferences"
        return f"{song.title} scored {score:.2f}: {reason_text}"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = {}
            for key, value in row.items():
                # Convert numeric strings to numbers so we can do math later.
                try:
                    song[key] = float(value) if "." in value else int(value)
                except (ValueError, TypeError):
                    song[key] = value
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Algorithm Recipe:
      +2.0  genre match
      +1.0  mood match
      +up to 1.0 for energy closeness: 1 - |song energy - target energy|
      +0.5  acoustic alignment (song matches the user's acoustic preference)
    Returns (score, reasons) so every recommendation can be explained.
    """
    score = 0.0
    reasons = []

    # Accept both key styles ("genre" from main.py, "favorite_genre" from profiles)
    fav_genre = user_prefs.get("genre", user_prefs.get("favorite_genre"))
    fav_mood = user_prefs.get("mood", user_prefs.get("favorite_mood"))
    target_energy = user_prefs.get("energy", user_prefs.get("target_energy"))
    likes_acoustic = user_prefs.get("likes_acoustic")

    if fav_genre is not None and song.get("genre") == fav_genre:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if fav_mood is not None and song.get("mood") == fav_mood:
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Reward closeness to the target energy, not just high or low values.
    # Energies are 0.0-1.0, so a perfect match earns +1.0 and a total miss earns 0.
    if target_energy is not None and "energy" in song:
        gap = abs(song["energy"] - target_energy)
        energy_points = 1.0 - gap
        score += energy_points
        reasons.append(f"energy closeness (+{energy_points:.2f})")

    # Acoustic alignment: acousticness above 0.5 counts as an "acoustic" song.
    if likes_acoustic is not None and "acousticness" in song:
        song_is_acoustic = song["acousticness"] > 0.5
        if likes_acoustic == song_is_acoustic:
            score += 0.5
            label = "acoustic" if song_is_acoustic else "non-acoustic"
            reasons.append(f"{label} preference match (+0.5)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no matching preferences"
        scored.append((song, score, explanation))
    # sorted() returns a new list (unlike .sort(), which mutates in place),
    # so the original catalog order stays untouched.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]