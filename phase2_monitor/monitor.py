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

from phase2_monitor import seen
from shared import notify, tavily_client

CATEGORIES = {
    "incident": {
        "label": "\U0001F6A8 Incident",
        "queries": [
            "transgender murder Africa 2026",
            "anti-trans violence attack Africa news",
            "hate crime transgender gender diverse Africa",
        ],
        "keywords": ["murder", "killed", "attack", "assault", "violence", "hate crime", "beaten", "stabbed"],
    },
    "policy": {
        "label": "\U0001F4DC Policy/legislative",
        "queries": [
            "anti-LGBT bill Africa 2026 parliament",
            "transgender rights law Africa criminalize",
            "Africa constitution amendment gender identity ban",
        ],
        "keywords": ["bill", "law", "legislation", "parliament", "criminalize", "ban", "constitution", "amendment"],
    },
    "anti_gender_movement": {
        "label": "\U0001F3DB️ Anti-gender movement",
        "queries": [
            "Family Watch International Africa",
            "anti-gender movement conference Africa",
        ],
        "keywords": ["family watch", "anti-gender", "conference", "coalition", "funding"],
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
            for result in tavily_client.search(query, max_results=5):
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
