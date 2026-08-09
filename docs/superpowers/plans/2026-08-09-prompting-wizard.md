# Prompting Wizard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a shippable 30-day prompting course as a portable markdown skill that assesses the learner, teaches one prompting lever per day using their own real tasks, and runs their prompts in a clean context so they see the difference rather than being told about it.

**Architecture:** The skill is markdown only. `SKILL.md` is the entire tutor loop; `days/01.md`–`days/30.md` and `rubrics.md` are content it loads; `PROGRESS.md` in the learner's directory is the only state. A dev-time Python validator, kept outside the shipped directory, enforces structural consistency across the 35 content files.

**Tech Stack:** Markdown. Python 3 stdlib for the dev-time validator. No runtime dependencies, no build step.

## Global Constraints

- **Shipped skill is markdown only.** No scripts, manifests, or plugin-marketplace assumptions inside `prompting-wizard/`.
- **Relative paths only** in every shipped file. The single documented exception is `~/.codex/config.toml`, referenced in `SKILL.md`.
- **No harness-specific tool names** in shipped instructions. Capabilities are stated as requirements ("run in a context with no lesson history"), never as tool calls.
- **Both harnesses read the same `SKILL.md` body.** `AGENTS.md` is a pointer only and contains no lesson logic.
- **Lever vocabulary is fixed** at exactly these 11 slugs, used identically in `rubrics.md`, `PROGRESS.md`, and every day file: `noun`, `verb`, `adjective`, `adverb`, `pronoun`, `preposition`, `conjunction`, `determiner`, `numeral`, `interjection`, `particle`.
- **Concept sections are ≤200 words.**
- **Every day file** has exactly these four H2 sections in this order: `## Concept`, `## Before / After`, `## Exercise`, `## Rubric`. `## Exercise` contains exactly `### Novice`, `### Working`, `### Advanced`.
- **Domain slot token is `{{TASK}}`** everywhere. The skill substitutes the learner's first `## Tasks` entry.
- **Commit after every task.** Conventional commit prefixes: `feat`, `docs`, `chore`, `test`.

---

## File Structure

```
prompting-wizard/          # the shipped skill — copy or clone anywhere
  SKILL.md                 # tutor loop, the only logic
  AGENTS.md                # Codex entry point, pointer to SKILL.md
  assessment.md            # day-0 script
  rubrics.md               # 26 rubrics (11 levers + 15 techniques)
  days/01.md … days/30.md  # lesson content
tools/
  validate.py              # dev-time structural check, never shipped
docs/superpowers/
  specs/2026-08-09-prompting-wizard-design.md
  plans/2026-08-09-prompting-wizard.md
README.md                  # install and run instructions
```

Responsibilities: `SKILL.md` owns control flow and nothing else. `rubrics.md` owns all scoring criteria, so critique language stays identical across 30 days. Each `days/NN.md` owns one lesson's content and references a rubric by slug rather than restating criteria. `tools/validate.py` owns the invariants that hold the 35 files together.

---

## Rubric slug registry

Every slug below is an H2 heading in `rubrics.md`. Day files reference them as `rubrics.md#<slug>`. The validator checks both directions.

**Levers (11):** `noun`, `verb`, `adjective`, `adverb`, `pronoun`, `preposition`, `conjunction`, `determiner`, `numeral`, `interjection`, `particle`

**Techniques (15):** `role-framing`, `few-shot-examples`, `output-schemas`, `task-decomposition`, `reasoning-scaffolds`, `negative-constraints`, `context-ordering`, `system-prompts`, `agent-and-tool-prompting`, `self-critique-loops`, `writing-evals`, `token-economy`, `failure-diagnosis`, `prompt-library`, `capstone`

---

### Task 1: Repo skeleton and structural validator

**Files:**
- Create: `tools/validate.py`
- Create: `prompting-wizard/days/.gitkeep`

**Interfaces:**
- Consumes: nothing.
- Produces: `tools/validate.py` exposing `check(require_all_days: bool = False) -> list[str]` returning human-readable problem strings, plus module-level `SKILL: Path` and `section(text: str, heading: str) -> str | None`. A `__main__` block prints problems to stderr and exits 1 if any. Every later task runs `python3 tools/validate.py` as its test.

- [ ] **Step 1: Write the validator**

Create `tools/validate.py`:

