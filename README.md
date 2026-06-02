# schedule-secretary

A **single-user, personal** AI schedule secretary. Send text / image / voice to a
Feishu (飞书/Lark) bot; an LLM parses it into a calendar event, you confirm via a
Feishu interactive card, and it lands in your Feishu calendar — which is the only
view, store, and reminder source. No app, no calendar UI; the tool lives entirely
inside Feishu.

It is built as a `schedule_secretary` **Skill** running on
[Hermes Agent](https://github.com/NousResearch/hermes-agent), not as a standalone
application.

## Documentation

- **[PROJECT.md](./PROJECT.md)** — the canonical project brief (intent, rejected
  alternatives, architecture, task plan). Read this first.
- **[CLAUDE.md](./CLAUDE.md)** — operational guidance for working in the repo.

## Status

Architecture design is complete; implementation has not started. See PROJECT.md §5
for the phased task plan.
