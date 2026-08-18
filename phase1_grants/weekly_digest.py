"""Sends the curated funder list to Telegram on a schedule (see
.github/workflows/weekly-grants-digest.yml -- weekly, not on-demand).

The /grants command (phase1_grants/commands.py) stays available too for
whenever someone wants to check on-demand -- this doesn't replace it,
it's a second, scheduled way to see the same list.
"""

import os

from phase1_grants import commands
from shared import telegram_api


def send_digest():
    chat_id = os.environ["ATN_TELEGRAM_CHAT_ID"]
    telegram_api.send_message(chat_id, commands.format_funder_list(), parse_mode="HTML")


if __name__ == "__main__":
    send_digest()
