"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

Implemented in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

# Phase 4: multiple distinct profiles, including an adversarial one
PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.85},
    "Chill Acoustic Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    "Moody Synthwave": {"genre": "synthwave", "mood": "moody", "energy": 0.75, "likes_acoustic": False},
    # Adversarial: conflicting preferences — a chill genre but maximum energy
    "Conflicted (lofi + max energy)": {"genre": "lofi", "mood": "intense", "energy": 0.97},
}


def run_profile(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top-k recommendations for one profile with scores and reasons."""
    print(f"\n{'=' * 62}")
    print(f"User profile: {name}  ->  {user_prefs}")
    print("-" * 62)
    recommendations = recommend_songs(user_prefs, songs, k=k)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} — {song['artist']}  (Score: {score:.2f})")
        print(f"   Because: {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, prefs in PROFILES.items():
        run_profile(name, prefs, songs, k=5)


if __name__ == "__main__":
    main()