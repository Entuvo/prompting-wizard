# Day 0 — Assessment

About 15 minutes. Run once. Ask the three parts in order. Do not teach during the assessment and do not correct the learner's prompts — you are measuring a baseline, and coaching contaminates it.

## Part 1 — Cold writing (7 min)

Ask for three prompts, one at a time. Give no guidance beyond the brief. Do not run them.

1. **Instruction task:** "Write the prompt you would send to get a model to reformat a messy CSV export into something you could hand to a colleague."
2. **Analysis task:** "Write the prompt you would send to get a model to tell you what is wrong with a piece of work you produced."
3. **Open-ended task:** "Write the prompt you would send to get a model to help you think through a decision you are stuck on."

Score all three together against each of the 11 levers, 1–5, using `rubrics.md`. One score per lever, not per prompt. Take the median where the three prompts disagree.

## Part 2 — Diagnosis (4 min)

Show these two prompts and ask what is wrong with each. Do not hint.

**Prompt A**

> You are a world-class expert. Help me improve this. Make it better and more professional. Thanks!

**Prompt B**

> Go through the codebase and fix the issues with it, and if there are tests update them too, and make sure it still works.

Expected findings — count how many the learner names unprompted, out of 10:

- A: no artifact named (noun); no operation named (verb); "better" and "more professional" are unmeasurable (adjective); "this" has no antecedent (pronoun); the role does nothing (role framing).
- B: three tasks in one (task decomposition); "the issues" is unbound (determiner); no scope (preposition); no stopping condition (agent and tool prompting); "make sure it still works" is uncheckable (numeral).

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
| Mean lever score 2.5 to 3.9 | `working` |
| Mean lever score 4.0 or above | `advanced` |

Then apply one adjustment: if the Part 2 diagnosis count is 8 or more but the mean lever score is below 2.5, set `working` instead. The learner already recognises weak prompting and needs practice, not first principles.

## Writing PROGRESS.md

Write `PROGRESS.md` in the learner's working directory — not inside the skill directory. Use exactly this structure. The values below are illustrative.

```markdown
# Progress

level: working
current_day: 1

## Levers
noun: 4    verb: 3    adjective: 2    adverb: 3
pronoun: 2    preposition: 4    conjunction: 3
determiner: 3    numeral: 5    interjection: 4    particle: 2

## Tasks
- Reviewing PRs on the payments service
- Writing incident postmortems
- Drafting API docs for external partners

## Log
- Day 0 — assessment — level working, diagnosis 6/10
```

All 11 lever keys must be present. `current_day` starts at 1. Then tell the learner the assessment is done and the course starts next session.
