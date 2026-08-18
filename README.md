# ATN Bot

One Telegram bot (`@AfricanTransNetworkbot`), two separate jobs sharing it:

- **Phase 1 + Phase 2 are African Trans Network's actual mission tooling.**
- **Phase 3 is an unrelated personal utility** (Theo's own Facebook/Instagram +
  the ZAF Consultancy website gallery) that happens to live in the same bot
  for convenience. Nothing in Phase 3 is ATN-branded or ATN-specific.

This repo is intentionally **fully separate** from Theo's existing
`visual-versatility-autopost` pipeline — own repo, own secrets, own Meta
app, own Telegram bot. Nothing here reuses that infrastructure.

## Phases

### Phase 1 — Grant / call-for-proposals discovery (`phase1_grants/`)
Finds funding opportunities relevant to African Trans Network: a curated,
maintained list of known LGBTQI+/human-rights funders active in Africa,
plus a broader web-search sweep for anything new. Triages eligibility and
drafts a summary — **never auto-submits an application**. A person always
does the actual submission.

### Phase 2 — Hate-crime & policy monitoring (`phase2_monitor/`)
Tracks anti-trans violence and policy/constitutional regressions across
Africa's regions, plus Africa-relevant activity from international
anti-gender-movement organizations (e.g. Family Watch International).
Surfaces candidates into a **human review queue** before anything counts
toward published statistics — verification before publication, always.
Public-facing stats stay at region/country aggregation; anything more
granular stays internal to ATN.

### Phase 3 — Personal content posting (`phase3_content/`)
Not ATN's. Send a photo/video to the bot, it generates a caption +
hashtags and posts to whichever destination you point it at:
- `destinations/personal_fb_ig.py` — Theo's personal Facebook/Instagram
- `destinations/zaf_gallery.py` — the ZAF Consultancy website's public
  gallery page (via a scoped API route/secret, not direct DB access)

Built first, since it's the lowest-risk, fastest way to prove the fresh
Telegram + Meta credentials work end to end.

## Status

Scaffold only — no phase logic implemented yet. Meta (Facebook/Instagram)
credentials pending; email (zsazsa@zafconsultancy.org, IMAP/SMTP) pending.
Telegram bot token is live and wired (`shared/telegram_api.py`).

## Structure

```
atn-bot/
  bot/                    — Telegram command router
    main.py                 entrypoint (long-poll loop for now; may move
                             to webhook mode once hosting is decided —
                             see "Open questions" below)
    handlers/                per-command handlers, one file per command
  phase1_grants/           — funder monitor + search sweep + eligibility triage
  phase2_monitor/          — incident/policy monitor + review queue + stats
  phase3_content/          — media ingest + caption/hashtag generation
    destinations/            one file per posting target
  shared/                  — telegram client, notification dispatcher, utils
```

## Open questions (not yet decided — flagging, not blocking)

- **Bot hosting**: an interactive Telegram bot needs either webhook mode
  (always-on HTTPS endpoint, Telegram POSTs to it) or long-running polling
  (needs a persistent process somewhere). ZAF Consultancy Portal is already
  live (Next.js/Supabase) — a webhook API route there could be a natural
  fit, matching the "ATN as a new org inside that platform" decision for
  Phase 1/2 data. Not decided yet; `bot/main.py` currently just does simple
  polling so it can be run and tested locally in the meantime.
- **Email**: zsazsa@zafconsultancy.org (IMAP `mail.zafconsultancy.org:993`,
  SMTP `:465`) is the account to wire up for send/receive. Password not
  yet stored anywhere — see `.env.example`.

## Leaving room for updates

Each phase is its own top-level module specifically so new capabilities
(Phase 4+, new Phase 3 destinations, new Phase 1/2 data sources) can be
added without touching the others. Update this README as phases and
decisions land.
