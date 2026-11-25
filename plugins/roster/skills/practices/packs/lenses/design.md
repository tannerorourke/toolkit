# Lens: design

How a design lead critiques a mockup before the person who asked for it sees it.

Judge whether a design unit's mockup or draft serves the experience core and its module's decisions.

The brief gives you the project's approved `core/core.md` from its design folder, the unit's module decisions, and the artifact as files: artboard images, a prototype's HTML, a screenshot of each state, or for a non-screen medium the draft `handoff.md` and `sample.md`.

Skill: invoke `design:design-critique` on each artboard or draft file the brief names, and fold its output into findings.

If that skill is absent, apply the rubric below alone.

## Rubric

| Check | Fails when | Severity |
| --- | --- | --- |
| The one question | A screen or step does not answer the question the core gives it, or buries the answer below what holds its prime position | high |
| Path | The top-ranked job takes a step the core's path does not have, or cannot be finished | high |
| States | A data region lacks one of its states: loading, empty for a new user, empty after filtering, empty because nothing exists, error, sparse, dense, long text, missing value | high |
| Ranked attributes | An object's most-needed attribute is not the most prominent one | medium |
| Consistency | Two places name, place, or style the same thing differently | medium |
| Copy | A label, error, or empty state leaves the user without the next action | medium |
| Visual system | A colour, type size, spacing, or radius falls outside the unit's design system | low |

For a non-screen medium, read "screen" as the step, question, reply, or call the module defines.

## Never shown

The designer's rationale, earlier rounds, the user's reactions from `review.md`, and who made the draft. A reviewer handed the author's view tends to confirm it.
