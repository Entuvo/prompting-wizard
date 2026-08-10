# Prompting Wizard — Design

**Date:** 2026-08-09
**Status:** Implemented; authoritative over the plan where wording differs

## Problem

A 30-day course to take a learner from wherever they are to strong practical prompting. It must assess the learner first, build on the tasks they actually do daily, start basic and ramp, run 20 minutes a day, and use the parts of speech as its organizing spine.

## Decision: skill, not a prompt

A prompt can generate the outline once. It cannot remember on day 12 that the learner failed the day-4 exercise on scope constraints, cannot carry the day-0 assessment forward, and cannot adapt day 20 to a weakness found on day 8. A 30-day course is thirty sessions sharing state.

The skill is the tutor loop. The state is a file. The lessons are content.

## Non-goals

- No scheduler, reminder system, or streak tracking. The learner opens the skill when they want the lesson.
- No CLI, no build step, no dependencies.
- No progress dashboard or visualization.
- No account, sync, or multi-learner support. One learner, one directory.

## Architecture

```
prompting-wizard/
  SKILL.md              # tutor loop — the only logic
  AGENTS.md             # Codex entry point; points at SKILL.md
  assessment.md         # day-0 script
  rubrics.md            # one critique rubric per lever, reused by all lessons
  days/
    01.md … 30.md       # pre-authored lesson content with domain slots
learner-working-directory/
  PROGRESS.md           # created in the learner's directory on day 0
```

`SKILL.md` logic, in outline:

1. Read `PROGRESS.md`. If absent, ask whether the learner is new or restoring lost state; run `assessment.md` only for a fresh start or when they choose reassessment.
2. Otherwise read `current_day`, load `days/NN.md`.
3. Run the daily loop (below).
4. Append the day's result to `PROGRESS.md` and increment `current_day`.

Everything else is markdown content. Lessons are data, not code.

## Portability: Claude Code and Codex

The skill ships as a plain directory that works when cloned anywhere. Requirements:

- **Markdown-only runtime.** The shipped skill has no scripts, manifest dependency, or plugin marketplace assumption; its Python validator remains outside the shipped directory.
- **Relative skill paths.** Content paths are relative. A named user configuration path may appear only as an illustrative capability-detection example, never as an install assumption.
- **Capability-first tool references.** `SKILL.md` states what isolation must achieve and may name harness tools only as examples of how to detect an actually available capability. No named tool or config key is a runtime prerequisite.

**Entry points.** Both harnesses read the same `SKILL.md` body; only discovery differs.

| Harness | Discovery |
|---|---|
| Claude Code | `SKILL.md` YAML frontmatter (`name`, `description`) → invoked via the Skill tool |
| Codex | `AGENTS.md` at the directory root, one paragraph: "To run the prompting course, read `SKILL.md` and follow it." |

`AGENTS.md` contains no lesson logic. It is a pointer, so the two entry points cannot drift.

## Capability tiers: clean-context execution

The daily loop requires running the learner's prompt **verbatim, in a context containing no lesson history**. Lesson context contaminates the result and destroys the comparison the exercise depends on.

`SKILL.md` states that requirement and lets the harness satisfy it:

- **Tier A — dispatch available.** The harness exposes an isolated-agent dispatch capability. The skill detects the tool that is actually available — not a config entry that may be absent even when dispatch works — dispatches the prompt, captures the output verbatim, and shows it unedited.
- **Tier B — no dispatch.** The skill prints the prompt in a fenced block and asks the learner to run it in a fresh chat and paste the output back.

One branch, not two implementations. Tier B is also the honest fallback when dispatch fails at runtime.

The stronger rewritten prompt runs in a **separate** clean context, never the same one — otherwise the first run's output primes the second.

## The 11 levers

Each part of speech maps to a prompting lever it genuinely controls. The mapping is the teaching device; no exercise requires using a part of speech for its own sake.

| Part of speech | Lever |
|---|---|
| Noun | Name the artifact. "something" → "a 300-word release note" |
| Verb | Task precision. summarize / critique / rank / refactor are different jobs |
| Adjective | Quality constraints. "idiomatic", "defensive", "terse" |
| Adverb | Manner and degree. "briefly", "exhaustively", "step by step" |
| Pronoun | Reference binding. Dangling "it" and "this" are a top cause of wrong output |
| Preposition | Scope and relation. "in this file", "for a junior dev", "without new deps" |
| Conjunction | Conditional logic. "if X then Y, otherwise Z", "and also", "but not" |
| Determiner | Definiteness and quantity binding. "the config" vs "a config" vs "each config" |
| Numeral | Budgets that make output checkable. "exactly 5", "≤200 words" |
| Interjection | Attention markers. `IMPORTANT:`, `Note:`, `Never:` — priority in prose |
| Particle | Phrasal precision. "look up" ≠ "look over" ≠ "look into" |

## 30-day outline

Difficulty ramps twice: single lever → composed levers → multi-turn systems.

**Week 1 — core levers**
1. Noun: name the artifact
2. Verb: task precision
3. Adjective: quality constraints
4. Adverb: manner and degree
5. Preposition: scope and relation
6. Compose all five in one prompt
7. Review: rewrite your worst real prompt

