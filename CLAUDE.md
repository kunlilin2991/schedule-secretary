# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Read This First

**Before doing anything, read [`PROJECT.md`](./PROJECT.md) in full.** It is the
canonical handoff document that captures the project from idea to architecture,
including *why* whole categories of work have been deliberately rejected. This
CLAUDE.md is the operational summary; PROJECT.md is the source of truth. When the
two disagree, PROJECT.md wins — and update this file to match.

## What This Project Is

`schedule-secretary` is a **single-user, personal** AI schedule secretary. The
user sends multimodal input (text / image / voice) to a Feishu (飞书/Lark) bot;
an LLM parses it into a structured calendar event; after the user confirms via a
Feishu interactive card, it is written to the **Feishu calendar**, which serves
as the only view, store, and reminder source. There is **no app and no calendar
UI** — the tool is invisible, living entirely inside Feishu.

The deliverable is **not** a standalone application. It is:

1. A `schedule_secretary` **Skill** (Anthropic Skill / Markdown format) that runs
   on top of **Hermes Agent** (NousResearch's agent harness).
2. Configuration wiring Hermes' Feishu adapter and the Feishu calendar API.

Hermes Agent provides the runtime: Feishu adapter (WebSocket mode), natural-language
cron scheduler, long-term memory (MEMORY.md), and LLM access (DeepSeek via OpenRouter).
**Prefer reusing Hermes' built-in capabilities over writing things from scratch.**

## Decisions That Are Off The Table

These were each evaluated and rejected (see PROJECT.md §1, §4.4, Appendix B).
**Do not re-propose them or design toward them:**

- ❌ Any standalone app — Android, iOS, Windows desktop, or Web client.
- ❌ Building a calendar view (month/week) or a custom reminder system — Feishu's
  native calendar owns both, including system-level alarms.
- ❌ Bidirectional sync between Feishu and Google Calendar. The Feishu calendar is
  the single source of truth; any Google mirror is **one-way write, read-only on
  the Google side**, and out of scope for the MVP.
- ❌ Commercialization of any kind (to-C, to-B, app-store listing).
- ❌ WeChat/微信 as an entry point (封号 risk); Feishu is the chosen channel.

## Architecture (Big Picture)

```
Home Ubuntu (compute, behind NAT)
  └─ Hermes Agent
       ├─ Feishu adapter (WebSocket mode — no public ingress needed)
       ├─ natural-language cron scheduler (proactive daily brief)
       ├─ MEMORY.md long-term memory + Honcho user modeling
       ├─ DeepSeek via OpenRouter (multimodal may use Qwen-VL / GPT-4o-mini)
       └─ skills/schedule_secretary/   ← the work in THIS repo
            ├─ parse_event   (multimodal → structured JSON)
            ├─ check_conflict (query Feishu calendar)
            ├─ draft_card    (send Feishu interactive card)
            ├─ write_event   (call Feishu calendar API)
            └─ daily_brief   (cron-driven proactive report)
                 │ Lark SDK over WebSocket
                 ▼
            Feishu servers → Feishu IM / Calendar / Docs
                 ▼  (auto multi-device sync + native strong reminders)
            Feishu apps on phone / PC / tablet
```

Key invariants:

- **Single entry point:** Feishu IM (user messages the bot).
- **Dual exit:** Feishu IM (confirmation cards, proactive reminders) + Feishu
  calendar (events + system-level reminders).
- **Single store:** the Feishu calendar is the only source of truth.
- **Zero clients:** no app, no Windows/Web client is written here.

## Repository Layout

```
PROJECT.md                          # canonical project brief — read first
CLAUDE.md                           # this file
skills/schedule_secretary/
  ├─ SKILL.md                       # Anthropic Skill entry point (name/description/triggers/tools)
  ├─ prompts/                       # system prompts (parse_event, classify_intent, daily_brief)
  ├─ tools/                         # Python helpers (Feishu calendar API, card builder, conflict checker)
  └─ tests/                         # parse_event_cases.md (edge cases) + e2e_test.py
```

The skill structure mirrors PROJECT.md §7. Build it out phase by phase per §5.

## Key Conventions

- **Skills are Markdown** (Anthropic Skill standard), not Python classes. Logic
  that the LLM drives lives in `SKILL.md` and `prompts/`; only mechanical I/O
  (API calls, card JSON construction) goes in `tools/*.py`.
- **`parse_event` is the hard part.** The prompt must handle (PROJECT.md §6.1):
  - **Inject the current datetime explicitly** (`current_datetime: ... Beijing`) so
    relative dates ("下周三") resolve correctly.
  - **Never guess missing fields** — return `time: null` and ask in the card.
  - **Always return an array of events**, even for a single event.
  - **Default timezone `Asia/Shanghai`**; convert foreign timezones per the prompt.
  - **Classify `event` (has a concrete time) vs `reminder` (a to-do)** — a memo is
    not a calendar event.
  - Recurring events → emit iCal **RRULE**; test boundaries carefully.
- **Reminders depend entirely on Feishu's native calendar.** Do not build a
  reminder system. Reliability on Chinese Android ROMs must be **field-tested**
  (locked screen 30+ min); if it fails, add a Feishu bot push as a second channel.
- **Feishu calendar permissions needed** (PROJECT.md §5 Phase 2): `calendar:calendar`
  and `calendar:calendar.event:{create,read,update,delete}`. Approval is async —
  request early.
- **Resilience:** wrap OpenRouter/DeepSeek calls with timeout + retry + fallback;
  back off against Feishu API rate limits for batch operations.
- **Language:** discussion/docs primarily Chinese; code comments and API docs may
  be English.

## Development Workflow

- No build system, dependency manifest, or test runner exists yet — establish them
  as the first tools land, and document the actual commands here (including how to
  run a **single** test).
- Deployment target is the home Ubuntu box running Hermes Agent; CI/CD is
  intentionally deferred (PROJECT.md §9).
- Active development branch: `claude/claude-md-docs-lFdsX`; default branch `main`.
- This is a **private** repo. Do not open a pull request unless explicitly asked.

## Current Status

Architecture design is complete; implementation has not started. The repo currently
holds the project docs and an empty skill scaffold. The next concrete steps are
PROJECT.md §5 Phase 0–1 (Feishu app credentials, Hermes Agent install, bot "hello").
Update this section and the conventions above as real code and commands are added.
