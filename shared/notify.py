"""Fires a notification to both surfaces at once: the /atn page on the
ZAF Consultancy Portal (via supabase_client) and Telegram (via
telegram_api). This is the single entrypoint Phase 1 and Phase 2 should
call -- neither phase should write to Supabase or Telegram directly.
"""

import os

from shared import supabase_client, telegram_api


def notify(phase, title, body=None, source_url=None):
    supabase_client.insert_notification(
        phase=phase, title=title, body=body, source_url=source_url
    )

    chat_id = os.environ.get("ATN_TELEGRAM_CHAT_ID")
    if chat_id:
        text = title
        if body:
            text += f"\n{body}"
        if source_url:
            text += f"\n{source_url}"
        telegram_api.send_message(chat_id, text)
