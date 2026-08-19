"""Monitoring sweep for hate crimes/violence, policy regression, and
Africa-relevant activity from international anti-gender-movement
organisations. Same architecture as phase1_grants/search.py (Tavily +
keyword heuristics + human-review framing), because that pattern is
already proven working -- see its README for why this doesn't use AI
judgment (billing).

Every result is explicitly marked [Unverified -- needs review] and
NOTHING here counts as a confirmed statistic on its own -- this sweep's
only job is to surface candidates for a human to verify, per the
verification-before-publication principle in phase2_monitor/README.md.
Cross-reference candidates against established trackers (TGEU/TvT Trans
Murder Monitoring, ILGA World) before treating anything as confirmed --
this sweep does not replace that verification step, only feeds it.

Deliberately does NOT collect or publish granular (city/address-level)
location detail beyond what a source headline/snippet already states --
publishing precise location data about anti-trans violence is itself a
safety risk. Region/country level only.
"""

from datetime import datetime

from phase2_monitor import seen
from shared import notify, tavily_client

CURRENT_YEAR = datetime.now().year

CATEGORIES = {
    "incident": {
        "label": "\U0001F6A8 Incident",
        "queries": [
            f"transgender murder Africa {CURRENT_YEAR}",
            "anti-trans violence attack Africa this week",
            "hate crime transgender gender diverse Africa latest",
        ],
        "keywords": ["murder", "killed", "attack", "assault", "violence", "hate crime", "beaten", "stabbed"],
        # Anti-gender-movement activity (conferences, coalition building)
        # moves slower than breaking incidents/policy news -- a 1-week
        # window would starve this category of almost everything, so it
        # gets its own wider setting below instead of the shared default.
        "time_range": "week",
    },
    "policy": {
        "label": "\U0001F4DC Policy/legislative",
        "queries": [
            f"anti-LGBT bill Africa {CURRENT_YEAR} parliament",
            "transgender rights law Africa criminalize latest",
            "Africa constitution amendment gender identity ban recent",
        ],
        "keywords": ["bill", "law", "legislation", "parliament", "criminalize", "ban", "constitution", "amendment"],
        "time_range": "week",
    },
    "anti_gender_movement": {
        "label": "\U0001F3DB️ Anti-gender movement",
        "queries": [
            f"Family Watch International Africa {CURRENT_YEAR}",
            "anti-gender movement conference Africa recent",
        ],
        "keywords": ["family watch", "anti-gender", "conference", "coalition", "funding"],
        "time_range": "month",
    },
}

AFRICA_KEYWORDS = ["africa", "african"]


def _looks_relevant(result, category_keywords):
    if len(result["title"].strip()) < 10:
        return False
    text = (result["title"] + " " + result["content"]).lower()
    return any(k in text for k in category_keywords) and any(k in text for k in AFRICA_KEYWORDS)


def run_sweep():
    already_seen = seen.load_seen()
    found = 0
    notified = 0

    for category_key, category in CATEGORIES.items():
        for query in category["queries"]:
            results = tavily_client.search(
                query, max_results=8, topic="news", time_range=category["time_range"],
            )
            for result in results:
                found += 1
                if result["url"] in already_seen:
                    continue
                already_seen.add(result["url"])

                if not _looks_relevant(result, category["keywords"]):
                    seen.mark_seen(result["url"])
                    continue

                notify.notify(
                    phase="phase2_monitor",
                    title=f"[Unverified -- needs review] {category['label']}: {result['title']}",
                    body=result["content"][:400],
                    source_url=result["url"],
                )
                seen.mark_seen(result["url"])
                notified += 1

    return {"found": found, "notified": notified}


if __name__ == "__main__":
    print(run_sweep())
