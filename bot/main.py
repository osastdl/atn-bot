"""ATN bot entrypoint.

Runs as ONE poll pass per invocation -- meant to be triggered by a
scheduled GitHub Actions job every ~5 minutes, not run as a standalone
long-lived loop. State (Telegram offset, pending post confirmations)
persists to content/*.json between runs; the calling workflow commits
those files back to the repo after each run.

Photo flow: photo in -> generate caption+hashtags from a template pool
(same approach as VV Outreach's poster.py -- not a vision API call) ->
publish image publicly -> send "post" or "cancel" as a plain message to
confirm. Deliberately NOT inline buttons: Telegram callback queries
expire within seconds, which a ~5-minute poll cycle can never catch in
time (confirmed by hitting exactly that error). Also deliberately not
requiring an actual Telegram reply-to-message, even though that would be
more precise when multiple posts are pending at once -- in practice not
every client reliably sends that gesture as real reply data (confirmed
by it silently not registering, twice), so "post"/"cancel" just resolves
to the oldest pending post for that chat instead.

Video is NOT wired yet -- destinations only know how to post images so
far. A video message gets acknowledged but not posted; see
phase3_content/README.md.
"""

import html
import os
import uuid

from bot import state
from phase1_grants import commands as grants_commands
from phase3_content.destinations import zaf_consultancy_fb_ig
from shared import caption_generator, github_publish, telegram_api

IMAGE_REPO = "osastdl/zaf-consultancy-post-images"

# Only one working destination right now (see phase3_content/README.md --
# personal_fb_ig has no linked Instagram yet, zaf_gallery isn't built).
# Wire a real selection step here once there's more than one live option.
DESTINATIONS = {"zaf_consultancy": zaf_consultancy_fb_ig}
DEFAULT_DESTINATION = "zaf_consultancy"

WELCOME = (
    "<b>\U0001F916 ATN bot is online</b>\n\n"
    "Send a photo and I'll draft a caption + hashtags for you to approve "
    "before it posts to Facebook and Instagram.\n\n"
    "/grants -- curated funder list (Phase 1)\n\n"
    "<i>Monitoring (Phase 2) and a live grant search sweep aren't wired up yet.</i>"
)

NOTHING_PENDING = "\U0001F937 Nothing pending to confirm right now."

UNRECOGNIZED = "Send a photo, or /start."

VIDEO_NOT_SUPPORTED = (
    "\U0001F3AC Got the video, but video posting isn't wired up yet -- "
    "only photos work right now."
)


def handle_start(message):
    telegram_api.send_message(message["chat"]["id"], WELCOME, parse_mode="HTML")


def handle_grants(message):
    telegram_api.send_message(
        message["chat"]["id"], grants_commands.format_funder_list(), parse_mode="HTML"
    )


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
            "file_id": file_id,
            "caption": full_caption,
            "destination": DEFAULT_DESTINATION,
        }
    )

    sent = telegram_api.send_photo(
        chat_id,
        photo=file_id,
        caption=(
            f"\U0001F4DD <b>Draft caption</b>\n\n{html.escape(full_caption)}\n\n"
            f'<i>Send "post" to publish, or "cancel" to discard.</i>'
        ),
        parse_mode="HTML",
    )

    pending = state.load_pending()
    pending[short_id]["chat_id"] = chat_id
    pending[short_id]["message_id"] = sent["result"]["message_id"]
    state.save_pending(pending)


def handle_video(message):
    telegram_api.send_message(message["chat"]["id"], VIDEO_NOT_SUPPORTED)


def handle_reply_confirmation(message):
    chat_id = message["chat"]["id"]
    action = message["text"].strip().lower()

    # Prefer an actual Telegram reply if there is one, but don't require
    # it -- in practice not every client/user reliably uses the reply
    # gesture, so fall back to "the oldest thing still waiting" instead
    # of leaving a plain "post" message with nowhere to go.
    short_id, entry = None, None
    if "reply_to_message" in message:
        short_id, entry = state.find_pending_by_message_id(message["reply_to_message"]["message_id"])
    if entry is None:
        short_id, entry = state.find_oldest_pending(chat_id)
    if entry is None:
        telegram_api.send_message(chat_id, NOTHING_PENDING)
        return

    state.pop_pending(short_id)

    if action == "cancel":
        telegram_api.send_photo(
            chat_id,
            photo=entry["file_id"],
            caption="\U0001F6AB <b>Cancelled</b> -- not posted.",
            parse_mode="HTML",
        )
        return

    destination = DESTINATIONS[entry["destination"]]
    try:
        result = destination.post(entry["image_url"], entry["caption"])
        fb_url = html.escape(result["facebook"]["url"])
        ig_url = html.escape(result["instagram"]["url"])
        telegram_api.send_photo(
            chat_id,
            photo=entry["file_id"],
            caption=(
                "<b>✅ Posted successfully</b>\n\n"
                f'\U0001F4D8 <a href="{fb_url}">View on Facebook</a>\n'
                f'\U0001F4F7 <a href="{ig_url}">View on Instagram</a>'
            ),
            parse_mode="HTML",
        )
    except Exception as e:
        telegram_api.send_photo(
            chat_id,
            photo=entry["file_id"],
            caption=f"❌ <b>Failed to post</b>\n\n{html.escape(str(e))}",
            parse_mode="HTML",
        )


def handle_message(message):
    text = message.get("text", "").strip().lower()
    if text in ("post", "cancel"):
        handle_reply_confirmation(message)
    elif "photo" in message:
        handle_photo(message)
    elif "video" in message:
        handle_video(message)
    elif text.startswith("/start"):
        handle_start(message)
    elif text.startswith("/grants"):
        handle_grants(message)
    else:
        telegram_api.send_message(message["chat"]["id"], UNRECOGNIZED)


def poll_once():
    offset = state.get_offset()
    result = telegram_api.get_updates(offset=offset, timeout=5)
    for update in result.get("result", []):
        state.set_offset(update["update_id"] + 1)
        if "message" in update:
            handle_message(update["message"])


if __name__ == "__main__":
    poll_once()
