# Concept–rubric alignment census

Read-only audit of `prompting-wizard/days/01.md`–`30.md` against `prompting-wizard/rubrics.md`.
All 30 days audited, none sampled. Nothing in the working tree was modified.

**Quoting convention.** Every anchor and `**Measures:**` line below is copied verbatim from
`/Users/shergill/projects/prompting_skills/prompting-wizard/rubrics.md` at the line numbers given.
For the three multi-rubric days (06, 07, 14) the full anchor tables of the eleven lever rubrics are
quoted verbatim once, in the single-rubric day that owns each lever (days 01–05, 08–13); those days'
entries carry the `**Measures:**` lines plus the full verbatim anchors for every rubric on which the
judgment actually turns, and line-range pointers for the rest. No anchor anywhere in this file is
paraphrased or recalled from memory.

**Scoring machinery this audit assumes** (`prompting-wizard/SKILL.md:34`): "Score the prompt against
the rubric named in the day's `## Rubric` section, criterion by criterion, 1–5, quoting the rubric's
anchor for each score you give." And `SKILL.md:28`: "Present the day's `## Concept` verbatim." The
concept is read to the learner word for word, and the cited rubric is the only scoring instrument.

**Global scoring rule that several findings turn on** (`rubrics.md:5`):
> "Scores are 1–5. Anchors are given for every point. Score the prompt as written, not the intent behind it."

---

## Summary table

| Day | Rubric(s) | Concept teaches | Rubric scores | Aligned? | After would score |
|---|---|---|---|---|---|
| 01 | `#noun` | Name the artifact as a noun phrase; "Today, just name the thing" | Artifact named unambiguously **and economically** (anchor 5) | Mostly — concept stops at anchor 4, economy lives only in the Advanced tier (**A13**, low) | 5 |
| 02 | `#verb` | One verb naming exactly one operation, not a generic stand-in | Exactly one operation, the one wanted, not a generic synonym | Yes | 5 |
| 03 | `#adjective` | Two qualities that each do rejection work; "A third rarely earns its place" | Every quality that matters named, **and none that do not** | Concept yes; Advanced tier forces a third quality the anchor penalises (**A05**, medium) | 5 |
| 04 | `#adverb` | A manner word without a measure is "a mood, not an instruction" | Depth/manner set so length and thoroughness are predictable in advance | **No** — the After's own headline adverb has no measure (**A01**, high) | 3 |
| 05 | `#preposition` | in what / for whom / without what — all three | Boundaries, audience **and** exclusions all set | Yes | 5 |
| 06 | `#noun` `#verb` `#adjective` `#adverb` `#preposition` | Five levers in one sentence; preposition = "where it stops and who it's for" | As above, incl. adverb measure and preposition exclusion | **No** — After scores 2 on adverb (**A02**, high); concept and After drop the exclusion (**A03**, high); word-budget tier unscored (**A16**, low) | noun 4, verb 5, adjective 5, **adverb 2**, **preposition 3** |
| 07 | `#noun` `#verb` `#adjective` `#adverb` `#preposition` | Find the open lever in your own prompt; every clause must be load-bearing | The five levers only | Partial — the tier's load-bearing test is scored by no cited rubric; no self-test (**A10**, medium) | n/a (tutor-driven, no supplied After) |
| 08 | `#pronoun` | Every pronoun must point at an exact word or quoted block | Every reference resolves, on first read | Concept yes; the day's gloss mis-binds its own pronoun and cites a block the After does not contain (**A06**, medium) | 4–5 |
| 09 | `#conjunction` | condition + outcome + fallback, ordered | Each branch with condition and fallback, in an unambiguous order | Yes | 5 |
| 10 | `#determiner` | Bind every noun with the/a/each/every/any | Each noun bound, no reading left open | Yes | 5 |
| 11 | `#numeral` | Every countable dimension gets a number, not "a few" | Every countable dimension bounded and checkable without judgement | Yes | 5 |
| 12 | `#interjection` | Mark one instruction and "move it to stand alone at the end" | Marked and positioned so it cannot be missed; anchor 4's only positional cue is "near the top" | Partial — lesson and ladder point in opposite directions (**A07**, medium) | 3 or 5 depending on how the grader reads anchor 4 |
| 13 | `#particle` | Choose a load-bearing particle; swap-test it | Every phrasal verb deliberate; no substitution preserves meaning | Yes | 5 |
| 14 | all eleven lever rubrics | "every lever considered, and either set deliberately **or left out on purpose**" | Absence scores 1–3 regardless of intent (`rubrics.md:5`) | **No** (**A04**, high) | n/a (tutor-driven) |
| 15 | `#role-framing` | Role must change what the output *contains*; "list two things the output contains" | Role changes what is included, **excluded** and assumed | Partial — self-test and Working tier test one of three scored dimensions; After states no exclusion (**A08**, medium) | 4–5 |
| 16 | `#few-shot-examples` | "Two examples that disagree do more work than ten that agree" | Examples cover the boundary case and the failure case | Partial — After's two examples agree (both "Not urgent"); disagreement is scored nowhere (**A09**, medium) | 5 on the rubric, fails the day's own Working tier |
| 17 | `#output-schemas` | Fields, types, order, empty values, filled with dummy data | An exact structure checkable mechanically | Yes | 5 |
| 18 | `#task-decomposition` | Each step's input is verbatim the last step's output | Each step has one output and a clear input from the last | Yes | 5 |
| 19 | `#reasoning-scaffolds` | Named intermediates must match what the answer depends on | The reasoning steps asked for match the ones the task requires | Yes (the earlier "gating" defect is fixed at 19.md:9) — but the After's intermediates are fixed while the rubric scores task-specific match (**A17**, low) | 5 for the assumption-audit family of tasks, 3 for others |
| 20 | `#negative-constraints` | Each exclusion names a failure you have watched happen | Exclusions specific, each preventing a failure actually seen | Yes | 5 |
| 21 | `#context-ordering` | Task first, material second, constraints last; pure reorder | Placement of instruction and material | Concept yes; self-test tests output sensitivity, not placement (**A11**, medium); exercise directs work on three levers the day scores none of (**A12**, medium) | 5 |
| 22 | `#system-prompts` | Durable rules in the system prompt, only the new thing per turn | Separation of standing rules from the turn | Yes | 5 |
| 23 | `#agent-and-tool-prompting` | Which tools, when, and an un-gameable stop condition | Which tools, when, and what "done" means | Yes — and 23.md:9 explicitly de-scopes the unscored habit | 5 |
| 24 | `#self-critique-loops` | A check that can fail, plus an action when it does | A check the model can apply, with a stated action on failure | Yes | 5 |
| 25 | `#writing-evals` | Criteria written before the output, objective enough to agree | Criteria written before the output, two people score the same | Yes | 5 |
| 26 | `#token-economy` | Cut, rerun, compare — the test is the cut | Every token earns its place; cuts made without losing accuracy | Yes | 5 |
| 27 | `#failure-diagnosis` | Name one lever or technique; the fix targets only it | The failing lever named and the fix targets it | Yes — rubric's own Fastest-fix line is narrower than its anchors (**A15**, low) | n/a (tutor-driven) |
| 28 | `#prompt-library` | Save the slot and how it has failed before | Slots **and their known failure modes** (plural) | Yes — self-test says "the one way it's failed" (**A14**, low) | 5 |
| 29 | `#capstone` | Anchor 3 is today's honest ceiling; 4–5 need criteria and documented failures | Production readiness ladder | Yes | 3 by design, correctly stated |
| 30 | `#capstone` | Criteria → unseen case → documented failure mode = anchors 3→4→5 | Same | Yes — ladder direction quoted correctly (previously-fixed defect confirmed fixed) | 5 |

