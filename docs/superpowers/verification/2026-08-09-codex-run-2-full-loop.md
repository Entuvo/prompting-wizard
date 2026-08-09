# Codex parity report 2: prompting-wizard Day 1

Test date: 2026-08-09  
Learner state: `/tmp/pw-codex-test/PROGRESS.md`  
Repository: `/Users/shergill/projects/prompting_skills/`

## 1. Exact `PROGRESS.md` contents and heading gate

This is the exact file content read from disk:

```markdown
# Progress

level: working
current_day: 1

## Levers
noun: 3    verb: 3    adjective: 3    adverb: 3
pronoun: 2    preposition: 3    conjunction: 3
determiner: 3    numeral: 3    interjection: 3    particle: 2

## Tasks
- Reviewing PRs on the payments service
- Writing incident postmortems
- Drafting API docs for external partners

## Log
- Day 0 — assessment — level working, diagnosis 6/10 — baseline noun 3, verb 3, adjective 3, adverb 3, pronoun 2, preposition 3, conjunction 3, determiner 3, numeral 3, interjection 3, particle 2
```

Confirmed: `## Levers`, `## Tasks`, and `## Log` were all present. The heading gate passed, so the lesson continued.

`AGENTS.md` was unambiguous:

> To run the prompting course, read `SKILL.md` and follow it.

## 2. Exercise tier

I presented the **Working** tier because the file says `level: working`. This is the tier text shown to the learner, after task substitution:

> Write a prompt for Reviewing PRs on the payments service whose deliverable is unambiguous. Someone reading only your prompt, without seeing any output, should be able to describe the finished artifact.

I then showed this separately as the secondary constraint:

> Secondary constraint: bind every reference explicitly; you scored 2 on pronoun. Add exactly this one secondary constraint.

The supplied learner answer was then accepted verbatim:

```text
Help me with the PR review
```

## 3. `{{TASK}}` substitution

Yes. In every piece of Day 1 lesson text I presented, including the Working exercise tier, I replaced `{{TASK}}` with the first `## Tasks` entry:

> Reviewing PRs on the payments service

The learner saw:

> Write a prompt for Reviewing PRs on the payments service whose deliverable is unambiguous. Someone reading only your prompt, without seeing any output, should be able to describe the finished artifact.

The Before/After examples shown were:

> Help me with Reviewing PRs on the payments service.

> Produce a five-bullet review of Reviewing PRs on the payments service, one bullet per correctness issue.

No raw placeholder was shown during the lesson. Raw `{{TASK}}` tokens in this report are meta-reporting, not lesson presentation.

## 4. The run step

### Isolated-agent tool

The available isolated-agent tool was `spawn_agent`, called with `fork_turns: "none"`. The two runs used different agents: `day1_original_run` and `day1_rewritten_run`.

### Config check and observed capability

Yes, I checked `~/.codex/config.toml`. It had a `[features]` heading but no explicit `multi_agent` setting. The `SKILL.md` version read at lesson start said:

> If this harness can dispatch an isolated agent, dispatch the prompt there and capture the output verbatim. In Codex this requires `multi_agent = true` under `[features]` in `~/.codex/config.toml`.

That did **not** match observed behavior: `spawn_agent` was exposed and both dispatches were accepted despite no explicit config entry. During the test, the working-tree copy of `SKILL.md` changed concurrently and now says capability should be detected from tool availability instead; that was not the text used to decide the run at lesson start.

### Original prompt run

Yes. The isolated agent received exactly this message and no lesson history:

```text
Help me with the PR review
```

Its final output was:

