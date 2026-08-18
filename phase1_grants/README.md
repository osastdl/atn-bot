# Phase 1 — Grant / call-for-proposals discovery

Not built yet. Planned shape:

- `funders.py` — curated, maintained list of funders active in this space
  (UHAI EASHRI, ISDAO, Other Foundation, Urgent Action Fund-Africa, Global
  Philanthropy Project, Astraea, Mama Cash, Wellspring, OSF, Ford
  Foundation, AJWS, etc.), checked on a schedule.
- `search.py` — broader web-search-API sweep as the catch-all for anything
  outside the curated list. Not raw web crawling — search-API-driven.
- Eligibility triage reads the CFP page and flags "ATN likely qualifies" —
  **never auto-submits**. Output is always a drafted summary for human
  review and manual submission.
- No direct LinkedIn scraping (violates their ToS and their anti-bot
  defenses are aggressive) — rely on search engines that already index
  public LinkedIn posts instead.
