"""ATN bot entrypoint.

Runs as ONE poll pass per invocation -- meant to be triggered by a
scheduled GitHub Actions job every ~5 minutes, not run as a standalone
long-lived loop. State (Telegram offset, pending post confirmations)
persists to content/*.json between runs; the calling workflow commits
those files back to the repo after each run.

Photo flow: photo in -> generate caption+hashtags from a template pool
(same approach as VV Outreach's poster.py -- not a vision API call) ->
publish image publicly -> reply to the bot's message with "post" or
"cancel". Deliberately NOT inline buttons: Telegram callback queries
expire within seconds, which a ~5-minute poll cycle can never catch in
time (confirmed by hitting exactly that error) -- plain text replies
don't have that problem.

Video is NOT wired yet -- destinations only know how to post images so
far. A video message gets acknowledged but not posted; see
phase3_content/README.md.
"""

import os
import uuid

from bot import state
from phase3_content.destinations import zaf_consultancy_fb_ig
from shared import caption_generator, github_publish, telegram_api

IMAGE_REPO = "osastdl/zaf-consultancy-post-images"

# Only one working destination right now (see phase3_content/README.md --
# personal_fb_ig has no linked Instagram yet, zaf_gallery isn't built).
# Wire a real selection step here once there's more than one live option.
DESTINATIONS = {"zaf_consultancy": zaf_consultancy_fb_ig}
DEFAULT_DESTINATION = "zaf_consultancy"

WELCOME = (
    "ATN bot is online.\n\n"
    "Send a photo and I'll draft a caption + hashtags for you to approve "
    "before it posts. Phase 1 (grants) and Phase 2 (monitoring) aren't "
    "wired up yet."
)


def handle_start(message):
    telegram_api.send_message(message["chat"]["id"], WELCOME)


def handle_photo(message):
    chat_id = message["chat"]["id"]
    file_id = message["photo"][-1]["file_id"]  # largest size
    file_path = telegram_api.get_file_path(file_id)
    image_bytes = telegram_api.download_file(file_path)

    full_caption = caption_generator.generate_caption(hint_text=message.get("caption"))

    repo_path = f"bot-uploads/{uuid.uuid4().hex}.jpg"
    image_url = github_publish.publish(
        token=os.environ["IMAGE_REPO_TOKEN"],
        repo=IMAGE_REPO,
        path=repo_path,
        content_bytes=image_bytes,
        message="Bot upload pending confirmation",
    )

    short_id = state.add_pending(
        {
            "image_url": image_url,
            "caption": full_caption,
            "destination": DEFAULT_DESTINATION,
        }
    )

    sent = telegram_api.send_message(
        chat_id,
        f"{full_caption}\n\n---\nReply to this message with \"post\" to publish, or \"cancel\" to discard.",
    )

    pending = state.load_pending()
    pending[short_id]["chat_id"] = chat_id
    pending[short_id]["message_id"] = sent["result"]["message_id"]
    state.save_pending(pending)


def handle_video(message):
    telegram_api.send_message(
        message["chat"]["id"],
        "Got the video, but video posting isn't wired up yet -- only "
        "photos work right now.",
    )


def handle_reply_confirmation(message):
    chat_id = message["chat"]["id"]
    replied_to_id = message["reply_to_message"]["message_id"]
    action = message["text"].strip().lower()

    short_id, entry = state.find_pending_by_message_id(replied_to_id)
    if entry is None:
        telegram_api.send_message(chat_id, "Couldn't find that pending post -- it may already be handled.")
        return

    state.pop_pending(short_id)

    if action == "cancel":
        telegram_api.send_message(chat_id, "Cancelled.")
        return

    destination = DESTINATIONS[entry["destination"]]
    try:
        result = destination.post(entry["image_url"], entry["caption"])
        telegram_api.send_message(chat_id, f"Posted.\n\n{result}")
    except Exception as e:
        telegram_api.send_message(chat_id, f"Failed to post: {e}")


def handle_message(message):
    text = message.get("text", "").strip().lower()
    if "reply_to_message" in message and text in ("post", "cancel"):
        handle_reply_confirmation(message)
    elif "photo" in message:
        handle_photo(message)
    elif "video" in message:
        handle_video(message)
    elif text.startswith("/start"):
        handle_start(message)
    else:
        telegram_api.send_message(
            message["chat"]["id"], "Send a photo, or /start."
        )


def poll_once():
    offset = state.get_offset()
    result = telegram_api.get_updates(offset=offset, timeout=5)
    for update in result.get("result", []):
        state.set_offset(update["update_id"] + 1)
        if "message" in update:
            handle_message(update["message"])


if __name__ == "__main__":
    poll_once()
