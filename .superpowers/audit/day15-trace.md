# Day 15 behavioural trace — Claude Code harness

**Status:** complete. Traced statically, read-only. No prompt was executed, no model
output was generated, nothing under `prompting-wizard/`, `tools/` or the working tree
was modified. This file is the only thing written inside the repo; the fixture
`PROGRESS.md` was written to the session scratchpad.

**Harness:** Claude Code, Opus 5 (1M context). **Not** traced on Codex — the spec's
testing item asks for both harnesses and only the Claude Code half is discharged here.

**Files read:** `prompting-wizard/SKILL.md`, `prompting-wizard/days/15.md`,
`prompting-wizard/rubrics.md`, `prompting-wizard/assessment.md`,
`prompting-wizard/AGENTS.md`, `prompting-wizard/days/06.md` and `days/07.md` (`## Rubric`
sections only, to build the log fixture), `days/14.md`, `tools/validate.py` (header only),
and audit context in `.superpowers/audit/MASTER-FIX-PLAN.md`, `wave3b-concepts.md`,
`wave3c-concepts.md`, `wave5-prose.md`, `wave6-execution.md`.

**Fixture:**
`/private/tmp/claude-501/-Users-shergill-projects-prompting-skills/75cf6906-d11a-4ba6-afd2-7d8285c2a33a/scratchpad/PROGRESS.md`

---

## 0. Headline answers

| Question | Answer |
|---|---|
| Does day 15's ladder read 3 / 4 / 5? | **Yes** — derived independently in §9. Novice = 3 is the one soft joint. |
| Tier selected for `level: working` | `### Working` (`days/15.md:35`) |
| Secondary lever added | **adjective**, scored **1** |
| Clean-context branch | **Bullet 1 fires** (isolated dispatch exists). Bullet 2 vs bullet 3 is genuinely ambiguous on this harness — see §5. **Tier B does not fire.** |
| FIX-3.22 check on day 15 | **CLEAN** — one close call recorded, no edit proposed |
| Ambiguities found | **6**, listed in §10 |

---

## 1. The fixture

`SKILL.md:13` requires a rebuilt or constructed file to carry `level`, a `current_day`
that is a whole number 1–31, `## Levers` with all eleven keys, `## Tasks` with at least
three entries, and a `## Log` section. The fixture satisfies all five.

```markdown
# Progress

level: working
current_day: 15

## Levers
noun: 4    verb: 4    adjective: 2    adverb: 3
preposition: 3    pronoun: 4    conjunction: 2
determiner: 3    numeral: 4    interjection: 3    particle: 2

## Tasks
- Reviewing PRs on the payments service
- Writing incident postmortems
- Drafting API docs for external partners

## Log
- Day 0 — assessment — level working, diagnosis 5/10 — baseline noun 3, verb 3, adjective 2, adverb 2, preposition 3, pronoun 2, conjunction 2, determiner 3, numeral 4, interjection 3, particle 2
- Day 1 — noun — self 3, rubric 4 — secondary adjective 2 — "naming the file I actually wanted changed everything"
- Day 2 — verb — self 3, rubric 4 — secondary adverb 3 — "'critique' and 'summarise' are not the same request"
- Day 3 — adjective — self 2, rubric 3 — secondary pronoun 2 — "I still can't say what makes me reject a review"
- Day 4 — adverb — self 3, rubric 4 — secondary conjunction 2 — "attaching a length to each section stopped the rambling"
- Day 5 — preposition — self 4, rubric 4 — secondary particle 3 — "saying who it was for cut half the output"
- Day 6 — composition — self 3, rubric 4 — secondary pronoun 3 — "five levers at once and the adjective one is the one I skip"
- Day 7 — review — self 3, rubric 4 — secondary conjunction 3 — "my worst prompt was worst because it named no artifact"
- Day 8 — pronoun — self 4, rubric 4 — "replacing every 'it' with the noun made the prompt longer and better"
- Day 9 — conjunction — self 3, rubric 3 — "I never write the otherwise branch down"
- Day 10 — determiner — self 3, rubric 4 — "'the issues' versus 'every issue' changed the whole scope"
- Day 11 — numeral — self 4, rubric 4 — "a count I could check with my finger"
- Day 12 — interjection — self 3, rubric 4 — "one marker on its own line beat three bold words"
- Day 13 — particle — self 3, rubric 4 — "'look over' and 'look into' were doing different jobs"
- Day 14 — review — self 3, rubric 3 — "adjective, conjunction and particle all collapsed when I had to hold eleven at once"
```

**Honesty note.** Every line of this file is constructed fixture, including the learner
quotations. It is a synthetic learner, and the task asked for one. Nothing in §5 or §7
below fabricates *day 15's* learner responses — where day 15 needs a learner answer I say
so and leave it unfilled.

**The fixture is internally consistent under `SKILL.md`'s own rules**, and that was the
point of building it rather than asserting it:

- **Secondary-constraint history is forward-derived.** Starting from the day-0 baseline
  and applying `SKILL.md:34` at every day, the secondaries fall out as
  adjective (d1) → adverb (d2) → pronoun (d3) → conjunction (d4) → particle (d5) →
  pronoun (d6) → conjunction (d7), then none from d8 to d13 because no lever sat at ≤2
  after day 7, and none on d14 because day 14's own rubric scores all eleven levers, so
  `SKILL.md:34`'s "Never choose a lever the day's own `## Rubric` already scores" leaves
  nothing qualifying. Day 14's line therefore carries no `secondary` field, which
  `SKILL.md:77` requires ("written only when a secondary constraint was added … and
  omitted otherwise").
- **Days 6, 7 and 14 log `composition`, `review`, `review`** per `SKILL.md:79`, and their
  `rubric N` fields are means rounded to the nearest integer per `SKILL.md:81`: days 6 and
  7 score noun/verb/adjective/adverb/preposition (verified in `days/06.md` and
  `days/07.md`) at 4/4/3/4/4 = 3.8 → 4; day 14 scores all eleven at the values now in
  `## Levers`, mean 34/11 = 3.09 → 3.
- **`level: working` is the value day 14's re-derivation would have written.**
  `SKILL.md:24` requires recomputing the mean over all eleven `## Levers` after day 14 and
  rewriting `level` from `assessment.md`'s table. Mean = 3.09, and `assessment.md:49` puts
  2.5–3.9 at `working`. The tier did not change, so no "your tier dropped" message is owed.

---

## 2. Session steps — which fire, in order, and what each touches

> `SKILL.md:10`, `## Every session`.

**Step 1** — `SKILL.md:12`: "Look for `PROGRESS.md` in the learner's working directory."
Reads the fixture. All five required fields parse, so the third bullet fires:
`SKILL.md:19`, "**Present and valid** → continue." Neither the **Absent** branch
(`SKILL.md:13`) nor the **Present but a required field is missing** branch
(`SKILL.md:14`) fires. Writes nothing.

*Trace artifact worth stating plainly:* the real cwd for this session is
`/Users/shergill/projects/prompting_skills`, which contains no `PROGRESS.md`. A literal
run of `SKILL.md` here would have fired the **Absent** branch and asked the learner
whether they were new or mid-course. The trace treats the scratchpad as the learner's
working directory. That is a property of the trace, not a defect in the skill.

**Step 2** — `SKILL.md:20`: "Read `level`, `current_day`, `## Levers`, `## Tasks`, and
`## Log`." Reads: `level: working`; `current_day: 15`; the eleven lever scores; the three
task entries; the fifteen log lines. Writes nothing. The `## Log` read is load-bearing
twice over on this day — once for the tie-break in §4, once because `SKILL.md:34` names
the `secondary` field as the recency record.

**Step 3** — `SKILL.md:21`: "If `current_day` is above 30, tell the learner the course is
complete and stop." 15 is not above 30. Does not fire. Writes nothing.

**Step 4** — `SKILL.md:22`: "Read `days/NN.md`, where NN is `current_day` zero-padded to
two digits." NN = `15`; reads `prompting-wizard/days/15.md`. Writes nothing.

**Step 5** — `SKILL.md:23`: "Run the daily loop below." Sections 3–7 of this report are
that loop. Writes nothing to state; the run step would dispatch (see §5).

**Step 6** — `SKILL.md:24`: "Append one `## Log` line, update lever scores, and increment
`current_day`." Writes `PROGRESS.md`. Detail in §7. Note that day 14's re-derivation
clause inside this step does **not** fire on day 15 — `SKILL.md:24` says "After day 14 has
written its eleven lever scores … This is the only re-derivation in the course."

**Daily-loop step 6** (`SKILL.md:42`, `## Completion`) does not fire: `days/15.md` has no
`## Completion` section. It ends at `## Rubric` (`days/15.md:41-43`).

---

## 3. Tier selection and `{{TASK}}` substitution

`SKILL.md:34`: "Then present the tier matching `level`: `### Novice`, `### Working`, or
`### Advanced`." `level: working` → **`### Working`**, `days/15.md:34-35`.

First, the `## Exercise` preamble. `SKILL.md:34`: "Read the text between `## Exercise` and
the first tier heading: present it if it addresses the learner, act on it if it is
direction." `days/15.md:27` reads "Pick one of your recurring tasks. Write a single prompt
for it." — second person, addresses the learner, so it is **presented**.

Then the tier. Raw text, `days/15.md:35`:

> Write a prompt for {{TASK}} whose role text names at least one thing the output
> includes, excludes, or assumes because of the role — named in the prompt, not left for a
> reader to infer from the role.

`SKILL.md:28` fixes the substitution: "Default to their first `## Tasks` entry; when the
exercise invites them to pick one and they do, use their pick. Never show the raw token to
the learner. `## Tasks` entries are noun or gerund phrases, not full sentences: fit the
substitution to read naturally in its sentence, adjusting the task phrase's wording or the
surrounding frame as grammar requires, without changing the meaning of the task or the
instruction around it."

Default entry = **"Reviewing PRs on the payments service"**.

**The naive substitution does not read naturally**, and this is exactly the failure the
trace was told to check for:

> ~~Write a prompt for reviewing PRs on the payments service whose role text names at
> least one thing the output includes, excludes, or assumes because of the role…~~

`whose` is intended to modify *a prompt*, but the nearest preceding noun phrase is *the
payments service*. With a one-word task ("Write a prompt for postmortems whose role
text…") the frame holds; with a multi-word task phrase the relative clause detaches. This
is a relative-clause attachment fault, not a grammar error, so it is silent — the sentence
scans, it just points at the wrong noun. **All three of day 15's tiers use the same
`for {{TASK}} whose …` frame** (`:31`, `:35`, `:39`), so the fault is not tier-specific.

`SKILL.md:28` explicitly authorises the repair ("adjusting … the surrounding frame as
grammar requires"). Recast, splitting the relative clause into its own sentence and
leaving every scored word of the tier intact:

> **Write a prompt for reviewing PRs on the payments service. Its role text should name at
> least one thing the output includes, excludes, or assumes because of the role — named in
> the prompt, not left for a reader to infer from the role.**

That is the text the learner sees. Nothing scored moved: "names at least one thing the
output includes, excludes, or assumes because of the role" and "named in the prompt, not
left for a reader to infer from the role" are both verbatim.

**A second, harder substitution site, in the `## Concept`.** `days/15.md:7`:

> "Answer as a reviewer who has to sign off on {{TASK}} and will be paged if it breaks"

`sign off on` takes an artifact, and `## Tasks` entries are activities. "sign off on
reviewing PRs on the payments service" is not English anyone writes, and "if it breaks"
has no referent — an activity does not break. Reading naturally requires swapping the
gerund for the artifact it produces:

> "Answer as a reviewer who has to sign off on each PR on the payments service and will be
> paged if it breaks"

That is arguably at the edge of `SKILL.md:28`'s "without changing the meaning of the
task": the task is *reviewing PRs*, and the repair substitutes *a PR*. It is the only
repair available, and the same substitution is needed again in the `## Before / After`
After at `days/15.md:21`. Filed as ambiguity **A2** in §10.

---

## 4. The weak-lever secondary constraint

**Governing text**, `SKILL.md:34`:

> If a lever other than last session's secondary scores 2 or below, add the lowest-scoring
> of those as a named secondary constraint — for example, "and bind every reference; you
> scored low on pronoun". One only; break ties by whichever you have used least recently
> as a secondary constraint, which the `secondary` field in `## Log` records — a lever
> never used as one counts as least recently used, and among those take the first in
> `## Levers` order. Never choose a lever the day's own `## Rubric` already scores.

**Candidate set.** Levers at ≤2 in `## Levers`: **adjective 2, conjunction 2, particle 2**.
Three, so the tie-break fires as required.

**Exclusion 1 — last session's secondary.** Day 14's log line carries no `secondary`
field, because day 14's `## Rubric` (`days/14.md:41`) scores all eleven levers and
`SKILL.md:34` forbids choosing a lever the day's own rubric scores; `SKILL.md:34`'s
last-resort clause then applies ("If setting aside last session's secondary and the day's
own levers leaves nothing qualifying, add none this session"). So nothing is excluded on
this ground. *This is itself a small reading question — see A4 in §10.*

**Exclusion 2 — the day's own rubric.** `days/15.md:43`: "Score against
`rubrics.md#role-framing`." `role-framing` is a **technique**, not one of the eleven
`## Levers` keys (`assessment.md:66-69`). So this clause excludes nothing on day 15. The
candidate set is untouched: {adjective, conjunction, particle}.

**Lowest-scoring.** All three sit at 2. Three-way tie → tie-break.

**Tie-break — least recently used as a secondary constraint**, read off the `secondary`
fields in `## Log`:

| Lever | Used as secondary on | Most recent |
|---|---|---|
| adjective | Day 1 | **Day 1** |
| particle | Day 5 | Day 5 |
| conjunction | Day 4, Day 7 | Day 7 |

None is unused, so the "never used counts as least recently used" clause and its
`## Levers`-order fallback do not fire. Least recently used = **adjective** (day 1).

**Determinate?** Yes, and doubly so: adjective wins under a most-recent-use reading
(1 < 5 < 7) and under a first-use reading (1 < 4 < 5). No further disambiguation needed.

**Exactly one?** Yes — `SKILL.md:34` "One only". **Not day 15's own lever?** Day 15's
rubric is `role-framing`, which is not a lever at all, so trivially satisfied.

**Presented to the learner**, in `SKILL.md:34`'s own example form, drawn from the
adjective rubric's Fastest fix (`rubrics.md:49`, "list the two qualities that would make
you reject the output, then state them"):

> — and name the two qualities that would make you reject the output; you scored low on
> adjective.

`SKILL.md:34` then ends the step: "Ask for the learner's prompt, then wait."

---

## 5. The run step — what would happen, and what did not

**Nothing was run.** No dispatch was made, no prompt was executed, no model output exists
for this trace. Everything below is a statement about what `SKILL.md` instructs and what
this harness exposes.

**What `SKILL.md` instructs**, `SKILL.md:36`: "Execute the learner's prompt **verbatim** in
a context containing no lesson history. See Clean-context execution." And `SKILL.md:60`:
"The verbatim rule governs the message, not the dispatch. Never add an instruction, a
constraint, or a reminder to the learner's prompt — including a safety one."

**Does this harness expose an isolated-dispatch tool?** **Yes.** The `Agent` tool
dispatches a subagent with a fresh context. `SKILL.md:48` requires detecting this by
availability, not configuration — "Detect this by whether an isolated-agent dispatch tool
is actually available to you, not by inspecting configuration" — and the tool is available.
One caveat that matters for this specific skill: the `Agent` tool's own documentation says
`subagent_type: "fork"` **inherits the parent's full conversation context**. A fork is
therefore the one dispatch mode that would violate `SKILL.md:53` ("Never run the learner's
prompt in the lesson context"). Any other `subagent_type`, or none, starts fresh. So the
correct dispatch here is a fresh general-purpose agent, explicitly **not** a fork.

**Does the dispatch tool accept a sandbox setting?** **Not directly, and this is where the
trace stops being clean.** `SKILL.md:49` says: "If the dispatch tool accepts a sandbox,
permission, or tool-allowlist setting, dispatch with the most restrictive one that still
lets the prompt run — read-only filesystem access by default. Set it on the dispatch call,
never in the message."

The `Agent` tool's parameters are `description`, `prompt`, `subagent_type`, `model`, and
`isolation`. There is **no** sandbox parameter and **no** permission parameter. The two
candidates for "tool-allowlist setting" are indirect:

- **`subagent_type`** selects an agent definition, and the definition carries a tool list.
  `Explore` is documented as "All tools except Agent, Artifact, ExitPlanMode, Edit, Write,
  NotebookEdit" — i.e. a read-only *agent*, chosen per dispatch call. But that set
  **still includes `Bash`**, and `Bash` writes. So `Explore` is not read-only filesystem
  access; it is read-only *minus the obvious write tools*. `SKILL.md:49`'s stated default
  — "read-only filesystem access by default" — is **not achievable** on this harness
  through any dispatch parameter.
- **`isolation: "worktree"`** gives the agent its own git worktree. That isolates the
  *repo*, not the filesystem or the network, and it is a workspace setting rather than a
  permission setting.

**Which branch of `## Clean-context execution` fires?**

- **Bullet 1 (`SKILL.md:48`) fires.** Dispatch is available; the prompt goes to a fresh
  agent and the output is captured verbatim.
- **Bullet 2 (`SKILL.md:49`) vs bullet 3 (`SKILL.md:50`) is genuinely ambiguous**, and I
  am not going to pick one silently. `SKILL.md:50` opens "If the dispatch tool offers no
  such setting", which makes the two exclusive. On this harness the honest description is
  *partial*: the tool offers a per-call knob that narrows the tool set (`subagent_type`)
  and one that narrows the workspace (`isolation`), but neither delivers the read-only
  filesystem bullet 2 names as its default, and `Bash` survives every option. A tutor
  reading bullet 2 dispatches `subagent_type: "Explore", isolation: "worktree"` and says
  nothing. A tutor reading bullet 3 dispatches and says, once, before the first run of the
  course: "Your prompt will run for real, with the file and network access this session
  has, in this directory." **Only the second tutor tells the learner the truth**, because
  under either reading `Bash` is reachable and the run can write. Filed as **A1** in §10;
  it is the most consequential ambiguity found, because the two readings differ in whether
  the learner is warned that their prompt can write to disk.
- **Bullet 4 (`SKILL.md:51`) — Tier B — does not fire.** Dispatch is available and no
  dispatch was attempted, so neither of its triggers ("If it cannot, or if dispatch fails")
  is met. **The spec's "confirm Tier B fallback triggers correctly" item is therefore
  still open for day 15 on this harness**: Tier B cannot be observed on a harness that has
  dispatch, and forcing it would mean simulating a dispatch failure, which is exactly the
  fabrication this trace is meant to avoid. It would have to be traced on a harness
  without an isolated-dispatch tool, or by an injected dispatch failure in a live run.

**What I would actually do here.** Dispatch the learner's prompt verbatim as the entire
`prompt` field to a fresh (non-fork) agent, with `subagent_type` set to the most restricted
available definition and `isolation: "worktree"`; add nothing to the message, per
`SKILL.md:60`; and, because the restriction is partial, still give the bullet-3 disclosure
once before the first run of the course. Then dispatch the rewrite to a **separate** fresh
agent with identical settings, per `SKILL.md:49` ("Apply the same setting to the rewrite's
run") and `SKILL.md:55` ("Run the rewritten prompt in a **separate** clean context").

---

## 6. The critique

**Governing text**, `SKILL.md:38`: "Score the prompt against each rubric named in the day's
`## Rubric` section, 1–5, quoting the anchor you are scoring against."

Day 15's `## Rubric` (`days/15.md:43`) names one: `rubrics.md#role-framing`.

**Learner prompt:**

> Answer as a senior reviewer. Look over the PR and tell me what you think.

**Not-applicable rule considered first** (`rubrics.md:7`): the task has an instance of the
property — the prompt asserts a role — so `role-framing` is scored, not `N/A`.

**Anchor-by-anchor:**

- **Anchor 1** — "Role asserted with no bearing on output ('you are a world-class
  expert')." Not this. "Senior reviewer" bears on the output: the task is reviewing a PR
  and the role is a reviewer, so the role is not decorative in the way "world-class expert"
  is. Above 1.
- **Anchor 2** — "The role is domain-relevant, but nothing in the prompt tells you what it
  includes, excludes, or assumes differently." Both halves hold. *Domain-relevant:*
  reviewer/PR. *Nothing in the prompt:* the second sentence is "Look over the PR and tell
  me what you think" — no inclusion, no exclusion, no assumption is named anywhere.
- **Anchor 3** — "The role implies a standard or a body of knowledge, but the prompt
  doesn't say which parts to draw on." The second half holds; **the first does not**.
  "Senior reviewer" names a job grade, not a standard and not a body of knowledge. Compare
  what the day itself treats as reaching this rung: `days/15.md:31` (Novice) requires "a
  concrete stake — something it's responsible for, something that happens if it's wrong",
  and `days/15.md:11` calls that "a stance". A stance implies a bar you are held to; a
  seniority label does not. "Senior" belongs to the same family as `rubrics.md:169`'s
  "world-class expert" — a competence claim, and `days/15.md:5` says competence is already
  the default: "the model already writes competently without the flattery".

**Score: `role-framing` 2.** Anchor: *"The role is domain-relevant, but nothing in the
prompt tells you what it includes, excludes, or assumes differently."*

**Where the boundary really sits, stated honestly.** The 2/3 line is the softest joint in
this rubric. Anchors 2 and 3 share the same negative finding — the prompt does not say what
changes — and differ only on whether the role *itself* implies a standard or a body of
knowledge. Nothing in `rubrics.md` says whether a job title alone counts. I score 2
because "senior reviewer" supplies no bar and no consequence, and because scoring it 3
would make anchor 3 reachable by any domain-relevant noun, which collapses 2 into 3. A
marker who reads "reviewer" as implying the body of knowledge *code review* would land on
3. The difference is one rung and it is not settled by the text. Filed as **A3** in §10.

**No freelance criticism**, per `SKILL.md:64` ("Score against the rubric only"). "Look
over" is a loose phrasal verb and "what you think" names no artifact, but those are
`particle` and `noun`, neither of which day 15 scores and neither of which is the
secondary. They are not mentioned to the learner.

**The comparison step is not reported**, because nothing was run. `SKILL.md:38` continues:
"Then write a stronger version of the prompt, run it in a **separate** clean context, and
show both outputs side by side" — and then requires a confounder check before concluding
which is stronger. Both runs and the side-by-side are unperformed here. No output is
invented.

---

## 7. The secondary lever, and the state write-back

### 7a. Is the secondary scored?

**Yes.** `SKILL.md:38`:

> If you added a secondary constraint in step 2, score that lever too, against its own
> rubric in `rubrics.md`, and tell the learner whether they met it.

**`rubrics.md#adjective`** — "**Measures:** quality constraints on the artifact."

Not-applicable check first (`rubrics.md:7`): reviewing PRs plainly admits quality
constraints on the output, so there is an instance to score. Not `N/A`.

- **Anchor 1** — "No quality named; any output passes." This. The only adjective in the
  prompt is *senior*, and it modifies the **role**, not the artifact. The artifact — "what
  you think" — carries no quality constraint at all, so no output can fail.
- **Anchor 2** — "A quality is named but so generically ('good', 'high-quality') that it
  rules nothing out." Does not apply: anchor 2 requires a quality *on the artifact*, and
  there is none. "Senior" is not a weak quality constraint on the output; it is not a
  constraint on the output.

**Score: `adjective` 1.** Anchor: *"No quality named; any output passes."*
**Constraint met?** No — the learner was asked to name the two qualities that would make
them reject the output, and named none.

### 7b. State write-back

**Governing text**, `SKILL.md:24`:

> Append one `## Log` line, update lever scores, and increment `current_day`. A lever's
> score changes only when the day actually scored it — the day's own rubric or a secondary
> constraint scored under step 4 of the daily loop. Set it to the score just given; do not
> average with the old score. Levers the day did not score are left untouched.

**Exactly what changes:**

| Field | Before | After | Why |
|---|---|---|---|
| `level` | `working` | `working` — **unchanged** | `SKILL.md:24`: the re-derivation runs "After day 14 has written its eleven lever scores … This is the only re-derivation in the course." Day 15 does not re-derive. |
| `current_day` | `15` | `16` | `SKILL.md:24`, "increment `current_day`". |
| `## Levers` → `adjective` | `2` | **`1`** | Scored as the secondary under step 4. "Set it to the score just given; do not average with the old score." Not (2+1)/2. |
| `## Levers` → all ten others | — | **untouched** | "Levers the day did not score are left untouched." |
| `## Tasks` | — | untouched | Not touched by any step. |
| Day 0 `## Log` line | — | untouched | `assessment.md:80`: "Never edit it after it's written." |
| `## Log` | 15 lines | 16 lines | One appended. |

**Note on where day 15's own score lives.** `role-framing` has no `## Levers` key — the
eleven keys are levers only (`assessment.md:66-69`). So the `role-framing` 2 is written
**only** into the log line's `rubric N` field and has no persistent home in `## Levers`.
That is by design, not a defect: `SKILL.md:83` says the levers a day rewrote are
recoverable from its log line, and for a technique day the log line is the sole record.
It does mean technique scores are never re-derived into `level`, which is consistent with
`SKILL.md:24` scoping the re-derivation to `## Levers`.

**Log-line spec**, `SKILL.md:71` and `:74`:

> Append one line per completed day. The fields are: day number, the day's lever or
> technique, the self-rating and rubric score, an optional secondary-constraint record,
> and the learner's own words from step 5.
>
> ```
> - Day 12 — interjection — self 3, rubric 4 — secondary pronoun 3 — "priority markers changed what it did first"
> ```

Field 2 per `SKILL.md:79` is "the day's lever or technique as it appears in the day file's
title". `days/15.md:1` is "# Day 15 — Role framing: name what changes", so the term is
**role framing**. `SKILL.md:81`'s mean rule is scoped to days 6, 7 and 14, so day 15's
single rubric score goes in directly — the secondary's 1 does **not** enter the mean; it
goes in the `secondary` field, per `SKILL.md:77`.

**The literal line:**

```
- Day 15 — role framing — self N, rubric 2 — secondary adjective 1 — "<learner's words>"
```

**`N` and the quotation are the only two fields I will not fill.** `SKILL.md:40` (step 5):
"Ask the learner which single change moved the output, and for a 1–5 self-rating. Log
both." Both come from a learner who was never asked, in a session whose run step was never
executed. Inventing them would be exactly the fabrication this trace exists to catch.
Every other field is derived and final: `Day 15`, `role framing`, `rubric 2`,
`secondary adjective 1`.

---

## 8. The imitate-the-After test

If the learner ignored the Working tier and copied `days/15.md:21` verbatim:

> Answer as a reviewer who has to sign off on **each PR on the payments service** and will
> be paged if it breaks. Sign-off puts your name on it, so flag anything you wouldn't want
> attached to you; the page comes to you, so call out any assumption you can't verify from
> what's given; and skip style commentary — it isn't what gets you paged.

**Derivation against `rubrics.md#role-framing`:**

- **Anchor 4** — "The role text names at least one thing the output includes, excludes or
  assumes because of the role, **but not how the role produces it**." The positive half is
  met several times over. The negative half is **violated** — the After says how, three
  times: "*Sign-off puts your name on it, so* flag…"; "*the page comes to you, so* call
  out…"; "skip style commentary — *it isn't what gets you paged*". So the After sits above
  anchor 4's ceiling.
- **Anchor 5** — "The role text names what the output includes, excludes **and** assumes
  because of the role, and says how the role produces each." Mechanism: present for all
  three clauses. Includes: "flag anything you wouldn't want attached to you". Excludes:
  "skip style commentary". **Assumes:** this is the contested leg.

**Two readings, and they differ by a rung.**

- **Reading A — anchor 5.** "call out any assumption you can't verify **from what's
  given**" fixes what the output may assume — only the supplied material — and anything
  beyond it must surface. That is a statement about the output's assumptions, with its
  mechanism ("the page comes to you"). Three dimensions, three mechanisms → **5**. This is
  the day's own reading: `days/15.md:23` glosses the After as naming "three things the
  output does and says what produces each", and counts the assumption clause as the third.
- **Reading B — anchor 4.** "call out any assumption you can't verify" is an instruction to
  *include* flagged assumptions in the output — an inclusion wearing the word *assumption*.
  Under this reading the After names two includes and one exclude and never says what the
  output *assumes*, so anchor 5's conjunctive list is incomplete, and the highest anchor
  whose requirements are fully met is **4** — with the oddity that the prompt also breaches
  anchor 4's "but not how" clause, so it sits in a gap between the two rungs.

**Answer: 5**, on the strength of `days/15.md:23`, which is the file's own authoritative
gloss on what the After demonstrates and which was rewritten in wave 3B specifically to
make all three items output-facing. Reading B is real and is filed as **A5** in §10.

**Consequence for the learner.** Either way an imitator lands at or above the Working
tier's 4. The imitate-the-After path on day 15 never puts the learner *below* their tier —
which is the healthy direction, and the opposite of the failure mode that motivated
FIX-3.07. It does mean day 15's `## Before / After` demonstrates rungs 1 and 5 and never
rung 4, so a Working-tier learner has no worked example of their own target; the anchor-4
exemplar has to come from `:11`'s ladder instead.

---

## 9. Does the ladder read 3 / 4 / 5?

**Yes.** Each tier derived independently against the current `rubrics.md#role-framing`,
without reference to the audit history.

### Novice (`days/15.md:31`) → **3**

> Write a role for {{TASK}} that has a concrete stake — something it's responsible for,
> something that happens if it's wrong — and send the completed prompt without saying
> anywhere in it what the output should include, exclude, or assume differently.

- **Anchors 4 and 5 are foreclosed outright.** The clause "without saying anywhere in it
  what the output should include, exclude, or assume differently" is the exact negative of
  anchor 4's positive content ("The role text names at least one thing the output includes,
  excludes or assumes because of the role"). A compliant Novice cannot reach 4.
- **Above anchor 1.** Anchor 1 is "Role asserted with no bearing on output ('you are a
  world-class expert')." A role carrying "something it's responsible for, something that
  happens if it's wrong" has bearing.
- **2 vs 3.** Anchor 2: "The role is domain-relevant, but nothing in the prompt tells you
  what it includes, excludes, or assumes differently." Anchor 3: "The role implies a
  standard or a body of knowledge, but the prompt doesn't say which parts to draw on."
  Both second halves are satisfied by the foreclosure clause. The discriminator is whether
  a *concrete stake* satisfies anchor 3's first half. Anchor 3 is disjunctive — "a standard
  **or** a body of knowledge" — so a standard alone suffices, and responsibility plus a
  consequence for being wrong *is* an implied standard: it names the bar the answer is held
  to without naming the parts to draw on. **3.**
- **This is the ladder's weakest joint, and I will not pretend otherwise.** The inference
  "a stake implies a standard" is nowhere in `rubrics.md`. It is strongly supported inside
  the day — `days/15.md:11` calls this rung "a stance", and `:7` calls a stake-bearing role
  "a stance" as opposed to flattery — but the rubric that actually scores it is silent.
  Filed as **A3** in §10, the same joint that decided the learner prompt's 2 in §6.

### Working (`days/15.md:35`) → **4**

> Write a prompt for {{TASK}} whose role text names at least one thing the output includes,
> excludes, or assumes because of the role — named in the prompt, not left for a reader to
> infer from the role.

- **Anchor 4**, verbatim: "The role text names at least one thing the output includes,
  excludes or assumes because of the role, but not how the role produces it." The tier
  reproduces the positive half word for word, including the disjunction ("includes,
  excludes, **or** assumes") and the at-least-one scoping.
- **Anchor 5 is foreclosed by the scoping alone.** Anchor 5 needs "what the output
  includes, excludes **and** assumes" — all three — so a tier satisfied by one cannot
  mandate 5. No separate prohibition on stating the mechanism was needed, and none is
  present; the tier simply does not ask for it, so a compliant learner's floor is 4.
- **The "not left for a reader to infer" clause is doing real work**, and it is what puts
  this at 4 rather than 3: the rubric scores a property of the *role text*, so a bare
  stance that a reader could infer effects from stays at 3. **4.**
- One consequence worth stating: a learner who volunteers all three dimensions plus
  mechanism scores 5 while remaining compliant. The tier's floor is 4; its ceiling is open.
  That is correct for a floor-setting ladder and is not a defect.

### Advanced (`days/15.md:39`) → **5**

> Write a prompt for {{TASK}} whose role text names one thing the output includes, one it
> excludes, and one it assumes because of the role — and says, in the prompt itself, how
> the role produces each of the three.

- **Anchor 5**, verbatim: "The role text names what the output includes, excludes and
  assumes because of the role, and says how the role produces each." All three dimensions
  enumerated; mechanism required for each.
- **"in the prompt itself"** is the load-bearing phrase. Without it the tier would be a
  readiness rider — *be ready to say how* — and readiness scores nothing against an anchor
  that inspects the role text. As written the demand is on the text. **5.**

**Ladder: 3 / 4 / 5.** Confirmed. The 4/4/4 degradation described in the brief is not
present in the current file: Novice is held at 3 by its foreclosure clause plus its stake
requirement, and Advanced reaches 5 because the mechanism is required *in the prompt*
rather than merely held ready.

---

## 10. Ambiguities found

Six. Ordered by how much they could change behaviour.

**A1 — `SKILL.md:49` vs `:50`: which sandbox branch a partial-restriction harness takes.**
Bullet 2 applies when "the dispatch tool accepts a sandbox, permission, or tool-allowlist
setting"; bullet 3 applies when it "offers no such setting". Claude Code's `Agent` tool
offers `subagent_type` (selects an agent definition, and with it a tool list) and
`isolation` (repo worktree) — per-call knobs that narrow capability but deliver neither
bullet 2's named default ("read-only filesystem access by default") nor anything that stops
`Bash` writing. Both readings are defensible and they differ in whether the learner is ever
told their prompt can write to disk. `SKILL.md` has no third case for partial restriction.
**Highest-consequence finding in this trace.** A one-clause fix would be to make the
disclosure conditional on the achieved restriction rather than on the existence of a
setting.

**A2 — `SKILL.md:32` "verbatim" vs `SKILL.md:28`'s substitution licence.** Step 1 says
"Present the day's `## Concept` verbatim" and attaches the substitution instruction
explicitly only to `## Before / After`. But `days/15.md:5` and `:7` both contain
`{{TASK}}`, and `SKILL.md:28` says "Wherever `{{TASK}}` appears in **any** text you
present" and "Never show the raw token". So "verbatim" cannot mean literally verbatim, and
on day 15 the natural-reading repair goes further than token replacement: "sign off on
{{TASK}}" with a gerund task requires swapping the activity for the artifact it produces
("sign off on **each PR on** the payments service"), which is a change to the concept's
frame and arguably to the task phrase's meaning — the boundary `SKILL.md:28` draws with
"without changing the meaning of the task". Two readings: substitute-and-repair (produces
readable English, is not verbatim) or substitute-only (is nearer verbatim, produces
"sign off on reviewing PRs on the payments service … if it breaks"). I took the first and
say so.

**A3 — `rubrics.md#role-framing` anchors 2 and 3 are not separated by any testable
property.** Both find that the prompt says nothing about includes/excludes/assumes. They
differ only on whether the role "implies a standard or a body of knowledge", and nothing
says whether a job title, a seniority label, or a stake qualifies. This decided two
findings in this trace — the learner prompt's 2 (§6) and Novice's 3 (§9) — and a marker
reading job titles as implying a body of knowledge would move both up one rung, turning
the ladder into 4/4/5 for a Novice learner. The day supplies the missing gloss at `:11`
("A stance that names nothing is where this starts"), but a tutor scoring from `rubrics.md`
alone, as `SKILL.md:38` directs, does not have it.

**A4 — "a lever other than last session's secondary" when last session had none.**
`SKILL.md:34` presumes a previous secondary exists. Day 14 can never have one, because its
rubric scores all eleven levers, so day 15 always meets this clause with an empty
exclusion. The reading is obvious (nothing to set aside) and I applied it without
hesitation, but the sentence never says so, and day 15 is the one day in the course where
the antecedent is guaranteed absent.

**A5 — whether day 15's After names something the output *assumes*.** "Call out any
assumption you can't verify from what's given" reads as an inclusion (flag assumptions) or
as an assumption bound (assume only what's given). Anchor 5 lists the three dimensions
conjunctively, so the reading decides 4 vs 5 for anyone imitating the After — including a
learner who copies it and a tutor scoring that copy. `days/15.md:23` settles it in the
file's favour, but the anchor alone does not.

**A6 — "the first in `## Levers` order" is the learner's file order.** `SKILL.md:34`'s
last-resort tie-break appeals to `## Levers` order. `assessment.md:66-69` fixes that order
for a freshly written file, but `SKILL.md:13` allows a file rebuilt from a stated day
number, whose lever order is whatever the tutor wrote then. (`tools/validate.py`'s own
`LEVERS` tuple lists a different order again — `adverb, pronoun, preposition` where
`assessment.md` has `adverb, preposition, pronoun` — which shows the order is not treated
as canonical anywhere.) Did **not** affect this trace: the day-15 tie-break resolved on
recency and never reached the order fallback.

---

## 11. FIX-3.22 check on `days/15.md`

**Scope of the check**, per FIX-3.22's standing consequence in `MASTER-FIX-PLAN.md`: read
**every sentence** of the day's `## Concept` against that day's own Novice and Working tier
text, and record the result. Day 15 is **not** among the nine confirmed members of the
class (06, 07, 14, 16, 17, 20, 27, 28, 30), and FIX-3.22's own words make that worthless as
evidence — "Absence from FIX-3.21's list, absence from this entry's list, and presence in
an entry that names other lines are all equally worthless as evidence." So the check is run
here from the file. The `## Before / After` is included, as the brief asks.

**Verdict: CLEAN.** No sentence in day 15's `## Concept` or `## Before / After` condemns a
state its Novice tier mandates, or instructs a state its Novice tier forecloses. One close
call is recorded rather than left for someone to re-derive. **No edit is proposed** — and
note that day 15's concept stands at 198 of the 200-word cap, so any future edit must be
word-neutral or better.

Sentence by sentence:

**`:5`, sentence 1–3** — "'You are a world-class expert. Help with {{TASK}}.' names nothing
that changes. No expert was invoked — the model already writes competently without the
flattery, and the sentence never says what an expert would check or refuse that a
generalist wouldn't. The role sits on the prompt like a sticker."
**Clean, but this is the close call and it deserves its evidence.** The clause "the sentence
never says what an expert would check or refuse that a generalist wouldn't" describes a
property a *compliant Novice prompt also has* — Novice (`:31`) forbids saying "what the
output should include, exclude, or assume differently", and *check ≈ includes*,
*refuse ≈ excludes*. Read alone, that clause condemns silence, and silence is mandated.
Three reasons it does not collide:
1. The verdict's subject is the quoted anchor-1 prompt, and the verdict is "names nothing
   that changes" / "No expert was invoked". A Novice-compliant role names a stake, so
   *something* changes and something is invoked; the verdict does not reach it.
2. The condemned property is the **conjunction** — flattery *and* silence. A compliant
   Novice breaks the first conjunct, which is the whole point of the tier.
3. Decisively, `:11` explicitly rules the silent stance a legitimate rung: "A stance that
   names nothing is where this starts". A concept that names the state as the bottom rung
   of its own ladder is not condemning it. This is the same test that cleared `days/20.md:9`
   — positional rather than verdictive.

**`:7`, sentence 1** — "A role earns its place when its text names what gets included,
excluded, or assumed." **Clean.** This is anchor 4's construction, and it states the bar
without calling anything below it wrong. It is aspirational, not a verdict on the Novice
state; compare `days/28.md:7`'s "stays low on the shelf", ruled clean under FIX-3.22 on the
same ground.

**`:7`, sentences 2–3** — "'Answer as a reviewer who has to sign off on {{TASK}} and will
be paged if it breaks' isn't flattery — it's a stance: assumptions get checked instead of
skimmed, and production failure matters more than style. A generalist and a pre-release
reviewer flag different things in the same document; naming the role picks which one you
get."
**Clean, with one recorded risk.** The quoted example is *itself a Novice-compliant role* —
a concrete stake (sign-off responsibility, paged if wrong) whose text names nothing the
output includes, excludes or assumes. That is the correct anchor-3 exemplar and it is the
one thing `## Before / After` does not supply, so its presence here is a positive. **The
recorded risk:** the gloss after the colon — "assumptions get checked instead of skimmed,
and production failure matters more than style" — describes effects a reader *infers* from
a role text that names none of them, and it sits one sentence below a framing sentence
about text that *names*. The Working tier (`:35`) forbids precisely that inference: "named
in the prompt, not left for a reader to infer from the role". A Working-tier learner who
takes `:7`'s example as the model answer submits an anchor-3 prompt and scores one rung
below their tier. This is **not** a FIX-3.22 collision — nothing condemns a mandated state
or mandates a foreclosed one — but it is a live mis-read path, and `:11` is the only thing
that closes it. Recorded so the next wave does not have to re-derive it.

**`:9`** — "'Act as a teacher' is empty until you can name what a teacher does differently,
like simplifying jargon."
**Clean.** "Act as a teacher" carries no stake, so it is *below* the Novice rung and
condemning it condemns nothing the tier mandates. The condition is "until you **can** name"
— an ability test, not a text test — and a compliant Novice can name what changes while the
tier forbids writing it down. Minor note only: the ability framing is the same
output-vs-text looseness FIX-3.14 chased out of the tiers, and it survives here. Harmless,
because nothing scores against it.

**`:11`, the self-test** — "read your role text and ask what it names. A stance that names
nothing is where this starts; one thing the output includes, excludes, or assumes — named
in the prompt, not left to inference — is a rung of its own; all three, plus how the role
produces each, is the top."
**Clean, and it is what makes the rest of the concept clean.** Three rungs mapping to
anchors 3, 4 and 5 in the day's own idiom, quantified over the learner's own role text,
positional throughout. A compliant Novice reads their mandated state named as the starting
rung rather than as an error; a compliant Working learner reads their tier's exact wording
("named in the prompt, not left to inference"); a compliant Advanced learner reads anchor
5. Correctly aimed at the text property the rubric now scores.

**`## Before / After`, `:17` and `:21`** — the Before is anchor 1, the After is anchor 5.
**Clean.** Neither is a Novice-mandated or Novice-foreclosed state, so neither can collide.
Noted rather than filed: the pair skips rung 4 entirely, so the Working learner's own
target has no worked example in `## Before / After` and depends on `:11`.

**`:23`, the gloss** — "The flattery is gone; what replaced it is a stance with
consequences. 'World-class expert' asked for competence, which was already the default.
'Reviewer who gets paged' names three things the output does and says what produces each:
issues you'd regret get flagged, because your name is on the sign-off; assumptions you
can't verify get called out, because the page comes to you; and style notes get left out,
because style doesn't page anyone."
**Clean.** All three items are output-facing and each carries its mechanism, so the
anchor-5 demonstration holds. Two observations, neither a collision: the attribution
"'Reviewer who gets paged' names three things" credits the stance phrase with naming that
the After's *second* sentence does, which is loose; and "names three things the output
does" is output-property idiom in a day whose rubric scores a text property. Neither is
scored against and neither touches a tier-mandated state.

**Result to record under FIX-3.22's standing consequence:** `days/15.md` opened, full
`## Concept` and `## Before / After` checked against the day's own Novice and Working tier
text, **CLEAN**, no edit made and none proposed, one close call recorded at `:7`.

---

## 12. What this trace does not establish

- **Nothing was executed.** No dispatch, no model output, no side-by-side comparison, no
  confounder check. Sections 5 and 6 report what `SKILL.md` instructs and what the harness
  exposes, not what happened.
- **Tier B was not observed.** The spec's "confirm Tier B fallback triggers correctly" item
  remains open for day 15; it cannot be discharged on a harness that has dispatch without
  injecting a dispatch failure, which would be simulation.
- **Codex was not traced.** The spec asks for both harnesses. This covers Claude Code only.
- **Step 5 was not performed.** The self-rating and the learner's words in §7b's log line
  are the only two fields left unfilled, deliberately.
- **The fixture is synthetic.** Days 1–14 of the log, including the quotations, are
  constructed. They are consistent with `SKILL.md`'s rules, which is what makes the
  tie-break in §4 meaningful, but they are not observations.
