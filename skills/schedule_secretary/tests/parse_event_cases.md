# parse_event test cases

Edge cases the parser must handle correctly. Each maps to a rule in
[`../prompts/parse_event.md`](../prompts/parse_event.md) and PROJECT.md §6.1.
Given `current_datetime` is injected, these become deterministic.

| # | Input | Expected behavior |
|---|---|---|
| 1 | "下周三和小王开会" | Resolve "下周三" against `current_datetime`; `time: null` (no hour given) → ask in card |
| 2 | "明天下午 3 点和小王开会" | One `event`, start = tomorrow 15:00 Asia/Shanghai |
| 3 | "周三开会" | Date resolved, `time: null` (must not guess the hour) |
| 4 | "每周一例会 10 点" | One `event` with `rrule: FREQ=WEEKLY;BYDAY=MO`, start 10:00 |
| 5 | A poster listing 3 sessions | Array of 3 events |
| 6 | A foreign email "meeting at 9am EST" | Convert to Asia/Shanghai, record `source_timezone` |
| 7 | "记得明天买牛奶" | `type: reminder`, NOT a calendar event |
| 8 | "我明天有什么安排?" | Should be routed away by `classify_intent` as `query`, not parsed as an event |
| 9 | "下午开会" with no date | Date `null` → ask; do not assume today |
| 10 | All-day note "6 月 10 号团建" | `all_day: true`, no specific time |

<!-- TODO: convert this table into executable fixtures once parse_event lands. -->