**Counts:** 4 high, 8 medium, 5 low. 18 of 30 days fully aligned.

---

## Findings

### DEFECT-A01 — Day 4's After uses an unmeasured manner word, the exact failure its own concept names — severity: high

**Day 4**, `prompting-wizard/days/04.md:21`.

Cited rubric: `rubrics.md#adverb`, `rubrics.md:49–61`.

> **Measures:** manner and degree of the action. (`rubrics.md:51`)

| Score | Anchor (verbatim, `rubrics.md:55–59`) |
|---|---|
| 1 | Manner unspecified; depth left to chance. |
| 2 | A manner word is used ("briefly", "carefully") but without a measure, so two readers would produce different depths. |
| 3 | Depth or manner is set for part of the task, but another part is left to guess. |
| 4 | Depth and manner set clearly enough that output length and thoroughness are mostly predictable. |
| 5 | Depth and manner set so output length and thoroughness are predictable in advance, not just in hindsight. |

Concept's central claim: *a manner word only instructs once a measure is attached to it.* Carrying sentence, `04.md:7`:

> "Without a measure attached, a manner word is a mood, not an instruction. "Carefully" tells the model to feel careful. "Line by line, checking each function against its callers" tells it what careful output looks like."

The After, `04.md:21`:

> "Review {{TASK}} exhaustively for correctness, then for style in three sentences at most, flagging only tone and word choice."

And the day's own gloss, `04.md:23`:

> ""Exhaustively" sets an open-ended, thorough pass for correctness."

**Why they diverge.** "Exhaustively" is a manner word with no measure attached — the model answer commits the failure the concept defines one paragraph earlier, and the gloss concedes it ("open-ended"). Anchor 2's wording fits it exactly: *"A manner word is used ... but without a measure, so two readers would produce different depths."* Only the style half carries a measure ("three sentences at most"), which lands the whole prompt on anchor 3: *"Depth or manner is set for part of the task, but another part is left to guess."* Anchors 4 and 5 both require the output's **length** to be predictable, and an open-ended exhaustive pass makes total length unpredictable by construction. The After also fails the day's own self-test at `04.md:11`: *"if two competent people followed this manner word, would their outputs be roughly the same length and thoroughness?"* — two people told "review exhaustively for correctness" would not.

The concept contains the seed of the contradiction at `04.md:9`: *"You can ask for one part done exhaustively and another done at a glance"* — blessing two bare manner words that `04.md:7` has just ruled out.

**Minimal fix.** Attach a measure to the correctness pass in the After and in `04.md:9`, e.g. "exhaustively — every function against its callers, one line per issue found". Leave the style half as is; the two-different-depths point survives intact.

---

### DEFECT-A02 — Day 6's composed model answer scores 2 on one of the five rubrics it is graded against — severity: high

**Day 6**, `prompting-wizard/days/06.md:21`.

Cited rubrics (`06.md:43`): `#noun`, `#verb`, `#adjective`, `#adverb`, `#preposition`.

> **Measures:** the artifact the prompt asks for. (`rubrics.md:9`)
> **Measures:** the operation requested. (`rubrics.md:23`)
> **Measures:** quality constraints on the artifact. (`rubrics.md:37`)
> **Measures:** manner and degree of the action. (`rubrics.md:51`)
> **Measures:** scope and relation. (`rubrics.md:79`)

Adverb anchors quoted verbatim in **A01** above (`rubrics.md:55–59`); noun `rubrics.md:13–17`, verb `rubrics.md:27–31`, adjective `rubrics.md:41–45`, preposition quoted verbatim in **A03** below.

The After, `06.md:21`:

> "Rank the correctness issues in {{TASK}} into a blunt, jargon-free list, exhaustively, for a reader new to the codebase."

The day's gloss, `06.md:23`:

> ""exhaustively" the adverb"

**Why they diverge.** Day 6 is scored on all five lever rubrics simultaneously, and the model answer's adverb is a single bare manner word with no measure — anchor 2 verbatim: *"A manner word is used ("briefly", "carefully") but without a measure, so two readers would produce different depths."* Day 6 is worse than Day 4 here, because Day 4 at least measured the style half; Day 6 has one adverb and no measure anywhere. The learner is shown a model answer that scores 5, 5, 5, **2**, 3 while the prose asserts *"nothing is left for the model to invent"* (`06.md:23`).

**Minimal fix.** Give the adverb a measure inside the 40-word budget the Advanced tier sets, e.g. "exhaustively — every changed file" or "one bullet per issue, no issue omitted".

---

### DEFECT-A03 — Day 6 redefines "preposition" as two of the three relations its rubric scores — severity: high

**Day 6**, `prompting-wizard/days/06.md:7` and `06.md:21`.

Cited rubric: `rubrics.md#preposition`, `rubrics.md:78–89`.

> **Measures:** scope and relation. (`rubrics.md:80`)

