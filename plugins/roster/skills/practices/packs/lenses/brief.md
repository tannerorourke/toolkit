# Lens: brief

Judge whether a checkpoint contract can be built and checked from its text alone, before an implementer runs. A contract has four fields: Inputs, Deliverable, Acceptance, and Non-goals.

The brief gives you the contract and the files its Inputs name. Skill: none.

## Rubric

Rate each failure at the severity beside it.

| Check | Fails when | Severity |
| --- | --- | --- |
| Observable acceptance | A clause names no command, file, or count, or mixes a checkable part with a vague one | high |
| Honest commands | A command clause claims more than its exit code shows | high |
| Deliverable covers acceptance | A path an Acceptance clause names is not created or changed by the Deliverable | high |
| Inputs suffice | Building the Deliverable needs a fact, file, or decision the Inputs do not name | high |
| One reading | A term, path, or quantity could be read two ways, and the two readings build different things | medium |
| Contradiction | Two fields, or the contract and an input file, disagree | high |
| Size | The Deliverable is more than one commit validated alone | medium |
| Scope fence | A neighbouring change an implementer would plausibly make is not ruled out by Non-goals | low |

For every `high` finding on Inputs or one reading, state the question the implementer would have to ask.

## Never shown

The plan's discussion, the author's reasons for the contract, and earlier versions of it. The contract stands or falls on its own text.
