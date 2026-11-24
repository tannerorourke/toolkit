# Design procedure

How a design lead takes a product from its approved experience questions to designs the user has approved and a builder can follow.

Read this when a project's experience core names its media and a design unit is next: the `gui` structure with the core, the design system before the first page, a page before its build, or a `conversation`, `output`, `voice`, or `api` unit before the part it describes is built. When you are done, each unit you ran has its folder in the project's design folder, `artifacts/design/` at the project's root unless the project names another, holding the approved work and a review record that ends on the user's approval line.

## Units and gates

Five modules, one per medium, and two gates.

| Module | Unit | Gate | The rules the designer reads |
| --- | --- | --- | --- |
| `gui` | Structure | Ideation, with the experience core, before the plan is approved | `rules.md` |
| `gui` | Design system | Build, before the first page mockup | `rules.md` |
| `gui` | Page | Build, before that page's build checkpoint | `rules.md` |
| `conversation` | Flow | Build, before the step is built | `conversation.md` |
| `output` | Format | Build, before the output is built | `output.md` |
| `voice` | Command set | Build, before the commands are built | `voice.md` |
| `api` | Surface | Build, before the public interface is built | `api.md` |

The ideation gate passes when the core and the structure unit each hold the user's approval line. The build gate passes for a build checkpoint when every unit it builds from has its approved folder and the checkpoint names that folder under Inputs. All rule files sit beside this one.

## Where work lives

- Work in progress for a `gui` unit lives on the project's canvas, a Design artifact with one page per unit. Log the canvas link once, as a `design` key in the project's metadata, and nowhere else. Never keep a local copy of the canvas source as the record: the user edits the canvas by hand, and a read of the canvas serves its files back.
- Drafts of a `conversation`, `output`, `voice`, or `api` unit live in the session's scratch.
- The design folder holds approved work only. A unit's folder appears at approval, so its existence is the approval the build gate checks.
- A canvas and every draft carry synthetic data and interface copy only, never a user's real records.

## Run a unit

1. **Brief.** Write the designer's brief: the unit and its kind; the absolute path of the rule file from the table above; the approved core, `core/core.md`; for a page, the approved structure and the design system file; the platform's frame and how the product is used; the canvas link, or "create the canvas"; a scratch folder for the canvas source; the absolute path of the return schema. Give the decisions, never the conversation that reached them.
2. **Design.** Dispatch `executor:designer` with the brief as the whole prompt. It reads its rule file, designs the unit, publishes the canvas page, and returns the link and the files it wrote. When it returns `blocked` because the publish was refused, publish its files yourself by path with the Artifact tool. Without subagents, run the designer's step inline from the same rule file.
3. **Check before the user sees it.** For a structure or a page, dispatch `executor:critic` twice in parallel, once with the `design` lens and once with the `accessibility` lens, each with the artboard files the designer returned. The `design` lens invokes `design:design-critique` on those files and the `accessibility` lens invokes `design:accessibility-review` on them. Triage each finding against the core and the unit's brief, kept, fixed, or dismissed with the reason, and record each run under `## Findings` in the unit's review record, the 1 place a critic run's triaged findings are kept. Send the kept findings back to the designer and continue to step 4 once they are fixed or put to the user.
4. **Show the user.** Give the user the canvas link, or the draft for a non-`gui` unit, with the kept findings and the questions the designer returned. Record the user's reactions in their own words under `## Reactions` in the review record.
5. **Revise.** Within a session, continue the same designer with the reactions and its context intact. In a later session, dispatch a fresh designer whose brief names the review record and the canvas link. Repeat from step 3 until the user approves.
6. **Approve.** At the user's approval, create `<unit>/` in the design folder. Pull the approved artboards from the canvas into `<unit>/artboards/` with an Artifact read of those paths. Invoke `design:design-handoff` on the approved artboard files to fill `<unit>/handoff.md` with the states, the interaction rules, the copy, and the tokens. Write `<unit>/review.md` with `## Reactions`, `## Findings`, and 1 line of the user's words of approval, last.

Pass condition for a unit: its folder exists in the design folder, its `review.md` ends on 1 approval line quoting the user, and every critic run on it has a triaged entry under `## Findings`.

## The skills at each step

- At the experience core, invoke `design:user-research` on the draft `core.md` to plan research into its answers marked *assumed*, only when real users can be reached. Invoke `design:research-synthesis` on the evidence files the user hands over, interview notes or survey exports, each named by its path in the call.
- For the design system unit, invoke `design:design-system` on the project's `direction.md` to audit or extend the tokens and components. Before a page unit, invoke it again on `direction.md` when the system changed since the last page.
- In a page's copy pass, invoke `design:ux-copy` on the page's copy deck in its draft handoff. For every `conversation`, `output`, and `voice` unit, invoke it on the unit's `sample.md`.
- Before a page mockup is shown, invoke `design:accessibility-review` on the artboard files, through the critic's `accessibility` lens or inline. Run it again on the built page.
- Before a page mockup is shown, invoke `design:design-critique` on the artboard files, through the critic's `design` lens or inline. Run it again on the built page against the approved artboards.
- At approval, invoke `design:design-handoff` on the approved artboard files to fill `handoff.md`.
- Before drawing any chart, invoke `dataviz`.

When one of these skills is not installed, apply the matching rules from the rule file and the critic's lens, and say which skill was missing.

## A non-`gui` unit

Run steps 1 to 6 with the medium's rule file in place of `rules.md`. The designer returns a draft `handoff.md` and `sample.md` (an `api` unit returns the handoff alone) in the brief's scratch folder. Skip the `accessibility` lens, and run the `design` lens on the sample. At approval, copy the drafts into `<unit>/`.

## Troubleshooting

**The canvas publish is refused, or asks for approval the designer cannot give.** The designer returns `blocked` with its files' paths. Publish them yourself by path, then continue at step 3.

**The user edited the canvas by hand.** Read the canvas before the next revision, and name its served files in the designer's brief. A publish over a hand edit is refused and names the file to read again.

**A build checkpoint names no approved design.** The build gate fails. Run the page unit first, then add its folder to the checkpoint's Inputs.

## See Also

- design:user-research: related; plans research with real users for the experience core.
- design:research-synthesis: related; turns research evidence into themes for the experience core.
- design:design-system: related; audits and extends the tokens and components in the design system unit.
- design:ux-copy: related; writes and reviews the copy of a page and of every text unit.
- design:accessibility-review: related; audits a mockup and a built page against WCAG 2.1 AA.
- design:design-critique: related; critiques a mockup and a built page against the core's goals.
- design:design-handoff: related; fills a unit's `handoff.md` at approval.
- dataviz: related; governs every chart on a page.
