# Wave 3, batch B — concepts, days 12–21

Scope executed: FIX-3.11 (day 12, all three collisions), FIX-3.21(f) (day 13), FIX-3.07 + FIX-3.14
(day 15), FIX-3.08 (day 16), FIX-3.12 (day 18), FIX-3.09 including its round-2 `:9` amendment +
FIX-3.21(g) (day 19), FIX-3.10 + FIX-3.13 (day 21), and the FIX-2.21(b) / checkpoint-item-10 ruling.

Out of range and untouched: days 01–11 (wave 3A), days 22–30 (batch C), `rubrics.md`, `SKILL.md`,
`assessment.md`, `tools/`. Day 14 not edited (CONFLICT-03). Day 17 not edited (FIX-3.15 is
tracking-only, and no defect was found in it). Day 20 has no filed wave-3 entry and was not edited.

Every anchor quoted below is read from `prompting-wizard/rubrics.md` by text, never by line number.
Every word count is recomputed with `validate.py`'s own `section(text, '## Concept')` plus
`len(str.split())` — no eye-counts, no arithmetic-only figures.

---

## Verification

| Check | Result |
|---|---|
| `python3 tools/validate.py --complete` | `ok`, exit 0 |
| `python3 -m unittest discover -s tools` | 103 tests, OK (no test file touched) |
| `## ` / `### ` headings | none touched (`git diff -U0 -- prompting-wizard/days \| grep '^[+-]#'` → empty) |
| `## Exercise` tier bodies | **none touched** — every day-file hunk is at line 5–11 (`## Concept`) or at a `## Before / After` line (15 `:21,:23`; 16 `:23,:26`; 19 `:23`) |
| `## Rubric` sections | none touched; `days/21.md:47` deliberately unchanged (see the ruling) |
| `rubrics.md`, `SKILL.md`, `assessment.md`, `tools/`, days 01–11, days 22–30 | untouched |
| `days/14.md:9`, `days/17.md`, `days/28.md:11` | not edited |
| `## Concept` 200-word cap | max in range is **197** (day 15) |

```
 prompting-wizard/days/12.md | 6 +++---
 prompting-wizard/days/13.md | 6 +++---
 prompting-wizard/days/15.md | 8 ++++----
 prompting-wizard/days/16.md | 8 ++++----
 prompting-wizard/days/18.md | 6 +++---
 prompting-wizard/days/19.md | 8 ++++----
 prompting-wizard/days/21.md | 6 +++---
 7 files changed, 24 insertions(+), 24 deletions(-)
```

`MASTER-FIX-PLAN.md` also changed — the amendments and the new FIX-5.09 required by lesson 5. It is
not a day file and is listed separately in the commit.

## Concept word counts (cap 200), recounted

| Day | Before | After | Headroom |
|---|---|---|---|
| 12 | 185 | **195** | 5 |
| 13 | 185 | **194** | 6 |
| 14 | 186 | 186 (unedited) | 14 |
| 15 | 182 | **197** | 3 |
| 16 | 178 | **190** | 10 |
| 17 | 178 | 178 (unedited) | 22 |
| 18 | 164 | **184** | 16 |
| 19 | 188 | **196** | 4 |
| 20 | 181 | 181 (unedited) | 19 |
| 21 | 182 | **196** | 4 |

Days 15, 19 and 21 are now within four words of the cap, and day 12 within five. Any later wave
adding a clause to those four must delete first. This is the same warning wave 3A left for days 02,
07, 09 and 11 — after both batches, **eight of the first twenty-one concepts have five words or less
of headroom.**

---

## Per day

### Day 12 — `rubrics.md#interjection` — 195 words — FIX-3.11 (a), (b), (c)

**Anchors now taught, quoted from `rubrics.md`.**

- 3: "The critical instruction is marked, but the marker sits **inline in a paragraph with other
  instructions rather than on a line of its own**."
- 4: "The must-not-fail instruction is marked and stands alone rather than sitting mid-paragraph, but
  **competes with one other marked item**."
- 5: "**Exactly one marker in the prompt**, on the instruction the writer names as highest-stakes,
  standing alone as its own line."

**(a) `:7` — position.** "Position matters as much as the word." deleted. The mid-paragraph clause
("buried mid-paragraph, it still competes for attention") is kept, because that is anchor 3's own
distinction and is still scored; the third sentence FIX-1.10 cites — "Standing alone, the same
sentence becomes the hardest thing to have missed" — is kept **verbatim**, as the entry requires.
Nothing in the concept now claims that *where in the prompt* the marked line sits carries weight.

