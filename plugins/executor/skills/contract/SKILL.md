---
name: contract
description: Write, upgrade, or check plan checkpoints as four-field contracts (Inputs, Deliverable, Acceptance, Non-goals). Use when drafting a plan, adding or rewriting a checkpoint, upgrading an old checkpoint to the contract, or checking that a plan's checkpoints are well formed before work starts.
---

# Contract

A checkpoint is a contract: a delegate or a later session can build it from the text alone, and anyone can tell whether it is done.

## Grammar

Inside a plan's checkpoints section, each checkpoint is:

```
#### Checkpoint <N>: <title>

**Inputs:** ...

**Deliverable:** ...

**Acceptance:** clause one; clause two; clause three.

**Non-goals:** ...
```

- The heading is exactly `#### Checkpoint <N>: <title>`. Add ` - COMPLETE` to the end once it is done.
- The four fields appear in that order, each starting its own paragraph with the bold label, each non-empty.
- **Inputs** names what must exist or be read first: files, earlier checkpoints, sections.
- **Deliverable** names what gets created or changed, by path.
- **Acceptance** is clauses separated by `;`. Each clause names an observable: a command or file in a code span, or a count (a number). A clause with neither fails. Split a clause that mixes a checkable part and a vague part.
- **Non-goals** names what this checkpoint deliberately leaves out.
- Once done, a short report may follow Non-goals as further paragraphs (cost, questions, notes).
- A change to a completed checkpoint is a new checkpoint that names what it overrides.

## Runnable clauses

The gate (`scripts/gate.py`) decides two clause shapes without judgment; the verifier judges the rest.

```
**Acceptance:** `$ python3 -m pytest -q`; `src/a.py` exists; `f` documents its return value.
```

- **Command:** a code span starting with `$ ` (dollar, space). The gate runs it in the working dir with a timeout. The clause passes iff every command span in it exits 0, so its text must claim nothing beyond that.
- **Existence:** a clause that is exactly one code span followed by `exists`. The gate checks the path under the working dir.
- Anything else is `not_run` and goes to the verifier, as the third clause above does. A clause like "pytest passes with at least 4 tests" is judgment; split it into a command clause and a counted clause.

## Writing a checkpoint

1. Size it to one commit that can be validated alone.
2. Write Acceptance first. If a clause cannot name a command, file, or count, the checkpoint is not understood yet.
3. Write Deliverable so every path an Acceptance clause names is created by it.
4. Fill Inputs and Non-goals.

## A screen in a plan

A plan states each screen's jobs and the data it shows, and leaves its layout to the design. Name no layout, panel, or tab before a design for it is approved. A build checkpoint for a screen names the approved design's folder under Inputs, as an existence clause such as `` `artifacts/design/outlook/` exists ``; rendering its brief fails while the folder is missing.

## Upgrading an old checkpoint

Map existing prose onto the four fields without dropping content. Keep each statement of intent where it fits; turn vague criteria into observable clauses, and ask the user when the observable is not recoverable from the text.

## Starting a plan

A project holds any number of plans, one per intent, in its plan directory. Copy `plan.template.md` from this skill's directory there as `<intent>-plan.md`, then replace the goal, decisions, and example checkpoint. Checkpoint numbers are scoped to their plan.

## Check after every edit

Run the checker on the plan after every edit and fix what it names:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/contract_check.py <plan>.md
```

Failures print one per line, such as `Checkpoint 3: missing Non-goals`. Exit 0 prints `ok: <n> checkpoints`; exit 1 means failures; exit 2 means the file has no checkpoints. `--json` prints the parsed checkpoints. The checker reads markdown only and never runs acceptance commands.
