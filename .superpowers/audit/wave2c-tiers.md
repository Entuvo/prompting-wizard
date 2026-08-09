# Wave 2, batch C — tier ladders for days 22–30

Scope: `prompting-wizard/days/22.md` … `days/30.md`, `## Exercise` tier bodies only.
Every anchor quoted below is the **settled** text of `prompting-wizard/rubrics.md`, read from the
file. Where the plan's quoted anchor differs from the file, the file wins and the difference is
recorded under "Discrepancies".

## Verification

| Check | Result |
|---|---|
| `python3 tools/validate.py --complete` | `ok`, exit 0 |
| `python3 -m unittest discover -s tools` | 103 tests, OK (no test file touched) |
| `git diff --stat` | days 22, 24, 26, 27, 28, 30 only — 6 files, 18 insertions / 18 deletions |
| `## ` / `### ` headings | none touched (`git diff -U0 -- prompting-wizard/days \| grep '^[+-]#'` → empty) |
| "be ready to" / "be able to" / "if asked" / "able to point" riders in 22–30 | **none** (grep clean; day 24 had one, removed) |
| Advanced tier whose added demand is a word or item budget | **none** in 22–30 (day 28's "three prompts" removed; day 22's three per-turn asks assessed below and kept as a detection procedure, not a budget) |
| `## Concept`, `## Before / After`, `## Rubric`, `## Completion` edited | none |
| Days 01, 23, 25, 29 | **not edited** — confirmed by `git diff --stat` |

```
 prompting-wizard/days/22.md | 6 +++---
 prompting-wizard/days/24.md | 6 +++---
 prompting-wizard/days/26.md | 6 +++---
 prompting-wizard/days/27.md | 6 +++---
 prompting-wizard/days/28.md | 6 +++---
 prompting-wizard/days/30.md | 6 +++---
```

Days 01–21, 23, 25 and 29 untouched. No edit outside a tier body.

The **imitate-the-After test** below is the batch-A/B escaped-defect check: `SKILL.md:28` presents
`## Before / After` immediately before the exercise, so the realistic bottom-rung learner copies the
day's own worked example. For each Novice tier: which anchor does that learner reach?

---

## Day 22 — `rubrics.md#system-prompts`

| Tier | Anchor | Anchor text (verbatim) | Why it lands there, and not a rung higher or lower |
|---|---|---|---|
| Novice (rewritten) | **3** | "Standing behaviour and per-turn request are separated into two blocks, but two or more lines are on the wrong side — in either direction." | The tier guarantees the count: the learner ensures the prompt carries "two details true only of this one request" and then puts "every other line, the two details included" in the system prompt. Two turn-specific lines promoted into standing rules = anchor 3 exactly. **Not 4**: anchor 4 needs *exactly one* wrong line; the tier mandates two. **Not 5**: same clause. **Not 2**: anchor 2 is partial separation ("**Some** durable rules are separated out"); here every durable line is in the system block. **Reaches 2** if the learner leaves durable rules down in the per-turn ask as well — room to fail preserved. |
| Working (rewritten) | **4** | "Standing behaviour and per-turn request are separated into two blocks, and exactly one line is on the wrong side — in either direction." | "Putting every line on the side it belongs on except one: leave **exactly one** rule that would still be true on a future turn sitting in the per-turn ask." Anchor 4's state, mandated. **Not 5**: see shortfall. **Not 3**: only one line is wrong. |
| Advanced (amended) | **5** | "Standing behaviour and per-turn request are separated into two blocks, and no line is on the wrong side — in either direction." | The three-ask stress test, now running **both** directions: "If any ask would force you to edit the system prompt, move that line down into the ask; if a line repeats in all three asks, move it up into the system prompt. Revise until neither move is left to make." Neither move remaining *is* "no line on the wrong side, in either direction". |

**Working leaves open:** *"exactly one line is on the wrong side — in either direction."*
**Mandated**, not silent. Anchor 5 on this rubric is the **absence** of error, so any tier that asks
for a correct split is asking for anchor 5 — silence is not available here, and the shortfall is a
positive state (a line present on the wrong side), which is rule 2's stated licence to mandate.
**Wave-3 entry filed: FIX-3.16.**

**Imitate-the-After test:** the After splits three durable rules from one request with nothing on the
wrong side — anchor 5. A Novice learner copying it reaches 5 *unless* the tier forecloses it, which
is why the two-detail mandate is in the tier text rather than left to the learner's own prompt
containing turn-specific detail by luck. A compliant imitator now lands at **3**.

**Before → after ladder:** 4–5 / 5 / 5 → 3 / 4 / 5.

## Day 23 — `rubrics.md#agent-and-tool-prompting` (model ladder — re-derived, not edited)

Re-derived against the settled anchors because wave 1's FIX-1.21 rewrote anchor 5, and because the
plan's rule 1 cites this day using the **pre-wave-1** wording ("the done-condition could still be
gamed" as anchor 5's negative). The citation's substance survives; the wording does not.

| Tier | Anchor | Anchor text (verbatim) | Why it lands there |
|---|---|---|---|
| Novice | **3** | "Tools and rough sequencing are given, but the stopping condition is missing or vague." | "Names which tools to use, **roughly** when each applies, and a stop condition — all three stated, in any order." No bar is set on the stop condition, so the least-effort compliant fill ("stop when it's done") is vague. **Reaches 4** for a learner who volunteers a checkable one — the permitted 3-or-4-by-learner shape. **Reaches 2** if timing is left out. |
| Working | **4** | "Which tools, when, and what \"done\" means are all stated, though the done-condition could still be gamed." | "A specific, checkable outcome rather than an action taken — something you could verify against the transcript." A checkable outcome is still gameable: "stop when the tests pass" is satisfied by deleting the failing test, and by tests that already passed. Checkability and un-gameability are different properties, which is the whole of `days/23.md:7`. |
| Advanced | **5** | "Which tools, when, and what \"done\" means are all stated, and the done-condition names a checkable state that motion alone cannot satisfy." | "State one way a model could satisfy it without doing the real work, then **rewrite the condition so that shortcut no longer counts as done**." The shortcut hunt is exactly the "motion alone cannot satisfy" test, and the rewrite lands in the prompt, so `rubrics.md:5` can see it. |

