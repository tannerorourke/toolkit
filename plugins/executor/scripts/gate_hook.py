"""Gate an implementer's work when it stops, and hand the verdict to the delegator.

Wired in hooks/hooks.json, reads hook JSON on stdin:
  SubagentStop (matcher executor:implementer): recover plan, checkpoint, and working dir
    from the brief header in the subagent's first prompt; validate the return block
    against return.schema.json; run gate.py unless the return is invalid or blocked;
    write <cwd>/.executor/gates/<agent_id>.json; show the verdict as a systemMessage.
    Never blocks the subagent.
  PostToolUse (matcher Agent): for a completed foreground implementer call, add the
    gate verdict to the delegator's context.
A prompt without a brief header is not gated.
"""
import json
import re
import sys
from pathlib import Path

import jsonschema

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brief import SCHEMA, read_header  # noqa: E402
import gate  # noqa: E402

IMPLEMENTER = "executor:implementer"
FENCE = re.compile(r"```json\s*\n(.*?)\n```", re.S)


def gate_path(meta: dict, agent_id: str) -> Path:
    return Path(meta["cwd"]) / ".executor" / "gates" / f"{agent_id}.json"


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    return "\n".join(b.get("text", "") for b in content if b.get("type") == "text")


def transcript(path: str) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def first_prompt(entries: list[dict]) -> str:
    return next(text_of(e["message"]["content"]) for e in entries if e.get("type") == "user")


def handback(entries: list[dict]) -> str:
    # -- a subagent with SubagentHandback delivers its report as that call's message
    msgs = [
        b["input"]["message"]
        for e in entries if e.get("type") == "assistant"
        for b in e["message"]["content"]
        if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "SubagentHandback"
    ]
    return msgs[-1] if msgs else ""


def return_block(text: str) -> tuple[dict | None, list[str]]:
    blocks = FENCE.findall(text)
    if not blocks:
        return None, ["no fenced json block"]
    try:
        ret = json.loads(blocks[-1])
    except json.JSONDecodeError as e:
        return None, [f"json: {e}"]
    validator = jsonschema.Draft202012Validator(json.loads(SCHEMA.read_text()))
    errors = [f"{'/'.join(map(str, err.path)) or '<root>'}: {err.message}" for err in validator.iter_errors(ret)]
    return ret, errors


def on_stop(event: dict) -> dict | None:
    entries = transcript(event["agent_transcript_path"])
    meta = read_header(first_prompt(entries))
    if meta is None:
        return None
    text = event.get("last_assistant_message") or ""
    ret, errors = return_block(text if FENCE.search(text) else handback(entries))
    base = {"plan": meta["plan"], "checkpoint": meta["checkpoint"], "cwd": meta["cwd"]}
    if errors:
        result = {**base, "verdict": "fail", "reason": "return block invalid", "return_errors": errors}
    elif ret["status"] == "blocked":
        result = {**base, "verdict": "blocked", "reason": "implementer returned blocked"}
    else:
        result = gate.run(Path(meta["plan"]), meta["checkpoint"], Path(meta["cwd"]), 300)
    result.update(agent_id=event["agent_id"], **{"return": ret})
    out = gate_path(meta, event["agent_id"])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    return {"systemMessage": f"executor gate: {result['verdict']} for checkpoint {meta['checkpoint']} ({out})"}


def on_agent_result(event: dict) -> dict | None:
    tin, tres = event.get("tool_input", {}), event.get("tool_response", {})
    if tin.get("subagent_type") != IMPLEMENTER or tres.get("status") != "completed":
        return None
    meta = read_header(tin.get("prompt", ""))
    if meta is None:
        return None
    path = gate_path(meta, tres["agentId"])
    if not path.exists():
        return None
    g = json.loads(path.read_text())
    failing = [c["clause"] for c in g.get("clauses", []) if c["result"] == "fail"]
    note = f"Gate verdict: {g['verdict']}. Gate file: {path}."
    if failing:
        note += " Failing clauses: " + "; ".join(failing)
    return {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": note}}


def main() -> None:
    event = json.load(sys.stdin)
    handler = on_stop if event["hook_event_name"] == "SubagentStop" else on_agent_result
    out = handler(event)
    if out:
        print(json.dumps(out))


if __name__ == "__main__":
    main()