```markdown
## Standards

- Low: six commits use `fix:` although the documented allowed prefixes are `feat`, `docs`, `chore`, and `test` ([plan](/Users/shergill/projects/prompting_skills/docs/superpowers/plans/2026-08-09-prompting-wizard.md:21)). No material code-smell findings.

## Spec

- High: global `{{TASK}}` substitution ([SKILL.md](/Users/shergill/projects/prompting_skills/prompting-wizard/SKILL.md:24)) erases the literal template slot that day 28 is teaching ([28.md](/Users/shergill/projects/prompting_skills/prompting-wizard/days/28.md:22)). Learners will see a concrete task where the example claims to show a reusable slot.

- High: day 29 records only the task ([29.md](/Users/shergill/projects/prompting_skills/prompting-wizard/days/29.md:25)), but day 30 expects the finished prompt in that same log entry ([30.md](/Users/shergill/projects/prompting_skills/prompting-wizard/days/30.md:25)). Since sessions share state only through `PROGRESS.md`, the capstone cannot resume.

- High: the same state gap breaks day 27’s fallback: it promises to retrieve a previous failed prompt from the log ([27.md](/Users/shergill/projects/prompting_skills/prompting-wizard/days/27.md:17)), while the canonical log stores only scores and the learner’s observation ([SKILL.md](/Users/shergill/projects/prompting_skills/prompting-wizard/SKILL.md:56)).

- High: day 30 requires an unfamiliar case followed by a fix ([plan](/Users/shergill/projects/prompting_skills/docs/superpowers/plans/2026-08-09-prompting-wizard.md:808)). Novice reruns the original case, while Working records the failure without explicitly fixing and revalidating it ([30.md](/Users/shergill/projects/prompting_skills/prompting-wizard/days/30.md:27)).

- Medium: day 21 Advanced changes ordering and three weak levers simultaneously ([21.md](/Users/shergill/projects/prompting_skills/prompting-wizard/days/21.md:43)), so output changes cannot be attributed to ordering as the lesson requires.

- Medium: raw task substitution creates malformed prompts using the assessment’s own examples: `Review {{TASK}}` becomes “Review Reviewing PRs…” ([assessment.md](/Users/shergill/projects/prompting_skills/prompting-wizard/assessment.md:69), [12.md](/Users/shergill/projects/prompting_skills/prompting-wizard/days/12.md:17)).

Structural validation, Python compilation, and `git diff --check` all pass. No files were changed.
```

The vague prompt caused the agent to infer a repository-wide PR review and spawn two review subagents of its own. That behavior was not requested by the lesson harness and was not simulated.

### Rewritten prompt run

The stronger prompt I wrote was:

```text
Produce a five-bullet review of the payments-service PR, one bullet per correctness issue.
```

Yes, it was run in a **separate** clean agent with no lesson history and no context from the first clean agent. The second agent emitted this exact response:

```text
I found no payments-service repository, branch, PR diff, or fixture in the workspace; the phrase is only the learner task substituted into Day 1's prompt. Do you have a PR URL/diff or want the run to demonstrate that the rewritten prompt still lacks the source artifact?
```

This was a clarification message rather than a final answer. I did not answer it, because supplying a PR URL, diff, or other new context would change the prompt being tested. I interrupted the waiting agent after capturing the message.

Did I run either prompt inside my own lesson context? **No.**

## 5. Secondary constraint

Yes. I added exactly **one** secondary constraint, using `pronoun`, which scored 2:

> Secondary constraint: bind every reference explicitly; you scored 2 on pronoun. Add exactly this one secondary constraint.

`particle` also scored 2, but I did not add it. The learner's supplied answer did not satisfy the pronoun constraint, and the Day 1 critique rubric did not provide a place to score that secondary lever.

## 6. Rubric critique

Yes. The critique used only the Noun rubric and quoted its score anchor. This is the complete critique shown:

> Critique against `rubrics.md#noun`:
>
> - Artifact: **1/5** — “No artifact named. The prompt describes a topic or a wish, not a thing to produce.” In “Help me with the PR review,” “PR review” names the activity being helped with, but the prompt never asks for a specific thing to be produced.

The quoted anchor is verbatim from `rubrics.md`:

> No artifact named. The prompt describes a topic or a wish, not a thing to produce.

There is one measured criterion in the Noun rubric—“the artifact the prompt asks for”—so there was one criterion-level score.

