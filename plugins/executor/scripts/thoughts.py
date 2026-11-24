"""Thought ledger: one markdown line per item plus a JSON record beside it.

Ledger path comes from the profile key thoughts_ledger (override: --ledger PATH).
Line: - [ ] <YYYY-MM-DD> | <category> | <cue> | <text> ^<id>   ([x] done, [-] dropped)
Records: <ledger dir>/thoughts/<id>.json

Commands:
  python3 thoughts.py add --category C --text T [--cue Q] [--project P] [--record JSON]
  python3 thoughts.py list [--project P] [--category C]
  python3 thoughts.py surfaced ID
  python3 thoughts.py done ID | drop ID
  python3 thoughts.py snooze ID --until YYYY-MM-DD
"""
import argparse
import json
import os
import re
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

import toolkit_profile as profile

CATEGORIES = ["buy", "do", "schedule", "idea", "question", "note"]
LINE = re.compile(r"^- \[(.)\] (\S+) \| (.*?) \| (.*?) \| (.*) \^(\w+)$")
TEMPLATE = (
    "# Reminders\n\n"
    "Captured by the make-task-reminder skill, one line per item. "
    "Check a box when done; change `[ ]` to `[-]` to drop.\n\n"
    "## Open\n\n"
)
CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def new_id() -> str:
    # -- ULID: 48-bit ms time + 80 random bits, Crockford base32
    n = (int(time.time() * 1000) << 80) | int.from_bytes(os.urandom(10), "big")
    return "".join(CROCKFORD[(n >> s) & 31] for s in range(125, -1, -5))


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def clean(s: str) -> str:
    return " ".join(s.split()).replace(" | ", " / ")


def rec_path(ledger: Path, tid: str) -> Path:
    return ledger.parent / "thoughts" / f"{tid}.json"


def load_rec(ledger: Path, tid: str) -> dict:
    p = rec_path(ledger, tid)
    return json.loads(p.read_text()) if p.is_file() else {}


def save_rec(ledger: Path, tid: str, rec: dict):
    p = rec_path(ledger, tid)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec, indent=2) + "\n")


def items(ledger: Path):
    """Yield (lineno, state, date, category, cue, text, id) for each ledger line."""
    if not ledger.is_file():
        return
    for i, line in enumerate(ledger.read_text().splitlines()):
        m = LINE.match(line)
        if m:
            yield (i, *m.groups())


def open_items(ledger: Path, project=None, category=None):
    """Open, unsnoozed items as dicts, newest first."""
    today = date.today().isoformat()
    out = []
    for _, st, d, cat, cue, text, tid in items(ledger):
        if st != " " or (category and cat != category):
            continue
        rec = load_rec(ledger, tid)
        slug = (rec.get("project") or {}).get("slug")
        until = ((rec.get("surface") or {}).get("snoozed_until") or "")[:10]
        if (project and slug != project) or until > today:
            continue
        out.append(dict(id=tid, date=d, category=cat, cue=cue, text=text, project=slug))
    return sorted(out, key=lambda x: x["id"], reverse=True)


def add(ledger: Path, a):
    if not ledger.is_file():
        ledger.parent.mkdir(parents=True, exist_ok=True)
        ledger.write_text(TEMPLATE)
    tid, text = new_id(), clean(a.text)
    line = f"- [ ] {date.today().isoformat()} | {a.category} | {clean(a.cue)} | {text} ^{tid}"
    lines = ledger.read_text().splitlines()
    at = lines.index("## Open") + 1 if "## Open" in lines else len(lines)
    while at < len(lines) and not lines[at].strip():
        at += 1
    # -- open items are newest first, so insert at the top of the section
    lines.insert(at, line)
    ledger.write_text("\n".join(lines) + "\n")
    ts = now()
    rec = {
        "id": tid, "schema_version": 1, "captured_at": ts,
        "source": {"layer": "claude-code"}, "raw": text, "text": text,
        "category": a.category, "surface": {"mode": "on_demand"},
        "action": {"kind": "none", "status": "skipped"},
        "routing": {"stage": "model"}, "state": "open",
        "events": [{"at": ts, "kind": "captured", "source": "claude-code"}],
    }
    if a.project:
        rec["project"] = {"slug": a.project}
        rec["surface"] = {"mode": "on_project_session"}
    rec.update(json.loads(a.record) if a.record else {})
    save_rec(ledger, tid, rec)
    print(tid)


def show(ledger: Path, a):
    found = open_items(ledger, a.project, a.category)
    for cat in CATEGORIES:
        group = [x for x in found if x["category"] == cat]
        if not group:
            continue
        print(f"{cat}:")
        if cat == "idea":
            for proj in sorted({x["project"] or "" for x in group}):
                print(f"  [{proj or 'no project'}]")
                for x in (x for x in group if (x["project"] or "") == proj):
                    print(f"    {fmt(x)}")
        else:
            for x in group:
                print(f"  {fmt(x)}")


def fmt(x) -> str:
    cue = f" ({x['cue']})" if x["cue"] else ""
    return f"{x['text']}{cue} ^{x['id']}"


def event(ledger: Path, tid: str, kind: str, payload=None):
    rec = load_rec(ledger, tid)
    if not rec:
        return
    ev = {"at": now(), "kind": kind, "source": "claude-code"}
    if payload:
        ev["payload"] = payload
    rec["events"].append(ev)
    save_rec(ledger, tid, rec)


def flip(ledger: Path, tid: str, mark: str, kind: str):
    lines = ledger.read_text().splitlines()
    for i, st, *_, lid in items(ledger):
        if lid == tid:
            lines[i] = lines[i].replace(f"[{st}]", f"[{mark}]", 1)
            ledger.write_text("\n".join(lines) + "\n")
            event(ledger, tid, kind)
            return
    sys.exit(f"no such id: {tid}")


def snooze(ledger: Path, tid: str, until: str):
    date.fromisoformat(until)
    rec = load_rec(ledger, tid)
    rec.setdefault("surface", {"mode": "on_demand"})["snoozed_until"] = f"{until}T00:00:00Z"
    rec["events"].append({"at": now(), "kind": "snoozed", "source": "claude-code",
                          "payload": {"until": until}})
    save_rec(ledger, tid, rec)


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--ledger")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("add")
    s.add_argument("--category", required=True, choices=CATEGORIES)
    s.add_argument("--text", required=True)
    s.add_argument("--cue", default="")
    s.add_argument("--project")
    s.add_argument("--record")
    s = sub.add_parser("list")
    s.add_argument("--project")
    s.add_argument("--category", choices=CATEGORIES)
    for name in ("surfaced", "done", "drop", "snooze"):
        s = sub.add_parser(name)
        s.add_argument("id")
        if name == "snooze":
            s.add_argument("--until", required=True)
    a = p.parse_args()
    ledger = Path(a.ledger or profile.get("thoughts_ledger")).expanduser()
    if a.cmd == "add":
        add(ledger, a)
    elif a.cmd == "list":
        show(ledger, a)
    elif a.cmd == "surfaced":
        event(ledger, a.id, "surfaced")
    elif a.cmd == "done":
        flip(ledger, a.id, "x", "done")
    elif a.cmd == "drop":
        flip(ledger, a.id, "-", "dropped")
    else:
        snooze(ledger, a.id, a.until)


if __name__ == "__main__":
    main()