```python
#!/usr/bin/env python3
"""Structural check for the prompting-wizard skill directory.

Dev-time only. Lives outside the shipped skill and is never loaded by it.

Run:  python3 tools/validate.py             # checks what exists
      python3 tools/validate.py --complete  # also requires all 30 day files
Exit: 0 clean, 1 problems (listed on stderr).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "prompting-wizard"

TOP_FILES = ("SKILL.md", "AGENTS.md", "assessment.md", "rubrics.md")

LEVERS = ("noun", "verb", "adjective", "adverb", "pronoun", "preposition",
          "conjunction", "determiner", "numeral", "interjection", "particle")

TECHNIQUES = ("role-framing", "few-shot-examples", "output-schemas",
              "task-decomposition", "reasoning-scaffolds", "negative-constraints",
              "context-ordering", "system-prompts", "agent-and-tool-prompting",
              "self-critique-loops", "writing-evals", "token-economy",
              "failure-diagnosis", "prompt-library", "capstone")

DAY_SECTIONS = ("## Concept", "## Before / After", "## Exercise", "## Rubric")
TIERS = ("### Novice", "### Working", "### Advanced")
CONCEPT_MAX_WORDS = 200
ABS_PATH = re.compile(r"(?:/Users/|/home/|~/)")
ABS_PATH_ALLOWED = ("~/.codex/config.toml",)


def slugify(heading):
    return re.sub(r"[^a-z0-9]+", "-", heading.strip().lower()).strip("-")


def h2_slugs(text):
    return {slugify(h) for h in re.findall(r"^## (.+)$", text, re.M)}


def section(text, heading):
    """Body of one section, up to the next heading of the same or higher level."""
    level = len(heading) - len(heading.lstrip("#"))
    pattern = rf"^{re.escape(heading)}\s*$\n(.*?)(?=^#{{1,{level}}} |\Z)"
    match = re.search(pattern, text, re.M | re.S)
    return match.group(1) if match else None


def check(require_all_days=False):
    if not SKILL.is_dir():
        return [f"skill directory not found: {SKILL}"]

    errors = []
    for name in TOP_FILES:
        if not (SKILL / name).is_file():
            errors.append(f"{name}: missing")

    rubrics_path = SKILL / "rubrics.md"
    rubric_slugs = h2_slugs(rubrics_path.read_text()) if rubrics_path.is_file() else set()
    for expected in LEVERS + TECHNIQUES:
        if expected not in rubric_slugs:
            errors.append(f"rubrics.md: no rubric for '{expected}'")

    for n in range(1, 31):
        day = SKILL / "days" / f"{n:02d}.md"
        label = f"days/{n:02d}.md"
        if not day.is_file():
            if require_all_days:
                errors.append(f"{label}: missing")
            continue

        text = day.read_text()
        for heading in DAY_SECTIONS:
            if section(text, heading) is None:
                errors.append(f"{label}: missing '{heading}'")

        concept = section(text, "## Concept")
        if concept is not None:
            words = len(concept.split())
            if words > CONCEPT_MAX_WORDS:
                errors.append(f"{label}: concept is {words} words (max {CONCEPT_MAX_WORDS})")

        exercise = section(text, "## Exercise") or ""
        for tier in TIERS:
            if tier not in exercise:
                errors.append(f"{label}: exercise missing '{tier}'")

        rubric = section(text, "## Rubric") or ""
        refs = re.findall(r"rubrics\.md#([a-z0-9-]+)", rubric)
        if not refs:
            errors.append(f"{label}: rubric section has no 'rubrics.md#slug' reference")
        for ref in refs:
            if ref not in rubric_slugs:
                errors.append(f"{label}: rubric '{ref}' not in rubrics.md")

    for path in sorted(SKILL.rglob("*.md")):
        for i, line in enumerate(path.read_text().splitlines(), 1):
            if ABS_PATH.search(line) and not any(a in line for a in ABS_PATH_ALLOWED):
                errors.append(f"{path.relative_to(SKILL)}:{i}: absolute path in shipped file")

    return errors


if __name__ == "__main__":
    problems = check(require_all_days="--complete" in sys.argv)
    for problem in problems:
        print(problem, file=sys.stderr)
    print(f"{len(problems)} problem(s)" if problems else "ok")
    sys.exit(1 if problems else 0)
```

- [ ] **Step 1b: Apply the three amendments below**

> **Amendment — human ruling, 2026-08-09.** The Task 1 review raised three findings against the source above. The ruling was to fix all three. Apply these on top of the code as written; the expected problem counts in Steps 3 and 4 are unchanged, because none of these paths fire against an empty skill directory.

**(a) Fenced code blocks must not be parsed as headings.** `section()`'s boundary lookahead `^#{1,2} ` matches any line starting with `# `, so a comment line inside a fenced example (day 17 requires a filled-in output schema) would truncate the section and report tiers as missing that are present. Add after `slugify()`:

