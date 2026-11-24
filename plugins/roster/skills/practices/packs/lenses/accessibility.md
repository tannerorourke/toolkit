# Lens: accessibility

Judge whether a page or prototype meets WCAG 2.1 AA, before it is shown for approval and again once built.

The brief gives you the artifact as files: the prototype's HTML and CSS, or the built page's source, and a screenshot of each state. It may also give the output of a contrast or keyboard check the orchestrator ran.

Skill: invoke `design:accessibility-review` on the files the brief names, and fold its output into findings.

## Rubric

| Check | Fails when | Severity |
| --- | --- | --- |
| Contrast | Body text falls below 4.5:1, large text or a control's boundary below 3:1 | high |
| Keyboard | A control cannot be reached, operated, or left by keyboard, or focus is invisible | high |
| Names | A control, image, or region has no accessible name, or a name that differs from its visible label | high |
| Colour alone | State or meaning is carried by colour with no text, icon, or pattern | high |
| Live updates | A value that changes on its own is not announced, or is announced on every tick | medium |
| Targets | A pointer target is under 24 by 24 CSS pixels with no spacing exemption, per WCAG 2.2 success criterion 2.5.8, which this lens adds to 2.1 AA | medium |
| Reflow | Content is lost or needs two-way scrolling at 320 CSS pixels wide or 200% zoom | medium |
| Motion | Motion over 5 seconds cannot be paused, or ignores a reduced-motion preference | low |

Name the WCAG success criterion in each finding.

## Never shown

The designer's rationale and earlier rounds. Judge the files.
