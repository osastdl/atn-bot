"""ATN bot entrypoint.

Simple long-poll loop for now so it can be run and tested locally
(`python bot/main.py`) before a hosting decision (webhook vs. persistent
polling process) is made — see README's "Open questions".

Command routing is deliberately flat and dumb right now: each phase gets
its handler wired in here as that phase's logic is actually built.
"""

import time

from shared import telegram_api

WELCOME = (
    "ATN bot is online.\n\n"
    "Phase 1 (grants), Phase 2 (monitoring), and Phase 3 (personal posting) "
    "aren't wired up yet — this just confirms the bot itself is reachable."
)


def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text.startswith("/start"):
        telegram_api.send_message(chat_id, WELCOME)
    else:
        telegram_api.send_message(
            chat_id, "No phases wired up yet — nothing to do with that."
        )


def main():
    print("ATN bot: polling for updates. Ctrl+C to stop.")
    offset = None
    while True:
        result = telegram_api.get_updates(offset=offset)
        for update in result.get("result", []):
            offset = update["update_id"] + 1
            if "message" in update:
                handle_message(update["message"])
        time.sleep(1)


if __name__ == "__main__":
    main()