```python
FENCE = re.compile(
    r"^(?P<fence>`{3,}|~{3,})[^\n]*\n.*?^(?P=fence)[`~]*[ \t]*$",
    re.M | re.S,
)


def strip_fences(text):
    """Blank out fenced code blocks, preserving line count so line numbers hold."""
    return FENCE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
```

Then make `h2_slugs()` and `section()` operate on stripped text — each begins with `text = strip_fences(text)`. The absolute-path scan keeps reading raw text: a bad path inside a fenced install snippet still has to be caught.

**(b) Unreadable files must report, not crash.** Add:

```python
def read_text(path, errors, label):
    """Return the file's text, or None after recording why it could not be read."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"{label}: unreadable ({type(exc).__name__})")
        return None
```

Route all three read sites through it. `rubrics.md`: `text = read_text(rubrics_path, errors, "rubrics.md")`, then `rubric_slugs = h2_slugs(text) if text else set()`. Day files and the absolute-path scan: `continue` when it returns `None`.

**(c) The absolute-path allowlist must be match-local.** `not any(a in line for a in ABS_PATH_ALLOWED)` exempts the whole line, so `~/.codex/config.toml` sitting beside a real absolute path hides it. Replace the loop body with:

```python
        for i, line in enumerate(text.splitlines(), 1):
            for match in ABS_PATH.finditer(line):
                tail = line[match.start():]
                if not any(tail.startswith(a) for a in ABS_PATH_ALLOWED):
                    errors.append(f"{path.relative_to(SKILL)}:{i}: absolute path in shipped file")
                    break
```

- [ ] **Step 2: Create the days directory placeholder**

```bash
mkdir -p prompting-wizard/days && touch prompting-wizard/days/.gitkeep
```

- [ ] **Step 3: Run the validator to verify it fails**

Run: `python3 tools/validate.py`
Expected: FAIL (exit 1). Output includes `SKILL.md: missing`, `AGENTS.md: missing`, `assessment.md: missing`, `rubrics.md: missing`, and 26 `rubrics.md: no rubric for '<slug>'` lines. Final line: `30 problem(s)`.

- [ ] **Step 4: Verify the day check is conditional**

Run: `python3 tools/validate.py --complete`
Expected: FAIL with the same 30 problems **plus** 30 `days/NN.md: missing` lines. Final line: `60 problem(s)`. This confirms unfinished day files do not block intermediate tasks.

- [ ] **Step 5: Commit**

```bash
git add tools/validate.py prompting-wizard/days/.gitkeep
git commit -m "chore: add structural validator for skill content"
```

---

### Task 2: Rubrics

**Files:**
- Create: `prompting-wizard/rubrics.md`

**Interfaces:**
- Consumes: the slug registry above.
- Produces: 26 H2 sections whose slugified headings match the registry exactly. Every day file references these as `rubrics.md#<slug>`.

- [ ] **Step 1: Write the file header and the canonical first rubric**

Create `prompting-wizard/rubrics.md` starting with:

````markdown
# Rubrics

One rubric per lever and per technique. Every lesson scores against a rubric here rather than restating criteria, so the same weakness gets the same name on day 3 and on day 27.

Scores are 1–5. Anchors are given for every point. Score the prompt as written, not the intent behind it.

## Noun

**Measures:** the artifact the prompt asks for.

| Score | Anchor |
|---|---|
| 1 | No artifact named. The prompt describes a topic or a wish, not a thing to produce. |
| 2 | A category is named ("a review", "some notes") but its shape is left open. |
| 3 | The artifact is recognisable, but a reasonable reader could still deliver two different things. |
| 4 | The artifact is named unambiguously. Someone reading only the prompt could describe the finished output. |
| 5 | Named unambiguously and economically — no words spent on the artifact beyond what pins it down. |

**Fastest fix:** ask what physical thing lands when the model finishes. Put that noun phrase in the prompt.
````

- [ ] **Step 2: Write the remaining 10 lever rubrics**

Use the identical structure — `## <Name>`, `**Measures:**`, a five-row 1–5 table, `**Fastest fix:**`. Write the 2, 3 and 4 anchors by interpolating between the 1 and 5 anchors given here, as done for `## Noun` above.

| Heading | Measures | Score 1 anchor | Score 5 anchor | Fastest fix |
|---|---|---|---|---|
| `## Verb` | the operation requested | No verb, or one that names no operation ("help", "look at") | Exactly one operation named, and it is the operation actually wanted | Name the operation: summarise, rank, critique, refactor, enumerate |
| `## Adjective` | quality constraints on the artifact | No quality named; any output passes | Every quality that matters is named, and none that do not | List the two qualities that would make you reject the output, then state them |
| `## Adverb` | manner and degree of the action | Manner unspecified; depth left to chance | Depth and manner set so output length and thoroughness are predictable | Say how thoroughly, and in what manner |
| `## Pronoun` | reference binding | Pronouns with no antecedent ("fix it", "do this") | Every reference resolves inside the prompt or to a quoted block | Replace each it/this/that with the thing it means |
| `## Preposition` | scope and relation | No scope; the task could touch anything | Boundaries, audience and exclusions all set | Add: in what, for whom, without what |
| `## Conjunction` | conditional logic | Branching cases collapsed into one instruction, so edge cases silently pick a branch | Each branch stated with its condition and its fallback | Write down the if/then/otherwise you are holding in your head |
| `## Determiner` | definiteness and quantity binding | Bare nouns leave it unclear whether one, some, or all are meant | Each noun is bound — the, a, each, every, any — with no reading left open | Put the/a/each in front of every noun and see which changes the meaning |
| `## Numeral` | budgets that make output checkable | No quantity anywhere; length and count unbounded | Every countable dimension bounded, and the bounds checkable without judgement | Add a count and a length you could verify with a ruler |
| `## Interjection` | attention and priority markers | All instructions carry equal weight; the critical one is buried mid-paragraph | The must-not-fail instruction is marked and positioned so it cannot be missed | Mark the one instruction you would be angry about being ignored |
| `## Particle` | phrasal precision | Phrasal verbs used loosely, so the operation is ambiguous (look up / look over / look into) | Every phrasal verb chosen deliberately; no substitution preserves the meaning | Swap the particle and check whether the task changed. If it did, you needed the precise one |

- [ ] **Step 3: Write the 15 technique rubrics**

Same structure. Headings must slugify to the registry values — `## Role framing` → `role-framing`, `## Few-shot examples` → `few-shot-examples`, and so on.

| Heading | Measures | Score 1 anchor | Score 5 anchor | Fastest fix |
|---|---|---|---|---|
| `## Role framing` | whether the role changes the output | Role asserted with no bearing on output ("you are a world-class expert") | Role changes what is included, excluded and assumed, and you can say how | Name the knowledge or standard the role brings; drop the flattery |
| `## Few-shot examples` | what the examples teach | No examples, or examples that only show the easy case | Examples cover the boundary case and the failure case | Add the example you would worry it gets wrong |
| `## Output schemas` | the format contract | Format unspecified, or described in prose only | An exact structure given, which output can be checked against mechanically | Write the shape you want, filled with dummy values |
| `## Task decomposition` | whether the work is split correctly | One prompt carries several tasks that interfere | Work split so each step has one output and a clear input from the last | Find the "and then" in your prompt and cut there |
| `## Reasoning scaffolds` | whether reasoning is structured where needed | Reasoning demanded without structure, or suppressed where it was needed | The reasoning steps asked for match the ones the task requires | Name the intermediate you want to see before the answer |
| `## Negative constraints` | what is ruled out | No exclusions; known failure modes not ruled out | Exclusions are specific, and each prevents a failure you have actually seen | Write down what it did wrong last time, and forbid exactly that |
| `## Context ordering` | placement of instruction and material | Instruction buried after a wall of context, or context missing where needed | Instruction and context ordered so the model reads what it needs when it needs it | Task first, material second, constraints last |
| `## System prompts` | separation of standing rules from the turn | Durable rules repeated per turn, or turn-specific detail promoted into standing rules | Standing behaviour and per-turn request cleanly separated | Ask which lines you would want true on every turn — those are the system prompt |
| `## Agent and tool prompting` | tool use and stopping conditions | Tool use implied but not specified; no stopping condition | Which tools, when, and what "done" means are all stated | State the stop condition first, then the tools |
| `## Self-critique loops` | whether output is checked | Single-pass output accepted with no check | A check the model can apply to its own output, with a stated action when it fails | Name the test the output must pass, and require it be run |
| `## Writing evals` | whether quality is measurable | Quality judged by feel; no criteria written down | Criteria written before the output, specific enough that two people would score the same | Write the three checks you would apply, then apply them |
| `## Token economy` | whether every token earns its place | Context padded with material the task never uses | Every included token earns its place; cuts made without losing accuracy | Delete a third of the context and see whether the output degrades |
| `## Failure diagnosis` | whether the cause is identified | Failure blamed on the model; prompt unchanged | The failing lever is identified by name and the fix targets it | Ask which of the 11 levers was underspecified, and fix that one |
| `## Prompt library` | reusability | Prompts rewritten from scratch each time | Reusable prompts stored with their slots and their known failure modes | Save the prompt with the task slot left as a blank |
| `## Capstone` | production readiness | Prompt works once, on the example it was written against | Prompt is specified, evaluated against written criteria, and its failure modes documented | Run it on the case you did not design it for |

- [ ] **Step 4: Run the validator**

Run: `python3 tools/validate.py`
Expected: FAIL, but with **zero** `no rubric for` lines. Only `SKILL.md: missing`, `AGENTS.md: missing`, `assessment.md: missing` remain. Final line: `3 problem(s)`.

- [ ] **Step 5: Commit**

```bash
git add prompting-wizard/rubrics.md
git commit -m "feat: add 26 scoring rubrics for levers and techniques"
```

---

### Task 3: Day-0 assessment

**Files:**
- Create: `prompting-wizard/assessment.md`

**Interfaces:**
- Consumes: the lever slugs from Task 2.
- Produces: the `PROGRESS.md` contract — keys `level` (one of `novice`, `working`, `advanced`) and `current_day` (integer), plus sections `## Levers`, `## Tasks`, `## Log`. `SKILL.md` in Task 4 reads exactly these names.

- [ ] **Step 1: Write the assessment script**

Create `prompting-wizard/assessment.md`:

````markdown
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
````

- [ ] **Step 2: Run the validator**

Run: `python3 tools/validate.py`
Expected: FAIL with `SKILL.md: missing` and `AGENTS.md: missing`. Final line: `2 problem(s)`.

- [ ] **Step 3: Commit**

```bash
git add prompting-wizard/assessment.md
git commit -m "feat: add day-0 assessment and PROGRESS.md contract"
```

---

### Task 4: The tutor loop

**Files:**
- Create: `prompting-wizard/SKILL.md`
- Create: `prompting-wizard/AGENTS.md`

**Interfaces:**
- Consumes: the `PROGRESS.md` contract from Task 3, the rubric slugs from Task 2, and the day-file section names from Global Constraints.
- Produces: nothing later tasks import. This is the top of the call graph.

- [ ] **Step 1: Write SKILL.md**

Create `prompting-wizard/SKILL.md`:

````markdown
---
name: prompting-wizard
description: Use when the user wants to learn, practise, or get better at prompting - runs a 30-day, 20-minute-a-day course that assesses the learner once and then teaches one prompting lever per day using the learner's own real tasks.
---

# Prompting Wizard

A 30-day course. One 20-minute lesson per session. All state lives in `PROGRESS.md` in the learner's working directory.

## Every session

1. Look for `PROGRESS.md` in the learner's working directory.
   - **Absent** → read `assessment.md` and run it. Writing `PROGRESS.md` ends the session.
   - **Present but a required field is missing or unparseable** → name the field that failed and stop. Never guess `current_day`, and never silently restart at day 1. Offer to re-run the assessment, or to accept a day number the learner states.
   - **Present and valid** → continue.
2. Read `level`, `current_day`, `## Levers`, and `## Tasks`.
3. If `current_day` is above 30, tell the learner the course is complete and stop.
4. Read `days/NN.md`, where NN is `current_day` zero-padded to two digits.
5. Run the daily loop below.
6. Append one `## Log` line, update any lever scores the day changed, and increment `current_day`.

## The daily loop — 20 minutes

**1. Concept — 3 min.** Present the day's `## Concept` verbatim. Then present `## Before / After`, substituting the learner's first `## Tasks` entry wherever `{{TASK}}` appears.

**2. Write — 5 min.** Present the `## Exercise` tier matching `level`: `### Novice`, `### Working`, or `### Advanced`. If any lever in `## Levers` scores 2 or below, add exactly one of them as a named secondary constraint — for example, "and bind every reference; you scored low on pronoun". One only. Ask for the learner's prompt, then wait.

**3. Run — 2 min.** Execute the learner's prompt **verbatim** in a context containing no lesson history. See Clean-context execution. Show the output unedited, and say nothing about it yet.

**4. Critique — 7 min.** Score the prompt against the rubric named in the day's `## Rubric` section, criterion by criterion, 1–5, quoting the rubric's anchor for each score you give. Then write a stronger version of the prompt, run it in a **separate** clean context, and show both outputs side by side.

**5. Name it — 3 min.** Ask the learner which single change moved the output, and for a 1–5 self-rating. Log both.

## Clean-context execution

The learner's prompt must run with no lesson history in context. Lesson context contaminates the output and destroys the comparison the exercise depends on.

- If this harness can dispatch an isolated agent, dispatch the prompt there and capture the output verbatim. In Codex this requires `multi_agent = true` under `[features]` in `~/.codex/config.toml`.
- If it cannot, or if dispatch fails, print the prompt in a fenced block and ask the learner to run it in a fresh chat and paste the output back.

Never run the learner's prompt in the lesson context. A contaminated run is worse than no run.

Run the rewritten prompt in a **separate** clean context from the learner's. Reusing one context primes the second run with the first run's output.

## Rules

- Never improve the learner's prompt before running it. They have to watch their own words fail.
- Never skip the run step, and never summarise output you did not actually get.
- Score against the rubric only. No freelance criticism.
- A lever scoring 2 or below is practised as a secondary constraint on a later day, never by repeating its lesson.
- Skipped days carry no penalty and no backlog. Resume at `current_day`.
- Days 14 and 21 are review days: draw their material from the three lowest-scoring levers.

## Log line format

Append one line per completed day:

```
- Day 12 — interjection — self 3, rubric 4 — "priority markers changed what it did first"
```
````

- [ ] **Step 2: Write AGENTS.md**

Create `prompting-wizard/AGENTS.md`:

```markdown
# prompting-wizard

To run the prompting course, read `SKILL.md` and follow it.

Nothing else in this directory is entry-point logic. `days/`, `rubrics.md`, and `assessment.md` are content that `SKILL.md` loads. Do not duplicate lesson behaviour here — this file is a pointer, so that the Claude Code and Codex entry points cannot drift apart.
```

- [ ] **Step 3: Run the validator**

Run: `python3 tools/validate.py`
Expected: PASS. Output `ok`, exit 0. The `~/.codex/config.toml` reference in `SKILL.md` must not trip the absolute-path check — if it does, the allowlist in `tools/validate.py` is wrong and the validator needs fixing, not `SKILL.md`.

- [ ] **Step 4: Check the frontmatter description covers the obvious asks**

Read the `description` field against these three requests and confirm each would plausibly match: "teach me to prompt better", "I want to get good at prompting", "start the prompting course". If any would not match, widen the description.

- [ ] **Step 5: Commit**

```bash
git add prompting-wizard/SKILL.md prompting-wizard/AGENTS.md
git commit -m "feat: add tutor loop and Codex entry point"
```

---

### Task 5: Day 1 — the canonical lesson

**Files:**
- Create: `prompting-wizard/days/01.md`

**Interfaces:**
- Consumes: `rubrics.md#noun` from Task 2, and the section contract from Global Constraints.
- Produces: the lesson file shape that days 2–30 follow. Tasks 6–9 depend on this exact structure.

This task stands alone so the template gets a full review before 29 more files are generated against it.

- [ ] **Step 1: Write the lesson**

Create `prompting-wizard/days/01.md`:

````markdown
# Day 1 — Noun: name the artifact

## Concept

Most weak prompts never say what they want made. "Help me with this PR" names no artifact, so the model guesses: a summary, a list of nitpicks, a rewrite, a question back. Any of those satisfies "help".

The noun is the deliverable. Naming it collapses the space of acceptable answers faster than any other lever. "A five-bullet review focused on correctness" and "a one-paragraph merge recommendation" are both help; only one of them is what you wanted.

Here is the test. Read your prompt and ask what physical thing lands when it finishes. If you cannot name it in a noun phrase, the model cannot either — so it will pick for you.

Nouns compound with counts and formats, but those are later levers. Today, just name the thing.

## Before / After

**Before**

> Help me with {{TASK}}.

**After**

> Produce a five-bullet review of {{TASK}}, one bullet per correctness issue.

The verb barely moved. The noun did the work: "a five-bullet review" is a thing that either exists at the end or does not.

## Exercise

Pick one of your recurring tasks. Write a single prompt for it.

### Novice

Fill the blank with a noun phrase naming exactly what you want back, then send the completed line as your prompt.

> Produce ________ for {{TASK}}.

### Working

Write a prompt for {{TASK}} whose deliverable is unambiguous. Someone reading only your prompt, without seeing any output, should be able to describe the finished artifact.

### Advanced

Write a prompt for {{TASK}} that names the artifact unambiguously in under 15 words total. Precision without length is the constraint — every word you spend has to be pinning the artifact down.

## Rubric

Score against `rubrics.md#noun`.
````

- [ ] **Step 2: Run the validator**

Run: `python3 tools/validate.py`
Expected: PASS, `ok`, exit 0.

- [ ] **Step 3: Check the concept word count has headroom**

Run: `python3 -c "import sys; sys.path.insert(0,'tools'); import validate; t=(validate.SKILL/'days/01.md').read_text(); print(len(validate.section(t,'## Concept').split()))"`
Expected: a number below 180. Later days need the same headroom, and exceeding 200 is a hard validator failure.

- [ ] **Step 4: Check the domain slot**

Run: `grep -c '{{TASK}}' prompting-wizard/days/01.md`
Expected: `4` or more. Every place the learner's real work should appear uses the token, and no day file hardcodes an example domain.

- [ ] **Step 5: Commit**

```bash
git add prompting-wizard/days/01.md
git commit -m "feat: add day 1 lesson and establish the lesson template"
```

---

### Task 6: Days 2–7 — remaining core levers and week-1 composition

**Files:**
- Create: `prompting-wizard/days/02.md` … `prompting-wizard/days/07.md`

**Interfaces:**
- Consumes: the lesson structure from Task 5 (`## Concept`, `## Before / After`, `## Exercise` with `### Novice`/`### Working`/`### Advanced`, `## Rubric`), and rubric slugs from Task 2.
- Produces: nothing later tasks import.

- [ ] **Step 1: Write days 2–7**

Each file carries the four H2 sections and three exercise tiers, with `{{TASK}}` as the domain slot. Content per day:

| Day | Title | Rubric reference | Before seed | After seed | Advanced constraint |
|---|---|---|---|---|---|
| 02 | Verb: task precision | `rubrics.md#verb` | `Look at {{TASK}}.` | `Rank the correctness issues in {{TASK}} by blast radius, worst first.` | Use exactly one verb in the whole prompt |
| 03 | Adjective: quality constraints | `rubrics.md#adjective` | `Write a summary of {{TASK}}.` | `Write a blunt, jargon-free summary of {{TASK}} that a new joiner could act on.` | Name three qualities, and for each state what it rules out |
| 04 | Adverb: manner and degree | `rubrics.md#adverb` | `Review {{TASK}}.` | `Review {{TASK}} exhaustively for correctness, then briefly for style.` | Set a different depth for two parts of the same task |
| 05 | Preposition: scope and relation | `rubrics.md#preposition` | `Fix the problems in {{TASK}}.` | `Fix the correctness problems in {{TASK}}, for a reader who has not seen the codebase, without introducing new dependencies.` | Include an audience, a boundary, and an exclusion, in that order |
| 06 | Composing the first five | `rubrics.md#noun`, `rubrics.md#verb`, `rubrics.md#adjective`, `rubrics.md#adverb`, `rubrics.md#preposition` | A one-line prompt for `{{TASK}}` with none of the five levers set | The same task with all five set | All five levers, under 40 words |
| 07 | Review: rewrite your worst prompt | `rubrics.md#noun`, `rubrics.md#verb`, `rubrics.md#adjective`, `rubrics.md#adverb`, `rubrics.md#preposition` | The learner supplies their own worst real prompt — no seed | The learner's own rewrite | Rewrite so that removing any single clause measurably degrades the output |

Days 06 and 07 differ from single-lever days in one way only: their `## Rubric` section lists five references instead of one, and the critique step scores against all five. Their `## Concept` sections explain composition — that the levers constrain different dimensions and therefore do not substitute for one another — rather than introducing a new lever.

Day 07 has no seed of its own. Its `## Before / After` section instructs the tutor to ask the learner for a real prompt they were unhappy with, use that as the "before", and withhold the "after" until the learner has attempted their own rewrite.

- [ ] **Step 2: Run the validator**

Run: `python3 tools/validate.py`
Expected: PASS, `ok`, exit 0.

- [ ] **Step 3: Check every rubric reference resolves**

Run: `grep -ho 'rubrics\.md#[a-z-]*' prompting-wizard/days/*.md | sort -u`
Expected: only slugs from the registry, and exactly the six rubric names used by days 1–7 (`noun`, `verb`, `adjective`, `adverb`, `preposition`). A slug not in `rubrics.md` would already have failed Step 2; this step catches a typo that happens to match a different valid slug.

- [ ] **Step 4: Commit**

```bash
git add prompting-wizard/days/0[2-7].md
git commit -m "feat: add days 2-7, core levers and week-1 composition"
```

---

### Task 7: Days 8–14 — remaining levers and full review

**Files:**
- Create: `prompting-wizard/days/08.md` … `prompting-wizard/days/14.md`

**Interfaces:**
- Consumes: the lesson structure from Task 5, and rubric slugs from Task 2.
- Produces: nothing later tasks import.

- [ ] **Step 1: Write days 8–14**

| Day | Title | Rubric reference | Before seed | After seed | Advanced constraint |
|---|---|---|---|---|---|
| 08 | Pronoun: reference binding | `rubrics.md#pronoun` | `Look at this and fix it.` | `Read the diff below. Fix the null-handling bug it introduces in the payment handler.` | Write the prompt with zero pronouns |
| 09 | Conjunction: conditional logic | `rubrics.md#conjunction` | `Update {{TASK}} and handle the edge cases.` | `Update {{TASK}}. If the input is empty, return an empty result rather than erroring; otherwise process every row.` | State two branches, and a fallback for each |
| 10 | Determiner: definiteness and quantity | `rubrics.md#determiner` | `Fix issues in {{TASK}}.` | `Fix every correctness issue in {{TASK}}. Leave each style issue alone.` | Bind every noun in the prompt with an explicit determiner |
| 11 | Numeral: checkable budgets | `rubrics.md#numeral` | `Give me some options for {{TASK}}.` | `Give me exactly three options for {{TASK}}, each under 40 words, ranked by cost.` | Every constraint must be verifiable without judgement |
| 12 | Interjection: attention markers | `rubrics.md#interjection` | A five-sentence prompt for `{{TASK}}` whose must-not-fail instruction is the fourth sentence | The same prompt with that instruction marked `IMPORTANT:` and moved last | Exactly one marker, on the one instruction that must not be missed |
| 13 | Particle: phrasal precision | `rubrics.md#particle` | `Look over {{TASK}}.` | `Look up each external call in {{TASK}} and check it against its documented contract.` | Use two phrasal verbs whose particles are load-bearing |
| 14 | Review: all 11 levers | all 11 lever slugs | The learner supplies a hard real task — no seed | The learner's prompt after critique | Hit all 11 levers in under 60 words |

Day 14's `## Concept` explains that the 11 levers constrain independent dimensions, which is why a prompt can score 5 on nine of them and still fail.

Day 14 is a review day. Its `## Exercise` instructs the tutor to read `## Levers` from `PROGRESS.md` and build the exercise around the three lowest-scoring levers, naming them to the learner.

- [ ] **Step 2: Run the validator**

Run: `python3 tools/validate.py`
Expected: PASS, `ok`, exit 0.

- [ ] **Step 3: Check all 11 levers now have a lesson**

Run: `for s in noun verb adjective adverb pronoun preposition conjunction determiner numeral interjection particle; do grep -lq "rubrics.md#$s" prompting-wizard/days/*.md || echo "no lesson references $s"; done`
Expected: no output. Every lever slug is referenced by at least one day file.

- [ ] **Step 4: Commit**

```bash
git add prompting-wizard/days/0[89].md prompting-wizard/days/1[0-4].md
git commit -m "feat: add days 8-14, remaining levers and full-lever review"
```

---

### Task 8: Days 15–21 — above the sentence

**Files:**
- Create: `prompting-wizard/days/15.md` … `prompting-wizard/days/21.md`

**Interfaces:**
- Consumes: the lesson structure from Task 5, and technique rubric slugs from Task 2.
- Produces: nothing later tasks import.

- [ ] **Step 1: Write days 15–21**

| Day | Title | Rubric reference | Before seed | After seed | Advanced constraint |
|---|---|---|---|---|---|
| 15 | Role framing | `rubrics.md#role-framing` | `You are a world-class expert. Help with {{TASK}}.` | `Answer as a reviewer who has to sign off on {{TASK}} and will be paged if it breaks.` | The role must change at least two specific things about the output, and you must name them |
| 16 | Few-shot examples | `rubrics.md#few-shot-examples` | A prompt for `{{TASK}}` with no examples | The same prompt with one boundary case and one failure case shown | Two examples only, and they must disagree in an instructive way |
| 17 | Output schemas | `rubrics.md#output-schemas` | `Give me the results in a nice format.` | A prompt containing the exact output structure, filled with dummy values | The schema must be checkable by a script, not by reading |
| 18 | Task decomposition | `rubrics.md#task-decomposition` | A single prompt for `{{TASK}}` containing three chained asks | The same work as three prompts, each with one output | Split so that step two's input is exactly step one's output, with nothing added |
| 19 | Reasoning scaffolds | `rubrics.md#reasoning-scaffolds` | `Think step by step about {{TASK}}.` | A prompt naming the specific intermediates to produce before the answer | Name the intermediates, and state what the answer must not do until they exist |
| 20 | Negative constraints | `rubrics.md#negative-constraints` | A prompt for `{{TASK}}` with no exclusions | The same prompt forbidding two failure modes the learner has actually hit | Every exclusion must cite a real failure, not a hypothetical one |
| 21 | Context ordering | `rubrics.md#context-ordering` | A prompt with 300 words of context before the instruction | The same content reordered: task, material, constraints | Reorder without deleting a word, and predict the change before running it |

Day 21 is a review day as well as a technique day. Its `## Exercise` instructs the tutor to build the reordering material from the learner's three lowest-scoring levers, so the reordered prompt exercises those too.

- [ ] **Step 2: Run the validator**

Run: `python3 tools/validate.py`
Expected: PASS, `ok`, exit 0.

- [ ] **Step 3: Commit**

```bash
git add prompting-wizard/days/1[5-9].md prompting-wizard/days/2[01].md
git commit -m "feat: add days 15-21, structure above the sentence"
```

---

### Task 9: Days 22–30 — systems and capstone

**Files:**
- Create: `prompting-wizard/days/22.md` … `prompting-wizard/days/30.md`
- Delete: `prompting-wizard/days/.gitkeep`

**Interfaces:**
- Consumes: the lesson structure from Task 5, and technique rubric slugs from Task 2.
- Produces: the complete day set. Task 10 runs the validator with `--complete` against it.

- [ ] **Step 1: Write days 22–30**

| Day | Title | Rubric reference | Before seed | After seed | Advanced constraint |
|---|---|---|---|---|---|
| 22 | System prompts vs user prompts | `rubrics.md#system-prompts` | A prompt repeating standing rules every turn | The same rules split into a system prompt and a lean per-turn ask | The system prompt must contain nothing that varies between turns |
| 23 | Agent and tool prompting | `rubrics.md#agent-and-tool-prompting` | `Use the tools to sort out {{TASK}}.` | A prompt stating the stop condition, then which tools and when | State the stop condition before naming a single tool |
| 24 | Self-critique loops | `rubrics.md#self-critique-loops` | A single-pass prompt for `{{TASK}}` | The same prompt with a named self-check and a stated action on failure | The check must be one the model can fail, and you must know what failing looks like |
| 25 | Writing evals | `rubrics.md#writing-evals` | `Make sure it is good.` | Three written criteria, applied after generation | Write the criteria before writing the prompt, and do not change them afterwards |
| 26 | Token economy | `rubrics.md#token-economy` | A prompt padded with unused context | The same prompt with a third of the context cut | Cut half, and be able to say which half mattered |
| 27 | Diagnosing a failed prompt | `rubrics.md#failure-diagnosis` | A real prompt of the learner's that failed | The learner's diagnosis naming the underspecified lever, and the targeted fix | Diagnose without running anything, then run to confirm |
| 28 | Building your prompt library | `rubrics.md#prompt-library` | Prompts rewritten from scratch each time | One saved prompt with its slots and known failure modes documented | Save three prompts sharing one slot vocabulary |
| 29 | Capstone I: build it | `rubrics.md#capstone` | The learner's highest-value recurring task, unprompted | The learner's production prompt for it | The prompt must score 4 or above on every lever it engages |
| 30 | Capstone II: harden it | `rubrics.md#capstone` | The day-29 prompt | The same prompt after eval, with failure modes documented | Run it on a case it was not designed for, and fix what breaks |

Day 27 has no seed of its own: the tutor asks the learner for a prompt of theirs that failed, and if the learner has none, uses the lowest-scoring day from their `## Log`.

Day 29's `## Exercise` instructs the tutor to record the learner's chosen task in the day-29 `## Log` line, so day 30 can pick it up. Day 30 reads that line rather than asking again.

Day 30 ends the course: after the critique step, the tutor sets `current_day` to 31 and shows the learner their day-0 lever scores against their current ones.

- [ ] **Step 2: Remove the placeholder**

```bash
git rm prompting-wizard/days/.gitkeep
```

- [ ] **Step 3: Run the full validator**

Run: `python3 tools/validate.py --complete`
Expected: PASS, `ok`, exit 0. All 30 day files present and structurally valid.

- [ ] **Step 4: Commit**

```bash
git add prompting-wizard/days/2[2-9].md prompting-wizard/days/30.md
git commit -m "feat: add days 22-30, systems and capstone"
```

---

### Task 10: Dry runs, README, and release

**Files:**
- Create: `README.md`
- Modify: whichever files the dry runs reveal to be wrong

**Interfaces:**
- Consumes: everything.
- Produces: the shipped repo.

- [ ] **Step 1: Dry-run the assessment at three levels**

Run the assessment three times in a fresh session, playing a learner who writes deliberately weak prompts, then average ones, then strong ones. Confirm the thresholds in `assessment.md` produce `novice`, `working`, and `advanced` respectively, and that `PROGRESS.md` is written with all 11 lever keys present each time.

Save the three resulting files to the scratchpad for the next steps. Do not commit them.

- [ ] **Step 2: Dry-run day 1 at all three tiers**

With each of the three `PROGRESS.md` files, run day 1. Confirm a different `###` tier is presented each time, and that `{{TASK}}` is substituted with the learner's first task in every place it appears.

- [ ] **Step 3: Dry-run the Tier B fallback**

Run day 1 in a session where isolated dispatch is unavailable. Expected: the skill prints the learner's prompt in a fenced block and asks them to run it elsewhere. It must **not** run the prompt in the lesson context, and must not proceed to critique without output.

- [ ] **Step 4: Verify weak-lever re-injection**

Take a `PROGRESS.md` with `pronoun: 2` and `current_day: 3`. Run day 3. Expected: the exercise names `pronoun` as a secondary constraint, and adds exactly one such constraint, not several.

- [ ] **Step 5: Verify error handling**

Three checks, each in a fresh session:

1. Delete `PROGRESS.md` after recording that `current_day` was 12. Expected: the skill reports the file is missing and offers to re-run the assessment or accept a stated day. It must not start day 1.
2. Set `current_day` to `twelve`. Expected: the skill names `current_day` as the failed field and stops.
3. Set `current_day: 31`. Expected: the skill reports the course complete and stops.

- [ ] **Step 6: Verify Codex parity**

In Codex, from the skill directory, confirm `AGENTS.md` leads to `SKILL.md` and that day 1 runs identically to Claude Code. Confirm the Tier A path works with `multi_agent = true` set, and that unsetting it falls through to Tier B rather than erroring.

- [ ] **Step 7: Write the README**

Create `README.md`:

````markdown
# Prompting Wizard

A 30-day course that turns you into a deliberate prompter. Twenty minutes a day. It assesses you first, then teaches using the tasks you actually do.

Each day covers one lever — starting with the parts of speech, because each one controls a different dimension of a prompt — then builds up to structure, systems, and a capstone. You write a prompt, it runs verbatim, you see the output, then you see a stronger version's output beside it.

## Install

**Claude Code**

```bash
git clone https://github.com/Entuvo/prompting-wizard.git
cp -r prompting-wizard/prompting-wizard ~/.claude/skills/
```

Then ask: "start the prompting course".

**Codex**

```bash
git clone https://github.com/Entuvo/prompting-wizard.git
```

Then, from the inner `prompting-wizard` directory, ask: "read AGENTS.md and start the prompting course".

For the run step to happen automatically, enable multi-agent support in `~/.codex/config.toml`:

```toml
[features]
multi_agent = true
```

Without it the course still works — it asks you to run each prompt in a fresh chat and paste the output back.

## How it works

Your progress lives in `PROGRESS.md` in whatever directory you start from. It holds your level, your day number, your score on each of the 11 levers, and the real tasks the exercises are built from. It is plain markdown — edit it if you want to redo a day or change your tasks.

Skipping days costs nothing. There is no backlog.

## Contributing

Lesson content lives in `prompting-wizard/days/`, scoring criteria in `prompting-wizard/rubrics.md`. Run `python3 tools/validate.py --complete` before opening a PR. It checks that every day has the required sections, that every rubric reference resolves, and that no shipped file contains an absolute path.
````

- [ ] **Step 8: Run the validator one final time**

Run: `python3 tools/validate.py --complete`
Expected: PASS, `ok`, exit 0.

- [ ] **Step 9: Commit and push**

```bash
git add README.md
git commit -m "docs: add install and usage README"
git push origin main
```

---

## Self-Review

**Spec coverage.** Every spec section maps to a task: decision and non-goals to the plan header and Global Constraints; architecture to Tasks 1, 4 and 5; portability and capability tiers to Task 4 and Task 10 steps 3 and 6; the 11 levers to Task 2 and Tasks 5–7; the 30-day outline to Tasks 5–9; day-0 assessment to Task 3; lesson file format to Task 5; daily loop to Task 4; rubrics to Task 2; scoring and adaptation to Task 4 and Task 10 step 4; `PROGRESS.md` format to Task 3; testing to Task 10; error handling to Task 4 and Task 10 step 5.

**Spec refinement made here.** The spec said `rubrics.md` holds one rubric per lever, which left days 15–30 with nothing to score against. This plan extends it to 26 rubrics — 11 levers plus 15 techniques — in the same format and the same file.

**Naming consistency.** The 11 lever slugs and 15 technique slugs are declared once in the slug registry and used identically in `tools/validate.py` (`LEVERS`, `TECHNIQUES`), in `rubrics.md` headings, in every day file's `## Rubric` reference, and in `PROGRESS.md`'s `## Levers` block. `{{TASK}}` is the sole domain slot token. `check(require_all_days=False)` is the only validator entry point; `--complete` is used in Tasks 9 and 10 only. The `.gitkeep` created in Task 1 is deleted in Task 9.
