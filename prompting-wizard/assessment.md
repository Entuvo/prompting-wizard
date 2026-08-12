# Day 0 — Assessment

About 15 minutes. Run once. Ask the three parts in order. Do not teach during the assessment and do not correct the learner's prompts — you are measuring a baseline, and coaching contaminates it. Before Part 1, tell the learner once: from day 1 onward their prompts are executed for real, unmodified, with this session's file and network access. Get their acknowledgement before writing `PROGRESS.md`.

## Part 1 — Cold writing (7 min)

Ask for three prompts, one at a time. Give no guidance beyond the brief. Do not run them.

1. **Instruction task:** "Write the prompt you would send to get a model to clean up a messy set of meeting notes into a structured briefing you could hand to a colleague."
2. **Analysis task:** "Write the prompt you would send to get a model to tell you what is wrong with a piece of work you produced."
3. **Open-ended task:** "Write the prompt you would send to get a model to help you think through a decision you are stuck on."

Score all three together against each of the 11 levers, 1–5, using `rubrics.md`. One score per lever, not per prompt. Take the median where the three prompts disagree. Where `rubrics.md`'s not-applicable rule applies — a prompt gives a lever nothing to score — take the median of the prompts that do give it something. Where that leaves two scores, their median is the midpoint; if it falls between two whole numbers, take the lower, so `## Levers` carries whole numbers throughout. Where none of the three gives it anything, record 3 and note it, and leave that lever out of the mean under "Setting the level": average only the levers the three prompts actually exercised, so the level is not skewed by a property they never touched. An imputed 3 counted in an eleven-lever mean drags it toward 3, and the bands either side of 3 are not symmetric, so counting it can move the learner a whole tier. Day 0 is the one place `N/A` is not written: all eleven `## Levers` keys carry a number before the course starts.

## Part 2 — Diagnosis (4 min)

Show these two prompts and ask what is wrong with each. Do not hint.

**Prompt A**

> You are a world-class expert. Help me improve this. Make it better and more professional. Thanks!

**Prompt B**

> Go through the project documents and fix all the issues in them, update the summary section too, and make sure everything is ready to send.

Expected findings — count how many the learner names unprompted, out of 10:

- A: no artifact named (noun); no operation named (verb); "better" and "more professional" are unmeasurable (adjective); "this" has no antecedent (pronoun); the role does nothing (role framing).
- B: three tasks in one (task decomposition); "the issues" is unbound (determiner); no scope (preposition); no stopping condition (agent and tool prompting); "make sure everything is ready to send" is uncheckable (numeral).

Record the count out of 10.

## Part 3 — Domain interview (4 min)

Ask, one at a time:

1. What do you spend most of your working time doing?
2. What do you currently use a model for, in your own words?
3. Where does it most often disappoint you?

Extract 3–5 recurring, concrete tasks. Write them in the learner's words, not yours. These become the substrate for all 30 exercises — a vague task here produces 30 vague lessons, so push for specifics until each one names a real artifact the learner actually produces.

## Setting the level

| Condition | Level |
|---|---|
| Mean lever score below 2.5 | `novice` |
| Mean lever score 2.5 or above but below 4.0 | `working` |
| Mean lever score 4.0 or above | `advanced` |

The mean is taken over the levers the three prompts actually exercised, per Part 1 — not over any lever recorded as an imputed 3.

Then apply one adjustment: if the Part 2 diagnosis count is 8 or more but the mean lever score is below 2.5, set `working` instead. The learner already recognises weak prompting and needs practice, not first principles.

## Writing PROGRESS.md

Write `PROGRESS.md` in the learner's working directory — not inside the skill directory. Use exactly this structure. The values below are illustrative.

```markdown
# Progress

level: working
current_day: 1
course_version: 1.0.0
last_update_check: 2026-08-10

## Levers
noun: 4    verb: 3    adjective: 2    adverb: 3
pronoun: 2    preposition: 4    conjunction: 3
determiner: 3    numeral: 5    interjection: 4    particle: 2

## Tasks
- Reviewing PRs on the payments service
- Writing incident postmortems
- Drafting API docs for external partners

## Log
- Day 0 — assessment — level working, diagnosis 6/10 — baseline noun 4, verb 3, adjective 2, adverb 3, pronoun 2, preposition 4, conjunction 3, determiner 3, numeral 5, interjection 4, particle 2
```

On a stateless host, return the updated `PROGRESS.md` as a downloadable file artifact instead of claiming it was saved across chats. If artifacts are unavailable, show the complete final file in one fenced Markdown block and ask the learner to save it as `PROGRESS.md`. This state export happens before ending the assessment session.

All 11 lever keys must be present. `current_day` starts at 1. Read the installed `version` from `VERSION.md` into `course_version`, and write today's local date as `last_update_check` in `YYYY-MM-DD` form; the literal values above are illustrative. These two update fields are optional when reading an older or rebuilt progress file, so their absence never invalidates learner state. The Day 0 `## Log` line must carry all eleven baseline scores, in the format shown, in addition to the level and diagnosis count — `## Levers` gets overwritten as the course progresses, so this line is the only surviving record of the learner's starting point. Never edit it after it's written. Then tell the learner the assessment is done and the course starts next session.
