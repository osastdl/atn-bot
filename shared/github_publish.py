"""Publishes a file to a public GitHub repo via the Contents API, so Meta's
Graph API has a public URL to fetch from -- same pattern as VV Outreach's
separate image-hosting repo, just done over the API instead of local git,
since the bot has no working copy to commit from when it runs in CI.

Env var: IMAGE_REPO_TOKEN -- a token scoped only to the image repos, not a
broad account token. Repo/branch are passed in per call since Phase 3 has
more than one destination-specific image repo.
"""

import base64
import json
import urllib.request


def publish(token, repo, path, content_bytes, message):
    """repo: 'owner/name'. Returns the raw.githubusercontent.com URL."""
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    body = {
        "message": message,
        "content": base64.b64encode(content_bytes).decode("ascii"),
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
        method="PUT",
    )
    with urllib.request.urlopen(req) as resp:
        json.loads(resp.read().decode("utf-8"))

    return f"https://raw.githubusercontent.com/{repo}/main/{path}"
