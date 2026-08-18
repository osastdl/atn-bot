# Phase 3 — Personal content posting

**Not ATN's.** Send the bot a photo/video, it generates a caption +
hashtags and posts to whichever destination you specify. Nothing in this
module is ATN-branded.

- `destinations/personal_fb_ig.py` — Theo's personal Facebook/Instagram,
  fresh Meta credentials (pending), unrelated to the VV Outreach pipeline.
- `destinations/zaf_gallery.py` — ZAF Consultancy website's public gallery
  page, via a scoped API route + its own secret — never direct DB access
  into the live ZAF Portal.

Built first among the three phases: fastest way to prove the fresh
Telegram + Meta credentials work end to end, lowest risk.
