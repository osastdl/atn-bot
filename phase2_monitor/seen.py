"""Tracks which monitoring-result URLs have already been surfaced, so the
sweep doesn't re-notify the same result every run. Same pattern as
phase1_grants/seen.py, deliberately a separate state file (content/seen_monitor.json)
-- these are two different queues, no reason to share one."""

import json
import os

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content")
SEEN_PATH = os.path.join(CONTENT_DIR, "seen_monitor.json")


def load_seen():
    with open(SEEN_PATH) as f:
        return set(json.load(f))


def mark_seen(url):
    seen = load_seen()
    seen.add(url)
    with open(SEEN_PATH, "w") as f:
        json.dump(sorted(seen), f, indent=2)
