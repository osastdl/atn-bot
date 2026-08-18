"""Publishes any scheduled_posts whose time has arrived. Runs on its own
schedule (.github/workflows/publish-scheduled.yml, every ~5 minutes,
matching the Telegram poll cadence) -- separate from bot/main.py since
this has nothing to do with incoming Telegram messages, it's just a
queue-drain job.

Deliberately reuses the SAME destination modules as the immediate-post
flow (bot/main.py's handle_reply_confirmation) rather than a third copy
of the Facebook/Instagram posting logic -- whether a post came from
Telegram or the website, and whether it's posted now or scheduled, there
is exactly one place that actually talks to the Graph API per
destination.
"""

import os
from datetime import datetime, timezone

from phase3_content.destinations import zaf_consultancy_fb_ig
from shared import supabase_client, telegram_api

DESTINATIONS = {"zaf_consultancy": zaf_consultancy_fb_ig}


def run():
    now_iso = datetime.now(timezone.utc).isoformat()
    due = supabase_client.list_due_scheduled_posts(now_iso)
    chat_id = os.environ.get("ATN_TELEGRAM_CHAT_ID")

    published, failed = 0, 0
    for post in due:
        destination = DESTINATIONS.get(post["destination"])
        try:
            if destination is None:
                raise RuntimeError(f"Unknown destination: {post['destination']}")
            result = destination.post(post["image_url"], post["caption"])
            supabase_client.mark_scheduled_post(post["id"], "published")
            published += 1
            if chat_id:
                telegram_api.send_message(
                    chat_id,
                    (
                        "<b>\U0001F4C5 Scheduled post published</b>\n\n"
                        f"\U0001F4D8 <a href=\"{result['facebook']['url']}\">View on Facebook</a>\n"
                        f"\U0001F4F7 <a href=\"{result['instagram']['url']}\">View on Instagram</a>"
                    ),
                    parse_mode="HTML",
                )
        except Exception as e:
            supabase_client.mark_scheduled_post(post["id"], "failed", error=str(e))
            failed += 1
            if chat_id:
                telegram_api.send_message(
                    chat_id, f"❌ Scheduled post failed: {e}"
                )

    return {"due": len(due), "published": published, "failed": failed}


if __name__ == "__main__":
    print(run())
