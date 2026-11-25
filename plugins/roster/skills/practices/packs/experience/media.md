# Media

How a product designer lists every surface a user meets a product through, before any of them is designed.

When you are done, the experience core names every medium the product uses, and each named medium has a module of design units planned. A medium is a surface the user meets the product through. Name a medium only when the user meets the product there; a command-line tool with prose output uses `conversation` or `output`, never `gui`.

| Medium | The user meets the product as | The module decides | Pack file |
| --- | --- | --- | --- |
| `gui` | Screens they look at and click | Navigation and page types; the design system; every state of every data region on every page; a clickable mockup of each page | `packs/design/rules.md` |
| `conversation` | Questions asked and answered in turns | The questions asked, their order and defaults, eligibility questions first, and when to stop asking | `packs/design/conversation.md` |
| `output` | A report, verdict, file, or message they read or a program parses | The format per consumer (a person, a script, an agent) and the copy deck | `packs/design/output.md` |
| `voice` | Spoken commands and spoken or audible replies | The command grammar; feedback for heard, matched, failed, and slow; escalating error prompts; wait cues | `packs/design/voice.md` |
| `api` | A library, CLI, or service interface a developer calls | Names, defaults, and errors; the first five minutes of use; the documented example | `packs/design/api.md` |

Pack paths are relative to the `practices` skill's folder, which holds `packs/`. When a medium's pack file is not installed, run its module from its row above and from the core.

## Units and gates

Each module's units pass a gate before the work they shape is built.

- The `gui` structure unit passes the ideation gate with the core. Its design system unit and each page unit pass the build gate before the first page mockup and before that page's build.
- A `conversation`, `output`, `voice`, or `api` unit passes the build gate before the step, output, command set, or public interface it describes is built.

A unit's files live under `<unit>/` in the project's design folder, `artifacts/design/` at the project's root unless the project names another: `handoff.md` with the decisions, `artboards/` for `gui` or `sample.md` for the other media, and `review.md` in the shape `core.md` gives. The folder appears at approval and holds approved work only.

Pass condition: the core's sixth heading names 1 or more of the 5 media above, and each named medium has 1 or more units planned.
