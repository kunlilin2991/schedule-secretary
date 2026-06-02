---
name: schedule_secretary
description: >-
  Receives multimodal messages (text / image / voice) from the user in Feishu IM,
  parses them into structured calendar events, confirms via a Feishu interactive
  card, and writes the result to the Feishu calendar. Also produces proactive daily
  briefs on a cron schedule.
triggers: >-
  A user message in Feishu IM that contains scheduling intent (a time, a meeting, a
  deadline, an event poster/screenshot, or a voice note describing an appointment).
tools:
  - feishu_calendar
  - feishu_card
  - conflict_checker
---

# schedule_secretary

> Status: **scaffold**. Sub-capabilities are designed but not yet implemented.
> See [`PROJECT.md`](../../PROJECT.md) §5 for the phased build order and §6 for the
> known pitfalls.

## Purpose

Turn "schedule entry" from a manual chore into "send a message to the AI". The user
never sees an app — they message the Feishu bot, the agent does the parsing and
conflict-checking, and the Feishu calendar provides the view + system-level reminders.

## Sub-capabilities

| Capability | Input | Output | Status |
|---|---|---|---|
| `parse_event` | text / image / voice | array of structured events (JSON) | TODO (Phase 3) |
| `classify_intent` | message | `event` \| `reminder` \| `query` | TODO (Phase 3) |
| `write_event` | structured event | Feishu calendar event | TODO (Phase 3) |
| `draft_card` | structured event(s) | Feishu interactive card | TODO (Phase 4) |
| `check_conflict` | time range | conflicting events | TODO (Phase 6) |
| `daily_brief` | (cron trigger) | proactive IM summary | TODO (Phase 6) |

## Flow (target)

1. User sends a message to the Feishu bot.
2. `classify_intent` decides whether this is an `event`, a `reminder`, or a `query`.
3. For events: `parse_event` produces structured JSON (see prompt for the schema and
   the strict rules — current datetime injection, `null` for missing fields, always
   return an array, `Asia/Shanghai` default, RRULE for recurrence).
4. `check_conflict` looks for overlapping events.
5. `draft_card` returns a Feishu interactive card for the user to confirm / edit / cancel.
6. On confirmation, `write_event` calls the Feishu calendar API.
7. The Feishu calendar fires the native (system-level) reminder.

## Prompts

- [`prompts/parse_event.md`](./prompts/parse_event.md) — the core parser. The hard part.
- [`prompts/classify_intent.md`](./prompts/classify_intent.md) — event vs reminder vs query.
- [`prompts/daily_brief.md`](./prompts/daily_brief.md) — the cron-driven daily report.

## Tools

- [`tools/feishu_calendar.py`](./tools/feishu_calendar.py) — Feishu calendar API wrapper.
- [`tools/feishu_card.py`](./tools/feishu_card.py) — interactive card construction.
- [`tools/conflict_checker.py`](./tools/conflict_checker.py) — overlap detection.

## Tests

- [`tests/parse_event_cases.md`](./tests/parse_event_cases.md) — edge cases the parser must pass.
- [`tests/e2e_test.py`](./tests/e2e_test.py) — end-to-end flow.
