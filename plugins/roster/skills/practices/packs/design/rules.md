# Design: gui

How a product designer turns a product's jobs and objects into screens.

Read this before every `gui` unit. Each step below settles one decision, in order. The structure unit runs steps 1 to 6; the design system unit runs steps 9 and 10 for the whole product; a page unit runs steps 7 to 10 for its page. Every unit closes with steps 11 and 12. When the core or an approved earlier unit already settled a step, carry its decision forward.

## 1. Frame the work

Decision: the primary jobs, the application's posture, and how success is measured.

Output: 3 to 7 job stories and a posture label.

Rules:

- Write each job as "When ___, I want to ___, so I can ___", and design for the situation it names. Prefer job stories to a cast of personas ([Intercom, How we accidentally invented Job Stories](https://www.intercom.com/blog/accidentally-invented-job-stories/)).
- Decide posture before layout: give a sovereign app, one that holds attention for long sessions, dense and persistent controls; give a transient tool one high-relief function ([Wikipedia, Application posture](https://en.wikipedia.org/wiki/Application_posture); limited evidence).
- State the measure that tells you each job went well ([Goodwin interview, Center Centre](https://articles.centercentre.com/?p=135)).

Pass condition: each job story names a situation, and the posture is sovereign or transient.

## 2. Analyze the tasks

Decision: which tasks are primary, which are secondary, and the key paths.

Output: a task hierarchy with each task's frequency and criticality.

Rules:

- Rank tasks by frequency and criticality; put the frequent and critical ones in the primary display and defer the rest ([NN/g, Task Analysis](https://www.nngroup.com/articles/task-analysis/); [NN/g, Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/)).

Pass condition: every task carries a frequency and a criticality, and the primary set is named.

## 3. Model the objects

Decision: the nouns, their relationships, their actions, and their ranked attributes.

Output: one table per object listing relationships, calls to action, and attributes in rank order; an object map.

Rules:

- Model objects before actions: forage the nouns from the job stories, list each object's content and metadata, nest related objects inside each other, and force-rank attributes before any layout ([Prater, Object-Oriented UX](https://alistapart.com/article/object-oriented-ux/); [OOUX, What is OOUX](https://www.ooux.com/what-is-ooux)).
- Treat calendars, maps, tables, and catalogs as views of objects, and find the object each one shows ([Prater, Object-Oriented UX](https://alistapart.com/article/object-oriented-ux/)).
- Let related objects link to each other in context, and keep the top navigation as the fire escape ([Prater, Object-Oriented UX](https://alistapart.com/article/object-oriented-ux/)).

Pass condition: every noun in the job stories maps to an object or a view, and each object's attributes are ranked.

## 4. Choose page types and navigation

Decision: one page type per object and task; flat or hierarchical navigation; where list-detail, a supporting pane, or a wizard applies.

Output: a sitemap with a page type for each page.

Rules:

- Pick a page type per object and task: an index or list report to find and act, a worklist to process a queue, an object page for one object, an overview for a cross-domain glance, and a wizard only for long or unfamiliar steps that are loosely coupled ([SAP Fiori, Floorplan overview](https://www.sap.com/design-system/fiori-design-web/v1-38/page-types/floorplan-overview); [Shopify, App layout](https://shopify.dev/docs/apps/design/layout.md); [NN/g, Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/)).
- Use flat navigation for fewer than 8 distinct peer pages and hierarchy for more than 7 or for parent-child relations; add a breadcrumb past two levels; avoid pogo-sticking between list and detail ([Microsoft, Navigation basics](https://learn.microsoft.com/en-us/windows/apps/design/basics/navigation-basics)).
- Use list-detail when the detail stands on its own and a supporting pane when its content makes sense only beside the main content ([Android, Canonical layouts](https://developer.android.com/develop/adaptive-apps/guides/canonical-layouts)).

Pass condition: every page has one page type, and every object from step 3 is reachable.

## 5. Set each screen's priority

Decision: the one question each screen answers, what holds the prime position, and what waits behind disclosure.

Output: a ranked content list per screen, headed by its question.

Rules:

- Give each screen one primary question and put its answer in the prime position; demote logos and navigation ([Few, Common Pitfalls in Dashboard Design](https://www.perceptualedge.com/articles/Whitepapers/Common_Pitfalls.pdf)).
- Cap progressive disclosure at two levels and label the path to the second ([NN/g, Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/)).
- Pair every number with a comparison, such as a target or the prior period, and a qualitative state ([Few, Common Pitfalls in Dashboard Design](https://www.perceptualedge.com/articles/Whitepapers/Common_Pitfalls.pdf)).
- Round to the precision the decision needs: $3.8M for a quarterly total ([Few, Common Pitfalls in Dashboard Design](https://www.perceptualedge.com/articles/Whitepapers/Common_Pitfalls.pdf)).
- Keep a monitoring dashboard to one screen, and move exploration to an analytical view ([Few, Common Pitfalls in Dashboard Design](https://www.perceptualedge.com/articles/Whitepapers/Common_Pitfalls.pdf); [NN/g, Dashboards](https://www.nngroup.com/articles/dashboards-preattentive/)).
- Structure an exploratory view as overview first, then zoom and filter, then details on demand, all without leaving the primary screen ([Shneiderman, The Eyes Have It](https://drum.lib.umd.edu/items/155a868e-fb83-4115-9899-9187ea8c0498); [NN/g, 8 Design Guidelines for Complex Applications](https://www.nngroup.com/articles/complex-application-design/)).

Pass condition: every screen states one question, and the first item on its list answers it.

## 6. Draw low-fidelity layouts

Decision: regions, grouping, the split between inputs and outputs, and density, with no visual styling.

Output: 2 or 3 grayscale layout alternatives for each key screen in `artboards/`, filled with realistic synthetic data.

Rules:

- Lock structure at low fidelity in grayscale with realistic data; add type, color, and effects only after the structure passes critique ([Goodwin interview, Center Centre](https://articles.centercentre.com/?p=135); [Refactoring UI notes](https://github-wiki-see.page/m/KeynesYouDigIt/Knowledge/wiki/Refactoring-UI); [NN/g, UX Prototypes: Low vs High Fidelity](https://www.nngroup.com/articles/ux-prototype-hi-lo-fidelity/); [NN/g, Prompt to Design Interfaces](https://www.nngroup.com/articles/vague-prototyping/)).
- Put configuration inputs in a supporting pane of about 30% width and the visualization or preview in the main area; keep the selection that drives the detail highlighted ([Android, Canonical layouts](https://developer.android.com/develop/adaptive-apps/guides/canonical-layouts); [Apple HIG, Split views](https://developer.apple.com/design/human-interface-guidelines/split-views); [Shopify, App layout](https://shopify.dev/docs/apps/design/layout.md); [Tidwell, Overview Beside Detail](https://www.mit.edu/~jtidwell/language/overview_beside_detail.html)).
- Emphasize by removing or muting surrounding elements before adding emphasis ([NN/g, 8 Design Guidelines for Complex Applications](https://www.nngroup.com/articles/complex-application-design/); [Refactoring UI notes](https://github-wiki-see.page/m/KeynesYouDigIt/Knowledge/wiki/Refactoring-UI)).
- Hold one density per page, one primary action per card, and one severity signal per table row ([Shopify, App layout](https://shopify.dev/docs/apps/design/layout.md)).

Pass condition: the alternatives differ in structure, each holds realistic data, and none uses color.

## 7. Specify every state

Decision: what each data region shows and says in every state.

Output: a state table for each data region on the page.

Rules:

- Before any visual design, specify each data region's states: loading; empty for a new user, empty after filtering, and empty because nothing exists or access is blocked; error; sparse; dense; long text; missing value ([Carbon, Empty states](https://carbondesignsystem.com/patterns/empty-states-pattern/); [Vercel, Web Interface Guidelines](https://vercel.com/design/guidelines); [Anthropic, design-handoff](https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/design/skills/design-handoff/SKILL.md)).
- Never leave a region blank, and never show "no results" while it loads ([NN/g, Designing Empty States in Complex Applications](https://www.nngroup.com/articles/empty-state-interface-design/)).
- Make each empty state say why it is empty and offer one next step, in place of the element it replaces ([Carbon, Empty states](https://carbondesignsystem.com/patterns/empty-states-pattern/); [Atlassian, Empty state](https://atlassian.design/foundations/content/designing-messages/empty-state); [Anthropic, ux-copy](https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/design/skills/ux-copy/SKILL.md)).
- Show no indicator under 1 s, a spinner for one module, a skeleton for a full-page load under 10 s, and a progress bar with an estimate beyond 10 s ([NN/g, Response Times](https://www.nngroup.com/articles/response-times-3-important-limits/); [NN/g, Skeleton Screens 101](https://www.nngroup.com/articles/skeleton-screens/)). Carbon skeletonizes tables and cards one by one ([Carbon, Loading](https://carbondesignsystem.com/patterns/loading-pattern/)); pick one convention and record it in the design system.

No public source covers stale live data, reconnecting, or a paused stream. When a region shows live data, ask the brief's author how it looks and behaves in each of those three states, and record the answer as the author's decision.

Pass condition: every region has a row for each state above, and each row gives both the display and its copy.

## 8. Set the interaction rules

Decision: live update or Apply, feedback by latency, Undo or confirmation, what the URL holds, and keyboard paths.

Output: an interaction spec for the page.

Rules:

- Update outputs live when recomputation returns within about 1 s; otherwise batch them behind an Apply button ([NN/g, User Intent Affects Filter Design](https://www.nngroup.com/articles/applying-filters/); [NN/g, Response Times](https://www.nngroup.com/articles/response-times-3-important-limits/); [Maersk, Filter patterns](https://designsystem.maersk.com/guidelines/search-filter-and-sort/filter-patterns/)). While inputs are unapplied, show that the results no longer match them ([DWP Design System, filters](https://design-system.dwp.gov.uk/); limited evidence).
- Persist filters, tabs, pagination, and panel state in the URL; prefer Undo to a confirmation for reversible actions, and confirm irreversible ones ([Vercel, Web Interface Guidelines](https://vercel.com/design/guidelines)).

Pass condition: every input names live or Apply with its expected latency, and every destructive action names Undo or a confirmation.

## 9. Write the copy

Decision: labels, actions, errors, and empty-state text, with one term per concept. The design system unit also sets the voice all copy follows.

Output: a copy deck for the page; voice rules in the design system.

Rules:

- Place each error next to its source and say in plain words what happened and how to fix it; preserve the user's input; leave out blame and error codes ([NN/g, Error-Message Guidelines](https://www.nngroup.com/articles/error-message-guidelines/); [Microsoft, Error Message Guidelines](https://learn.microsoft.com/en-us/windows/win32/debug/error-message-guidelines); [Google, Writing helpful error messages](https://developers.google.com/tech-writing/error-messages); [Carbon, Empty states](https://carbondesignsystem.com/patterns/empty-states-pattern/)).
- Label each action with a verb and a noun, such as "Delete 3 files"; never "OK" or "Submit" ([Vercel, Teaching agents product design](https://vercel.com/blog/teaching-agents-product-design-at-vercel); [Anthropic, ux-copy](https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/design/skills/ux-copy/SKILL.md)).
- Use one term per concept across the product ([Anthropic, ux-copy](https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/design/skills/ux-copy/SKILL.md)).
- Write errors without apologies or jokes, and make a message shorter the more often it appears ([Anthropic, frontend-design](https://raw.githubusercontent.com/anthropics/skills/HEAD/skills/frontend-design/SKILL.md); [Carbon, Empty states](https://carbondesignsystem.com/patterns/empty-states-pattern/); [Atlassian, Empty state](https://atlassian.design/foundations/content/designing-messages/empty-state)).

Pass condition: no action reads "OK" or "Submit", every error names a fix, and each concept has one term.

## 10. Set the visual system

Decision: tokens, the type scale, color reserved for meaning, chart encodings, and the component inventory with each component's states.

Output: for the design system unit, a token set, chart rules, and a component inventory; for a page unit, the page drawn in that system as a clickable mockup in `artboards/`, with every state from step 7 reachable.

Rules:

- For a data-dense brief, specify a concrete visual system or offer a choice among 2 or 3 drawn directions, never a list of things to avoid; a list of avoidances only moves the output to another default ([Anthropic, Prompting Claude Opus 4.8](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8); [Anthropic, Improving frontend design through Skills](https://claude.com/blog/improving-frontend-design-through-skills)).
- Encode quantity with position and length; use color only to reinforce what another channel already shows, never for magnitude; drop pies, gauges, 3D, and decorative chrome ([NN/g, Dashboards](https://www.nngroup.com/articles/dashboards-preattentive/); [Few, Common Pitfalls in Dashboard Design](https://www.perceptualedge.com/articles/Whitepapers/Common_Pitfalls.pdf); [Stasko, Tufte lecture notes](https://faculty.cc.gatech.edu/~stasko/4460/Notes/tufte.pdf)).
- Use tabular numerals and the same decimal places in comparable columns ([Vercel, Web Interface Guidelines](https://vercel.com/design/guidelines)).
- Spend boldness in one place at most, and remove decoration from data displays ([Anthropic, frontend-design](https://raw.githubusercontent.com/anthropics/skills/HEAD/skills/frontend-design/SKILL.md); [Few, Common Pitfalls in Dashboard Design](https://www.perceptualedge.com/articles/Whitepapers/Common_Pitfalls.pdf)).
- Give every component its states: default, hover, active, disabled, loading, error, and empty ([Anthropic, design-handoff](https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/design/skills/design-handoff/SKILL.md)).

Pass condition: every color, type size, and spacing comes from a token, and no quantity is carried by color alone.

## 11. Critique

Decision: what to fix before submitting the unit.

Output: findings, each rated from P0 (blocks release) to P3.

Rules:

- Critique against goals agreed in advance, the job stories and each screen's question; reframe opinions as questions about the goal; rate findings by severity ([NN/g, Design Critiques](https://www.nngroup.com/articles/design-critiques/); [Anthropic, design-critique](https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/design/skills/design-critique/SKILL.md); [Impeccable README](https://cdn.jsdelivr.net/npm/impeccable@2.3.2/README.repo.md)).
- Check the design against the ten usability heuristics ([NN/g, 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)).

Pass condition: no P0 or P1 finding remains open.

## 12. Approve and hand off

Decision: ship the unit or revise it.

Output: `handoff.md` covering every state, edge case, accessibility need, and responsive change, with the reasoning behind each decision.

Rules:

- Specify everything the builder needs; what you leave out, the developer will guess ([Anthropic, design-handoff](https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/design/skills/design-handoff/SKILL.md)).
- Lint what code can check, keep judgment in prose, and never generalize a rule from one example ([Vercel, Teaching agents product design](https://vercel.com/blog/teaching-agents-product-design-at-vercel)).

Pass condition: a builder could build each page from `handoff.md` and `artboards/` without asking a question.