**(b) `:9` — the way-station sentence.** The Working tier (`:35`) mandates two marked instructions.
The concept now presents that state as a scored rung:

> Marked inline among its neighbours is where this starts; **standing alone but competing with one
> other marked item is the climb from there**; exactly one marker, on the instruction whose failure
> you'd actually be angry about, is what makes the word mean something.

Three rungs, in anchor order, quoting anchor 4's "competes with one other marked item" and anchor 5's
"exactly one marker" rather than paraphrasing them. "If everything is IMPORTANT, nothing is" is kept
— it is anchors 1–2, genuinely below the Novice rung — but it no longer frames the two-marker state,
which is what made a Working learner hear their own instruction called a failure mode.

**(c) `:11` — the self-test.** Now the two countable properties and nothing else:

> Here is the test: count the markers in your prompt, and ask whether the one you'd be angriest to
> see ignored stands alone on its own line.

"Move it or mark it" is gone (it instructed the opposite of the Novice tier's "not moved"), and so is
"could a skimming reader still miss it" — the unfalsifiable outcome test FIX-1.11 removed from anchor
5.

**Before / After.** `:17`, `:21`, `:23` **unchanged**, as FIX-3.11 and checkpoint item 7 require.

### Day 13 — `rubrics.md#particle` — 194 words — FIX-3.21(f)

**Anchors now taught.**

- 3: "The phrasal verb is **close to right**, but a stricter synonym would remove a small remaining
  ambiguity."
- 4: "Each phrasal verb present was **chosen deliberately**, but at least one could be swapped for a
  plain verb without changing the task."
- 5: "Each phrasal verb present is load-bearing and **no plain verb would have served** — swapping any
  particle changes the task."

**Way-station** (Novice `:31` mandates "the phrasal verb you'd reach for by habit rather than one
whose particle you've chosen deliberately — close to right, with a small ambiguity a stricter synonym
would remove"):

> **Close to right, with a small ambiguity a stricter synonym would remove, is a rung of its own.**
> Choosing the particle deliberately, so swapping it changes the task, is the climb from there; a
> phrasal verb no plain verb would have served is the top.

That is the rung the Novice tier occupies, stated in anchor 3's own words, where the line previously
read "A particle earns its place **only if** changing it would change the task" — anchor 4's
deliberateness as a universal gate, taught aloud to a tier capped at 3.

`:11` now runs both swaps, because anchor 5 is conjunctive and the particle swap alone only reaches 4:

> Here is the test: swap the particle for a plausible alternative, then swap the whole phrasal verb
> for a plain verb. Two changed tasks mean it is load-bearing; if the plain verb serves just as well,
> use it.

**Before / After.** Unchanged. Floor "unchanged" (FIX-3.21's preamble) holds. The tracking note filed
with (f) — that `days/13.md:21` is itself a `particle` anchor-4 prompt — was **not** acted on, as that
entry directs; it remains open in the plan.

### Day 15 — `rubrics.md#role-framing` — 197 words — FIX-3.07 (a) and (b), under FIX-3.14

**Anchors now taught.**

- 3: "The role implies a standard or a body of knowledge, but the prompt doesn't say which parts to
  draw on."
- 4: "**The role text names at least one thing** the output includes, excludes **or** assumes because
  of the role, **but not how the role produces it**."
- 5: "The role text names what the output includes, excludes **and** assumes because of the role, and
  **says how the role produces each**."

**Way-station and three rungs**, at `:11`. The Working tier (`:35`) legitimately names **one**, not
three — anchor 4 is disjunctive and at-least-one, which is FIX-3.14's correction to checkpoint item 6:

> Here is the test: read your role text and ask what it names. A stance that names nothing is where
> this starts; **one thing the output includes, excludes, or assumes — named in the prompt, not left
> to inference — is a rung of its own**; all three, plus how the role produces each, is the top.

This is a **text** property, per FIX-3.14's "Re-aim it at the text property the rubric now scores".
The old test counted things the *output contains*, which anchor 4 stopped measuring after FIX-1.13,
and demanded two of them, which matches no rung at all.

Tiers `:31`, `:35`, `:39` **not touched** — FIX-3.14 is explicit that all three are settled.

**Before / After — edited. Floor and re-derivation below.**

### Day 16 — `rubrics.md#few-shot-examples` — 190 words — FIX-3.08, plus one concept edit no entry files

**Anchors now taught.**

- 3: "Examples show variety, but **none demonstrates a boundary or a near-miss**."
- 4: "Examples cover the boundary case but not a genuine failure case."
- 5: "Examples cover the boundary case **and** the failure case."

**Way-station** (Novice `:34` mandates "both ordinary cases, **neither one you'd hesitate over
yourself**"), at `:11`:

> **Two examples that show variety but no edge is a rung of its own**; a boundary case is the climb
> from there; the boundary case and the failure case together is the top.

and "Anything softer is padding." was deleted from `:9`. See departure 3 for why this edit was made
at all — it is the FIX-3.11(b) collision class on a day no entry lists.

**Before / After — edited. Floor and re-derivation below.**

### Day 18 — `rubrics.md#task-decomposition` — 184 words — FIX-3.12

**Anchors now taught.**

- 3: "Tasks are split into steps, but one step's output isn't a clean input to the next."
- 4: "Work split so each step has one output, and the next step's input is the previous step's output
  **plus exactly one added instruction or re-explanation**."
- 5: "…each step's input is **verbatim** the previous step's output — nothing added, nothing
  re-explained."

**Way-station** (Working `:45` mandates "the previous step's output **plus exactly one line of added
instruction**"), at `:11`:

> Here is the test: cut a chained prompt of yours at every "and then," and read what crosses each
> seam. A paraphrase at the seam is a rung of its own; **the last step's output plus exactly one added
> line of instruction is the climb from there**; that output verbatim — nothing added, nothing
> re-explained — is the top.

`:7`'s absolute — "Splitting into three prompts **only fixes this if** each step's input is exactly
the last step's output" — became "Splitting into three prompts fixes this only as far as the seams
are clean." The verbatim language FIX-1.16 homed here is kept, at the top of the ladder, per
FIX-3.12's instruction.

`:9`'s "check that what crosses it is an output, **not a summary of one**" became "ask what crosses it
— the last step's output, or a summary of one" (departure 5): the verdict form condemned the Novice
tier's mandated paraphrase in the tier's own word.

**Before / After.** `:15-33` **unchanged**, as FIX-3.12 requires.

### Day 19 — `rubrics.md#reasoning-scaffolds` — 196 words — FIX-3.09 (gloss + round-2 `:9` amendment) and FIX-3.21(g)

**Anchors now taught.**

- 3: "Some intermediate steps are named, but **one that the task actually depends on is missing**."
- 4: "The reasoning steps asked for match the ones the task requires, **but the prompt does not fix
  the order they are produced in**."
- 5: "…**in the order the task requires them produced**."

**Checkpoint item 11 — gating is no longer called secondary.** `:9` closed on "Naming steps can also
gate the answer on them — useful, but **secondary to getting the list right**." It now reads:

> **Getting the list right comes first; gating the answer on the order they are produced in is what
> separates a complete scaffold from a finished one.**

The set-match keeps its primacy (anchors 3→4 turn on it), and ordering is named as the discriminator
it became after FIX-1.17 — which is what the Advanced tier at `:39` demands.

**Way-station** (Novice `:31` mandates "two or three only … so **at least one thing it depends on
goes unnamed**"), at `:11`:

> **Two or three named with one dependency left off is a rung of its own**; every item named and
> nothing else is the climb; the order they must be produced in is the top.

**Before / After.** The **After prompt at `:21` is untouched** and keeps its ordering "then" — the
floor FIX-3.21 names for day 19. Only the gloss at `:23` moved, taking FIX-3.09's replacement text
verbatim.

### Day 21 — `rubrics.md#context-ordering` — 196 words — FIX-3.10 and FIX-3.13 (a), (b)

**Anchors now taught.**

- 3: "Instruction is findable, but **constraints are scattered** rather than grouped at the end."
- 4: "Task first, material second, with constraints grouped last **except for one placed early**."
- 5: "Task first, material second, **constraints grouped last**."

**(a) Way-station** (Working `:39` mandates "**leaving exactly one constraint where it currently sits
mid-material**"), at `:11`:

> Here is the test: is the instruction the first thing read, and where does each constraint sit?
> Constraints scattered through the material is where this starts; **all but one grouped at the end is
> the climb from there**; every one grouped last is the top.

`:7` now says "constraints **grouped** last" in both places, quoting anchor 5's exact phrase where it
previously said only "constraints last".

**(b) The prediction test is re-homed, declared unscored in day 23's exact form** — `days/23.md:9`
reads "a useful habit, not a scored one":

> Predicting what the reordered version changes about the output is a useful habit, not a scored one.

This satisfies checkpoint item 9's first branch. The dynamic test is no longer presented as the day's
scored test, which is A11 / FIX-3.10's whole complaint.

`:9` is untouched, per FIX-3.10's closing note.

**Before / After.** Unchanged.

---

## Before / After edits — floors and re-derived imitate-the-After

Three days in range have a `## Before / After` hunk: 15, 16 and 19. Each derivation below is run
against the **new** text, and each names the copy routes the Novice tier forecloses, including the
trailing free-form route by name.

### Day 19 — the only sanctioned exception the brief names

**Floor (FIX-3.21's preamble):** "the After prompt at `:21` must keep its ordering clause — the
'then' between the assumption list and the confirmation pass."

**Held, trivially: the After prompt was not edited.** `:21` still reads "list the assumptions the
answer would depend on that aren't stated in the material, **then** check each against what's
actually given." Only the gloss at `:23` changed, and the gloss is not the scored artifact.

**Imitate-the-After, re-run.** Novice `:31`: "…naming two or three specific things the answer depends
on in place of 'step by step' — **two or three only, even if the answer depends on more, so at least
one thing it depends on goes unnamed** — and send the rewritten version."

- **Copy the whole After.** It names exactly the intermediates *its* task depends on and leaves
  nothing unnamed, which the tier forbids by mandate. Non-compliant.
- **Anchor transfer fails independently.** `reasoning-scaffolds` is the one rubric whose anchors are
  defined relative to the task at hand ("the ones **the task** requires"), so the After's pair
  transplanted onto a different `{{TASK}}` is a 3, not a 5. The new gloss now says exactly this in the
  file ("A ranking task would name its comparison criteria instead").
- **Trailing free-form route.** Day 19's Novice has no fill-in template — it is free composition —
  and the foreclosure is a hard count ("two or three **only**"), so there is no tail into which a
  fourth intermediate or an ordering clause can be smuggled without breaking the count. This is the
  route days 05 and 09 leaked through; it is closed here by the numeral, not by inspection of the
  tier.

**Result: imitator 3, unchanged from `wave2d-sweep.md`.** Ladder 3 / 4-or-5 / 5 intact.

### Day 15 — mandated by FIX-3.07(b); no floor named by any entry

FIX-3.21's floor list covers days 1, 2, 5, 6, 8, 9, 11, 13 and 19 only, and day 15 is not among them
— FIX-3.21 never applied to it. The operative constraint is therefore checkpoint item 18 as
reconciled: **the edit may not change the anchor day 15's wave-2D derivation is measured against**,
which is `wave2d-sweep.md`'s "Day 15 — `rubrics.md#role-framing`. Imitator: **3**."

**New After (`:21`):**

> Answer as a reviewer who has to sign off on {{TASK}} and will be paged if it breaks. Sign-off puts
> your name on it, so flag anything you wouldn't want attached to you; the page comes to you, so call
> out any assumption you can't verify from what's given; and skip style commentary — it isn't what
> gets you paged.

**Re-scored (checkpoint item 3):** `role-framing` **5**. It names an inclusion (flag the issues), an
exclusion (skip style commentary) and an assumption (call out the unverifiable ones), and it says how
the role produces each — the sign-off puts your name on it, the page comes to you, style never pages
anyone. Before this batch it was **4**: it named no exclusion and no mechanism. See departure 2 for
why the plan's literal replacement stops at 4.

**Imitate-the-After, re-run against the new After.** Novice `:31`: "Write a role for {{TASK}} that has
a concrete stake … and send the completed prompt **without saying anywhere in it what the output
should include, exclude, or assume differently**."

- **Copy the whole After.** All three effect clauses say, in the prompt, what the output should
  include, exclude and assume. Forbidden by name — the tier negates anchor 4's positive content in
  anchor 4's own vocabulary.
- **Copy one clause only** — e.g. "so flag anything you wouldn't want attached to you". Still names an
  inclusion. Forbidden by the same clause.
- **Copy the stake sentence alone** ("Answer as a reviewer who has to sign off on {{TASK}} and will be
  paged if it breaks"). This *is* compliant, and it is anchor **3** word for word: "The role implies a
  standard or a body of knowledge, but the prompt doesn't say which parts to draw on." That is the
  rung, reached by the only copy route the tier leaves open.
- **Trailing free-form route.** Day 15's Novice is free composition with no template blank, so the
  whole prompt is the tail. The foreclosure is scoped to the whole prompt — "**anywhere in it**" — not
  to a slot, which is precisely what closes it. Pasting the After's tail after a compliant stake
  sentence lands the forbidden text *anywhere in it*.
- **Effort gradient.** Composing one stake sentence costs less than copying four clauses and then
  deleting three of them. Points the right way.

**Result: imitator 3, unchanged.** The anchor the derivation is measured against did not move; the
After rose 4 → 5 on the rubric it demonstrates, which is a strengthening on the Advanced side only.
Ladder 3 / 4 / 5 intact.

### Day 16 — mandated by FIX-3.08; no floor named by any entry

Measured against `wave2d-sweep.md`'s "Day 16 — `rubrics.md#few-shot-examples`. Imitator: **3**."

**New boundary case (`:23`):** "latency crept from 200ms to 3s over an hour, no alert fired, no user
report. Urgent — no threshold crossed yet, but the trend crosses one within the day." FIX-3.08's text
verbatim. Failure case at `:24` unchanged, as the entry requires.

**Re-scored:** `few-shot-examples` **5**, before and after — "Examples cover the boundary case and the
failure case." Both are present in both versions; what changed is that they now *disagree*, which is
the day's headline property and its Working tier's demand, not an anchor.

**Imitate-the-After, re-run against the new After.** Novice `:34`: "…add two examples that show
different kinds of item — **both ordinary cases, neither one you'd hesitate over yourself** — each
with a one-line reason."

- **Copy both examples.** The boundary case is now, by construction, one you would hesitate over: the
  verdict is *urgent* on a case where nothing has crossed a threshold. Forbidden by name. The edit
  **strengthens** this route rather than weakening it — the old boundary case returned the same
  verdict as the failure case ("Not urgent"), so a copier could argue neither was a hesitation case.
- **Copy the failure case alone.** It is a near-miss ("looks like a match on tone alone but isn't"),
  also a hesitation case, and one example is anchor 2 — below the rung, not above it. Foreclosed
  twice over.
- **Copy the labels, invent the content.** The compliant result is two ordinary cases with one-line
  reasons: anchor **3** word for word, "Examples show variety, but none demonstrates a boundary or a
  near-miss."
- **Trailing free-form route.** Day 16's Novice is free composition with no template blank, and the
  foreclosure is quantified over every example the learner writes — "**both** ordinary cases" — so
  there is no tail in which a third, borderline example can be smuggled without violating "both".
- **Effort gradient.** Two ordinary examples from the learner's own task cost less than transplanting
  a latency example onto an unrelated `{{TASK}}` and rewriting its verdict. Points the right way.

**Result: imitator 3, unchanged.** Ladder 3 / 4 / 5 intact.

---

## FIX-2.21(b) / wave-3 checkpoint item 10 — ruling

**Closed as ACCEPTED. FIX-2.21(b) is rejected. `days/21.md:47` keeps its single rubric citation, and
the review-day gap is recorded, not left silent.** The ruling is written into
`MASTER-FIX-PLAN.md` under FIX-3.13 — not only here — because a ruling that lives in a batch report is
the project's recorded failure mode.

Three reasons, in order of weight.

1. **Naming four rubrics would score work no tier asks for.** `days/21.md:31` builds the *material*
   around the learner's three weakest levers — an unresolved "it", a quantity buried in prose, an
   unstated fallback. Every tier then demands a **pure reorder**: Novice moves the instruction
   "leaving every constraint exactly where it falls"; Working and Advanced both say "**without
   deleting a word**". A learner who obeys their tier cannot repair any of the three levers. Scoring
   `#pronoun`, `#numeral` and `#conjunction` would grade a defect the exercise planted and then
   forbade them to fix — a worse outcome than the gap.
2. **Restoring the lever work to Advanced re-opens a settled ladder.** Wave 2B removed it under rule 7
   and wave 2D re-derived day 21 at 3 / 4 / 5 with imitator 3. It is also barred to this batch by
   charter: `## Exercise` tiers are wave 2's and are not to be touched. And SYS-2 forbids an Advanced
   tier whose added demand is not the cited rubric's own 4→5 discriminator, which for
   `context-ordering` is "constraints grouped last", not lever repair.
3. **The lever-targeted material earns its place unscored**, exactly as day 23's
   condition-before-tools habit does: it makes the reorder concrete and surfaces the learner's weak
   levers for the day-28 review without pretending to be graded.

**One residue, filed rather than left in this report: FIX-5.09** — `days/21.md:31` does not *say* the
lever work is unscored, so a tutor reading it aloud may imply a grade `:47` does not give. That is a
prose fix in day 23's established form ("a useful habit, not a scored one"), not a tier change, and it
is all that remains of T19 / A12 / S13. The entry carries the text, the constraints (no tier edit, no
extra rubric at `:47`), and day 21's post-batch concept count.

---

## Filed into `MASTER-FIX-PLAN.md` (lesson 5 — nothing a later wave must act on is left here)

| Location | What was filed |
|---|---|
| **FIX-5.09** (new, wave 5) | Day 21 `:31` unscored-lever disclaimer — the residue of the FIX-2.21(b) ruling. Carries replacement text and the do-not-touch constraints. |
| **FIX-3.13** | The FIX-2.21(b) / checkpoint-item-10 ruling in full, with its three reasons; plus a landed-as note for `:7` and `:11` and the unfiled `:5` cut. |
| **FIX-3.07** | Both departures: why (a)'s literal text was not used (FIX-3.14 supersedes it) and why (b)'s After was carried to anchor 5. Marked do-not-restore. |
| **FIX-3.08** | The day-16 **concept** edit that no entry files, with the collision derivation and an explicit "do not restore either sentence"; plus the `:26` punctuation departure. Confirms FIX-5.05's replacement text is still applicable. |
| **FIX-3.09** | Landed-as note for `:9`, `:23` and the unfiled `:7` deletion that paid for them; confirms the After's ordering "then" is intact. |
| **FIX-3.11** | Landed-as note for (a), (b), (c), recording that `:17,:21,:23` are unchanged. |
| **FIX-3.12** | Landed-as note for `:7` and `:11`, plus the unfiled `:9` softening and why it was needed. |
| **FIX-3.21(f)** | Landed-as note for day 13's `:9` and `:11` and the two unfiled `:7` cuts; records that the day-13 After tracking note was **not** acted on. |

**Nothing found stale in wave 4 or wave 5.** FIX-5.01's table covers days 01–06 only and is
unaffected. FIX-5.05 rewrites `days/16.md:19-24` and its replacement text **already carries** FIX-3.08's
corrected boundary case, so it is still applicable verbatim; checked in the file rather than assumed.
FIX-5.07 remains the last edit to the repository.

---

## Departures from the plan's literal text

Seven. Five substantive.

**1. FIX-3.07(a)'s literal replacement was not used — substantive, and required by FIX-3.14.** The
plan's text is "list one thing the output **contains** because of it, one thing it leaves out, and one
thing it assumes. **If you can't fill all three, the role is decoration.**" Two defects against the
settled anchors. It is still an *output-effect* test, where anchor 4 after FIX-1.13 measures what the
**role text names**; and it condemns anything short of three, which is the state the settled Working
tier mandates, because anchor 4 is disjunctive and at-least-one. FIX-3.14 says so explicitly ("Re-aim
it at the text property the rubric now scores") and amends checkpoint item 6 to match. Landed instead
as the three-rung text-property ladder quoted under day 15.

**2. FIX-3.07(b)'s After was carried past the plan's replacement text, to anchor 5 — substantive.**
The plan's version adds the exclusion but names the mechanism for none of the three dimensions, so it
lands at anchor **4** — "names at least one thing … **but not how the role produces it**". Checkpoint
item 3 requires every edited After to score **5**, and FIX-3.14 makes it "load-bearing rather than
cosmetic" that this After demonstrate anchor 5, since day 15's Advanced tier demands the mechanism and
no worked example showed it. The plan contradicts itself here, the same way FIX-3.02(a) did for wave
3A (its departure 2). Resolved by attaching the mechanism to each of the three clauses; FIX-3.07(b)'s
own exclusion wording ("skip style commentary — it isn't what gets you paged") is kept intact. The
imitator result is unchanged at 3, derived above.

**3. `days/16.md:9` and `:11` were edited — substantive, filed by no entry.** FIX-3.08 is a
`## Before / After` entry only. But day 16 carries the FIX-3.11(b) collision in full: the Novice tier
(`:34`) mandates "both ordinary cases, neither one you'd hesitate over yourself" — `few-shot-examples`
anchor 3 — while `:9` called exactly that state padding ("**Anything softer is padding**") and `:11`
required each example to earn its place by disagreeing with the other. `SKILL.md:28` reads both aloud
immediately before the tier. Day 16 appears on no FIX-3.21 sub-item only because its foreclosure clause
came from wave 2B rather than wave 2D, so wave 2D never re-read its concept — an accident of batch
boundaries, not a finding that the day is clean. Wave 3A took the identical departure on `days/04.md:11`
(its departure 3). Fixed here rather than filed, because wave 3 is the concepts wave and deferring a
concept fix to wave 4 or 5 is strictly worse. Recorded in the plan under FIX-3.08 as do-not-restore.

**4. FIX-3.10's closing clause was dropped — substantive.** The entry's replacement ends "If a
constraint sits mid-material, move it." Under the settled ladder that instructs a Working learner to
undo the one constraint their own tier mandates they leave mid-material (`:39`). The ladder sentence
that replaces it covers the same ground and scores it correctly at three rungs. The rest of FIX-3.10's
text — "is the instruction the first thing read, and where does each constraint sit" — is kept.

**5. `days/18.md:9` was softened — substantive, filed by no entry.** FIX-3.12 names `:7` and `:11`.
But `:9`'s "check that what crosses it is an output, **not a summary of one**" condemns the Novice
tier's mandated paraphrase in the tier's own word ("summarised in your own words"), which is the same
collision FIX-3.12 exists to fix, one sentence away from the two it lists. Changed to the diagnostic
form — "ask what crosses it — the last step's output, or a summary of one" — at a cost of one word.

**6. Five unfiled cuts paid for the additions inside the 200-word cap — non-substantive.** Recorded
because the standing convention is to record every deviation. None removes an anchor reference or a
worked example.

| Day | Cut | Words | Why it was the cheapest loss |
|---|---|---|---|
| 13 `:7` | "look up / look over," from the pair list | 5 | `:5` contrasts that exact pair in full, three lines above |
| 13 `:7` | "'Look over each external call' doesn't signal a check against documentation; 'look up' does." | 14 | the gloss at `:23` makes the same point about the same sentence, two lines below |
| 19 `:7` | "The steps come from what the task needs, not from what makes reasoning look thorough." | 15 | restates `:7`'s own opening sentence; the task-relative point also lands in the new `:23` gloss and in `:11`'s opening instruction |
| 19 `:9` | "The hard part, and the scored part, is the match" → "The scored part is the match" | 4 | pure tightening |
| 21 `:5` | "Everything gets equal attention on the first pass, because nothing has said yet what to look for." | 17 | restates `:5`'s first sentence ("reads the whole block without knowing what it's for") |

Day 15 also lost `:9`'s opening clause ("If you can't say what changes, the role changes nothing —",
11 words), which is listed separately because it is not purely a budget cut: it was the sentence
closest to reading as a verdict on a prompt whose role text names nothing, which is what the Novice
tier mandates.

**7. `days/16.md:26`'s gloss was split into two sentences — non-substantive.** FIX-3.08's instruction
implies keeping the semicolon join, but the replacement clause itself carries an em-dash pair, and
three clause-separators in one sentence read badly aloud — `SKILL.md:28` reads it verbatim. The
wording is otherwise the entry's, including the italicised *match*.

### The rung idiom, applied

No concept in these ten days names a tier, per wave 3A's departure 5 and `SKILL.md:30`'s one-tier
rule. Where the ladder allowed three rungs, three were named: days 12, 13, 15, 16, 18, 19 and 21 all
carry a three-rung sentence. Day 19's `:9` additionally carries a two-rung ordering statement, because
the third rung there is `:11`'s.

## Nothing was stopped on

Every filed entry in range was executed. Day 17 was read and left alone: FIX-3.15's two preservation
conditions hold in the file — `:7`'s "shows what an empty value looks like" is still a description of
the goal, and the `"note": ""` example is not coupled to the Working tier — and no defect was found
that would have required filing.
