"""Tracks which grant/funding URLs have already been surfaced, so the
search sweep doesn't re-notify the same result every time it runs. Same
committed-JSON-state pattern as bot/state.py."""

import json
import os

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content")
SEEN_PATH = os.path.join(CONTENT_DIR, "seen_grants.json")


def load_seen():
    with open(SEEN_PATH) as f:
        return set(json.load(f))


def mark_seen(url):
    seen = load_seen()
    seen.add(url)
    with open(SEEN_PATH, "w") as f:
        json.dump(sorted(seen), f, indent=2)
