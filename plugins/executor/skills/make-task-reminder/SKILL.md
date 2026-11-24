---
name: make-task-reminder
description: Capture something the user wants to remember, buy, schedule, or try later (a reminder, an errand, an appointment, a question or idea for a project) as one line in the thought ledger, without derailing the current task. Use whenever the user says "remind me", "don't let me forget", "I should", "later", "when I get home", "next time I", "add to my list", "we're out of", "schedule", "idea for", or otherwise voices a to-do, an intention, or a future event in passing. Also invoked directly as /make-task-reminder <text>; with no text it lists the open items.
---

# make-task-reminder

One-turn capture. The user's thought becomes a record the moment it is voiced. Never ask a clarifying question at capture time, and never let the capture take over the turn: write, acknowledge in one plain line, resume the prior task.

Ledger access goes through `thoughts.py`; never edit the ledger by hand. `T` below is `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/thoughts.py"`.

## Procedure

1. Keep the utterance verbatim as `raw`. `thoughts.py` mints the id.
2. Restate the item as `text`: shortest complete imperative, about fifteen words at most. Keep names and places exactly as the user said them.
3. Route. Rules first: an explicit date and time is `schedule` with action `calendar`; "remind me" or a place or time phrase is `do` with action `reminder`; "buy", "pick up", "we're out of" is `buy` with action `list`; a repo or project named is `idea` with `project`; a question for Claude is `question`. When rules leave anything ambiguous, you are the capture model in this host: fill the schema in [thought-schema.json](thought-schema.json) yourself (category, `when`, `where`, `project`, `lifecycle` if obvious, `surface.mode`, `surface.remind`) with confidences, at most one `action`. Resolve "tomorrow", "Thursday" against today's date. Below 0.8 confidence on a date or place, do not set a reminder action; log instead. For an `idea`, write two or three possible directions into `notes`. If the thought needs more than the fixed kinds (an edit you cannot resolve, a multi-step lookup), set `routing.escalate` and log it; do not attempt it in this turn.
4. Write to the sink (below). Never edit or remove existing lines.
5. If the kind is `calendar` and this session has a calendar tool, execute it, record `status`, `tool`, and `external_id`, and append `(-> calendar)` to the ledger text. If the kind is `lookup` and this session has web search, run one search, put the one-line result in `notes`, and close the record. If the tool is absent, set `action.status` to `skipped` and say nothing about it. This host has no reminders tool; `reminder` and `list` actions are recorded as `pending`, for a client that has one to apply.
6. Acknowledge in one line, then continue the prior task in the same turn. Format: `Got it: <text>` plus the cue in plain words if any, plus "added to calendar" if step 5 acted. Nothing else: no list names, category, type, or field name.

## Sink

Use the first that exists:

1. A tool named `capture` (a memory service's inbound port). Pass raw, text, category, cue, lifecycle, route, source=claude-code, and the id.
2. The ledger, when the host has a filesystem. Its path is never assumed; `thoughts.py` takes it from the profile (`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/toolkit_profile.py" thoughts_ledger`). Run:

   `T add --category <category> --text "<text>" [--cue "<cue>"] [--project <repo>] [--record '<json>']`

   `--record` takes the routed fields as a JSON object (`raw`, `notes`, `when`, `where`, `lifecycle`, `surface`, `action`, `routing`), merged over the defaults and written to `thoughts/<id>.json` beside the ledger. The command prints the id.
3. Otherwise emit the formatted line in the reply and ask the user to paste it into the ledger. This covers a chat host with no filesystem and no `capture` tool.

Line format, for sink 3: `- [ ] <YYYY-MM-DD> | <category> | <cue> | <text> ^<id>`. State lives in the checkbox: `[ ]` open, `[x]` done, `[-]` dropped. Edits the user makes in the ledger are authoritative.

## Bare invocation

`/make-task-reminder` with no text runs `T list` and shows the result: open lines grouped by category (buy, do, schedule, idea by project, question, note), newest first within a group. `T list --project <repo>` or `--category <c>` narrows it. Closing out: `T done <id>`, `T drop <id>`, `T snooze <id> --until YYYY-MM-DD`, `T surfaced <id>` after bringing an item up.
