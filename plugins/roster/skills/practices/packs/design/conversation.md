# Conversation

How a content designer writes the questions a conversational tool asks.

Read this when you design a unit of the `conversation` medium: the questions asked and answered in turns, such as an intake, an interview, or a setup flow.

## What the unit decides

The questions asked, their order and defaults, eligibility questions first, and when to stop asking.

## Steps this file owns

1. *Identify consumers.* Name who answers (a person, a script, an agent) and what the answers feed next. A question with no downstream use does not ship.
2. *Map the steps.* List every turn and what the answerer must know at each one: what changed, what comes next.
5. *Handle input and danger.* Decide what happens on a blank, a wrong, an unclear, or a risky answer.
6. *Test with real consumers.* Run the draft against real or realistic answerers and read the transcripts. The output file covers steps 3 and 4.

## Rules

1. Write down every piece of information the flow needs before you write any question. Add a question only when you can say why you need it, what you will do with the answer, and how you will check and protect it (GOV.UK Service Manual, "Structuring forms": https://www.gov.uk/service-manual/design/form-structure).
2. Put the questions that rule people out first, so an ineligible answerer stops early (GOV.UK, same page).
3. Branch: ask a question only when earlier answers make it relevant (GOV.UK, same page).
4. Ask one thing per turn. Merge two questions only when transcripts show answerers handle them together (GOV.UK, same page).
5. State why you ask each question, and allow "I do not know" where it is a valid answer (GOV.UK Design System, "Question pages": https://design-system.service.gov.uk/patterns/question-pages).
6. Stop asking when every field the plan needs has a stated purpose and either an answer or an explicit "I do not know". This stopping rule is an inference from the question protocol; no source states it for language models. Ask more on complex or underspecified work and less on simple work.
7. Ask before you assume when a missing answer would change the result. Models default to non-interactive behavior and misjudge which briefs are underspecified; interaction improved results by up to 74% on underspecified software tasks (Vijayvargiya et al., Ambig-SWE: https://arxiv.org/abs/2502.13069). Separating the check for missing information from the work that follows reached results near fully specified instructions (Edwards and Schuster, Ask or Assume: https://arxiv.org/abs/2603.26233).
8. End each prompt with a question the system can handle. Assume the answerer is cooperative and the answer is relevant (Google conversation design, errors: https://developers.google.com/assistant/conversation-design/errors).
9. On the first failed answer, reprompt briefly with a condensed question. On the second, add examples or options. After two failures, end gracefully and offer another path. Never allow more than three errors in a row (Google conversation design, errors).
10. Write errors as what went wrong and how to fix it, in plain words (Google, "Writing helpful error messages": https://developers.google.com/tech-writing/error-messages).

## Files

Under `<unit>/` in the design folder:

- `handoff.md`: the question list with, per question, its purpose, default, branch condition, "I do not know" handling, and the stop rule.
- `sample.md`: one full realistic transcript, including one failed answer and one early exit.
- `review.md`: the user's reactions and approval line, in the shape the core gives.

## Pass condition

Every question has a stated purpose and a branch condition, eligibility questions come first, the stop rule is written, and `sample.md` shows the failure path.