**Working leaves open:** *"though the done-condition could still be gamed."* **Left silent** — the
tier never asks the learner to look for a shortcut, which is the only thing the rewritten anchor 5
adds.

**Imitate-the-After test:** the After is an anchor-5 prompt. A Novice imitator would reach 4–5 — but
imitation here is strictly *more* work than compliance, not less (the After's condition is longer and
harder than "stop when it's done"), so the least-effort compliant path is still anchor 3. This is the
distinction that separated day 12's and day 18's real leaks — where the anchor-5 shape was the
*easier* branch — from the ordinary case where a diligent learner outperforms their tier. **No edit.**

**Before → after ladder:** 3 / 4 / 5 → 3 / 4 / 5, unchanged. **Verdict: sound.**

## Day 24 — `rubrics.md#self-critique-loops`

| Tier | Anchor | Anchor text (verbatim) | Why it lands there, and not a rung higher or lower |
|---|---|---|---|
| Novice (amended) | **3** | "A concrete check is named, but there's no stated action for when it fails." | "Add one named check the model applies to its own output before finishing — **the check only, with nothing said about what to do if it fails**." The added clause negates anchor 4's positive content ("with an action on failure") in the anchor's own terms. **Not 4 or 5**: both require an action on failure, which the tier forbids. **Reaches 2** if the "check" is "review your answer" with no criteria — room to fail. |
| Working (rewritten) | **4** | "A check the model can apply to its own output is given, with an action on failure that names no operation (\"fix it\", \"try again\")." | "Plus an instruction to do something about it when it fails — **\"fix it\" or \"try again\", without naming what to do to the failing element**." Anchor 4 in the anchor's own two examples, with anchor 5's discriminator negated in anchor 5's own words. |
| Advanced (rewritten) | **5** | "A check the model can apply to its own output, with an action on failure that names what to do to the failing element." | "Whose action on failure **names what to do to the failing element**: the operation to perform on it, not \"fix it\". Say **in the prompt** what output would trigger that correction." Exactly the 4→5 discriminator; the plausibly-failable check is the pre-existing anti-degenerate guard, and the rider is gone. |

**Working leaves open:** *"with an action on failure that names no operation (\"fix it\", \"try
again\")."* **Mandated**, not silent. **Wave-3 entry filed: FIX-3.17.** Mandating is a judgement call
here — the shortfall is an action that is *present* but unnamed, which is positive enough to qualify
under rule 2 — and the decisive fact is the imitate-the-After result below: left silent, the
imitating Working learner reaches 5 and the ladder returns to the 3/5/5 T21 reported.

**Imitate-the-After test:** the After is "check every factual claim against the source material; if
any claim doesn't trace to something in the source, **cut it or mark it \"unverified\"**" — a named
operation on the failing element, anchor **5**. Before this batch, a Novice learner copying it
reached 5 from the bottom rung (the old Novice said only "add one named check" and forbade nothing).
That is the escaped-defect shape, and it was live on day 24. The tier now caps the imitator at **3**.

