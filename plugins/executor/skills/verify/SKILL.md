---
name: verify
description: Gate an implementer's checkpoint work, deterministic checks first, then the verifier on what is left, then the human's approve or reject. Use after dispatching a checkpoint to executor:implementer, or when asked to verify, gate, or accept a delegated checkpoint.
---

# Verify

The implementer's `status` is a claim. The gate settles what a command or a path can settle, the verifier judges the rest, the human decides.

## Steps

1. Dispatch the implementer with the brief skill, in the foreground (`run_in_background: false`), so the verdict arrives with its result.
2. When the implementer stops, a hook runs the gate and writes `.executor/gates/<agent_id>.json` in the brief's working dir. Its path and verdict are added to your context beside the Agent result. If they are not (a background run), read the file named by the agent id. No file means the brief had no header: re-render it with `brief.py`.
3. Read the gate file's `verdict`:
   - `blocked`: follow the brief skill's blocked step. Stop here.
   - `fail`: stop. Report each clause whose `result` is `fail` to the human, with its command, exit code, and `output_tail`, or the `return_errors` if the return block was invalid. Never dispatch the verifier on a failed gate.
   - `pass`: continue.
4. Render the verifier brief and dispatch `executor:verifier` with it as the whole prompt:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/brief.py --verifier <gate file>
```

5. Check the verifier's json block against the schema in its brief. A missing or invalid block is a failed delegation: re-dispatch.
6. Present both to the human: the gate's per clause results and the verifier's `status` and `deviations`. The human approves or rejects. Never mark a checkpoint complete, commit, or start the next checkpoint on your own verdict.

## Rules

- Deterministic first, always. The verifier never sees work that failed the gate.
- Report results as written in the gate file and the return block; do not re-run or reinterpret them.
- A rejection goes back through the brief skill as a fresh brief, amended by the human's reason.
