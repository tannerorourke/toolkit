# Lifecycle

The design folder is `artifacts/design/` at the project's root unless the project names another. Every project moves through one flow, from its idea or its stopped state to an accepted checkpoint. This file names the two entries, the three gates, the role and lens at each step, and where a critic's findings are recorded. The practice packs it names come from the `roster:practices` skill when the roster plugin is installed; without it, run each step from this file. Name a pack to the user by the practice in its opening line, never by its pack name alone.

## Two entries

1. **New project.** The idea goes through a brainstorm, which runs the experience core before the plan is approved.
2. **Re-entry.** A project stopped midway is surveyed first. Dispatch `executor:surveyor` with the brief in `reentry.md` beside this file. Draft a retro core from its return block, each entry marked `built`, `partial`, or `absent`, and have the user mark each entry `keep` or `change`. Each `change` becomes a unit of work and, where the project has a board, a card.

Both entries meet at the ideation gate.

## Three gates

| Gate | Before | Passes when |
| --- | --- | --- |
| Ideation | The plan is approved | `core/review.md` in the project's design folder holds the user's approval line, and each named medium's ideation unit (the `gui` structure unit) holds one too |
| Build | A build checkpoint runs | Every design unit the checkpoint builds from has its approved folder, `<unit>/` in the design folder with an approval line in its `review.md`, and the checkpoint names that folder under Inputs |
| Acceptance | A checkpoint is marked complete | The gate's deterministic checks pass, the verifier passes the rest, the critic lenses have run and been triaged, and the user accepts |

## Steps, roles, and lenses

| Step | Author | Reviewer |
| --- | --- | --- |
| Experience core | The orchestrator, with the user | The user |
| Contract written | The orchestrator | Critic, `brief` lens, before the implementer is dispatched |
| Design unit drafted | The designer, or the orchestrator inline | Critic, `design` and `accessibility` lenses, before the user sees it; then the user, until approval |
| Build | `executor:implementer` | The gate, then `executor:verifier` (the verify skill), then the critic, `code` lens, and for a built page the `design` and `accessibility` lenses |
| Close | The orchestrator, with the close skill | None |

Dispatch `executor:critic` once per lens, in parallel. Its brief holds the absolute path of the lens file, the paths of the artifact and of any output that exercises it (test results, screenshots, a rendered page), and the path of `return.schema.json`. Never put the author's reasoning, a transcript, earlier rounds, or the user's reactions in a critic's brief.

## Triage and the record

1. Check each finding against the intent: the contract for a build, the core and the unit's decisions for a design unit. Call each finding `kept`, `fixed`, or `dismissed`, with the reason.
2. Show the user the kept findings, with the fix or the question each raises.
3. Copy the run into the `## Findings` section of the unit's `review.md`: one entry per run, with its date, its lens, each finding verbatim, and the triage call.
4. A build checkpoint has no `review.md`. Copy its runs into the checkpoint's report, the paragraphs after its Non-goals.

Findings never go in the close trace.

## Without subagents

Run every role inline. Run a lens in a context that has not seen the work it judges, and triage its findings exactly as above.

Pass condition: each accepted checkpoint has passed its three gates in order, and every critic run on it has an entry under `## Findings` or in the checkpoint's report.