## 7. Intended `PROGRESS.md` write-back

I did not write to `PROGRESS.md`. `SKILL.md` instructed:

> Append one `## Log` line, update any lever scores the day changed, and increment `current_day`.

It also instructed:

> Ask the learner which single change moved the output, and for a 1–5 self-rating. Log both.

The final learner-facing question was:

> Name it: Which single change moved the output, and what is your 1–5 self-rating?

The test instructions supplied a prompt answer but supplied no answer to this final question. Therefore an honest complete log line could not be formed. Based on the completed rubric scoring, the intended write-back template would be:

```markdown
current_day: 2
noun: 1
- Day 1 — noun — self <not supplied>, rubric 1 — "<single change not supplied>"
```

The exact `noun` update policy is only implied by “update any lever scores the day changed”; `SKILL.md` does not explicitly say whether to overwrite it with the rubric score, average it, or use another rule. That makes even `noun: 1` less than fully specified. No write-back was performed.

## 8. Confusing, contradictory, or broken

- **The literal task substitution is grammatically broken.** The required first entry is a gerund phrase, producing “Help me with Reviewing PRs…” and “review of Reviewing PRs…”. The skill substitutes raw task text without adapting grammar.
- **The improved noun prompt lacked its source artifact.** Naming “a five-bullet review” clearly did not provide a PR URL, branch, or diff, so the rewritten run stopped for clarification. The comparison tests both noun specificity and missing input/context; it does not isolate the noun lever cleanly.
- **The vague original looked more successful by exploiting workspace context.** It inferred a repository-wide review, delegated work, and returned findings. The stronger prompt returned no review. This is genuine output, but pedagogically it can teach the opposite lesson unless the tutor explains the missing-input confounder—which the rubric-only rule discourages as “freelance criticism.”
- **The secondary constraint is not integrated into critique.** The learner violated the named pronoun constraint, but Day 1 says to score only the Noun rubric. The skill says to add a weak lever yet provides no instruction to score or discuss whether it was practised successfully.
- **The config requirement was false in this harness.** No explicit `multi_agent` entry was present, yet `spawn_agent` worked. A concurrent working-tree edit changed this rule during the test, confirming the mismatch but also making the tested source version unstable.
- **Clean conversation context is not an isolated filesystem.** `fork_turns: "none"` removed lesson history, but the agent shared the workspace and could inspect or potentially modify the repository. Adding the user's read-only rule to its message would have violated the requirement to execute the learner prompt verbatim. The original agent claimed “No files were changed,” but the repository was dirty at the final integrity check.
- **Repository state changed during the run.** An integrity check showed modifications to `README.md`, `SKILL.md`, and several day files. Before report finalization, a concurrent process committed those changes as `09a9a88182d0d5f41a94ca184ca8cef758ce09ba` (`fix: final review wave — capstone handoff, completion section, tutor directions, rubric alignment`), advancing HEAD from `66ddd978615f2deb09384890320de7a3a0e84e17` and leaving the worktree clean. I made no direct repository edits or commits, and the original clean agent reported no writes, but I did not capture a fresh status baseline at the start of this request and therefore cannot attribute the changes honestly. I did not revert or alter them.
- **The two outputs were not naturally comparable.** The first was a final multi-section review; the second was a non-final clarification message. Both are authentic, but “side by side” does not yield a controlled quality comparison.
- **The Name-it step cannot finish unattended.** The supplied test answer covered only the Write step. Without a single-change answer and self-rating, the required log entry cannot be completed without fabrication.
- **Lever update semantics are underspecified.** “Update any lever scores the day changed” does not define whether the daily rubric score replaces the existing score or how secondary-lever performance affects state.

**Verdict: NO—not fully; clean-agent dispatch and authentic outputs were verified, but a complete Day 1 log/write-back, controlled output improvement, secondary-lever evaluation, repository-write attribution, and lever-score update semantics remain unverified.**
