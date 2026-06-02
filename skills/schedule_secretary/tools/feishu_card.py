"""Feishu interactive card construction.

SCAFFOLD — not yet implemented. See PROJECT.md Phase 4.

Builds the "AI gives a draft, user confirms with a button" card that gates every
write to the calendar. The card must support: confirm, edit, cancel — and, when a
conflict is detected, surface it with "add anyway" / "suggest alternative" options
(PROJECT.md Phase 6).

Verify that Hermes' Feishu adapter delivers the card callback (open question in
PROJECT.md section 8 — README says yes, must be field-tested).
"""

from __future__ import annotations


def draft_card(events: list[dict]) -> dict:
    """Return a Feishu interactive card (as dict / JSON) presenting the parsed
    event(s) for confirmation. Not yet implemented."""
    raise NotImplementedError("feishu_card.draft_card — Phase 4")


def handle_card_action(action: dict) -> dict:
    """Handle a card button callback (confirm / edit / cancel). Not yet implemented."""
    raise NotImplementedError("feishu_card.handle_card_action — Phase 4")
