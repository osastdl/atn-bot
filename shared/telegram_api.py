"""Raw urllib Telegram Bot API wrapper — no python-telegram-bot dependency,
mirroring the pattern already proven in VV Outreach's telegram_api.py."""

import json
import os
import urllib.request

API_BASE = "https://api.telegram.org/bot{token}/{method}"


def _token():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN not set")
    return token


def call(method, **params):
    url = API_BASE.format(token=_token(), method=method)
    data = json.dumps(params).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_me():
    return call("getMe")


def get_updates(offset=None, timeout=30):
    params = {"timeout": timeout}
    if offset is not None:
        params["offset"] = offset
    return call("getUpdates", **params)


def send_message(chat_id, text):
    return call("sendMessage", chat_id=chat_id, text=text)
