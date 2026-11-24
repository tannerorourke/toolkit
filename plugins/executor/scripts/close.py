"""Write the close-port trace of a run from its gate files.

  python3 close.py --project NAME --plan PATH [--cwd DIR] [--decision TEXT ...]
      [--friction TEXT] [--outcome N=accepted|rejected|blocked|abandoned ...]
      [--verifier-fail N ...] [--rework-contract N ...] [--keep-gates]
Reads <cwd>/.executor/gates/*.json for PATH, groups by checkpoint, validates the trace
against trace.schema.json, and creates <traces_dir>/<project>/<run_id>.json (never
overwrites). Prints the path.
  rework_count: gated runs of a checkpoint minus one
  outcome: --outcome, else blocked if the last gate blocked, else abandoned
  verifier failures: only from --verifier-fail (verifier returns are not gated)
  friction: at most 200 words
  consumed gate files move to <cwd>/.executor/gates/closed/<run_id>/ so the next
  close cannot recount them; --keep-gates leaves them
"""
import argparse
import json
import shutil
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import jsonschema

sys.path.insert(0, str(Path(__file__).resolve().parent))
import toolkit_profile as profile  # noqa: E402
from contract_check import parse  # noqa: E402

SCHEMA = Path(__file__).resolve().parent.parent / "trace.schema.json"
OUTCOMES = ("accepted", "rejected", "blocked", "abandoned")
MAX_WORDS = 200


def iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).isoformat(timespec="seconds")


def read_gates(cwd: Path, plan: Path) -> list[tuple[float, Path, dict]]:
    found = []
    for f in (cwd / ".executor" / "gates").glob("*.json"):
        g = json.loads(f.read_text())
        if Path(g["plan"]).resolve() == plan:
            found.append((f.stat().st_mtime, f, g))
    return sorted(found, key=lambda t: t[0])


def build(args, gates, now: datetime, run_id: str) -> dict:
    titles = {cp["number"]: cp["title"] for cp in parse(args.plan.read_text())}
    outcomes = dict(o.split("=", 1) for o in args.outcome)
    by_cp = defaultdict(list)
    for _, _, g in gates:
        by_cp[g["checkpoint"]].append(g)
    numbers = sorted(set(by_cp) | set(map(int, outcomes)) | set(args.verifier_fail))
    checkpoints = []
    for n in numbers:
        runs = by_cp[n]
        last = runs[-1]["verdict"] if runs else None
        checkpoints.append({
            "number": n,
            "title": titles[n],
            "outcome": outcomes.get(str(n), "blocked" if last == "blocked" else "abandoned"),
            "rework_count": max(len(runs) - 1, 0),
            "gate_verdicts": [g["verdict"] for g in runs],
            "verifier_failures": args.verifier_fail.count(n),
            "deviations": [d for g in runs for d in (g["return"] or {}).get("deviations", [])],
        })
    return {
        "schema_version": 1,
        "run_id": run_id,
        "project": args.project,
        "plan": str(args.plan),
        "opened": iso(gates[0][0]) if gates else now.isoformat(timespec="seconds"),
        "closed": now.isoformat(timespec="seconds"),
        "checkpoints": checkpoints,
        "decisions": args.decision,
        "contracts_reworked": {"count": len(set(args.rework_contract)), "which": sorted(set(args.rework_contract))},
        "verifier_failures": len(args.verifier_fail),
        "deviation_notes": [d for c in checkpoints for d in c["deviations"]],
        "friction": args.friction,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--plan", required=True, type=lambda p: Path(p).resolve())
    ap.add_argument("--cwd", default=".", type=lambda p: Path(p).resolve())
    ap.add_argument("--decision", action="append", default=[])
    ap.add_argument("--friction", default="")
    ap.add_argument("--outcome", action="append", default=[], metavar="N=OUTCOME")
    ap.add_argument("--verifier-fail", action="append", default=[], type=int, metavar="N")
    ap.add_argument("--rework-contract", action="append", default=[], type=int, metavar="N")
    ap.add_argument("--keep-gates", action="store_true")
    args = ap.parse_args()
    if len(args.friction.split()) > MAX_WORDS:
        sys.exit(f"friction is over {MAX_WORDS} words")

    now = datetime.now(timezone.utc)
    run_id = now.strftime("%Y%m%dT%H%M%S%fZ")
    gates = read_gates(args.cwd, args.plan)
    trace = build(args, gates, now, run_id)
    jsonschema.Draft202012Validator(json.loads(SCHEMA.read_text())).validate(trace)

    out = Path(profile.get("traces_dir")) / args.project / f"{run_id}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x") as f:
        f.write(json.dumps(trace, indent=2) + "\n")
    if not args.keep_gates:
        dest = args.cwd / ".executor" / "gates" / "closed" / run_id
        dest.mkdir(parents=True)
        for _, f, _ in gates:
            shutil.move(f, dest / f.name)
    print(out)


if __name__ == "__main__":
    main()
