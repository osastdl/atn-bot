# Phase 3 — Personal content posting

**Not ATN's.** Send the bot a photo/video, it generates a caption +
hashtags and posts to whichever destination you specify. Nothing in this
module is ATN-branded.

- `destinations/personal_fb_ig.py` — Theo's personal Facebook/Instagram.
  Pending: neither of the two personal-looking Pages discovered so far
  ("Dame Zsa-Zsa", "Zsa-Zsa: Miss Gay R.S.A") have an Instagram Business
  account linked, so this destination has no working IG target yet.
- `destinations/zaf_gallery.py` — ZAF Consultancy website's public gallery
  page, via a scoped API route + its own secret — never direct DB access
  into the live ZAF Portal. Not built yet.
- `destinations/zaf_consultancy_fb_ig.py` — **working, credentials live**
  (2026-08-18). ZAF Consultancy's actual Facebook Page + Instagram
  Business account (`@zzwgh2010`) — this turned out to be the only Page
  of the three available under the Meta app that had Instagram linked,
  so it became the first real destination even though it wasn't the
  original plan. Posts to both Facebook and Instagram from one `post()`
  call.

Built first among the three phases: fastest way to prove the fresh
Telegram + Meta credentials work end to end, lowest risk.
