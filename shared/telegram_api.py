"""Raw urllib Telegram Bot API wrapper — no python-telegram-bot dependency,
mirroring the pattern already proven in VV Outreach's telegram_api.py."""

import json
import os
import urllib.error
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
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Telegram API error {e.code}: {e.read().decode('utf-8')}") from None


def get_me():
    return call("getMe")


def get_updates(offset=None, timeout=30):
    params = {"timeout": timeout}
    if offset is not None:
        params["offset"] = offset
    return call("getUpdates", **params)


def send_message(chat_id, text, reply_markup=None):
    params = {"chat_id": chat_id, "text": text}
    if reply_markup is not None:
        params["reply_markup"] = reply_markup
    return call("sendMessage", **params)


def get_file_path(file_id):
    return call("getFile", file_id=file_id)["result"]["file_path"]


def download_file(file_path):
    url = f"https://api.telegram.org/file/bot{_token()}/{file_path}"
    with urllib.request.urlopen(url) as resp:
        return resp.read()
