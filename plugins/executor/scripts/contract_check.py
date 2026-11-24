"""Check a plan's checkpoints against the four-field contract.

Used by: the contract skill, after every plan edit.
  python3 contract_check.py <plan.md>          one line per failure; exit 1 on any, 2 if no checkpoints
  python3 contract_check.py <plan.md> --json   print the parsed checkpoints
Import: parse(text) returns a list of checkpoint dicts; check(cp) returns failure strings.
"""
import argparse
import json
import re
import sys
from pathlib import Path

FIELDS = ("Inputs", "Deliverable", "Acceptance", "Non-goals")
HEADING = re.compile(r"^#### Checkpoint (\d+): (.+?)( - COMPLETE)?\s*$")
LABEL = re.compile(r"^\*\*(Inputs|Deliverable|Acceptance|Non-goals):\*\*[ \t]*(.*)$")
ANY_HEADING = re.compile(r"^#{1,6} ")
SPAN = re.compile(r"`[^`]+`")
NUMBER = re.compile(
    r"\d|\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten)\b", re.I
)


def split_clauses(text: str) -> list[str]:
    # -- split on ; outside code spans
    parts, last = [], 0
    spans = [m.span() for m in SPAN.finditer(text)]
    for i, ch in enumerate(text):
        if ch == ";" and not any(a <= i < b for a, b in spans):
            parts.append(text[last:i])
            last = i + 1
    parts.append(text[last:])
    return [p.strip().rstrip(".").strip() for p in parts if p.strip().rstrip(".").strip()]


def names_observable(clause: str) -> bool:
    return bool(SPAN.search(clause) or NUMBER.search(clause))


def parse(text: str) -> list[dict]:
    checkpoints, current, field = [], None, None
    for line in text.splitlines():
        m = HEADING.match(line)
        if m:
            current = {
                "number": int(m.group(1)),
                "title": m.group(2),
                "complete": bool(m.group(3)),
                "fields": {},
                "order": [],
                "acceptance_clauses": [],
            }
            checkpoints.append(current)
            field = None
            continue
        if current is None:
            continue
        if ANY_HEADING.match(line):
            current, field = None, None
            continue
        m = LABEL.match(line)
        if m:
            field = m.group(1)
            current["order"].append(field)
            current["fields"].setdefault(field, m.group(2).strip())
        elif not line.strip():
            field = None
        elif field:
            current["fields"][field] = (current["fields"][field] + " " + line.strip()).strip()
    for cp in checkpoints:
        cp["acceptance_clauses"] = split_clauses(cp["fields"].get("Acceptance", ""))
    return checkpoints


def check(cp: dict) -> list[str]:
    name = f"Checkpoint {cp['number']}"
    out = [f"{name}: missing {f}" for f in FIELDS if f not in cp["order"]]
    out += [f"{name}: empty {f}" for f in FIELDS if f in cp["order"] and not cp["fields"][f]]
    present = [f for f in cp["order"] if f in FIELDS]
    if not out and present != list(FIELDS):
        out.append(f"{name}: fields out of order, expected {', '.join(FIELDS)}")
    out += [
        f"{name}: acceptance clause names no observable: {c}"
        for c in cp["acceptance_clauses"]
        if not names_observable(c)
    ]
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    checkpoints = parse(Path(args.plan).read_text())
    if args.json:
        print(json.dumps(checkpoints, indent=2))
    if not checkpoints:
        print("no checkpoints found", file=sys.stderr)
        return 2
    failures = [f for cp in checkpoints for f in check(cp)]
    if args.json:
        return 1 if failures else 0
    for f in failures:
        print(f)
    if failures:
        return 1
    print(f"ok: {len(checkpoints)} checkpoints")
    return 0


if __name__ == "__main__":
    sys.exit(main())
