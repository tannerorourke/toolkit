# toolkit

Two Claude Code plugins for work that runs from a written plan. I use them to hand most of a build to cheaper models and still check every piece before it counts as done.

| Plugin | What it gives |
|---|---|
| `executor` | Five skills that take a plan from a written contract to a checked result, and five agents to hand the work to. Its hooks run the gate each time an implementer stops, keep the read-only agents to read-only shell commands, and list parked ideas when a session starts. |
| `roster` | One skill, `practices`, that routes a kind of work to the pack files that govern it: the experience rules every project passes, a design procedure with rules for five media (gui, conversation, output, voice, api), and four review lenses for the critic (brief, code, design, accessibility). |

Each plugin installs alone. `roster` names the executor's agents where they help and runs every pack inline without them. Neither needs a server or an API key beyond Claude Code itself.

## Install

From my plugin index:

```
claude plugin marketplace add tannerorourke/plugins
claude plugin install executor@tannerorourke
claude plugin install roster@tannerorourke
```

To change the plugins, clone the repository and add the working tree as its own marketplace. An edit is then live in the next session:

```
git clone https://github.com/tannerorourke/toolkit
claude plugin marketplace add ./toolkit
claude plugin install executor@toolkit
claude plugin install roster@toolkit
```

## The loop

A project holds any number of plan files. Each plan holds checkpoints, and each checkpoint is a contract with four fields: Inputs, Deliverable, Acceptance, and Non-goals. The session that owns the plan runs the skills in order:

| Skill | Does |
|---|---|
| `executor:contract` | writes and upgrades checkpoints; `scripts/contract_check.py <plan>.md` checks them |
| `executor:brief` | renders one checkpoint into a delegate brief (`scripts/brief.py`, under 2,000 tokens) |
| `executor:verify` | runs the gate first (`scripts/gate.py`, on the implementer's SubagentStop), then the `verifier` agent on the clauses the gate could not run |
| `executor:close` | writes the run's trace to `<traces_dir>/<project>/<run_id>.json` (`scripts/close.py`) |
| `executor:make-task-reminder` | captures a passing thought as one ledger line (`scripts/thoughts.py`) |
| `roster:practices` | routes a practice, such as a gui or a conversation, to the pack files that govern it |

An acceptance code span starting with `$ ` is a command the gate runs. A span followed by `exists` is a path check.

## Agents

| Agent | Model | Does |
|---|---|---|
| `surveyor` | Haiku | reads files to answer a question in the brief, and changes nothing |
| `implementer` | Sonnet | makes the changes a brief specifies and runs its acceptance commands |
| `verifier` | Sonnet | judges the acceptance clauses with read-only tools and test or lint commands |
| `critic` | Opus | reviews one artifact through one lens and returns ranked findings |
| `designer` | Opus | designs one unit of a product's experience from a brief |

None of them can spawn another agent.

## Profile

The profile holds machine-specific values: the trace directory, the thought ledger, the test commands a verifier may run, and `engine_url`, a reserved key for a memory service's address that no script reads (`null` by default). The real copy lives at `~/.claude/toolkit/profile.json`; set `TOOLKIT_PROFILE` to use another path. Any missing key falls back to `plugins/executor/profile.example.json`.

```
python3 plugins/executor/scripts/toolkit_profile.py            # whole resolved profile
python3 plugins/executor/scripts/toolkit_profile.py traces_dir # one value
```

## Requirements

Python 3.11+ with `jsonschema`.

## License

MIT, in `LICENSE`.
