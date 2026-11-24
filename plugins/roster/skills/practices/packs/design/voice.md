# Voice

How a voice designer writes the spoken commands a device understands and the replies it speaks back.

Read this when you design a unit of the `voice` medium: spoken commands and spoken or audible replies.

## What the unit decides

The command grammar; feedback for heard, matched, failed, and slow; escalating error prompts; wait cues.

## Rules

1. Never let a conversation reach a dead end. Every failure path ends in a prompt the user can answer or a clean exit (Amazon Alexa Haus, "Handling errors gracefully": https://developer.amazon.com/en-US/alexa/alexa-haus/patterns-and-components/patterns-errors).
2. Separate the failures and answer each differently. No input gets "I didn't catch that ...". Input with no match gets "I'm not sure about that ..." (Alexa Haus, same page).
3. Escalate across repeated errors: a short reprompt, then examples or options, then an exit. End the session after repeated silence (Alexa Haus, same page; Google conversation design, errors: https://developers.google.com/assistant/conversation-design/errors).
4. Accept incomplete commands and ask for the missing piece. Do not make the user restate what they already said (Alexa Haus, same page).
5. Offer to retry only when a retry can plausibly succeed. Do not offer it after a failure that will not resolve soon (Alexa Haus, same page).
6. End each prompt with a question the system can handle; a prompt without one rarely gets an answer. Rephrase on silence instead of announcing that nothing was heard (Google conversation design, errors).
7. Acknowledge before slow work. Silence registers fast: speakers across 10 languages keep gaps between turns near 250 ms (Stivers et al., PNAS 2009: https://pubmed.ncbi.nlm.nih.gov/19553212/). Speak the acknowledgment first, then work.
8. Fill the wait with short interstitials: up to five, within about 8 seconds, such as "OK, please wait while I look up details for your ride ..." (Alexa progressive responses: https://developer.amazon.com/en-US/docs/alexa/custom-skills/send-the-user-a-progressive-response.html). Their purpose is to reduce perceived latency.
9. Design for simple queries and for hands-busy use such as driving and cooking. Assistants served complex queries poorly (NN/g, "Intelligent Assistants Have Poor Usability": https://www.nngroup.com/articles/intelligent-assistants-poor-usability-high-adoption/).
10. Write every reply to be heard once. Put the answer first and keep it short; the user cannot scan back (inference from the medium, no source).

## Files

Under `<unit>/` in the design folder:

- `handoff.md`: the command grammar (phrases and variants per command); the reply for each of heard, matched, failed, and slow; the escalation ladder with its exact prompts; the wait cue and its timing.
- `sample.md`: a scripted dialogue for the happy path, a no-input path, a no-match path, and a slow path.
- `review.md`: the user's reactions and approval line, in the shape the core gives.

## Pass condition

Each command has all four feedback replies written, the escalation ladder ends in an exit, and no path in `sample.md` dead-ends.
