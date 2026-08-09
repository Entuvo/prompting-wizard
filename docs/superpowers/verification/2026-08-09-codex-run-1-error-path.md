# Codex parity report: prompting-wizard

Test date: 2026-08-09  
Lesson workspace: `/tmp/pw-codex-test`  
Skill repository: `/Users/shergill/projects/prompting_skills/prompting-wizard` (read-only)

The supplied `PROGRESS.md` caused the skill to stop at session step 1. It contains task-like lines, but it does not contain the required `## Tasks` heading. I did not infer a missing section because the skill explicitly forbids continuing when a required field is missing.

## 1. AGENTS.md entry point

Yes. `AGENTS.md` led to `SKILL.md` without ambiguity:

> To run the prompting course, read `SKILL.md` and follow it.

It also clarified that the other files are not entry-point logic:

> Nothing else in this directory is entry-point logic. `days/`, `rubrics.md`, and `assessment.md` are content that `SKILL.md` loads.

## 2. Numbered session steps and what happened

1. The skill said:

   > 1. Look for `PROGRESS.md` in the learner's working directory.

   Done. `/tmp/pw-codex-test/PROGRESS.md` was present. The applicable branch was:

   > **Present but a required field is missing or unparseable** → name the field that failed and stop. Never guess `current_day`, and never silently restart at day 1. Offer to re-run the assessment, or to accept a day number the learner states.

   I named `## Tasks` as the failed field and stopped the lesson. My exact learner-facing output was:

   > Required field failed: `## Tasks` is missing from `/tmp/pw-codex-test/PROGRESS.md`. The file has task-like lines, but the required section heading is absent, so the skill says to stop rather than infer the section. I can re-run the assessment to reconstruct a valid progress file; I will not silently restart or guess.

   > For this verification request, I’m treating that mandated stop as the observed result and documenting all later lesson stages as not reached.

2. The skill said:

   > 2. Read `level`, `current_day`, `## Levers`, and `## Tasks`.

   Partly done. `level: working`, `current_day: 1`, and all `## Levers` values were readable. `## Tasks` was not readable as a section because that heading is absent. This is the field failure that required the stop.

3. The skill said:

   > 3. If `current_day` is above 30, tell the learner the course is complete and stop.

   Not reached. The parsed value was 1, but step 1 had already required a stop.

4. The skill said:

   > 4. Read `days/NN.md`, where NN is `current_day` zero-padded to two digits.

   Not performed as a lesson action because of the required stop. I later inspected `days/01.md` read-only only to prepare this parity report; I did not present or execute it.

5. The skill said:

   > 5. Run the daily loop below.

   Not performed.

6. The skill said:

   > 6. Append one `## Log` line, update any lever scores the day changed, and increment `current_day`.

   Not performed. The temporary `PROGRESS.md` remained unchanged.

The numbered daily-loop instructions—“1. Concept”, “2. Write”, “3. Run”, “4. Critique”, and “5. Name it”—were consequently not reached.

## 3. Exercise tier

No exercise tier was presented. The file's `level: working` would ordinarily select `### Working`, whose Day 1 text is:

> Write a prompt for {{TASK}} whose deliverable is unambiguous. Someone reading only your prompt, without seeing any output, should be able to describe the finished artifact.

That quotation is the tier text inspected for this report, not text shown as part of a lesson. Presenting it would have violated the required stop.

## 4. `{{TASK}}` substitution

No. `{{TASK}}` was not substituted or presented anywhere in the lesson because `## Tasks` was missing. I did not guess that `Task 10: Dry runs, README, release` was the first task entry. The literal placeholder appears above only because item 3 quotes the source text for reporting.

The current rule is:

> Wherever `{{TASK}}` appears in any text you present, substitute the learner's first `## Tasks` entry. Never show the raw token to the learner.

Because no daily-loop text was presented, there were zero presentation sites requiring substitution and no raw token was shown during the lesson.

## 5. The key question: clean-context run

- Codex in this session has an isolated-agent dispatch tool named `spawn_agent`; it supports `fork_turns: "none"`, which can omit the lesson history.
- I did not run a learner prompt. No exercise was presented and no learner prompt was collected before the required stop, so there is no prompt or output to paste.
- The no-tool fallback was not applicable, but `SKILL.md` says:

  > If it cannot, or if dispatch fails, print the prompt in a fenced block and ask the learner to run it in a fresh chat and paste the output back.

  I did not output that fallback because no learner prompt existed and an isolated-agent tool was available.
- Did I at any point run the learner's prompt inside my own lesson context? **No.**

The prohibition was clear:

> Never run the learner's prompt in the lesson context. A contaminated run is worse than no run.

## 6. Secondary constraint

No secondary constraint was added because the Write step was not reached. If the lesson had proceeded, the two eligible weak levers would have been `pronoun: 2` and `particle: 2`; the skill requires selecting exactly one, not both:

> If any lever in `## Levers` scores 2 or below, add exactly one of them as a named secondary constraint — for example, "and bind every reference; you scored low on pronoun". One only.

Observed constraint count: **0**. No lever was selected.

## 7. Codex assumptions

No required tool, path, or feature was missing in this session. The skill contains this Codex-specific assumption:

> If this harness can dispatch an isolated agent, dispatch the prompt there and capture the output verbatim. In Codex this requires `multi_agent = true` under `[features]` in `~/.codex/config.toml`.

The runtime did expose `spawn_agent`, even though the local config's `[features]` section did not contain an explicit `multi_agent` entry. Thus the stated config requirement does not match the observable capability in this harness; capability detection by actual tool availability is more reliable here. This did not become an execution blocker because no prompt was collected.

## 8. Confusing, contradictory, or broken details

- The test fixture and skill contract disagree. The fixture has indented task-like lines but lacks the required `## Tasks` heading. The skill explicitly says to read `## Tasks` and to stop on a missing required field, so the intended Day 1 flow cannot start from the supplied exact fixture.
- The recovery instruction is overly broad: after any required field failure it says to “accept a day number the learner states.” A day number can repair a missing or unparseable `current_day`, but it cannot repair the missing `## Tasks` section encountered here.
- The supplied fixture also has no `## Log` heading, although session step 6 requires appending a `## Log` line and `assessment.md`'s canonical structure includes `## Log`. The earliest blocker was `## Tasks`, so this later ambiguity was not exercised.
- The task display is truncated (`… +5 completed`), so even if the missing heading were inferred, the state is not a complete canonical task list. The first visible open line could plausibly be treated as the first task, but the skill gives no permission to infer malformed state.
- The repository changed concurrently during this read-only test: it began at HEAD `7e55e98ea680d04191b7d8747d52af0cda727e2a` with a pre-existing modified `SKILL.md`, then advanced to clean HEAD `66ddd978615f2deb09384890320de7a3a0e84e17` via commit `fix: substitute {{TASK}} in exercise tiers and handle absent PROGRESS.md`. This test made no repository writes. The concurrent commit did not change the missing-`## Tasks` stop condition, but it is a reproducibility caveat.
- Because the mandated stop occurred before the daily loop, exercise presentation, placeholder substitution, isolated execution, critique comparison, self-rating, logging, lever updates, and day increment remain unverified.

**Verdict: NO—this exact skill/fixture combination does not complete a lesson; valid-state daily-loop behavior, `{{TASK}}` substitution, isolated before/after runs, critique, secondary-constraint selection, and progress updates remain unverified.**
