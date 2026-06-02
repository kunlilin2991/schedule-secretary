"""Feishu (Lark) calendar API wrapper.

SCAFFOLD — not yet implemented. See PROJECT.md sections 3, 5 (Phase 2/3) and 6.5.

The Feishu calendar is the single source of truth for the project. This module is
the only place that talks to the calendar HTTP API; all higher-level logic stays in
the Skill markdown / prompts.

Required app permissions (request early — approval is async, PROJECT.md Phase 2):
    calendar:calendar
    calendar:calendar.event:create
    calendar:calendar.event:read
    calendar:calendar.event:update
    calendar:calendar.event:delete

Implementation notes:
    - Reuse Hermes Agent's Feishu/Lark auth and SDK where possible rather than
      re-implementing token management.
    - Default timezone Asia/Shanghai.
    - Respect calendar API rate limits; back off on batch operations.

Docs: https://open.feishu.cn/document/server-docs/calendar-v4/
"""

from __future__ import annotations


def create_event(event: dict) -> dict:
    """Create a calendar event from a structured event dict (see parse_event schema).

    Returns the created event (including its Feishu event id). Not yet implemented.
    """
    raise NotImplementedError("feishu_calendar.create_event — Phase 3")


def list_events(start: str, end: str) -> list[dict]:
    """Return events overlapping the [start, end] window. Used by conflict checking
    and the daily brief. Not yet implemented."""
    raise NotImplementedError("feishu_calendar.list_events — Phase 3/6")


def update_event(event_id: str, patch: dict) -> dict:
    raise NotImplementedError("feishu_calendar.update_event")


def delete_event(event_id: str) -> None:
    raise NotImplementedError("feishu_calendar.delete_event")
