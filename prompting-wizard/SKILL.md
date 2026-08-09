---
name: prompting-wizard
description: Use when the user wants to learn, practise, or get better at prompting - runs a 30-day, 20-minute-a-day course that assesses the learner once and then teaches one prompting lever per day using the learner's own real tasks.
---

# Prompting Wizard

A 30-day course. One 20-minute lesson per session. All state lives in `PROGRESS.md` in the learner's working directory.

## Every session

1. Look for `PROGRESS.md` in the learner's working directory.
   - **Absent** → the file is missing either because the learner is new or because it was lost mid-course, and an absent file cannot tell you which. Ask. If they are starting fresh, read `assessment.md` and run it; writing `PROGRESS.md` ends the session. If they were mid-course, accept a day number they state and rebuild the file from it, or re-run the assessment if they prefer. Never silently restart at day 1.
   - **Present but a required field is missing or unparseable** → name the field that failed and stop. Never guess `current_day`, and never silently restart at day 1. Fit the offered repair to the field that failed: if `current_day` is the field that failed, offer to accept a day number the learner states; for any other missing or unparseable field (`## Levers`, `## Tasks`, or `level`), offer to re-run the assessment instead — a day number cannot repair those.
   - **Present and valid** → continue.
2. Read `level`, `current_day`, `## Levers`, and `## Tasks`.
3. If `current_day` is above 30, tell the learner the course is complete and stop.
4. Read `days/NN.md`, where NN is `current_day` zero-padded to two digits.
5. Run the daily loop below.
6. Append one `## Log` line, update any lever scores the day changed, and increment `current_day`.

## The daily loop — 20 minutes

Wherever `{{TASK}}` appears in any text you present, substitute the task the learner is working on this session. Default to their first `## Tasks` entry; when the exercise invites them to pick one and they do, use their pick. Never show the raw token to the learner.

Some passages are written to you rather than to the learner — they refer to "the tutor", or describe reading `PROGRESS.md`. That text is direction, not script: act on it, never read it out.

**1. Concept — 3 min.** Present the day's `## Concept` verbatim. Then present `## Before / After`, substituting the learner's first `## Tasks` entry wherever `{{TASK}}` appears.

**2. Write — 5 min.** Present the `## Exercise` tier matching `level`: `### Novice`, `### Working`, or `### Advanced`. If any lever in `## Levers` scores 2 or below, add exactly one of them as a named secondary constraint — for example, "and bind every reference; you scored low on pronoun". One only. If several qualify, take the lowest-scoring; break ties by whichever you have used least recently, which you can see in `## Log`. Do not use the same lever on consecutive sessions. Ask for the learner's prompt, then wait.

**3. Run — 2 min.** Execute the learner's prompt **verbatim** in a context containing no lesson history. See Clean-context execution. Show the output unedited, and say nothing about it yet.

**4. Critique — 7 min.** Score the prompt against the rubric named in the day's `## Rubric` section, criterion by criterion, 1–5, quoting the rubric's anchor for each score you give. Then write a stronger version of the prompt, run it in a **separate** clean context, and show both outputs side by side.

**5. Name it — 3 min.** Ask the learner which single change moved the output, and for a 1–5 self-rating. Log both.

**6. Completion.** If the day file has a `## Completion` section, carry it out after step 5, whatever the learner's tier.

## Clean-context execution

The learner's prompt must run with no lesson history in context. Lesson context contaminates the output and destroys the comparison the exercise depends on.

- If this harness can dispatch an isolated agent, dispatch the prompt there and capture the output verbatim. Detect this by whether an isolated-agent dispatch tool is actually available to you, not by inspecting configuration — Codex, for example, can expose a `spawn_agent` tool with no corresponding entry in `~/.codex/config.toml`, so a missing config entry does not mean dispatch is unavailable.
- If it cannot, or if dispatch fails, print the prompt in a fenced block and ask the learner to run it in a fresh chat and paste the output back.

Never run the learner's prompt in the lesson context. A contaminated run is worse than no run.

Run the rewritten prompt in a **separate** clean context from the learner's. Reusing one context primes the second run with the first run's output.

## Rules

- Never improve the learner's prompt before running it. They have to watch their own words fail.
- Never skip the run step, and never summarise output you did not actually get.
- Some days call for more than the two runs above — chained prompts, a system prompt with several per-turn asks, or reruns across two cases. Where the day's `## Exercise` asks for more, follow the day. Every run happens in a clean context, and each rewrite runs in a separate context from the prompt it is compared against.
- Score against the rubric only. No freelance criticism.
- A lever scoring 2 or below is practised as a secondary constraint on a later day, never by repeating its lesson.
- Skipped days carry no penalty and no backlog. Resume at `current_day`.
- Days 14 and 21 are review days: draw their material from the three lowest-scoring levers.

## Log line format

Append one line per completed day:

```
- Day 12 — interjection — self 3, rubric 4 — "priority markers changed what it did first"
```
