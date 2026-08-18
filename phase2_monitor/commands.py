"""/monitor Telegram command -- shows the most recent Phase 2 monitoring
alerts on demand, pulled straight from Supabase (the same table the daily
sweep writes to). This doesn't run a new search -- it's a "show me what's
already been found" button, since the actual sweep only runs once a day
on the GitHub Actions schedule.
"""

import html

from shared import supabase_client

NOTHING_YET = (
    "\U0001F4E1 No monitoring alerts yet. The daily sweep runs once a day -- "
    "check back after it's had a chance to run."
)


def format_recent_alerts(limit=5):
    results = supabase_client.list_recent_notifications("phase2_monitor", limit=limit)
    if not results:
        return NOTHING_YET

    lines = ["\U0001F4E1 <b>Recent monitoring alerts</b> (Phase 2)\n"]
    for n in results:
        lines.append(
            f'<b>{html.escape(n["title"])}</b>\n'
            f'{html.escape(n["body"]) if n.get("body") else ""}\n'
            f'{html.escape(n["source_url"]) if n.get("source_url") else ""}\n'
        )
    lines.append(
        "<i>Human-review flagged findings only -- nothing here is a "
        "verified statistic. Full history is also on the ATN portal "
        "website.</i>"
    )
    return "\n".join(lines)
