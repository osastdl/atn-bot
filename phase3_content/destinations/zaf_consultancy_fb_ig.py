"""Posts to ZAF Consultancy's real Facebook Page + Instagram Business
account via the Meta Graph API.

This is NOT the same thing as zaf_gallery.py -- that one writes to a
gallery section of the ZAF Consultancy *website*. This one posts to their
actual public Facebook/Instagram, discovered 2026-08-18: of the three
Pages available under this Meta app, only ZAF Consultancy had an
Instagram Business account linked (the two personal-looking pages did
not), so this ended up being the one real, working destination.

Env vars: ZAF_CONSULTANCY_FB_PAGE_ID, ZAF_CONSULTANCY_FB_PAGE_TOKEN,
ZAF_CONSULTANCY_IG_USER_ID. Page token is long-lived (~60 days) --
re-exchange periodically, same process as before.
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request

GRAPH = "https://graph.facebook.com/v21.0"


def _config():
    return {
        "page_id": os.environ["ZAF_CONSULTANCY_FB_PAGE_ID"],
        "page_token": os.environ["ZAF_CONSULTANCY_FB_PAGE_TOKEN"],
        "ig_user_id": os.environ["ZAF_CONSULTANCY_IG_USER_ID"],
    }


def _post(url, params):
    query = urllib.parse.urlencode(params)
    req = urllib.request.Request(f"{url}?{query}", method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Graph API error {e.code}: {e.read().decode('utf-8')}") from None


def post_to_facebook(image_url, caption):
    cfg = _config()
    return _post(
        f"{GRAPH}/{cfg['page_id']}/photos",
        {"url": image_url, "caption": caption, "access_token": cfg["page_token"]},
    )


def post_to_instagram(image_url, caption):
    cfg = _config()
    container = _post(
        f"{GRAPH}/{cfg['ig_user_id']}/media",
        {"image_url": image_url, "caption": caption, "access_token": cfg["page_token"]},
    )
    creation_id = container["id"]

    # For static images (unlike video/reels) the container is ready
    # immediately -- querying its status_code right after creation is a
    # known source of a spurious "object does not exist" 400, so don't.
    return _post(
        f"{GRAPH}/{cfg['ig_user_id']}/media_publish",
        {"creation_id": creation_id, "access_token": cfg["page_token"]},
    )


def post(image_url, caption):
    return {
        "facebook": post_to_facebook(image_url, caption),
        "instagram": post_to_instagram(image_url, caption),
    }
