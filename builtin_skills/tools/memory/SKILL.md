---
name: memory
description: How Mira's memory is split (project memory you maintain vs long-term memory Dream maintains) and how to search past conversations in history.jsonl.
metadata:
  aliases: ["knowledge base", "remember", "store information", "recall"]
---

# Memory

## Two layers

**Project memory**: `<project>/memory/MEMORY.md`, present only when working in a project. **You maintain it.**
- Record what the project needs to move on: decisions, experiment results, data and file locations, pitfalls, current status.
- Update it when the fact is settled, not at the end of the session. Keep it concise and current; remove what is stale.
- Facts about the user in general (preferences, expertise, habits) do not belong here. They reach long-term memory through the history log.

**Long-term memory**: `MIRA_HOME/mind/` (default `~/.mira/mind/`). **Dream maintains it. Do NOT edit it.**
- `MEMORY.md`: long-term knowledge useful across projects.
- `USER.md`: the user's profile and preferences.
- `SOUL.md`: your personality and communication style.

Dream runs on a schedule and reads the history log, including project entries tagged `[project NAME]`. If something there is outdated, Dream fixes it on its next run. Users can review Dream's changes with `/dream-log` and undo one with `/dream-restore`.

## Search past events

Each layer has an append-only `history.jsonl`: `<project>/memory/history.jsonl` for a project, `MIRA_HOME/mind/history.jsonl` for everything. The system prompt gives the exact path. Every line is a JSON object with `cursor`, `timestamp`, `content`.

- For broad searches, start with `grep(..., output_mode="count")` or the default `files_with_matches` mode, then expand to full content.
- Use `output_mode="content"` with `context_before` / `context_after` when you need the exact matching lines.
- Use `fixed_strings=true` for literal timestamps or JSON fragments.
- Use `head_limit` / `offset` to page through long histories.
- Use `exec` only as a last-resort fallback when the built-in search cannot express what you need.

Examples (replace `keyword` and the path):
- `grep(pattern="keyword", path="memory/history.jsonl", case_insensitive=true)`
- `grep(pattern="2026-04-02 10:00", path="memory/history.jsonl", fixed_strings=true)`
- `grep(pattern="oauth|token", path="<history path>", output_mode="content", case_insensitive=true)`
