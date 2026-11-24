# Project plan

## Goal

One paragraph: what this project delivers and for whom.

## Decisions

| Decision | Choice | Why |
| -------- | ------ | --- |
| Language | Python 3.11, stdlib only | No install step for users |
| Layout | One package, one CLI entry point | Small surface to test |

## Checkpoints

Commit-sized and individually validated. When a checkpoint is done, append a short report under it. A change to a completed checkpoint is a new checkpoint that names what it overrides.

#### Checkpoint 1: word-count CLI

**Inputs:** an empty repository with Python 3.11.

**Deliverable:** `wc_tool.py` printing the word count of the file named on its command line, and `test_wc_tool.py` with its tests.

**Acceptance:** `python3 wc_tool.py sample.txt` prints `3` for a file containing three words; `python3 -m unittest test_wc_tool` exits 0 with 2 tests run; `python3 wc_tool.py missing.txt` exits 2.

**Non-goals:** no directory recursion; no option flags; no packaging.

#### Checkpoint 2: summary screen

**Inputs:** Checkpoint 1; `artifacts/design/summary/` exists.

**Deliverable:** `summary.html`, built from the approved design in `artifacts/design/summary/`: it answers "how long is this file?" with the word count in the prime position and the line count beside it.

**Acceptance:** `summary.html` exists; `python3 wc_tool.py --html sample.txt` writes `summary.html` showing `3 words`; the page matches every state in `artifacts/design/summary/handoff.md`, checked by the verifier.

**Non-goals:** no layout decided here; no styling beyond the approved design's tokens.

