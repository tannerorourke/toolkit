"""Render one plan checkpoint into a delegate brief.

  python3 brief.py <plan.md> <N> [--cwd DIR] [--excerpt PATH[:START-END] ...]
  python3 brief.py --verifier <gate.json>
Prints the brief on stdout: a header line naming plan, checkpoint, and working dir
(read back by gate_hook.py), the four contract fields verbatim, the named excerpts
(line numbers 1-based inclusive), and the return-block instruction with the schema
inline. --verifier renders the contract plus the gate results and asks the verifier
to judge only the not_run clauses. Token estimate on stderr (chars / 4). Exits 1 if
the estimate exceeds the profile's 'brief_token_budget' or an Inputs path named by an `exists` clause is missing
under the working dir (stderr names each), 2 if the checkpoint does not exist.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import toolkit_profile  # noqa: E402
from contract_check import FIELDS, parse, split_clauses  # noqa: E402

SCHEMA = Path(__file__).resolve().parent.parent / "return.schema.json"
HEADER = re.compile(r"<!-- executor-brief (\{.*?\}) -->")
EXISTS = re.compile(r"^`([^`$][^`]*)` exists$")


def header(plan: Path, n: int, cwd: Path) -> str:
    meta = {"plan": str(plan.resolve()), "checkpoint": n, "cwd": str(cwd.resolve())}
    return f"<!-- executor-brief {json.dumps(meta)} -->"


def read_header(text: str) -> dict | None:
    m = HEADER.search(text)
    return json.loads(m.group(1)) if m else None


def excerpt(spec: str) -> str:
    path, _, rng = spec.partition(":")
    lines = Path(path).read_text().splitlines()
    if rng:
        a, b = rng.split("-")
        lines = lines[int(a) - 1 : int(b)]
    return f"### {spec}\n\n```\n" + "\n".join(lines) + "\n```"


def return_block() -> str:
    schema = json.dumps(json.loads(SCHEMA.read_text()), separators=(",", ":"))
    return (
        "## Return\n\nEnd your reply with exactly one fenced json block matching this "
        f"schema, and nothing after it:\n\n```json\n{schema}\n```"
    )


def contract(cp: dict, head: str) -> list[str]:
    return [head, f"# Checkpoint {cp['number']}: {cp['title']}"] + [
        f"**{f}:** {cp['fields'][f]}" for f in FIELDS
    ]


def render(cp: dict, head: str, excerpts: list[str]) -> str:
    parts = contract(cp, head)
    if excerpts:
        parts.append("## Excerpts\n\n" + "\n\n".join(excerpt(s) for s in excerpts))
    parts.append(return_block())
    return "\n\n".join(parts) + "\n"


def render_verifier(cp: dict, head: str, gate: dict) -> str:
    parts = contract(cp, head)
    rows = [f"- {c['result']}: {c['clause']}" for c in gate["clauses"]]
    parts.append("## Gate\n\nDeterministic clauses were already run:\n\n" + "\n".join(rows))
    files = [a["path"] for a in (gate.get("return") or {}).get("artifacts", [])]
    if files:
        parts.append("## Changed files\n\n" + "\n".join(f"- `{f}`" for f in files))
    parts.append(
        "## Judge\n\nJudge only these not_run clauses, reading the changed files and "
        "running test or lint commands as needed:\n\n"
        + "\n".join(f"- {c}" for c in gate["not_run"])
        + "\n\nReturn status pass with empty deviations if every one holds; otherwise "
        "status fail with each failing clause, verbatim, in deviations."
    )
    parts.append(return_block())
    return "\n\n".join(parts) + "\n"


def missing_inputs(cp: dict, cwd: Path) -> list[str]:
    clauses = split_clauses(cp["fields"].get("Inputs", ""))
    paths = [m.group(1) for c in clauses if (m := EXISTS.match(c))]
    return [p for p in paths if not (cwd / p).exists()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan", nargs="?")
    ap.add_argument("n", type=int, nargs="?")
    ap.add_argument("--cwd", default=".")
    ap.add_argument("--excerpt", action="append", default=[])
    ap.add_argument("--verifier", metavar="GATE_JSON")
    args = ap.parse_args()
    gate = json.loads(Path(args.verifier).read_text()) if args.verifier else None
    plan, n, cwd = (
        (Path(gate["plan"]), gate["checkpoint"], Path(gate["cwd"]))
        if gate else (Path(args.plan), args.n, Path(args.cwd))
    )
    cps = [c for c in parse(plan.read_text()) if c["number"] == n]
    if not cps:
        print(f"no checkpoint {n}", file=sys.stderr)
        return 2
    if not gate:
        missing = missing_inputs(cps[0], cwd)
        if missing:
            print("missing input path: " + ", ".join(missing), file=sys.stderr)
            return 1
    head = header(plan, n, cwd)
    brief = render_verifier(cps[0], head, gate) if gate else render(cps[0], head, args.excerpt)
    tokens = len(brief) // 4
    print(brief, end="")
    print(f"estimated tokens: {tokens} (chars/4)", file=sys.stderr)
    return 1 if tokens > toolkit_profile.get("brief_token_budget") else 0


if __name__ == "__main__":
    sys.exit(main())
