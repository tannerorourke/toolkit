"""Run a checkpoint's deterministic acceptance clauses and report per clause.

  python3 gate.py <plan.md> <N> [--cwd DIR] [--timeout SECONDS]
Prints gate JSON on stdout; exit 0 on verdict pass, 1 on fail, 2 if the checkpoint
does not exist. Clause rules (see the contract skill):
  a code span starting with "$ " is a command, run in DIR; the clause passes iff every one exits 0
  a clause that is exactly a code span then "exists" checks that path under DIR
  anything else is not_run, left to the verifier
Import: run(plan, n, cwd, timeout) returns the gate dict.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contract_check import parse  # noqa: E402

COMMAND = re.compile(r"`\$ ([^`]+)`")
EXISTS = re.compile(r"^`([^`$][^`]*)` exists$")
TAIL = 2000


def run_command(cmd: str, cwd: Path, timeout: int) -> dict:
    try:
        p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"command": cmd, "exit_code": None, "reason": f"timeout after {timeout}s"}
    out = {"command": cmd, "exit_code": p.returncode}
    if p.returncode:
        out["output_tail"] = (p.stdout + p.stderr)[-TAIL:]
    return out


def judge(clause: str, cwd: Path, timeout: int) -> dict:
    cmds = COMMAND.findall(clause)
    if cmds:
        runs = [run_command(c, cwd, timeout) for c in cmds]
        ok = all(r["exit_code"] == 0 for r in runs)
        return {"clause": clause, "result": "pass" if ok else "fail", "check": "command", "runs": runs}
    m = EXISTS.match(clause)
    if m:
        ok = (cwd / m.group(1)).exists()
        return {"clause": clause, "result": "pass" if ok else "fail", "check": "exists",
                "path": m.group(1), "reason": "present" if ok else "missing"}
    return {"clause": clause, "result": "not_run", "check": None, "reason": "needs judgment"}


def run(plan: Path, n: int, cwd: Path, timeout: int) -> dict | None:
    cps = [c for c in parse(plan.read_text()) if c["number"] == n]
    if not cps:
        return None
    clauses = [judge(c, cwd, timeout) for c in cps[0]["acceptance_clauses"]]
    return {
        "plan": str(plan.resolve()),
        "checkpoint": n,
        "cwd": str(cwd.resolve()),
        "verdict": "fail" if any(c["result"] == "fail" for c in clauses) else "pass",
        "clauses": clauses,
        "not_run": [c["clause"] for c in clauses if c["result"] == "not_run"],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("n", type=int)
    ap.add_argument("--cwd", default=".")
    ap.add_argument("--timeout", type=int, default=300)
    args = ap.parse_args()
    gate = run(Path(args.plan), args.n, Path(args.cwd), args.timeout)
    if gate is None:
        print(f"no checkpoint {args.n}", file=sys.stderr)
        return 2
    print(json.dumps(gate, indent=2))
    return 0 if gate["verdict"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