**Rider:** the checkpoint names day 24 as carrying one. "Be ready to say what output would have
triggered it" is deleted and replaced with "Say **in the prompt** what output would trigger that
correction". Working's surviving phrase "a check specific enough that **you can say**, in one
sentence, what a failure would look like" was assessed and kept: it states a property of the *check*
(the day's own self-test at `:11`), not a spoken artifact the tutor must score — the same class as
day 12's retained "Say which of the two is the one that must not fail".

**Before → after ladder:** 3 / 5 / 5 → 3 / 4 / 5.

## Day 25 — `rubrics.md#writing-evals` (model ladder — re-derived, not edited)

Re-derived because FIX-1.23 rewrote all five rows under CONFLICT-08's hard constraint that this day
must not move, and because the plan's rule 1 cites its Advanced tier.

| Tier | Anchor | Anchor text (verbatim) | Why it lands there |
|---|---|---|---|
| Novice | **3** | "Criteria written before the output, but at least one names a feeling rather than a checkable property." | "Before writing a prompt for {{TASK}}, write three checks you'll apply to whatever it produces." Timing is satisfied; no specificity bar is set, so the least-effort fill ("is it clear? is it useful?") names feelings. **Not 4**: nothing requires a checkable property. **Reaches 2** if the checks are written after the output exists — the learner has to get the order right, which is the only thing this rung tests. |
| Working | **4** | "Criteria written before the output, each naming a checkable property a reader who has not seen the output could apply without asking the writer, but at least one could be applied two ways." | "Specific enough that **someone else could apply them without asking you what you meant**." Anchor 4's clause verbatim — FIX-1.23 deliberately placed "apply … without asking" at 4, not 5. |
| Advanced | **5** | "Criteria written before the output, and every criterion is specific enough that two readers who have not seen the output would produce the same score." | "Score it against exactly those three — **don't add a fourth, and don't soften one it narrowly misses**." The no-drift test is what makes two scorers converge: a criterion that survives a narrow miss without softening is one that two readers apply identically. |

**Working leaves open:** *"but at least one could be applied two ways."* **Left silent** — the tier
asks only that the criteria be *applicable*, never that they admit one reading, so a precise learner
may reach 5. Permitted 4-or-5 shape.

**Imitate-the-After test:** the After's three checks ("every claim traces to a source, no paragraph
exceeds five sentences, the conclusion appears in the first paragraph") are anchor-5 criteria. As on
day 23, imitating them is more work than complying with Novice, and the rung the tier *tests* is
timing, which the After also models and which imitation cannot shortcut. Least-effort compliant path
stays at **3**. **No edit.**

**Before → after ladder:** 3 / 4 / 5 → 3 / 4 / 5, unchanged. **Verdict: sound**, and CONFLICT-08's
constraint holds against the shipped file.

## Day 26 — `rubrics.md#token-economy`

| Tier | Anchor | Anchor text (verbatim) | Why it lands there, and not a rung higher or lower |
|---|---|---|---|
| Novice (rewritten) | **3** | "Most padding is removed, but one section is included \"just in case\" rather than because the task needs it." | "Cut the parts you can point to no use for at all, and **keep the one section you're least sure about**." Anchor 3 word for word. **Not 4**: anchor 4 needs every included token to earn its place on inspection, and the kept section explicitly does not. **Not 5**: "do not run the two versions and compare". **Reaches 2** if only the obvious padding goes and restatements remain. |
| Working (rewritten) | **4** | "Every included token earns its place on inspection, but the cuts have not been tested against the output to confirm accuracy held." | "Cut a third … so that **every line left has to earn its place**. Make every cut **by inspection alone**: do not run the two versions and compare." Anchor 4's two clauses, in order. |
| Advanced (rewritten) | **5** | "Every included token earns its place, and the cut version was rerun and the output held." | "Run the cut version and the original and compare the two outputs. **Put back only what the comparison shows the output needed**, and send **the version whose output held**." Both halves of anchor 5's evidence clause — the rerun, and the output holding — and nothing else. |

**Working leaves open:** *"but the cuts have not been tested against the output to confirm accuracy
held."* **Mandated**, not silent: the day's concept and self-test both demand the rerun, so silence
would send every learner to anchor 5 — which is precisely T22's finding. **Wave-3 entry filed:
FIX-3.18.**

Note on the harness: `SKILL.md:32` still runs the learner's prompt, so "do not rerun" is scoped to
the learner's own *comparison* ("do not run the two versions and compare"), which is what anchor 5's
evidence actually is. A single harness run of the cut prompt produces no comparison and does not lift
Working to 5.

**Imitate-the-After test:** the After keeps one paragraph "because a rerun without it changed what
counted as resolved" — anchor 5. A Novice imitator would rerun and compare, reaching 5; the tier now
forbids the comparison in the anchor's own terms and mandates a kept "just in case" section, capping
the imitator at **3**.

**Before → after ladder:** 5 / 5 / 5 → 3 / 4 / 5.

## Day 27 — `rubrics.md#failure-diagnosis`

No seed: `## Before / After` is tutor instruction (procure a real failed prompt, then have the learner
record a written diagnosis before anything runs). The ladder is built on the diagnosis-and-fix, which
is what the rubric scores.

| Tier | Anchor | Anchor text (verbatim) | Why it lands there, and not a rung higher or lower |
|---|---|---|---|
| Novice (amended) | **3** | "A lever or technique is named as the cause, but the fix doesn't actually target it." | Lever-by-lever hunt, "have them name it before anything is run, then **run the failed prompt unchanged** to confirm what it produces — **no fix today**." A named cause with no fix is anchor 3; **not 4 or 5**, both of which require a fix that changes the named lever. **Reaches 2** if the learner names something that isn't one of the eleven levers or the techniques. |
| Working (plan text) | **4** | "The failing lever or technique is identified by name and the fix changes it, but it also changes a second lever or technique that was not implicated." | "Name the single lever or technique responsible **and state the fix for it**", with "only" removed. The fix targets the named lever; nothing constrains what else the rewrite disturbs. |
| Advanced (rewritten) | **5** | "The failing lever or technique is identified by name and the fix targets it and nothing else." | "A fix that **changes nothing but the named one** — every other lever and technique left exactly as it was — then run both the original and the fixed version and check that nothing else moved." Exactly the 4→5 discriminator, with the two-run comparison as its verification. |

**Working leaves open:** *"but it also changes a second lever or technique that was not implicated."*
**Left silent** — the tier neither requires nor forbids collateral change. Mandating here would mean
instructing a learner to damage a second lever on purpose, which teaches the opposite of the day; and
the natural outcome of rewriting a prompt to fix one lever *is* collateral change, so anchor 4 is the
default and anchor 5 takes the deliberate discipline Advanced names. **No wave-3 mandate entry
required**; FIX-3.20 is filed as tracking only, because `:9` ("the fix has to target **only** what you
named") teaches the anchor-5 discipline to every tier and a wave-3 editor could turn it into a
tier-level demand.

**Imitate-the-After test:** the After has the learner name the lever **and what they'd change** — a
diagnosis plus a fix, anchor 4 or 5. The Novice imitator would therefore write a fix; "no fix today"
forecloses it and caps the imitator at **3**. The clause is recorded in FIX-3.20 as the sentence to
scope if wave 3 touches the day.

**Rule 4:** the old Novice ended "Name it before running anything" and produced no artifact for
`SKILL.md:32` to run. It now ends by running the failed prompt unchanged, which is the artifact the
day's `## Exercise` preamble already procures — the day-14/T12 defect, closed without inventing a
revision that would have landed on a higher rung.

**Before → after ladder:** 3 / 5 / 5 → 3 / 4 / 5.

## Day 28 — `rubrics.md#prompt-library`

| Tier | Anchor | Anchor text (verbatim) | Why it lands there, and not a rung higher or lower |
|---|---|---|---|
| Novice (rewritten) | **3** | "Saved prompts mark their variable slots, but don't record how they've failed before." | "Save it with every variable part marked as a named slot — **the slots only, nothing yet about how it has failed** — and send the saved prompt." Anchor 3 word for word, with anchor 4's positive content ("at least one failure mode recorded") negated in the anchor's own words. **Reaches 2** if the prompt is saved without marking which parts change. **Was anchor 4** before this batch: the old text required "one failure mode you've actually seen written underneath it". |
| Working (plan text) | **4** | "Reusable prompts stored with their slots and at least one failure mode recorded, but not specifically enough for a stranger to recognise it before running the prompt." | "Every variable part marked as a named slot, and **note underneath each way you remember it failing**." Slots plus recorded failures, with no specificity bar. |
| Advanced (rewritten) | **5** | "Reusable prompts stored with their slots and their failure modes recorded specifically enough that a stranger would recognise each one before running the prompt." | "Every failure mode written **specifically enough that a stranger would recognise the failure before running it** — name what the bad output looked like, not just the category." Anchor 5's clause, plus the one operational reading of it, and nothing else. |

**Working leaves open:** *"but not specifically enough for a stranger to recognise it before running
the prompt."* **Left silent** — the shortfall is privative (a note that is not specific enough), and
mandating vagueness would be absurd, so rule 2's preference applies. A learner who writes specifically
reaches 5; permitted 4-or-5 shape.

**Imitate-the-After test:** the After records "invents a fifth risk when fewer than five exist. Fix:
state the count found before listing" — stranger-recognisable, anchor **5**. Before this batch the
Novice tier explicitly asked for a failure mode, so both the imitator *and* the compliant learner sat
at 4–5 from the bottom rung. The foreclosure caps the imitator at **3**.

**Wave-2 checkpoint item 6, day-28 half — SATISFIED, not left open.** `days/28.md:42` no longer
requires three `## Tasks` entries: the Advanced tier saves **one** prompt, for `{{TASK}}`. S15's
day-28 exposure is closed at source; FIX-4.15's count check is still worth adding but no longer has a
consumer that breaks without it. (Day 21's half remains open by design, re-homed to wave-3 checkpoint
item 10 by FIX-3.13.)

**Before → after ladder:** 4 / 5 / 5 → 3 / 4 / 5.

## Day 29 — `rubrics.md#capstone` (model ladder, capped by design — re-derived, not edited)

Re-derived because FIX-1.27 carried a robustness axis into anchors 4 and 5, which is the change
CONFLICT-09 flagged as the one that could break this day's cap.

| Tier | Anchor | Anchor text (verbatim) | Why it lands there |
|---|---|---|---|
| Novice | **1** | "Prompt works once, on the example it was written against." | "Write a first pass … run it once, and confirm it produces the deliverable they wanted — anchor 1, the floor everyone starts from." Stated aloud in the tier, per rule 6. |
| Working | **2–3** | 2: "works on a couple of close variants, but hasn't been tried on anything unlike the original case." / 3: "Prompt is specified and works on varied cases, but has no written evaluation criteria." | "Two cases of the named task that differ from each other, not just from the original … until it holds up on both." Robustness rises; nothing requires the prompt be *specified*, so it lands at 2 or 3 depending on the learner. |
| Advanced | **3** | "Prompt is specified and works on varied cases, but has no written evaluation criteria." | "Specify the prompt fully — every lever and technique the task actually depends on — then run it on the most different case they can construct." Specified plus varied cases. **Capped at 3**: anchors 4 **and** 5 both open with written criteria, and day 29 produces none. FIX-1.27 did not touch that gate. |

**The cap survives FIX-1.27 intact.** Anchor 5's new robustness clause ("holds on a case it was not
designed for") is arguably *reached* by the Advanced tier's most-different case, but anchor 5 is
conjunctive and its written-criteria and documented-failure clauses are not, so the ceiling is
unmoved. `days/29.md:9` ("Reaching that rung honestly caps you at anchor 3. Anchors 4 and 5 need
written criteria and documented failures — day 30's work") remains true word for word, and the
Advanced tier repeats it. Rule 6 satisfied. No rider, no budget. **No edit.**

**Before → after ladder:** 1 / 2–3 / 3 → 1 / 2–3 / 3, unchanged. **Verdict: sound, and still
correctly capped.**

## Day 30 — `rubrics.md#capstone` (the inversion)

| Tier | Anchor | Anchor text (verbatim) | Why it lands there, and not a rung higher or lower |
|---|---|---|---|
| Novice (rewritten) | **3** | "Prompt is specified and works on varied cases, but has no written evaluation criteria." | Three checks written, then "run it on a second case of the same task — **a close variant, not a case it was never built for** — and score it against those checks. **Record the scores only; nothing about what broke gets written down at this tier.**" Criteria exist, but anchors 4 and 5 both gate on failure modes being *noted*, and the tier forbids that; anchor 5 additionally needs a case it was not designed for, which the tier forbids. **Reaches 2** if the checks are never really written and the prompt is only tried on close variants. |
| Working (plan text) | **4** | "Prompt is specified, holds on varied cases, and is evaluated against written criteria, with failure modes noted but not specifically enough for someone else to recognise them." | "Run … on a case unlike the one it was designed for, **score it against the written criteria, and note what broke**." Criteria applied, failures noted, no specificity bar, no fix — so the prompt does not yet *hold* on the case it was not designed for. |
| Advanced (plan text) | **5** | "Prompt is specified, holds on a case it was not designed for, is evaluated against written criteria, and its failure modes are documented specifically enough that someone else could recognise each one." | "Write down each failure mode the case exposed **specifically enough that someone else could recognise it**, fix only what that case revealed, and **rerun until it passes the criteria on both cases**." Both halves of the 4→5 gap — documentation specificity and holding on the unfamiliar case — and nothing else. |

**Working leaves open:** *"with failure modes noted but not specifically enough for someone else to
recognise them"*, and, by omission, anchor 5's "holds on a case it was not designed for" — Working
notes the break and never fixes it. **Left silent** on the specificity clause: the shortfall is
privative and mandating vagueness is not available. Permitted 4-or-5 shape.

**Imitate-the-After test:** the After runs "a case unlike the one it was built against", documents
what broke, fixes and re-runs — anchor **5**. The old Novice ("run it once more on the same case")
did not forbid any of that, so an imitating Novice reached 4–5 and, per R38, could reach anchor 5
without ever leaving the original case. The rewritten tier forecloses both routes — close variant
only, scores only — and caps the imitator at **3**.

**The inversion is fixed.** Before: Working wrote the failure mode down specifically enough for
someone else to recognise it (anchor 5) while Advanced only "fixed what that case revealed" (anchor
4), so the Advanced learner finished the course a rung below the Working learner. After: documentation
specificity moves up to Advanced and joins the robustness clause there; Working keeps the un-specific
note.

**Before → after ladder:** 3 / 5 / **4** → 3 / 4 / 5.

**Wave-3 entry filed: FIX-3.19** — `days/30.md:9` quotes the pre-FIX-1.27 anchor text ("not
systematically", "documented" versus "noted") and omits the robustness axis entirely; it is read
aloud verbatim on the last day of the course. The entry also records that FIX-4.07 is now unblocked
and that `## Completion`'s "passes **both**" (`:45`) has no referent under the rebuilt Novice tier.
`## Completion` was **not** edited — it is wave 4's, per FIX-2.27's blocking note.

---

## Summary — before and after

| Day | Rubric | Before (census) | After | Edited |
|---|---|---|---|---|
| 22 | system prompts | 4–5 / 5 / 5 | 3 / 4 / 5 | yes |
| 23 | agent and tool prompting | 3 / 4 / 5 | 3 / 4 / 5 | no (model) |
| 24 | self-critique loops | 3 / 5 / 5 | 3 / 4 / 5 | yes |
| 25 | writing evals | 3 / 4 / 5 | 3 / 4 / 5 | no (model) |
| 26 | token economy | 5 / 5 / 5 | 3 / 4 / 5 | yes |
| 27 | failure diagnosis | 3 / 5 / 5 | 3 / 4 / 5 | yes |
| 28 | prompt library | 4 / 5 / 5 | 3 / 4 / 5 | yes |
| 29 | capstone | 1 / 2–3 / 3 | 1 / 2–3 / 3 | no (model, capped) |
| 30 | capstone | 3 / 5 / 4 | 3 / 4 / 5 | yes |

Every Novice checked against `census-tiers.md` including where the plan had no entry: days **24**
(plan called it "correctly at anchor 3" — it was, but nothing foreclosed the After's anchor-5 shape),
**26**, **27** and **28** (census had it at 4) all needed work the plan did not ask for.

---

## Departures from the plan, and why

Eleven. Each is a case where the plan entry conflicts with the brief's bar, with the settled
`rubrics.md`, or with the imitate-the-After test, and the plan entry loses.

1. **FIX-2.22 says day 22's Novice reaches "anchor 3–4 by a different route" and asks only that it be
   verified.** Verification fails: "underline anything that would still be true on a future turn …
   and move it into a system prompt; leave the rest as the per-turn ask" is the concept's own test at
   `:11`, and a learner who applies it correctly produces a split with no line on the wrong side —
   anchor **5**, from the bottom rung, against a Working tier the same entry caps at 4. That is the
   inverted 5/4/5 both earlier batches shipped a fix round for. Novice rewritten to guarantee two
   misplaced lines.

2. **FIX-2.22's replacement Working tier reaches anchor 5.** Its text — "putting each line where it
   belongs. **One line may still sit on the wrong side**; the split itself is the exercise" — states
   anchor 5's positive content as the demand and merely *permits* the shortfall. Because anchor 5 on
   this rubric is the absence of error, permission is not enough: the diligent learner complies and
   scores 5. Replaced with a mandate ("leave **exactly one** rule … in the per-turn ask"), which is
   the day-18 / day-21 shape, and FIX-3.16 filed for the concept collision that follows.

3. **FIX-2.22 says "Leave `:45` as written" (day 22 Advanced).** As written it checks one direction
   only — whether an ask forces a system-prompt edit — which catches turn-specific detail promoted
   upward but not a durable rule left in the per-turn ask. Anchor 5 says "**in either direction**",
   and the rebuilt Working tier now plants an error in precisely the direction the old Advanced could
   not see, so Advanced would have tied Working for any learner who left a rule below. One clause
   added for the second direction.

4. **Day 24's Novice, not addressed by the plan.** FIX-2.23 states it "sits correctly at anchor 3 —
   a named check, no failure action", but nothing in the tier forbade the failure action, and the
   day's After models the anchor-5 form immediately before the exercise. Foreclosed in anchor 4's own
   words.

5. **FIX-2.23's replacement Working tier is silent where silence leaks.** "Plus an instruction to do
   something about it when it fails" permits "cut it or mark it unverified" — the After's own
   wording — which is anchor 5. Tightened to mandate anchor 4's state in the anchor's two examples,
   and FIX-3.17 filed.

6. **FIX-2.23's Advanced replacement under-specifies the discriminator.** It keeps "with a stated
   correction", which does not say what separates 4 from 5 after FIX-1.22 (whether the action *names
   the operation on the failing element*). Rewritten to demand exactly that. The plan's own rider
   replacement — "say in the prompt what output would trigger the correction" — is kept verbatim.

7. **FIX-2.24's replacement Novice for day 26 lands at anchor 4, not 3.** "Cut the parts you can't
   point to a use for" leaves every remaining token earning its place on inspection, which is anchor
   4 — where the same entry also puts Working. Same defect class as batch B's departures 3 and 5.
   Retargeted to anchor 3 by keeping the one section the learner is least sure about. Its trailing
   "say for each cut why the task doesn't need it" is also a rule-5 rider — spoken, scored by nothing
   — and was dropped.

8. **FIX-2.24's replacement Working tier for day 26 carries a rider**: "you should be able to say
   what each one does". Same class as batch A's departures 1 and 2. Dropped; the scored property
   ("every line left has to earn its place") is kept.

9. **FIX-2.24 says "Leave `:39` as written" (day 26 Advanced).** Three problems. (a) "Before
   rerunning, **predict which half mattered**" is unscored work on a property `token-economy` does
   not measure — SYS-2's fourth variant, and the same removal batch B made on day 21's Advanced.
   (b) It never requires the output to hold, which is half of FIX-1.24's anchor-5 evidence ("the cut
   version was rerun **and the output held**"). (c) "Cut **half**" versus Working's third is a
   quantity escalation the entry's own *Why* says the rubric does not measure. Rewritten to the
   anchor-5 clause and nothing else.

10. **FIX-2.25's replacement Advanced for day 27 keeps a prediction the rubric does not score.**
    "Predict in one sentence what the rerun will show" is rule-7 / SYS-2 work; the entry's own *Why*
    concedes "the rubric scores the diagnosis and the fix, not the prediction". It is also redundant:
    the day's `## Before / After` already makes a written prediction the universal procedure for
    every tier. Removed; the two-run comparison is kept as the verification of anchor 5's own claim.

11. **FIX-2.26 does not touch day 28's Novice, which `census-tiers.md` records at anchor 4.** The
    tier required "one failure mode you've actually seen written underneath it", which is anchor 4's
    positive content. Lowered to slots-only, anchor 3. Its Advanced replacement also ends "Then hand
    it to someone who has never used it and check" — a third party the daily loop cannot supply and
    the tutor cannot verify at scoring time. Dropped; the scoreable form of the same test ("name what
    the bad output looked like, not just the category") is kept.

## Departures from literal plan text, non-substantive

Recorded separately because none changes an anchor.

- **`days/24.md:31`** — rule 4's send step ("then send the completed prompt") added, as batches A and
  B did on `days/04.md:31`, `14.md:29`, `18.md:41` and `19.md:31`. The plan proposes no text for this
  line at all.
- **`days/26.md:31`** and **`days/28.md:34`** — same addition ("send the shortened prompt", "send the
  saved prompt"); neither line has plan text.
- **`days/22.md:37`** — same ("Send both blocks"); the artifact on this day is two blocks, not one
  prompt, on every tier.
- **`days/27.md:29`** — rule 4 has no send step available on a tutor-driven day whose Novice writes
  no new prompt, so the tier now ends by running the failed prompt unchanged. This is the minimum
  that gives `SKILL.md:32` an artifact without inventing a revision that would land above anchor 3.
- **`days/30.md:37`** — the plan's Advanced replacement is used verbatim except that "rerun until it
  passes the criteria on both cases" is kept as written; no change of substance, noted only because
  the surrounding clause order was preserved rather than re-flowed.

## Discrepancies between the plan's quoted anchors and the settled file

The file wins in all three; wave 1 is settled.

- **(a) `agent-and-tool-prompting` anchor 5 — the plan's rule 1 citation.** Rule 1 says day 23's
  anchors "differ by 'the done-condition could still be gamed'" and cites the pre-wave-1 rows. The
  file, after FIX-1.21, states the property positively at 5: "the done-condition names a checkable
  state that motion alone cannot satisfy." The citation's *substance* survives — Advanced's
  shortcut-and-rewrite is that clause — but the wording it quotes is gone, and a reader who inherits
  the citation would be checking day 23 against a row that no longer exists.
- **(b) `writing-evals` anchors 4 and 5 — the plan's rule 1 citation.** Rule 1 says they "differ by
  'agree most of the time' vs 'score the same'". Neither phrase is in the file: FIX-1.23 replaced the
  whole ladder, and the settled split is "could be applied two ways" at 4 against "two readers …
  would produce the same score" at 5. CONFLICT-08's hard constraint still holds — day 25 lands
  3 / 4 / 5 — but it holds for a different reason than rule 1 states.
- **(c) `capstone` anchors 4 and 5.** `census-tiers.md`'s day-30 findings (T25, T26) reason from
  "noted but not systematically" and "documented"; the file carries FIX-1.27's replacement, with
  stranger-recognisability at both rows and a robustness clause at each. FIX-2.27 is already
  re-derived against it and was followed; the census entry is stale and should not be re-read.

## Wave-3 entries filed in `MASTER-FIX-PLAN.md`

Added after FIX-3.15, with the wave-3 file list (now 16 day files) and the wave-3 checkpoint
(now 17 items) updated to match.

- **FIX-3.16 — Day 22** (medium). `:7`'s "move a durable rule into the per-turn slot and you retype
  it forever" and `:11`'s one-directional self-test versus a Working tier that mandates exactly that
  rule staying in the per-turn ask, and an Advanced tier that now checks both directions. Explicit
  **do not touch** on the Before / After at `:15-29`.
- **FIX-3.17 — Day 24** (medium). `:9` treats anything short of a named correction as an unfinished
  loop; after FIX-1.22 the unnamed action is anchor 4 and no action is anchor 3, and both are now
  tier rungs. Explicit **do not touch** on `:15-23` and a note that `:11`'s self-test is a bar on the
  check, not the action, and is correct at every rung.
- **FIX-3.18 — Day 26** (medium). `:7`, `:9` and `:11` all require the rerun that Novice and Working
  are now forbidden to perform. Direction: declare the rerun the top rung's addition, in day 29's
  self-cap shape. Explicit **do not touch** on `:15-23`.
- **FIX-3.19 — Day 30** (high). The concept quotes two anchors FIX-1.27 deleted and omits the
  robustness axis, and is read aloud verbatim on the final day. Also records that FIX-4.07 is
  unblocked and that `## Completion`'s "passes both" needs a tier-independent trigger.
- **FIX-3.20 — Day 27** (low, tracking only). `:9`'s "target **only** what you named" is anchor 5
  taught to every tier, and the After's "what they'd change" contradicts the Novice tier's "no fix
  today". Nothing is broken — Working permits 4 and does not forbid 5 — but a wave-3 editor
  tightening `:9` would reclose anchor 4.

## The flat stretch, days 22–28

Noted, not fixed (wave 5's concern). After this batch every day from 22 to 28 rises 3 / 4 / 5 within
itself, so the ladders are sound, but the *absolute* demand across the stretch is close to level:
each day asks for one artifact exercising one technique, and none of days 22–28 is harder than day
21's reorder-a-200-word-prompt exercise. The two places it is most visible:

- **Day 26 Working** now asks for less physical work than before (one cut, no runs) because the rerun
  moved up a rung. That is correct against the rubric and it does reduce day 26's session length, as
  FIX-2.24's sequencing note predicts.
- **Day 27 Novice** asks for no new prompt at all — the artifact is the learner's existing failed
  prompt. It is the lightest tier in the stretch. The rubric gives no honest way to make it heavier
  without lifting it off anchor 3, so the fix, if one is wanted, belongs to pacing rather than to
  tiers.

## Nothing was stopped on

Two candidates were considered and resolved rather than escalated.

- **Day 23's Novice tier** admits an anchor-4 reading for a diligent learner, and the day's After is
  an anchor-5 prompt. Day 23 is a model day carrying an explicit do-not-touch, and wave 2's
  checkpoint item 3 requires it to stay out of the diff. It was left alone on the substantive ground
  recorded above: imitating its After is *more* effort than complying with its Novice, so the
  least-effort compliant path stays at anchor 3, which is the standard the two escaped defects
  failed. Recorded here so a reviewer can overrule it cheaply.
- **Day 27's Novice tier** produces no new prompt, which rule 4 requires. The rubric makes a
  prompt-producing anchor-3 tier impossible (any fix at all lands at 4 or 5), so the tier now runs the
  existing failed prompt instead. Recorded as a non-substantive departure rather than a stop, since
  `SKILL.md:32` gets its artifact either way.

---

# Round 2 — day 22's Novice bounded to lines, and three declarations corrected

Two tier-body edits, both in scope. Days 24, 27, 28 and 30 were **not** touched this round
(round-2 `git diff --stat` against the round-1 commit: `days/22.md` 1 line, `days/26.md` 2 lines,
`MASTER-FIX-PLAN.md`).

## Critical — `days/22.md:37` did not reliably reach anchor 3

Round 1 mandated "two **details** true only of this one request". `rubrics.md` `## System prompts`
counts **lines**: anchor 3 is "two or more **lines** are on the wrong side — in either direction",
anchor 4 "exactly one line", anchor 5 "no line". Two details commonly live in one sentence — "Summarise
the 12 May budget.xlsx figures" carries both — and the same tier sends "the request itself" to the
per-turn ask, so the details travel down with the request and the split comes out clean: **anchor 5,
from the bottom rung**, against a Working tier mandated down to 4. The unit the tier counted was not
the unit the rubric counts.

Round 1 also failed to apply its own day-23 clearance criterion to day 22. Days 24, 26, 27, 28 and 30
all ask the learner to do *less* than the day's After; day 22 alone asked for *more* — find or
fabricate two turn-specific details, then deliberately strand them — while `:9` had just been read
aloud telling them a promoted detail "is a landmine for the next request". Drift to the After was
both cheaper than compliance and endorsed by the concept, which is exactly the least-effort test that
cleared day 23.

**Fixed at `days/22.md:37`:**

> Take a prompt you've sent more than once for {{TASK}}. If it doesn't already carry two lines, each carrying a detail true only of this request — a date, a file name, this week's numbers — add them, kept separate from the request line. Then split it into two blocks: the request line goes in the per-turn ask, and every other line, those two included, goes in the system prompt. Send both blocks.

One clause does both jobs. Counting in **lines** matches the rubric's unit, and "kept separate from
the request line" plus "the **request line** goes in the per-turn ask" makes the two lines
un-smuggleable: they cannot ride down with the request, because the request is now a named single
line. The effort gradient flattens with it — the learner adds two short lines to a prompt they
already have and then splits on a line boundary, which is less work than reproducing the After's
judgement about which rules are durable.

## Day 22 re-derived against `rubrics.md` `## System prompts`

| Tier | Anchor | Anchor text (verbatim from the file) | Why it lands there, and not a rung higher or lower |
|---|---|---|---|
| Novice | **3** | "Standing behaviour and per-turn request are separated into two blocks, but two or more lines are on the wrong side — in either direction." | Exactly two lines carrying request-only detail sit in the system block, by instruction, and they are lines by construction. **Not 4**: anchor 4 needs *exactly one* line wrong; the tier mandates two, and they can no longer collapse into one line or ride down with the request. **Not 5**: same clause. **Not 2**: every durable rule is in the system block, so the separation is not partial. **Reaches 2** if the learner also leaves durable rules in the per-turn ask — room to fail preserved. |
| Working | **4** | "Standing behaviour and per-turn request are separated into two blocks, and exactly one line is on the wrong side — in either direction." | "Leave **exactly one** rule that would still be true on a future turn sitting in the per-turn ask." Anchor 4's state, mandated, in the opposite direction to Novice's. |
| Advanced | **5** | "Standing behaviour and per-turn request are separated into two blocks, and no line is on the wrong side — in either direction." | The three-ask stress test run in both directions, revised "until neither move is left to make" — which is anchor 5's clause restated as a stopping condition. |

**Imitate-the-After test, revised Novice:** the After (`:21-27`) splits three durable rules from one
request with nothing on the wrong side — **anchor 5**. A learner who copies it is now visibly
non-compliant twice over: the tier requires two request-only lines to exist and requires them to be
in the system block, and neither can be satisfied by the After's shape. A compliant imitator lands at
**3**, and the cheaper path is now compliance rather than drift.

## Declarations corrected — the departure count is thirteen, not eleven

Both were real edits past plan text and both were mis-filed in round 1. Neither is withdrawn; each is
now declared.

12. **`days/30.md:29` was substantively rewritten past FIX-2.27's replacement text.** The plan's
    Novice reads "run it on a **second case of the same task** and score it against those checks".
    Two clauses were added that the plan does not contain: "**a close variant, not a case it was
    never built for**", which forecloses anchor 5's "holds on a case it was not designed for", and
    "**Record the scores only; nothing about what broke gets written down at this tier**", which
    forecloses anchors 4 and 5 at their shared failure-modes-noted gate. Without them the imitating
    Novice reaches 4–5, since the day's After documents what broke, fixes and re-runs. These two
    clauses are what hold day 30's bottom rung at 3; filing them as "the plan's text" understated the
    edit.

13. **`days/27.md:29` was edited where FIX-2.25 says explicitly "Novice (`:29`) is correctly at
    anchor 3 … Leave it."** Round 1 filed the change as non-substantive on the grounds that the run
    step was a rule-4 formality. That contradicts round 1's own imitate-the-After paragraph, which
    says the added "**no fix today**" caps an imitating learner at 3. A clause that moves a learner
    from 4–5 to 3 changes an anchor, and it is the clause that makes the day's ladder rise at all.
    Declared here as substantive: the plan's "leave it" was written against a tier read in isolation
    from its own `## Before / After`, which is tutor instruction telling the learner to write down
    "what they'd change".

`days/27.md:29`'s run clause ("then run the failed prompt unchanged to confirm what it produces")
remains what the non-substantive list described — rule 4's artifact — but it travels with the
substantive clause and is no longer listed separately.

**Corrected ledger: thirteen substantive departures, four non-substantive** (`days/22.md:37`,
`24.md:31`, `26.md:31`, `28.md:34` — the send steps, none of which appears in plan text). The
round-1 "Departures from literal plan text, non-substantive" list is superseded by this paragraph on
its `days/27.md:29` and `days/30.md:37` entries; the latter recorded no change of substance and is
withdrawn as a non-departure (the plan's Advanced text was used verbatim).

## Wave-3 filings corrected

- **FIX-3.16 completed.** Round 1 named `days/22.md:7` and `:11` but not `:9` — "a turn-specific
  detail promoted into the system prompt is a landmine for the next request" — which is the sentence
  the rebuilt **Novice** tier now has every bottom-tier learner violate, deliberately and twice, and
  the collision this batch actually created. It is now the entry's first and most acute item, with
  the reason the mandate is unavoidable (anchor 5 is the absence of error, so every sub-5 rung must
  be specified as an error state) recorded alongside it. Wave-3 checkpoint item 13 now requires all
  three sentences.
- **FIX-3.20 re-graded from "low, tracking only" to medium, with a mandated edit.** The `days/27.md:21`
  versus `:29` collision is not the concept-versus-anchor tension days 22, 24, 26 and 30 have, where
  the After is an illustrative model prompt a learner may aim below. Day 27's After is **tutor
  instruction about the learner's own actions** — `SKILL.md:28` reads it aloud and `days/27.md:25`
  directs the tutor to run the exercise "per `## Before / After`" — so the learner is told to write
  down what they'd change and then told "no fix today". The mandated direction is to scope `:21`'s
  "and what they'd change" to Working and above, keeping the written prediction itself, which is the
  day's method for the upper tiers. The `:9` half stays tracking-only. Checkpoint item 17 rewritten
  to match.
- **Wave-3 file-list convention stated.** A day is listed when some entry mandates an edit to it;
  tracking-only entries mandate nothing and their days are not listed. Day 27 is listed because
  FIX-3.20 now mandates its `:21` edit; `days/17.md` (FIX-3.15) remains the only excluded day. The
  convention is written into the file-list paragraph so the next batch does not have to re-derive it.

## Minors folded in

- **`days/26.md:31`** — "Cut the parts you can point to no use for at all" replaced with the plan's
  own phrasing, "Cut the parts you can't point to a use for". Same foreclosure, plainer sentence; the
  anchor-3 clause that follows ("keep the one section you're least sure about") is unchanged.
- **`days/26.md:35`** — "Send the cut version." added. It was the only tier on its day without a send
  step after round 1 gave one to Novice and Advanced; rule 4 applies to every tier, not only to
  Novice.

## Round 2 verification

| Check | Result |
|---|---|
| `python3 tools/validate.py --complete` | `ok`, exit 0 |
| `python3 -m unittest discover -s tools` | 103 tests, OK |
| Round-2 diff scope | `days/22.md` (1 line), `days/26.md` (2 lines), `MASTER-FIX-PLAN.md` — days 24, 27, 28 and 30 untouched this round |
| Days 01, 23, 25, 29 | still not edited, in either round |
| `## ` / `### ` headings | none touched |
| Day 22 ladder | 3 / 4 / 5, counted in the rubric's own unit (lines), with no formatting or smuggling route to anchor 5 from Novice |
| Riders in 22–30 | still none |
| Advanced word/item budgets in 22–30 | still none |
