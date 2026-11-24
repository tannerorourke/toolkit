# Lens: code

Judge whether a change does what its contract says and breaks nothing it touches.

The brief gives you the contract, the diff or the changed files, and the output of the checks the orchestrator ran (tests, linters, the gate's results). Read the surrounding code a changed line depends on. Skill: none.

## Rubric

| Check | Fails when | Severity |
| --- | --- | --- |
| Contract | The change misses a Deliverable item or does something its Non-goals rule out | high |
| Correctness | An input the code accepts produces a wrong result, a crash, or lost data; name the input | high |
| Passing by accident | A check passes for a reason other than the behaviour it names, such as a test asserting nothing or a skipped case | high |
| Callers | A changed signature, schema, or format breaks a caller the diff does not update | high |
| Error paths | A failure the code can meet is swallowed, misreported, or leaves state half-written | medium |
| Repository rules | The change breaks a rule in the repository's instruction files, such as a style or comment budget | medium |
| Simplicity | Code repeats a helper that exists, or adds a layer nothing uses | low |

Report a correctness finding only with the concrete input or state that triggers it.

## Never shown

The implementer's report, its reasoning, its transcript, and its own account of what it tested. Judge the code and the check output.
