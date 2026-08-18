"""/grants Telegram command -- lists the curated funder list directly.
This is a reference lookup, not a "new opportunity found" alert, so it
replies straight to Telegram rather than going through shared/notify.py
(that's reserved for genuinely new, time-sensitive findings once the
search-sweep half of Phase 1 exists -- see README.md).
"""

import html

from phase1_grants.funders import FUNDERS

FUNDING_TYPE_LABEL = {
    "rolling": "\U0001F7E2 Rolling (no fixed deadline)",
    "regional_call": "\U0001F4E2 Periodic regional call",
    "cycle": "\U0001F4C5 Fixed funding cycles",
    "loi_invitation": "✉️ By invitation / LOI",
}


def format_funder_list():
    lines = ["\U0001F4B0 <b>Curated funder list</b> (Phase 1)\n"]
    for f in FUNDERS:
        lines.append(
            f'<b>{html.escape(f["name"])}</b>\n'
            f'{FUNDING_TYPE_LABEL.get(f["funding_type"], f["funding_type"])}\n'
            f'{html.escape(f["focus"])}\n'
            f'{html.escape(f["notes"])}\n'
            f'{html.escape(f["url"])}\n'
        )
    lines.append(
        "<i>Last verified 2026-08-18 -- this is a reference list, not a live "
        "search. No automated \"new opportunity\" sweep is built yet.</i>"
    )
    return "\n".join(lines)
