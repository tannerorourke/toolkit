# Re-entry survey

Dispatch this brief to `executor:surveyor` when a project stopped midway re-enters the lifecycle. Fill the four bracketed slots, keep the rest verbatim, and pass the whole text as the prompt. The return block maps what is built onto the six headings of the experience core.

```
Survey the project in [REPOSITORY PATH] and report what it does today for its users. Read
[ENTRY POINTS: the README, the main modules, the routes or commands, the UI files]
[ARCHITECTURE DOC, if the user names one; else delete this line].
List a directory entry point with `ls` or `git ls-files`, then read the files it
holds. Read nothing else. Never change a file.

Map what you find onto these six headings:
1. Who uses it: the users the code serves and how often it expects them.
2. Their jobs: the tasks the code supports and the objects it acts on, with their fields.
3. The path of steps: the order a user moves through, from arrival to leaving.
4. What each step tells them: what each screen, prompt, reply, or call shows or returns.
5. What they leave with: the output, file, or changed state at the end.
6. The media: gui, conversation, output, voice, or api, each the code implements.

Report one artifacts entry per finding. Set "path" to the file that shows it, or "." for
something absent. Set "change" to "<heading number> | <built, partial, or absent> | <what
you found, in one sentence>". Mark absent anything a heading needs that the code lacks.
Put each guess about intent in open_questions, never in artifacts.

Return schema: [PATH TO return.schema.json]
```

After the return:

1. Check the block against the schema. A missing or invalid block is a failed delegation: re-dispatch.
2. Draft the retro core in the experience core's shape, one heading per number, each entry with its state.
3. Show the user the draft, with the open questions, and have them mark each entry `keep` or `change`.

Pass condition: the return block validates, and every one of the 6 headings holds 1 or more entries.
