"""Vision-based caption + hashtag generation via the Anthropic API.

Looks at the actual image content and writes a caption relevant to what's
in it -- not a generic template. No persona/voice shaping (deliberately
dropped per 2026-08-18 direction: just accurate captions and hashtags).

Env var: ANTHROPIC_API_KEY.
"""

import base64
import json
import os
import urllib.request

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-5"

PROMPT = """Look at this image and write a short, natural social media caption \
describing what's actually happening in it -- specific to this photo, not generic. \
Then suggest 5-8 relevant hashtags.

Respond with ONLY valid JSON in this exact shape, nothing else:
{"caption": "...", "hashtags": ["#tag1", "#tag2", ...]}"""


def generate_caption(image_bytes, media_type="image/jpeg"):
    api_key = os.environ["ANTHROPIC_API_KEY"]
    body = {
        "model": MODEL,
        "max_tokens": 500,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": base64.b64encode(image_bytes).decode("ascii"),
                        },
                    },
                    {"type": "text", "text": PROMPT},
                ],
            }
        ],
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    text = result["content"][0]["text"]
    parsed = json.loads(text)
    return parsed["caption"], parsed["hashtags"]


def format_caption(caption, hashtags):
    return f"{caption}\n\n{' '.join(hashtags)}"
