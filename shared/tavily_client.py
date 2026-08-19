"""Tavily search API client -- raw REST call via urllib, no SDK dependency
(matches the stdlib-only approach used everywhere else in this repo).
Free tier: 1,000 searches/month, no credit card.

Env var: TAVILY_API_KEY.
"""

import json
import os
import urllib.error
import urllib.request

API_URL = "https://api.tavily.com/search"


def search(query, max_results=5, time_range=None, topic=None):
    """Returns a list of {title, url, content} dicts.

    time_range: "day"/"week"/"month"/"year" -- filters Tavily's own index
    by publish/last-updated date. Without this, results have no recency
    bias at all and old-but-still-well-ranked pages (seen in production:
    results from 2022) surface just as readily as current ones.
    topic: "news" biases toward dated news coverage (best for monitoring
    breaking events); leave as default "general" for things like funder
    pages that are live/rolling application forms, not news articles.
    """
    body = {
        "api_key": os.environ["TAVILY_API_KEY"],
        "query": query,
        "max_results": max_results,
    }
    if time_range:
        body["time_range"] = time_range
    if topic:
        body["topic"] = topic
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Tavily API error {e.code}: {e.read().decode('utf-8')}") from None

    return [
        {"title": r["title"], "url": r["url"], "content": r.get("content", "")}
        for r in result.get("results", [])
    ]
