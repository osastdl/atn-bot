# Phase 2 — Hate-crime & policy monitoring

Not built yet. Planned shape:

- `incidents.py` — candidate incident collection (curated news/social
  sources, not unrestricted crawling) → **human review queue** → only
  confirmed incidents count toward published stats/graphs. Cross-reference
  and cite established trackers (TGEU/TvT Trans Murder Monitoring, ILGA
  World) rather than rebuilding verification from scratch.
- `policy.py` — legislative/constitutional regression tracking (AfricanLII,
  ILGA World's State-Sponsored Homophobia report, Human Dignity Trust's
  country map) — a different pipeline from incident monitoring, not
  social-media-driven.
- Africa-relevance filter on international anti-gender-movement
  organizations' public statements (e.g. Family Watch International).
- **Public-facing output stays at region/country aggregation.** Anything
  more granular (city-level, identifying detail) stays internal to ATN —
  publishing precise location data about anti-trans violence is itself a
  safety risk.
