# Output

How a content designer shapes a message, report, or command's output for the reader or program that consumes it.

Read this when you design a unit of the `output` medium: a report, verdict, file, or message that a person reads or a program parses.

## What the unit decides

The format per consumer (a person, a script, an agent) and the copy deck.

## Steps this file owns

1. *Identify consumers.* Name each consumer and what it does with the output next. Do this for questions as well as output; the conversation file holds the rules.
3. *Write step copy.* Write the success line, the state-change notice, the next-step suggestion, and every error.
4. *Shape output per consumer.* Choose the format, stream, length, and structure per consumer.
6. *Test with real consumers.* Read agent transcripts, run the consumer with and without the guidance, and confirm the agent loads it at all.

The conversation file owns *map the steps* and *handle input and danger*.

## Rules

1. Print human-readable output by default. Offer `--json` and `--plain` for programs. Send data to stdout and messages to stderr (clig.dev: https://clig.dev/; Heroku CLI style guide: https://devcenter.heroku.com/articles/cli-style-guide).
2. Tell the user about every state change, keep success output brief, and suggest the next command (clig.dev).
3. Make each row self-contained so `grep` works. Add output fields freely; never change an existing field after release (Heroku CLI style guide).
4. Rewrite errors for the reader: what happened, why, and how to fix it (clig.dev; Microsoft: https://learn.microsoft.com/en-us/windows/win32/debug/error-message-guidelines; Google: https://developers.google.com/tech-writing/error-messages).
5. Lead with the verb and the outcome in labels and calls to action: "Create account", never "Submit". Name the count in confirmations: "Delete 3 files?" Use one term per concept (Anthropic ux-copy skill: https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/design/skills/ux-copy/SKILL.md).
6. Front-load the point. Reports for people run conclusion first, then support, then background; start each paragraph with its key point (NN/g, "Inverted Pyramid": https://www.nngroup.com/articles/inverted-pyramid/; Microsoft style guide: https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice). On a terminal, clig.dev puts the most important line last, where the eye lands; the medium decides.
7. Agent consumers get concise output by default and a detailed mode on request. Paginate or truncate, and tell the agent how to get more. Prefer names over opaque IDs. Return errors that say what to do next, with a machine code (Anthropic, "Writing effective tools for agents": https://www.anthropic.com/engineering/writing-tools-for-agents).
8. Fail on an unknown flag for agent consumers, with a distinct exit code per failure class. Offer a suggested correction to human consumers (Arcjet, "Designing a CLI for AI agents": https://arcjet.com/blog/designing-a-cli-for-ai-agents; clig.dev). Choose by consumer.
9. Write prose for reasoning and lists for discrete items. Make the template strict when a program parses it and flexible otherwise (Anthropic prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices; Anthropic skill authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
10. Keep a skill or agent document's entry file short, and reference files one level deep (Anthropic skill authoring best practices). Test that the agent loads them (Vercel, AGENTS.md evals: https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals).

## Files

Under `<unit>/` in the design folder:

- `handoff.md`: per consumer, the format, stream, and fields; the copy deck with every success line, notice, and error; the strictness of any template.
- `sample.md`: one real output per consumer, one error output, and one truncated or paginated output.
- `review.md`: the user's reactions and approval line, in the shape the core gives.

## Pass condition

Every consumer has a named format, every error in the copy deck states what, why, and fix, and `sample.md` shows each consumer's real output.
