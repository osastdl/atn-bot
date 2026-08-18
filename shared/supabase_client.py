"""Talks to the ZAF Consultancy Portal's Supabase project as a normal,
restricted logged-in user -- NOT a service-role key. This account is an
org_member of the African Trans Network organisation, so the portal's
existing Row Level Security policies (same ones that isolate every other
client's data) are what actually restrict it to inserting atn_notifications
rows for ATN's own organisation_id. No new privileged secret type.

Env vars expected (see .env.example): SUPABASE_URL, SUPABASE_ANON_KEY,
ATN_BOT_EMAIL, ATN_BOT_PASSWORD, ATN_ORG_ID.
"""

import json
import os
import urllib.request


def _config():
    return {
        "url": os.environ["SUPABASE_URL"].rstrip("/"),
        "anon_key": os.environ["SUPABASE_ANON_KEY"],
        "email": os.environ["ATN_BOT_EMAIL"],
        "password": os.environ["ATN_BOT_PASSWORD"],
        "org_id": os.environ["ATN_ORG_ID"],
    }


def _request(method, url, headers, body=None):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        raw = resp.read()
        return json.loads(raw) if raw else None


def _access_token(cfg):
    result = _request(
        "POST",
        f"{cfg['url']}/auth/v1/token?grant_type=password",
        headers={"apikey": cfg["anon_key"], "Content-Type": "application/json"},
        body={"email": cfg["email"], "password": cfg["password"]},
    )
    return result["access_token"]


def insert_notification(phase, title, body=None, source_url=None):
    """phase: 'phase1_grants' or 'phase2_monitor'."""
    cfg = _config()
    token = _access_token(cfg)
    _request(
        "POST",
        f"{cfg['url']}/rest/v1/atn_notifications",
        headers={
            "apikey": cfg["anon_key"],
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        },
        body={
            "organisation_id": cfg["org_id"],
            "phase": phase,
            "title": title,
            "body": body,
            "source_url": source_url,
        },
    )