**Week 2 — remaining levers**
8. Pronoun: reference binding
9. Conjunction: conditional logic
10. Determiner: definiteness and quantity
11. Numeral: budgets and checkable output
12. Interjection: attention and priority markers
13. Particle: phrasal precision
14. Review: all 11 levers on one hard task

**Week 3 — above the sentence**
15. Role framing
16. Few-shot examples
17. Output schemas and format contracts
18. Task decomposition
19. Reasoning scaffolds
20. Negative constraints
21. Context ordering and placement

**Week 4 — systems**
22. System prompts vs user prompts
23. Agent and tool prompting
24. Self-critique and iteration loops
25. Writing evals for your own prompts
26. Token economy and context budget
27. Diagnosing a failed prompt
28. Building your prompt library
29. Capstone I: build a production prompt for your top real task
30. Capstone II: eval it, harden it, ship it

## Day-0 assessment

Roughly 15 minutes, run once, three parts:

1. **Cold writing.** Three prompts written with no guidance — one instruction task, one analysis task, one open-ended. Scored against all 11 levers.
2. **Diagnosis.** Two deliberately weak prompts to critique. This separates *recognizing* bad prompting from *producing* good prompting; they are different skills, and the gap between the two scores sets pacing.
3. **Domain interview.** What the learner does daily, what they currently use a model for, where it disappoints them.

Output written to `PROGRESS.md`:

- `level`: novice | working | advanced
- `## Levers`: per-lever score 1–5 from part 1
- `## Tasks`: 3–5 recurring real tasks, in the learner's own words

Those tasks become the substrate for every exercise across all 30 days. `level` selects the exercise tier within each day's lesson.

## Lesson file format

Each `days/NN.md` contains:

- **Concept** — one lever, explained in 200 words or fewer
- **Before/after pair** — one weak prompt and its strong counterpart, normally with the domain slot filled from the learner's `## Tasks`; a fixed example may replace the slot when the lever needs an exact textual contrast
- **Exercise brief at three tiers** — novice is partial and advanced reaches the top anchor; working is the bridge between them, with its shortfall made explicit where the exercise can pin one without distorting the learner's real task. The capstone is deliberately staged: day 29 targets anchors 1/2/3, and day 30 finishes the climb, so its Novice tier may begin at anchor 2. An adversarial constraint appears where the technique needs one, not as a universal decoration. Three short paragraphs, not three lessons.
- **Rubric reference** — points at the lever's entry in `rubrics.md`

Pre-authored and committed. Only the domain slots are filled per learner.

## Daily loop — 20 minutes

| Time | Step |
|---|---|
| 3 min | Concept: one lever, one before/after pair drawn from the learner's domain |
| 5 min | Learner writes a prompt for one of their real tasks |
| 2 min | Prompt runs verbatim in a clean context; output shown unedited |
| 7 min | Critique against the lever's rubric; when a targeted textual improvement exists, a stronger version is written, run in a separate clean context, and both outputs are shown side by side; no rewrite is manufactured when every named rubric is already at its top anchor or N/A, or when the remaining gap requires run evidence rather than changed words |
| 3 min | Learner names the one change that moved the output, the existing strength, or the evidence still missing; logged |

The run step is the point of the design. The learner sees their prompt fail rather than being told it would.

## Rubrics

`rubrics.md` holds one rubric per lever and technique, each a short checklist scored 1–5. Reused verbatim by every lesson that touches that property, so critique stays consistent across 30 days and the same weakness gets the same name every time.

## Scoring and adaptation

Each day ends with two numbers: the learner's 1–5 self-rating and the rubric score from the critique.

- A lever scoring ≤2 is re-injected as a **secondary constraint** in a later day's exercise rather than repeating its lesson. Practice under new material beats re-reading.
- Days 14 and 21 are review days that draw their material from the three weakest levers.

## PROGRESS.md format

Plain markdown, human-editable, committed by the learner if they want history. Synthetic example:

```markdown
# Progress

level: working
current_day: 12

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
- Day 11 — numeral — self 4, rubric 5 — "budgets made the output checkable"
- Day 12 — interjection — self 3, rubric 4 — "priority markers changed what it did first"
```

Weak levers (≤2) are read directly off the `## Levers` block when selecting secondary constraints. Lever scores are updated in place as the course reassesses them; the `## Log` keeps the per-day history.

## Testing

The skill is markdown, so testing is a dry-run rather than a suite:

- Run the assessment cold as a novice, a working, and an advanced learner; confirm three different exercise tiers are selected.
- Run day 1 and day 15 on both Claude Code and Codex; confirm identical lesson behaviour and that Tier B fallback triggers correctly when dispatch is unavailable.
- Confirm a lever scored ≤2 on day 3 appears as a secondary constraint by day 14.

## Error handling

- **`PROGRESS.md` missing mid-course** — the skill does not silently restart at day 1. It reports the file is missing and offers to re-run the assessment or accept a manually stated day number.
- **`PROGRESS.md` malformed** — report which field failed to parse and stop. Never guess `current_day`.
- **Clean-context dispatch fails at runtime** — fall through to Tier B rather than running the prompt in the lesson context. A contaminated run is worse than no run.
- **Learner skips days** — no penalty, no catch-up backlog. Resume at `current_day`.
