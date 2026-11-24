---
name: brief
description: Render a plan checkpoint into a delegate brief and dispatch it to a subagent. Use when handing a checkpoint or a read-only survey to the surveyor, implementer, or verifier agents.
---

# Brief

A delegate gets the contract and nothing else. The brief is its whole prompt.

Which role and lens runs at each step, the three gates, and where a critic's findings go are in `lifecycle.md` beside this file. The survey brief for a project re-entering midway is `reentry.md`.

## Steps

1. Pick the agent: `executor:surveyor` for a read-only survey, `executor:implementer` for changes, `executor:verifier` to judge acceptance clauses, `executor:critic` to review through one lens.
2. Render the brief:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/brief.py <plan>.md <N> [--cwd DIR] [--excerpt PATH[:START-END] ...]
```

   Name only the excerpts the delegate needs; each is inlined, nothing else is. The estimate prints on stderr. Exit 1 means it is over 2000 tokens: trim the excerpts or split the checkpoint. The first line is a header comment naming plan, checkpoint, and working dir (default: the current dir); keep it, the gate hook reads it. For the verifier, the verify skill renders the brief with `--verifier`.
3. Dispatch with the Agent tool, `subagent_type` set to the chosen agent, the rendered brief as the whole prompt.
4. Read the one fenced json block at the end of the reply. `status` is the delegate's claim, never the verdict. For an implementer, follow the verify skill.
5. On `status: blocked`, run no gate and no verifier. Read `open_questions`: answer from the plan if the answer is already there, else ask the human. Then amend the checkpoint (contract skill) or the excerpts, and re-dispatch with a fresh brief. Never answer by forwarding conversation.

## Rules

- Fresh context by default. Never forward conversation, history, or a summary of either.
- The brief states what to do; the delegate decides nothing outside it. Judgment calls stay with the delegator.
- A reply without a valid json block is a failed delegation: re-dispatch, do not repair it by hand.
