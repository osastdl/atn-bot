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

**Photo flow (built 2026-08-18)**: send the bot a photo, `shared/caption_generator.py`
drafts a caption + hashtags from a template pool -- same proven, zero-cost
approach as VV Outreach's `poster.py` (a large pool of pre-written openers
+ a random sample of hashtags, with whatever you typed as the photo's own
Telegram caption folded in as a hint), NOT a vision/AI API call. Tried the
vision-API route first, hit a real billing wall, and it turned out VV's
bot never actually read the photo either -- so this matches what's already
proven in production rather than a new dependency. Publishes the image
publicly, and replies with Post/Cancel buttons -- nothing goes to
Facebook/Instagram until you tap Post. Runs as a scheduled GitHub Actions
job polling every ~5 minutes (`bot/main.py`, `.github/workflows/poll.yml`),
not a persistent server. State lives in `content/offset.json` and
`content/pending_posts.json`, committed back to the repo each run.

**Video is not wired up yet** -- the bot acknowledges a video message but
doesn't post it. Would need: a video-specific Graph API flow (container +
status polling + publish) in the destination modules, which currently
only handle images.

**Still needed before this actually runs**: `IMAGE_REPO_TOKEN` (a GitHub
token scoped to the image repos, so the scheduled job can publish photos
without a local git checkout) -- already stored as a repo secret.
