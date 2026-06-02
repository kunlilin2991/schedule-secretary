"""Conflict detection against the Feishu calendar.

SCAFFOLD — not yet implemented. See PROJECT.md Phase 6.

Given a candidate event, query the calendar (via feishu_calendar.list_events) for
the same window and report overlaps so the confirmation card can warn the user.
"""

from __future__ import annotations


def find_conflicts(candidate: dict) -> list[dict]:
    """Return existing events that overlap the candidate event's time range.
    Empty list means no conflict. Not yet implemented."""
    raise NotImplementedError("conflict_checker.find_conflicts — Phase 6")
