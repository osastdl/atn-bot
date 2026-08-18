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


def search(query, max_results=5):
    """Returns a list of {title, url, content} dicts."""
    body = {
        "api_key": os.environ["TAVILY_API_KEY"],
        "query": query,
        "max_results": max_results,
    }
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