| Score | Anchor (verbatim, `rubrics.md:83–87`) |
|---|---|
| 1 | No scope; the task could touch anything. |
| 2 | One boundary is given (e.g. audience) but others (what's excluded, for whom) are missing. |
| 3 | Most of scope, audience and exclusion are set, but one relation is left implicit. |
| 4 | Boundaries, audience and exclusions are all set, though phrased loosely enough to invite a small stretch. |
| 5 | Boundaries, audience and exclusions all set precisely — in what, for whom, without what. |

Concept sentence carrying the claim, `06.md:7`:

> "The preposition says where it stops and who it's for."

Compare Day 5, which taught the same lever correctly (`05.md:7`): *"Prepositions carry scope and relation: in what, for whom, without what."* — and Day 5's self-test (`05.md:11`): *"Test it by asking three questions of your prompt: in what, for whom, without what."*

The After, `06.md:21`, sets scope ("the correctness issues in {{TASK}}") and audience ("for a reader new to the codebase") and **no exclusion at all**.

**Why they diverge.** The rubric's anchors 4 and 5 both require exclusions; anchor 3 is the ceiling for a prompt with "one relation left implicit". A learner who follows Day 6's one-sentence definition of the lever will write exactly what the model answer writes, and be capped at 3 on a rubric whose top two rungs they were never told about — one day after being told all three relations matter and that dropping any one lets "the model fill the gap with its own default" (`05.md:9`). The composition day quietly un-teaches the exclusion.

**Minimal fix.** Restore the third relation in `06.md:7` ("where it stops, who it's for, and what it must not touch") and add an exclusion to the After — e.g. "...for a reader new to the codebase, without proposing API changes."

---

### DEFECT-A04 — Day 14 tells the learner an unset lever is legitimate; the rubrics score it 1 regardless — severity: high

**Day 14**, `prompting-wizard/days/14.md:9`.

Cited rubrics (`14.md:41`): all eleven lever rubrics — `#noun` `#verb` `#adjective` `#adverb` `#pronoun` `#preposition` `#conjunction` `#determiner` `#numeral` `#interjection` `#particle`.

> **Measures:** the artifact the prompt asks for. (`rubrics.md:9`)
> **Measures:** the operation requested. (`rubrics.md:23`)
> **Measures:** quality constraints on the artifact. (`rubrics.md:37`)
> **Measures:** manner and degree of the action. (`rubrics.md:51`)
> **Measures:** reference binding. (`rubrics.md:65`)
> **Measures:** scope and relation. (`rubrics.md:80`)
> **Measures:** conditional logic. (`rubrics.md:93`)
> **Measures:** definiteness and quantity binding. (`rubrics.md:107`)
> **Measures:** budgets that make output checkable. (`rubrics.md:121`)
> **Measures:** attention and priority markers. (`rubrics.md:135`)
> **Measures:** phrasal precision. (`rubrics.md:149`)

The anchors that decide this finding, verbatim — every rubric's score-1 anchor describes *absence*, not intent:

- `rubrics.md:97` (conjunction, 1): "Branching cases collapsed into one instruction, so edge cases silently pick a branch."
- `rubrics.md:83` (preposition, 1): "No scope; the task could touch anything."
- `rubrics.md:123` (numeral, 1): "No quantity anywhere; length and count unbounded."
- `rubrics.md:137` (interjection, 1): "All instructions carry equal weight; the critical one is buried mid-paragraph."
- `rubrics.md:99` (conjunction, 3): "Branches and conditions are named, but the fallback (the otherwise) is missing."

Concept sentence carrying the claim, `14.md:9`:

> "Independence cuts both ways. Not every lever needs pulling hard; some tasks have no fallback to state. What matters is every lever considered, and either set deliberately or left out on purpose."

**Why they diverge.** The rubrics have no not-applicable rung and an explicit instruction against reading intent — `rubrics.md:5`: *"Score the prompt as written, not the intent behind it."* A learner who does exactly what Day 14 licenses (considers `conjunction`, concludes their task has no fallback, leaves it out) is scored 1 on conjunction, and `SKILL.md:20` writes that score into `## Levers`: *"Set it to the score just given; do not average with the old score."* A score of 2 or below then triggers the secondary-constraint machinery at `SKILL.md:30` and `SKILL.md:57`. The learner is remediated for following the lesson.

The concept contradicts itself two sentences later, at `14.md:11`: *"A score of 2 or below is a dimension you thought you'd covered and hadn't"* — which is the rubric's position, not `14.md:9`'s.

**Minimal fix.** Either drop "or left out on purpose" from `14.md:9` and say plainly that every lever is scored as written, or add an explicit not-applicable rule to `rubrics.md` and to `SKILL.md` step 4 so a deliberate omission is recorded as unscored rather than as a 1. The first is smaller and consistent with `rubrics.md:5`.

---

### DEFECT-A05 — Day 3's Advanced tier requires a third quality the concept and the anchor both penalise — severity: medium

**Day 3**, `prompting-wizard/days/03.md:41` against `03.md:9`.

Cited rubric: `rubrics.md#adjective`, `rubrics.md:35–47`.

> **Measures:** quality constraints on the artifact. (`rubrics.md:37`)

| Score | Anchor (verbatim, `rubrics.md:41–45`) |
|---|---|
| 1 | No quality named; any output passes. |
| 2 | A quality is named but so generically ("good", "high-quality") that it rules nothing out. |
| 3 | One real quality is named, but a second quality that matters as much is left unstated. |
| 4 | Every quality that matters is named, though some slack remains in how they're worded. |
| 5 | Every quality that matters is named, and none that do not — each word does rejection work. |

Concept, `03.md:9`:

> "A third rarely earns its place, and padding the list with qualities that don't matter here just adds noise the model has to reconcile."

Advanced tier, `03.md:41`:

> "Write a prompt for {{TASK}} that names exactly three qualities."

**Why they diverge.** Anchor 5 is a two-sided test — everything that matters, **and nothing that does not**. The concept agrees. The hardest tier then mandates a fixed count of three, so any learner whose task genuinely has two qualities must add a third that does no rejection work, which is precisely the "none that do not" half of anchor 5. The tier's escape hatch — *"If a quality doesn't rule anything out, replace it"* — says replace, never cut, so the count stays binding. The strongest learners are the ones penalised.

**Minimal fix.** Change `03.md:41` to "names every quality that matters and no more — for most tasks two, for some three" and keep the per-quality rejection test that follows.

---

### DEFECT-A06 — Day 8's gloss mis-binds the pronoun in its own model answer — severity: medium

**Day 8**, `prompting-wizard/days/08.md:23` against `08.md:21`.

Cited rubric: `rubrics.md#pronoun`, `rubrics.md:63–75`.

> **Measures:** reference binding. (`rubrics.md:65`)

| Score | Anchor (verbatim, `rubrics.md:69–73`) |
|---|---|
| 1 | Pronouns with no antecedent ("fix it", "do this"). |
| 2 | An antecedent exists somewhere in the prompt, but it's ambiguous which of two candidates it refers to. |
| 3 | Most references resolve, but one pronoun still requires the reader to guess. |
| 4 | Every reference resolves, though the resolution takes a re-read to confirm. |
| 5 | Every reference resolves inside the prompt or to a quoted block, on first read. |

The After, `08.md:21`:

> "Read the diff below. Fix the null-handling bug it introduces in the payment handler."

The gloss, `08.md:23`:

> ""This" now names nothing left to guess at — the diff is quoted directly under the sentence. "It" resolves inside the same clause, to a bug the sentence just named, not to whatever the reader happens to be looking at."

**Why they diverge.** Two errors, both in the sentence that models the skill being scored.

1. Grammatically, "it" in "the null-handling bug it introduces" is the **subject of "introduces"** and binds to *the diff*. It cannot bind to "the null-handling bug" — a bug does not introduce itself. The gloss asserts the impossible reading. The day's self-test (`08.md:11`) is *"point at the exact word or quoted block it refers to"*; the worked example points at the wrong word, teaching the mis-binding it exists to prevent.
2. The gloss claims "the diff is quoted directly under the sentence", but the After block contains no quoted diff — compare Day 17, whose After does embed its fenced block (`17.md:30–35`). Anchor 5 requires resolution *"inside the prompt or to a quoted block"*; the block is asserted, not shown.

Against the anchors the After itself is defensible at 4–5 (only one viable antecedent exists), so this is a teaching defect rather than a scoring one — but a learner imitating the gloss's analysis learns to resolve pronouns wrongly, and `SKILL.md:28` has the tutor read it aloud verbatim.

**Minimal fix.** Rewrite `08.md:23` to bind "it" to the diff — ""It" resolves to the diff named in the previous sentence, the only candidate in the prompt" — and either show a short fenced diff in the After or drop the "quoted directly under the sentence" claim.

---

### DEFECT-A07 — Day 12 teaches end-placement; the interjection ladder's only positional cue is "near the top" — severity: medium

**Day 12**, `prompting-wizard/days/12.md:21`, `12.md:31`.

Cited rubric: `rubrics.md#interjection`, `rubrics.md:133–145`.

> **Measures:** attention and priority markers. (`rubrics.md:135`)

| Score | Anchor (verbatim, `rubrics.md:139–143`) |
|---|---|
| 1 | All instructions carry equal weight; the critical one is buried mid-paragraph. |
| 2 | A priority word is used ("important:") but attached to something that isn't actually the highest-stakes instruction. |
| 3 | The critical instruction is marked, but its position in the prompt still lets it get skimmed past. |
| 4 | The must-not-fail instruction is marked and positioned near the top, but competes with one other marked item. |
| 5 | The must-not-fail instruction is marked and positioned so it cannot be missed. |

Concept sentence carrying the claim, `12.md:7`:

> "But marking alone isn't enough: buried mid-paragraph, it still competes for attention. Position matters as much as the word. Standing alone, the same sentence becomes the hardest thing to have missed."

Novice tier, `12.md:31`: *"Mark that instruction IMPORTANT: and move it to stand alone at the end"*. The After, `12.md:21`, does exactly that — the marked line is last.

**Why they diverge.** The rubric never says where the marked instruction should sit except in anchor 4, which names "near the top" as the position associated with a high score. A grader working anchor by anchor, as `SKILL.md:34` requires, has anchor 3 ("its position in the prompt still lets it get skimmed past") available for a last-line instruction and anchor 4 unavailable (the After has no competing second marker, so anchor 4's disqualifier does not apply either). The result is an unstable 3-or-5, decided by whether the grader imports anchor 4's "near the top" as the rubric's position rule. The lesson's whole positional teaching — stand alone at the end — is unscored, and its only trace in the rubric points the other way.

**Minimal fix.** Rewrite anchor 4 to drop the positional direction, e.g. "The must-not-fail instruction is marked and positioned where it stands alone, but competes with one other marked item" — or add "at the top or standing alone at the end" to anchor 5 so the taught position is explicitly a 5.

---

### DEFECT-A08 — Day 15 tests one of the three properties role-framing scores — severity: medium

**Day 15**, `prompting-wizard/days/15.md:11`, `15.md:35`, `15.md:21`.

Cited rubric: `rubrics.md#role-framing`, `rubrics.md:161–173`.

> **Measures:** whether the role changes the output. (`rubrics.md:163`)

| Score | Anchor (verbatim, `rubrics.md:167–171`) |
|---|---|
| 1 | Role asserted with no bearing on output ("you are a world-class expert"). |
| 2 | The role is domain-relevant, but nothing in the prompt tells you what it includes, excludes, or assumes differently. |
| 3 | The role implies a standard or a body of knowledge, but the prompt doesn't say which parts to draw on. |
| 4 | Role changes what is included, excluded and assumed, though the mechanism is only implied, not stated. |
| 5 | Role changes what is included, excluded and assumed, and you can say how. |

Concept's self-test, `15.md:11`:

> "Here is the test: name your prompt's role, then list two things the output contains because of it that it wouldn't contain otherwise. Fewer than two, and the role is decoration."

Working tier, `15.md:35`: *"whose role changes what's included, excluded, **or** assumed"* (emphasis added).

The After, `15.md:21`:

> "Answer as a reviewer who has to sign off on {{TASK}} and will be paged if it breaks. Flag anything you wouldn't want your name attached to, and call out any assumption you can't verify from what's given."

**Why they diverge.** Anchors 4 and 5 are conjunctive: *included, excluded and assumed* — all three, every time. The self-test asks only for things the output **contains** (inclusion), the Working tier softens the conjunction to a disjunction ("or"), and the After demonstrates inclusion (flagged regrets) and assumption-handling (unverified assumptions) but names nothing the role **excludes**. A learner who passes the self-test and the Working tier as written has satisfied one or two of three scored dimensions and can be capped at 3 by a grader reading anchor 4 strictly. The concept's own prose knows better — `15.md:7` says the stance means "production failure matters more than style" — but that exclusion never reaches the test, the tier, or the model answer.

**Minimal fix.** Change "or" to "and" in `15.md:35`, change the self-test to "list one thing the output contains, one thing it leaves out, and one thing it assumes because of the role", and add an exclusion clause to the After, e.g. "...and skip style commentary."

---

### DEFECT-A09 — Day 16's two examples do not disagree, and disagreement is scored nowhere — severity: medium

**Day 16**, `prompting-wizard/days/16.md:23–24` against `16.md:7` and `16.md:38`.

Cited rubric: `rubrics.md#few-shot-examples`, `rubrics.md:175–187`.

> **Measures:** what the examples teach. (`rubrics.md:177`)

| Score | Anchor (verbatim, `rubrics.md:181–185`) |
|---|---|
| 1 | No examples, or examples that only show the easy case. |
| 2 | One example given, showing a typical case with nothing instructive about its edges. |
| 3 | Examples show variety, but none demonstrates a boundary or a near-miss. |
| 4 | Examples cover the boundary case but not a genuine failure case. |
| 5 | Examples cover the boundary case and the failure case. |

Concept's central claim, `16.md:7`:

> "Two examples that disagree do more work than ten that agree."

Working tier, `16.md:38`: *"whose two examples disagree — one a borderline pass, one a near-miss failure"*.

The After, `16.md:23–24`:

> "Boundary case: latency crept from 200ms to 350ms overnight, no alert fired, no user report. Not urgent — slow, silent, no threshold crossed.
> Failure case: a customer wrote in all caps with three exclamation marks about a typo in the footer copy. Not urgent — dramatic tone, but the impact is cosmetic."

**Why they diverge.** Both examples resolve to the same verdict — "Not urgent". They agree. The day is titled "two that disagree" (`16.md:1`), its thesis sentence is the one quoted above, and its Working tier explicitly requires "one a borderline pass" — which the model answer does not contain, because neither example passes. The rubric, meanwhile, scores only whether a boundary case and a failure case are present, so the After scores 5 while failing the day's own tier and illustrating none of its headline property. The learner is taught "disagree", shown two agreeing examples, and graded on something else again.

**Minimal fix.** Flip the boundary case to a borderline **urgent** verdict, so the pair straddles the line the examples are supposed to draw — e.g. "latency crept from 200ms to 3s over an hour, no alert fired. Urgent — no threshold crossed, but the trend crosses one within the day." That satisfies anchors 4–5, the concept, and the Working tier at once.

---

### DEFECT-A10 — Day 7's Advanced tier is graded on a property none of its five rubrics score — severity: medium

**Day 7**, `prompting-wizard/days/07.md:9`, `07.md:35`.

Cited rubrics (`07.md:39`): `#noun` `#verb` `#adjective` `#adverb` `#preposition` — Measures lines quoted in **A02**; full anchors verbatim at days 01–05 entries below.

The only anchors in those five that mention economy at all:

- `rubrics.md:17` (noun, 5): "Named unambiguously and economically — no words spent on the artifact beyond what pins it down."
- `rubrics.md:45` (adjective, 5): "Every quality that matters is named, and none that do not — each word does rejection work."

Concept, `07.md:9`:

> "A composed prompt earns its length. If you can delete a clause and the output wouldn't change, that clause wasn't constraining anything — it was decoration wearing a lever's clothes. The rewrite you're aiming for is the opposite: every clause, if removed, visibly weakens the result."

Advanced tier, `07.md:35`:

> "Rewrite your prompt so that removing any single clause measurably degrades the output — no clause is decorative, every one is load-bearing."

**Why they diverge.** The delete-a-clause-and-check test is the `#token-economy` rubric's measure — *"whether every token earns its place"* (`rubrics.md:317`), whose Fastest fix is *"delete a third of the context and see whether the output degrades"* (`rubrics.md:327`). Day 7 does not cite it. Of the five rubrics it does cite, verb, adverb and preposition contain no economy clause at any anchor, so a learner who spends the session making every clause load-bearing is scored on five other things. The whole Advanced tier is unscored work.

Day 7 is also the only day of the thirty whose `## Concept` has no closing self-test (verified by grep across `days/*.md`), so there is nothing to check the alignment against either.

**Minimal fix.** Add `rubrics.md#token-economy` to Day 7's `## Rubric` line, or recast the Advanced tier as a five-lever test ("removing any single clause leaves one of the five levers unset — name which"). Adding a self-test that names the five levers would close the second half.

---

### DEFECT-A11 — Day 21's self-test measures whether ordering mattered, not whether the ordering is right — severity: medium

**Day 21**, `prompting-wizard/days/21.md:11`.

Cited rubric: `rubrics.md#context-ordering`, `rubrics.md:245–257`.

> **Measures:** placement of instruction and material. (`rubrics.md:247`)

| Score | Anchor (verbatim, `rubrics.md:251–255`) |
|---|---|
| 1 | Instruction buried after a wall of context, or context missing where needed. |
| 2 | Instruction and context are both present but interleaved in a way that obscures which material serves which step. |
| 3 | Instruction is findable, but constraints are scattered rather than grouped at the end. |
| 4 | Instruction and context are ordered sensibly, with constraints mostly grouped but one placed early. |
| 5 | Instruction and context ordered so the model reads what it needs when it needs it. |

Self-test, `21.md:11`:

> "Here is the test: before you run the reordered version, predict what changes about the output. If nothing does, either order didn't matter here, or you didn't reorder enough to actually test it."

**Why they diverge.** Every anchor scores a static property of the prompt — where the instruction sits, whether the constraints are grouped at the end. The self-test scores a dynamic one: whether the learner's prediction about output change held. A learner can pass the self-test with a badly ordered prompt (any reorder that changes the output passes) and fail it with a perfectly ordered one (a short prompt where order genuinely does not matter). Nothing in the self-test checks task-first / material-second / constraints-last, which is the whole of anchors 3–5.

The adjacent paragraph at `21.md:9` has the same shape — *"The test is whether you deleted anything to make the new version read better"* — which is a `#token-economy` property (`rubrics.md:317`), not a placement one.

**Minimal fix.** Replace the self-test with a placement check: "Point at your instruction and at your constraints. Is the instruction the first thing read, and are all the constraints grouped last? If a constraint sits mid-material, move it." Keep the prediction exercise in the Working tier, where it already lives (`21.md:39`).

---

### DEFECT-A12 — Day 21 directs a session's work at three levers it scores none of — severity: medium

**Day 21**, `prompting-wizard/days/21.md:31`, `21.md:43`, `21.md:47`.

Cited rubric: `rubrics.md#context-ordering` only (`21.md:47`) — anchors quoted verbatim in **A11**.

Exercise direction, `21.md:31`:

> "Before presenting a tier, read `## Levers` from the learner's `PROGRESS.md`, identify the three lowest-scoring levers, and name them to the learner. Build the context-heavy material below around exercising those three"

Advanced tier, `21.md:43`:

> "...while also fixing the three levers named as weakest wherever they surface in the reordered material."

**Why they diverge.** The learner is told to fix three named levers and then scored against one rubric that measures none of them (`rubrics.md:247`: "placement of instruction and material"). The harness cannot make up the gap: `SKILL.md:30` allows exactly **one** secondary lever per session — *"add exactly one of them as a named secondary constraint ... One only"* — so at most one of the three is scored, and `SKILL.md:20` leaves the other two untouched. Two thirds of the day's named work is unscorable by construction.

Day 14 has the same three-weakest-levers direction (`14.md:25`) but cites all eleven rubrics (`14.md:41`), so it is covered. Day 21 is the unpatched twin.

**Minimal fix.** Either add the eleven lever rubrics to Day 21's `## Rubric` line as Day 14 does, or reduce `21.md:31`/`21.md:43` to the single lever `SKILL.md:30` can actually score.

---

### DEFECT-A13 — Day 1's concept caps at anchor 4; the anchor-5 property appears only in the Advanced tier — severity: low

**Day 1**, `prompting-wizard/days/01.md:11`, `01.md:41`.

Cited rubric: `rubrics.md#noun`, `rubrics.md:7–19`.

> **Measures:** the artifact the prompt asks for. (`rubrics.md:9`)

| Score | Anchor (verbatim, `rubrics.md:13–17`) |
|---|---|
| 1 | No artifact named. The prompt describes a topic or a wish, not a thing to produce. |
| 2 | A category is named ("a review", "some notes") but its shape is left open. |
| 3 | The artifact is recognisable, but a reasonable reader could still deliver two different things. |
| 4 | The artifact is named unambiguously. Someone reading only the prompt could describe the finished output. |
| 5 | Named unambiguously and economically — no words spent on the artifact beyond what pins it down. |

Concept, `01.md:11`:

> "Nouns compound with counts and formats, but those are later levers. Today, just name the thing."

**Why they diverge.** Anchor 4 is exactly what the concept teaches; anchor 5 adds economy, which the concept explicitly defers. Economy is recovered by the Advanced tier (`01.md:41`: *"names the artifact unambiguously in under 15 words total. Precision without length is the constraint"*), so Advanced learners are fine, but Novice and Working learners are scored against a top rung the concept told them was a later lever. The After (`01.md:21`) does score 5, so the ceiling is only reachable by imitation, not by instruction.

**Minimal fix.** One clause in `01.md:11`: "…but those are later levers. Today, just name the thing — in as few words as pin it down."

---

### DEFECT-A14 — Day 28's self-test asks for one failure mode; the anchor asks for the known ones — severity: low

**Day 28**, `prompting-wizard/days/28.md:11`.

Cited rubric: `rubrics.md#prompt-library`, `rubrics.md:343–355`.

> **Measures:** reusability. (`rubrics.md:345`)

| Score | Anchor (verbatim, `rubrics.md:349–353`) |
|---|---|
| 1 | Prompts rewritten from scratch each time. |
| 2 | A prompt is saved, but without marking which parts change between uses. |
| 3 | Saved prompts mark their variable slots, but don't record how they've failed before. |
| 4 | Reusable prompts stored with their slots and most known failure modes noted. |
| 5 | Reusable prompts stored with their slots and their known failure modes. |

Self-test, `28.md:11`:

> "Here is the test: open one saved prompt. Could a stranger use it correctly, and would they know, before running it, the one way it's failed before?"

**Why they diverge.** Anchors 4 and 5 are separated purely by coverage — *most* known failure modes versus *their* known failure modes, i.e. all of them. The self-test asks after "the one way it's failed", which is anchor 4's territory whenever more than one failure is known. The Working tier does say "its known failure modes documented" (`28.md:38`), so only the self-test is off. The After (`28.md:21–24`) records a single failure and is a legitimate 5 if that is the only one known.

**Minimal fix.** "…would they know, before running it, every way it's failed before?"

---

### DEFECT-A15 — The failure-diagnosis Fastest fix is narrower than its own anchors and Day 27's concept — severity: low

**Day 27**, `prompting-wizard/days/27.md:7`; `rubrics.md:341`.

Cited rubric: `rubrics.md#failure-diagnosis`, `rubrics.md:329–341`.

> **Measures:** whether the cause is identified. (`rubrics.md:331`)

| Score | Anchor (verbatim, `rubrics.md:335–339`) |
|---|---|
| 1 | Failure blamed on the model; prompt unchanged. |
| 2 | A cause is guessed at, but it isn't named as one of the specific levers or techniques. |
| 3 | A lever or technique is named as the cause, but the fix doesn't actually target it. |
| 4 | The failing lever is identified by name and the fix changes that lever, but it also changes a second lever that was not implicated. |
| 5 | The failing lever is identified by name and the fix targets it. |

> **Fastest fix:** ask which of the 11 levers was underspecified, and fix that one. (`rubrics.md:341`)

Concept, `27.md:7`:

> "A real diagnosis names one of the eleven levers or one of the techniques from the last two weeks: the pronoun had no antecedent, the stop condition was never stated, the reasoning steps weren't named."

**Why they diverge.** Anchors 2 and 3 admit "levers **or techniques**"; the concept does too, and two of its three worked examples are techniques (stop condition = day 23, named reasoning steps = day 19). The Fastest fix line, which is the guidance a tutor reaches for when a learner scores low, restricts the search to the 11 levers. A learner whose real cause was a missing stop condition is pointed at the wrong catalogue. Anchors 4 and 5 also say "lever" only, which reads as an oversight given anchors 2–3.

**Minimal fix.** "ask which of the 11 levers or the techniques from weeks 3–4 was underspecified, and fix that one" — and the same substitution in anchors 4 and 5.

---

### DEFECT-A16 — Day 6's and Day 14's word budgets are scored by no cited rubric — severity: low

**Day 6**, `prompting-wizard/days/06.md:39`; **Day 14**, `days/14.md:37`.

Cited rubrics as listed in **A02** (day 6) and **A04** (day 14). The only anchor across all eleven that scores length is `rubrics.md:17` (noun, 5): *"Named unambiguously and economically — no words spent on the artifact beyond what pins it down"* — and it scores the artifact phrase, not the prompt.

Advanced tiers:
- `06.md:39`: "Write a prompt for {{TASK}} that sets all five levers in under 40 words total."
- `14.md:37`: "…sets all eleven levers in under 60 words total, holding the three named as weakest to the same standard as the rest."

**Why they diverge.** Total prompt length is a `#token-economy` property (`rubrics.md:317`), which neither day cites. A learner who blows the budget by ten words but sets all levers scores identically to one who hits it. The constraint is real work with no scoring consequence. Harmless as a discipline; listed for completeness.

**Minimal fix.** Say so in the tier ("the budget is a discipline, not a scored criterion") — the pattern Day 23 already uses correctly at `23.md:9`: *"Stating the condition before the tools is a useful habit, not a scored one."*

---

### DEFECT-A17 — Day 19's model answer fixes intermediates the rubric scores as task-relative — severity: low

**Day 19**, `prompting-wizard/days/19.md:21`.

Cited rubric: `rubrics.md#reasoning-scaffolds`, `rubrics.md:217–229`.

> **Measures:** whether reasoning is structured where needed. (`rubrics.md:219`)

| Score | Anchor (verbatim, `rubrics.md:223–227`) |
|---|---|
| 1 | Reasoning demanded without structure, or suppressed where it was needed. |
| 2 | Reasoning is requested, but the intermediate steps expected aren't named. |
| 3 | Some intermediate steps are named, but one that the task actually depends on is missing. |
| 4 | The reasoning steps asked for match the ones the task requires, with minor slack in ordering. |
| 5 | The reasoning steps asked for match the ones the task requires. |

The After, `19.md:21`:

> "For {{TASK}}: list the assumptions the answer would depend on that aren't stated in the material, then check each against what's actually given. Answer citing which of those assumptions it relies on and whether each was confirmed."

**Why they diverge.** `SKILL.md:24` substitutes the learner's own task into `{{TASK}}` before the After is shown. This rubric is the only one of the twenty-six whose anchors are defined purely relative to *the task at hand* — "the ones the task requires". A fixed pair of intermediates (assumption list, confirmation pass) is a 5 for verification-shaped tasks and a 3 for anything whose answer depends on something else — a ranking task depends on the comparison criteria, not on unstated assumptions. The concept is correct (`19.md:11` tells the learner to derive the list from the task); the model answer is the part that cannot generalise.

Note: the previously-fixed gating defect is confirmed fixed — `19.md:9` now reads *"Naming steps can also gate the answer on them — useful, but secondary to getting the list right"*, which correctly subordinates the unscored property.

**Minimal fix.** Add one clause to the After's gloss at `19.md:23` making the task-dependence explicit: "these two intermediates are the ones *this* task depends on; a ranking task would name its comparison criteria instead."

---

## Per-day dossier

Days not carrying a finding are recorded here with the judgment that cleared them. Rubric text is
verbatim from `rubrics.md` at the line numbers shown; where a rubric's full anchor table is already
quoted verbatim in the Findings section above, that location is given rather than re-quoted.

**Day 01** — `#noun` (`rubrics.md:7–19`, anchors quoted in **A13**). Central claim: the deliverable must be nameable as a noun phrase. Carrying sentence, `01.md:7`: "The noun is the deliverable. Naming it collapses the space of acceptable answers faster than any other lever." Self-test (`01.md:9`) tests the scored property directly. After (`01.md:21`) — "Produce a five-bullet review of {{TASK}}, one bullet per correctness issue" — is unambiguous and economical: **5**. Finding **A13** (low) only.

**Day 02** — `#verb` (`rubrics.md:21–33`). **Measures:** the operation requested (`rubrics.md:23`). Anchors: 1 "No verb, or one that names no operation ("help", "look at")." 2 "A verb is present but names a family of operations, not one ("handle", "deal with"), so the model must guess which." 3 "An operation is named, but a nearby operation would satisfy the same wording just as well." 4 "Exactly one operation named, and it is the operation wanted, but expressed with a generic synonym ("check" instead of "audit") where a more specific verb in the same family exists." 5 "Exactly one operation named, and it is the operation actually wanted." Central claim, `02.md:9`: "One prompt, one verb, doing the operation you actually want." Self-test (`02.md:11`) isolates the verb — exactly the scored property. Working tier names anchor 4's failure verbatim ("not a generic stand-in like 'check' or 'handle'"). After: "Rank the correctness issues in {{TASK}} by blast radius, worst first" — one operation, specific: **5**. **Aligned.**

**Day 03** — `#adjective` (`rubrics.md:35–47`, anchors quoted in **A05**). Central claim, `03.md:7`: "A quality word that rules nothing out — "good", "high-quality", "professional" — is not a constraint, it is decoration." Self-test (`03.md:11`) tests rejection work, which is anchor 5's language. After (`03.md:21`): two qualities, each with a stated rejection, plus a reader-applicable test: **5**. Finding **A05** (medium) on the Advanced tier.

**Day 04** — `#adverb` (`rubrics.md:49–61`, anchors quoted in **A01**). Finding **A01** (high). After: **3**.

**Day 05** — `#preposition` (`rubrics.md:78–89`, anchors quoted in **A03**). Central claim, `05.md:7`: "Prepositions carry scope and relation: in what, for whom, without what." Self-test (`05.md:11`) asks all three. After (`05.md:21`): "Fix the correctness problems in {{TASK}}, for a reader who has not seen the codebase, without introducing new dependencies" — scope, audience, exclusion, precisely: **5**. **Aligned.**

**Day 06** — five rubrics, Measures lines in **A02**. Findings **A02** (high), **A03** (high), **A16** (low). After: noun 4, verb 5, adjective 5, adverb 2, preposition 3.

**Day 07** — five rubrics, Measures lines in **A02**. Tutor-driven, no supplied After (`07.md:17–19` explicitly defers the rewrite until the learner has attempted one). Finding **A10** (medium).

**Day 08** — `#pronoun` (`rubrics.md:63–75`, anchors quoted in **A06**). Central claim, `08.md:7`: "A pronoun is a shortcut for a noun already named — it only works once naming happens first." Self-test (`08.md:11`) tests the scored property. Finding **A06** (medium) on the gloss.

**Day 09** — `#conjunction` (`rubrics.md:91–103`). **Measures:** conditional logic (`rubrics.md:93`). Anchors: 1 "Branching cases collapsed into one instruction, so edge cases silently pick a branch." 2 "One branch is acknowledged but its condition or its outcome is missing." 3 "Branches and conditions are named, but the fallback (the otherwise) is missing." 4 "Each branch stated with its condition and its fallback, though the wording leaves the order of checks ambiguous." 5 "Each branch stated with its condition and its fallback, in an order that resolves without ambiguity." Central claim, `09.md:9`: "…or the fallback can be missing, exactly as underspecified as no branching at all, since it's the branch everything else defaults to." Concept covers ordering at `09.md:11`, which is the 4→5 step, and the Advanced tier (`09.md:43`) exercises it. Self-test (`09.md:13`) names condition, outcome and fallback — the scored triple. After (`09.md:23`): one condition, one outcome, an explicit otherwise, no ordering ambiguity possible with a single branch: **5**. **Aligned.**

**Day 10** — `#determiner` (`rubrics.md:105–117`). **Measures:** definiteness and quantity binding (`rubrics.md:107`). Anchors: 1 "Bare nouns leave it unclear whether one, some, or all are meant." 2 "A determiner is used on the main noun, but supporting nouns nearby are still bare." 3 "Most nouns are bound, but one noun that changes scope significantly ("the" vs "any") is left bare." 4 "Each noun is bound — the, a, each, every, any — with only a minor reading left open." 5 "Each noun is bound — the, a, each, every, any — with no reading left open." Central claim, `10.md:9`: "A bare noun next to a bound one is still a gap" — which is anchor 2 stated as a lesson. Self-test (`10.md:11`) is the rubric's Fastest fix. After (`10.md:21`): "Fix every correctness issue in {{TASK}}. Leave each style issue alone" — both scope-bearing nouns bound: **5**. **Aligned.**

**Day 11** — `#numeral` (`rubrics.md:119–131`). **Measures:** budgets that make output checkable (`rubrics.md:121`). Anchors: 1 "No quantity anywhere; length and count unbounded." 2 "One quantity is given (e.g. a word count) but other countable dimensions (item count, number of examples) are open." 3 "Most countable dimensions are bounded, but the bound is vague enough to need judgement ("a few", "several")." 4 "Every countable dimension is bounded with a number, though one bound is awkward to verify without counting carefully." 5 "Every countable dimension bounded, and the bounds checkable without judgement." Central claim, `11.md:11`: "Count, length, and any other countable property each need their own bound, or the one left open becomes the loophole the constraint leaks through" — anchor 2 as a lesson. Self-test (`11.md:13`) tests checkability-without-judgement, anchor 5's clause. After (`11.md:23`): "exactly three options … each under 40 words, ranked by cost": **5**. **Aligned.**

**Day 12** — `#interjection` (`rubrics.md:133–145`, anchors quoted in **A07**). Finding **A07** (medium).

**Day 13** — `#particle` (`rubrics.md:147–159`). **Measures:** phrasal precision (`rubrics.md:149`). Anchors: 1 "Phrasal verbs used loosely, so the operation is ambiguous (look up / look over / look into)." 2 "A phrasal verb is used, and swapping its particle would plausibly change the intended task without the writer noticing." 3 "The phrasal verb is close to right, but a stricter synonym would remove a small remaining ambiguity." 4 "Every phrasal verb is chosen deliberately, with only cosmetic substitutions available." 5 "Every phrasal verb chosen deliberately; no substitution preserves the meaning." Central claim, `13.md:9`: "A particle earns its place only if changing it would change the task." Self-test (`13.md:11`) is the swap test the anchors describe. After (`13.md:21`): "Look up each external call in {{TASK}} and check it against its documented contract" — "up" is load-bearing against "over"/"into": **5**. **Aligned.**

**Day 14** — all eleven lever rubrics, Measures lines in **A04**. Concept enumerates all eleven at `14.md:5` ("an operation, two qualities, a manner, a reference, a boundary, a condition, a quantity binding, a count, a marker, and a particle" plus the artifact), so coverage is complete. Tutor-driven, no supplied After. Finding **A04** (high).

**Day 15** — `#role-framing` (`rubrics.md:161–173`, anchors quoted in **A08**). Finding **A08** (medium).

**Day 16** — `#few-shot-examples` (`rubrics.md:175–187`, anchors quoted in **A09**). Finding **A09** (medium).

**Day 17** — `#output-schemas` (`rubrics.md:189–201`). **Measures:** the format contract (`rubrics.md:191`). Anchors: 1 "Format unspecified, or described in prose only." 2 "A format is named ("as a table", "in JSON") but its fields or columns are not enumerated." 3 "Fields are enumerated, but types, order, or optionality are left unstated." 4 "An exact structure is given, checkable in most cases, with one edge (e.g. empty values) unaddressed." 5 "An exact structure given, which output can be checked against mechanically." Central claim, `17.md:7`: "A schema is checkable when it names every field, its type, and its order, and shows what an empty value looks like — filled with dummy data before a single real value exists." That is anchors 3, 4 and 5 in one sentence, in order. Self-test (`17.md:18`) — "could you write a script that rejects a malformed output without you reading it first?" — is anchor 5's "checked against mechanically". After (`17.md:28–37`) supplies the fenced dummy payload, fixes the status literals, addresses the empty value, and forbids adding or omitting keys: **5**. **Aligned** — and the only day whose After embeds the artifact it describes.

**Day 18** — `#task-decomposition` (`rubrics.md:203–215`). **Measures:** whether the work is split correctly (`rubrics.md:205`). Anchors: 1 "One prompt carries several tasks that interfere." 2 "The tasks are listed, but their inputs and outputs aren't separated, so they still interfere." 3 "Tasks are split into steps, but one step's output isn't a clean input to the next." 4 "Work split so each step has one output and a mostly clear input from the last." 5 "Work split so each step has one output and a clear input from the last." Central claim, `18.md:7`: "Splitting into three prompts only fixes this if each step's input is exactly the last step's output: nothing added, nothing re-explained" — anchor 3 stated as a lesson. Self-test (`18.md:11`) checks the seam verbatim-ness, which is the 3→5 distinction. After (`18.md:21–33`): three prompts, each seam carrying the prior output unedited, with the gloss confirming no re-explanation: **5**. **Aligned.**

**Day 19** — `#reasoning-scaffolds` (`rubrics.md:217–229`, anchors quoted in **A17**). Finding **A17** (low). Previously-fixed gating defect confirmed fixed at `19.md:9`.

**Day 20** — `#negative-constraints` (`rubrics.md:231–243`). **Measures:** what is ruled out (`rubrics.md:233`). Anchors: 1 "No exclusions; known failure modes not ruled out." 2 "An exclusion is stated, but it's generic ("don't be verbose") rather than tied to an observed failure." 3 "One real failure mode is excluded, but a second, equally likely one is not." 4 "Exclusions are specific and mostly map to failures you've seen, with one still speculative." 5 "Exclusions are specific, and each prevents a failure you have actually seen." Central claim, `20.md:5`: "A negative constraint only works when it names the exact failure it forbids, and that failure has to be one you've actually watched happen, not one you're guessing at" — anchor 5 restated. The Novice tier (`20.md:31`) even uses anchor 2's own example, "don't be verbose", as the thing to replace. Self-test (`20.md:11`) tests observedness, the anchor-4/5 discriminator. After (`20.md:21`): two exclusions, each citing a named incident: **5**. **Aligned.**

**Day 21** — `#context-ordering` (`rubrics.md:245–257`, anchors quoted in **A11**). Findings **A11** and **A12** (both medium). The After itself (`21.md:21–25`) is a clean **5**: instruction first, material unchanged, constraints grouped last, nothing deleted.

**Day 22** — `#system-prompts` (`rubrics.md:259–271`). **Measures:** separation of standing rules from the turn (`rubrics.md:261`). Anchors: 1 "Durable rules repeated per turn, or turn-specific detail promoted into standing rules." 2 "Some durable rules are separated out, but turn-specific detail still leaks into them." 3 "Durable rules and turn request are mostly separated, but one standing rule is restated per turn out of habit." 4 "Standing behaviour and per-turn request are separated into two blocks, but one line in the system prompt is turn-specific and could move to the per-turn request without changing behaviour." 5 "Standing behaviour and per-turn request cleanly separated." Central claim, `22.md:9`: "Leakage runs both ways: a durable rule restated every turn is redundant, and a turn-specific detail promoted into the system prompt is a landmine for the next request" — anchor 1's two halves. Self-test (`22.md:11`) — "would this be false on some future turn?" — is the exact discriminator anchor 4 uses. After (`22.md:21–27`): three durable rules in the system block, the request alone per turn, nothing turn-specific left standing: **5**. **Aligned.**

**Day 23** — `#agent-and-tool-prompting` (`rubrics.md:273–285`). **Measures:** tool use and stopping conditions (`rubrics.md:275`). Anchors: 1 "Tool use implied but not specified; no stopping condition." 2 "Tools are named, but when to use each one and what counts as done are both unstated." 3 "Tools and rough sequencing are given, but the stopping condition is missing or vague." 4 "Which tools, when, and what "done" means are all stated, though the done-condition could still be gamed." 5 "Which tools, when, and what "done" means are all stated." Central claim, `23.md:7`: "What separates strong from merely adequate is whether "done" can be gamed" — the 4→5 step, named as such. `23.md:9` explicitly de-scopes the unscored habit: "Stating the condition before the tools is a useful habit, not a scored one — tools listed first with an airtight, ungameable condition after them score no lower." Self-test (`23.md:11`) tests gameability. After (`23.md:21`): three tools with their situations, ordered, plus a transcript-checkable stop condition: **5**. **Aligned** — and the model for how an unscored teaching point should be flagged (cf. **A16**).

**Day 24** — `#self-critique-loops` (`rubrics.md:287–299`). **Measures:** whether output is checked (`rubrics.md:289`). Anchors: 1 "Single-pass output accepted with no check." 2 "A check is mentioned ("review your answer") but with no criteria to check against." 3 "A concrete check is named, but there's no stated action for when it fails." 4 "A check the model can apply to its own output is given, with an action on failure that's only loosely defined." 5 "A check the model can apply to its own output, with a stated action when it fails." Central claim, `24.md:9`: "The loop isn't finished until it says what to do when the check fails" — anchor 3's gap, named. Self-test (`24.md:11`) tests whether the check can fail, which is anchor 2's gap. After (`24.md:21`): a named check (traceability to source) with a stated two-branch action (cut it or mark it "unverified"): **5**. **Aligned.**

**Day 25** — `#writing-evals` (`rubrics.md:301–313`). **Measures:** whether quality is measurable (`rubrics.md:303`). Anchors: 1 "Quality judged by feel; no criteria written down." 2 "Criteria exist but are subjective enough ("sounds right") that two scorers would diverge." 3 "Criteria are written and mostly objective, but one is still a judgement call." 4 "Criteria written before the output, specific enough that two people would agree most of the time." 5 "Criteria written before the output, specific enough that two people would score the same." Central claim, `25.md:9`: "The order is the whole discipline. Criteria written after the output are a justification for a verdict you already reached by feel." Both anchor-4 and anchor-5 clauses — written first, and two scorers converging — are taught. Self-test (`25.md:11`) — "show your criteria to someone who hasn't seen the output. Could they score it without asking you what you meant?" — is anchor 5. After (`25.md:21`): three mechanically checkable criteria, stated before generation, scored unchanged after: **5**. **Aligned.**

**Day 26** — `#token-economy` (`rubrics.md:315–327`). **Measures:** whether every token earns its place (`rubrics.md:317`). Anchors: 1 "Context padded with material the task never uses." 2 "Some unused material is trimmed, but redundant restatements of the same instruction remain." 3 "Most padding is removed, but one section is included "just in case" rather than because the task needs it." 4 "Every included token earns its place on inspection, but the cuts have not been tested against the output to confirm accuracy held." 5 "Every included token earns its place; cuts made without losing accuracy." Central claim, `26.md:9`: "The test is the cut, not the eyeballing" — precisely the 4→5 discriminator, which is the one anchor pair a course could easily miss. Self-test (`26.md:11`) is the rubric's Fastest fix. After (`26.md:21`) plus its gloss (`26.md:23`: "Keeping it wasn't a guess; it was confirmed") demonstrates the tested cut: **5**. **Aligned.**

**Day 27** — `#failure-diagnosis` (`rubrics.md:329–341`, anchors quoted in **A15**). Central claim, `27.md:9`: "The fix has to target only what you named. Touch three things at once, and even if the output improves you won't know which one did it" — anchor 4, stated as a lesson. Self-test (`27.md:11`) tests naming-before-touching, anchors 2–3. Tutor-driven, no supplied After. Finding **A15** (low), and it sits in `rubrics.md`, not the day.

**Day 28** — `#prompt-library` (`rubrics.md:343–355`, anchors quoted in **A14**). Central claim, `28.md:9`: "Marking the slot without the failure gets you partway … The failure note turns reusable into reliable" — anchor 3 to anchor 5, in order. After (`28.md:21–24`): template, named slot, known failure and its fix: **5**. Finding **A14** (low) on the self-test only.

**Day 29** — `#capstone` (`rubrics.md:357–369`). **Measures:** production readiness (`rubrics.md:359`). Anchors: 1 "Prompt works once, on the example it was written against." 2 "Prompt works on a couple of close variants, but hasn't been tried on anything unlike the original case." 3 "Prompt is specified and works on varied cases, but has no written evaluation criteria." 4 "Prompt is specified and evaluated against written criteria, with failure modes noted but not systematically." 5 "Prompt is specified, evaluated against written criteria, and its failure modes documented." Central claim, `29.md:9`: "Reaching that rung honestly caps you at anchor 3. Anchors 4 and 5 need written criteria and documented failures — day 30's work, not more polish today." The ladder direction is stated correctly: anchor 3 is characterised by the *absence* of written criteria, and the day tells the learner not to add them. Tier-to-anchor mapping checks out (`29.md:29` → anchor 1, `29.md:33` → anchor 2/3, `29.md:37` → anchor 3). Self-test (`29.md:11`) tests "works on varied cases", anchor 3's clause. **Aligned.**

**Day 30** — `#capstone` (`rubrics.md:357–369`, anchors above). Central claim, `30.md:9`: "The rubric's rungs are exact, not impressionistic. Day 29's target — "specified and works on varied cases" — sits at anchor 3 only because it has "no written evaluation criteria" yet. Add the criteria and evaluate against them: anchor 4, "evaluated against written criteria, with failure modes noted but not systematically." Document what the unseen case breaks, systematically: anchor 5, the same evaluation with failure modes "documented" rather than just noted." Every quoted fragment matches `rubrics.md:365–367` word for word, and the direction of the ladder is correct. **Aligned** — the third previously-fixed defect is confirmed fixed.

---

## Notes for the fixer (not findings)

- Two of the four high findings (**A01**, **A02**) are the same root cause: the word "exhaustively" is treated across the course as if it were a measure. It appears at `04.md:9`, `04.md:21`, `04.md:23`, and `06.md:21`, `06.md:23`. Fixing the adverb rubric is not the answer — anchor 2 is correct and the prose is what drifted.
- **A03** and **A08** are the same shape: a later day compresses a three-part lever into two parts, and the model answer inherits the compression. Worth grepping for other three-part definitions before shipping fixes.
- `rubrics.md` has no not-applicable rung on any of the 26 rubrics. **A04** is the first place that gap becomes visible to a learner, but any day that scores a lever the learner's task genuinely does not use has the same exposure.
- Day 23 (`23.md:9`) and Day 19 (`19.md:9`) both contain explicit "this part is not scored" sentences. They are the pattern the other unscored-property findings (**A10**, **A16**) should be fixed toward.
