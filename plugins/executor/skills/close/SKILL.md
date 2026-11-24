---
name: close
description: Write the run trace when a unit or project closes. Use when a plan, checkpoint run, or project is done or abandoned, or when asked to close, wrap up, or write the trace.
---

# Close

The trace records what the loop did and where the contracts failed. The delegator writes it from the session, never a delegate.

## Steps

1. Collect from the session:
   - decisions: one short string per thing decided in the run
   - friction: prose under 200 words on what the contracts got wrong (missing inputs, unobservable acceptance, scope that leaked). Facts, not mood.
   - the human's outcome per checkpoint: accepted, rejected, blocked, or abandoned
   - checkpoints where the verifier failed the work (verifier returns are not gated)
   - checkpoints whose contract was amended mid-run
2. Run, from the working dir the briefs used:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/close.py --project NAME --plan <plan>.md [--cwd DIR] \
  --decision "..." --friction "..." --outcome 1=accepted --outcome 2=rejected \
  --verifier-fail 2 --rework-contract 3
```

   Gate files give per-checkpoint verdicts, rework count (gated runs minus one), and deviations. The consumed gate files move to `.executor/gates/closed/<run_id>/`, so the next close starts clean; `--keep-gates` leaves them in place.
3. Report the printed path. A friction text over 200 words fails: shorten it and rerun.

## Rules

- Never overwrite a trace; every call writes a new file.
- An outcome not passed is recorded as blocked (last gate blocked) or abandoned. Pass the human's decision, do not infer acceptance.
- Record what happened. Do not interpret the numbers or propose changes in the trace.
