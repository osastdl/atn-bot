"""Search sweep for grant/funding opportunities beyond the curated list in
funders.py. Runs on its own schedule (see .github/workflows/grants-sweep.yml
-- daily, not the 5-minute Telegram poll, since new CFPs don't appear that
often).

No AI judgment available (see funders.py / README for why -- billing),
so relevance is a plain keyword heuristic, not real understanding. That
means false positives are expected -- every result is explicitly flagged
as unverified in its notification, matching the human-review-only
principle for Phase 1 (this sweep finds and surfaces candidates, it never
applies to anything).
"""

import re
from datetime import datetime

from phase1_grants import seen
from shared import notify, tavily_client

CURRENT_YEAR = datetime.now().year

SEARCH_QUERIES = [
    f"call for proposals LGBTQI Africa grant {CURRENT_YEAR} apply now",
    f"trans rights Africa funding opportunity open {CURRENT_YEAR}",
    f"transgender gender diverse Africa grant application deadline {CURRENT_YEAR}",
    f"emergency fund LGBTQI Africa rapid response grant {CURRENT_YEAR}",
    f"human rights defenders Africa grant call {CURRENT_YEAR} currently accepting applications",
]

# Coarse relevance filter -- must look like an actual funding
# opportunity AND be Africa-relevant, not just any article that happens
# to mention these search terms.
FUNDING_KEYWORDS = ["grant", "funding", "call for proposals", "apply", "application", "fund"]
AFRICA_KEYWORDS = ["africa", "african"]

# A grant's underlying page can outlive its actual deadline by years --
# Tavily's own recency filtering (time_range on the API call) only tells
# us the PAGE was recently crawled/updated, not that the opportunity
# itself is still open. This catches the common, explicit "this already
# closed" phrasing and a stated deadline year that's already passed.
CLOSED_PHRASES = [
    "applications are now closed", "no longer accepting applications",
    "this call has closed", "deadline has passed", "application closed",
    "call for applications closed",
]
DEADLINE_YEAR_RE = re.compile(r"deadline[^\d]{0,25}(20\d{2})", re.IGNORECASE)


def _looks_expired(result):
    text = result["title"] + " " + result["content"]
    if any(p in text.lower() for p in CLOSED_PHRASES):
        return True
    m = DEADLINE_YEAR_RE.search(text)
    if m and int(m.group(1)) < CURRENT_YEAR:
        return True
    return False


def _looks_relevant(result):
    # Short/generic titles (bare social-media links with no real
    # headline, e.g. a title that's literally just "Instagram") are a
    # reliable low-quality signal on their own, cheap to filter before
    # even checking keywords.
    if len(result["title"].strip()) < 10:
        return False
    if _looks_expired(result):
        return False
    text = (result["title"] + " " + result["content"]).lower()
    return any(k in text for k in FUNDING_KEYWORDS) and any(k in text for k in AFRICA_KEYWORDS)


def run_sweep():
    # Loaded once, then kept in sync in-memory as we go -- load_seen()
    # only reflects what was on disk at the START of this run, so without
    # this the same URL surfacing from two different queries in the same
    # sweep would slip through as a duplicate (confirmed happening).
    already_seen = seen.load_seen()
    found = 0
    notified = 0

    for query in SEARCH_QUERIES:
        for result in tavily_client.search(query, max_results=8, time_range="month"):
            found += 1
            if result["url"] in already_seen:
                continue
            already_seen.add(result["url"])

            if not _looks_relevant(result):
                seen.mark_seen(result["url"])  # skip permanently, don't re-check every run
                continue

            notify.notify(
                phase="phase1_grants",
                title=f"[Unverified -- needs review] {result['title']}",
                body=result["content"][:400],
                source_url=result["url"],
            )
            seen.mark_seen(result["url"])
            notified += 1

    return {"found": found, "notified": notified}


if __name__ == "__main__":
    print(run_sweep())
