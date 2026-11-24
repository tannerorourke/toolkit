# Experience core

When you are done, the project's design folder holds `core/core.md`, answering the six questions below, and `core/review.md` holding the user's approval line. The design folder is `artifacts/design/` at the project's root unless the project names another. Every project passes the core at the ideation gate, before its plan is approved, whatever media it uses.

Run the core in two cases:

- A new project, from its idea, before its plan is approved.
- A project re-entering midway, from a read-only survey of what is built. Mark each entry `built`, `partial`, or `absent`, and have the user mark each one `keep` or `change`. Each `change` becomes a unit of work.

## The six questions

Answer each under its own heading in `core.md`, in this order.

1. **Who uses it.** Name each kind of user and their posture: how often they arrive, how long they stay, and what state they arrive in. A tool open all day differs from one run once a week.
2. **Their jobs.** Write each job as a story: "When [situation], I want to [motivation], so I can [outcome]." Rank the tasks by frequency and, separately, by weight, the cost of getting one wrong. Name the objects the tasks act on, with each object's attributes ranked by how often the user needs them.
3. **The path of steps.** List the steps of the top-ranked job in order, from arrival to leaving. Branch only where the user makes a choice.
4. **What each step tells them.** For each step, write the one question it answers for the user and the fact they need in order to answer it.
5. **What they leave with.** Name the outcome, a decision, a file, or a changed state, and how the user knows they are done.
6. **The media.** Name each medium the product uses, from `media.md` beside this file. Each medium adds its own module, and its units follow the core.

## Steps

1. Draft the six answers from the idea or the survey. Mark every fact the user has not given as `assumed`.
2. Invoke `design:user-research` to plan research, or `design:research-synthesis` to synthesize it, only when evidence from real users exists or can be gathered. Skip both otherwise.
3. Show the user the draft. Record their reactions in their words under `## Reactions` in the review, then revise. Repeat until they approve.
4. At approval, create `core/` in the design folder, write `core.md`, and write `review.md` with the approval line last.

The folder holds approved work only. Keep drafts in the session's scratch until the user approves.

## `review.md`

```markdown
# Review: core

## Reactions

- YYYY-MM-DD: "the user's words"

## Findings

- YYYY-MM-DD, lens `name`: `path:line | severity | finding`; triage: kept, fixed, or dismissed, with the reason

Approved YYYY-MM-DD: "the user's words of approval"
```

`## Findings` holds each critic run's findings after triage, one entry per run. A unit with no critic run omits the section.

Pass condition: `core.md` holds 6 headings, each answered with no unresolved `assumed` mark, and `review.md` ends on 1 approval line quoting the user.
