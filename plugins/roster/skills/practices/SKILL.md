---
name: practices
description: Route a practice (experience core, a medium such as gui, conversation, output, voice, or api) to its pack files. Use when planning, briefing, or reviewing practice work.
---

# Practices

When you are done, you hold the pack files for the practice in front of you, read in full or named by absolute path in a delegate's brief. A pack is a set of markdown files carrying a practice's procedure and rules. This skill routes to packs and holds no rules of its own.

## Critical

- Resolve every pack path against this skill's folder, `${CLAUDE_SKILL_DIR}`. Hand a delegate the absolute path, never the relative one.
- Read a pack file in full before acting on it. A pack is loaded every run, never summarized.
- Run every pack inline when no subagent is available. A role agent is a context optimization, and the pack carries the whole procedure.

## Routing

| Practice or medium | When | Pack files |
| --- | --- | --- |
| Experience core | A new project before its plan is approved; a project re-entering midway | `packs/experience/core.md` |
| Media | Naming the media in the core's sixth heading; planning a medium's units | `packs/experience/media.md` |
| Design procedure | Running any design unit, from the brief to the user's approval, and the two gates | `packs/design/procedure.md` |
| `gui` design rules | The designer's method for a structure, design system, or page unit | `packs/design/rules.md` |
| `conversation` | A unit for the questions a tool asks in turns | `packs/design/conversation.md` |
| `output` | A unit for a report, verdict, file, or message read by a person, a script, or an agent | `packs/design/output.md` |
| `voice` | A unit for spoken commands and replies | `packs/design/voice.md` |
| `api` | A unit for a library, CLI, or service interface | `packs/design/api.md` |
| Critic lens `brief` | A checkpoint contract, before an implementer runs | `packs/lenses/brief.md` |
| Critic lens `code` | A change, after the gate's deterministic checks | `packs/lenses/code.md` |
| Critic lens `design` | A design unit's mockup or draft, before the user sees it | `packs/lenses/design.md` |
| Critic lens `accessibility` | A page mockup before the user sees it; the built page | `packs/lenses/accessibility.md` |

Dispatch `executor:designer` for a design unit with the procedure's brief, when the executor plugin is installed; otherwise run the designer's step inline from the same rule file. For a medium in `media.md` whose pack file is not installed, run its module from its row in `media.md`.

A lens file is the critic's rubric. Dispatch `executor:critic` once per lens, in parallel, with the lens file and the artifact, never the author's reasoning. Without the agent, run the lens inline in a context that has not seen the work being judged, and triage its findings against the intent before the user sees them.

## Steps

1. Find the row for the work. A project with no approved core starts at the experience core, whatever was asked.
2. Read the row's files, or name their absolute paths in the brief under Inputs.
3. Follow the pack's procedure to its pass condition.

## Troubleshooting

**No row matches the practice.**
The practice has no pack yet. Do the work without one and tell the user which practice lacked a pack.

**A pack path does not resolve.**
The path was resolved against the working directory. Resolve it against this skill's folder, where `packs/` sits beside this file.

## See Also

- executor:brief: related; renders a checkpoint into a delegate brief that names these pack files, when the executor plugin is installed.
