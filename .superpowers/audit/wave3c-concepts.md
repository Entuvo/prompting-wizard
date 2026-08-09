# Wave 3, batch C — concepts, days 22–30

Scope executed: FIX-3.16 (day 22, all three sentences), FIX-3.17 (day 24), FIX-3.18 (day 26),
FIX-3.19 (day 30), FIX-3.20 (day 27 — the mandated `:21` half and the tracking `:9` half), and
FIX-3.22's day-28 confirmation.

Out of range and untouched: days 01–21 (batches A and B), `rubrics.md`, `SKILL.md`, `assessment.md`,
`tools/`. Days 23, 25 and 29 had no tier change and no entry names them; 23 and 25 were not opened,
day 29's `:9` was read only as the self-cap *shape* FIX-3.18 points at. Day 28 was read in full and
**not edited** — verdict below.

Every anchor quoted below is read from `prompting-wizard/rubrics.md` by text, never by line number.
Every word count is recomputed with `validate.py`'s own `section(text, '## Concept')` plus
`len(str.split())` — no arithmetic-only figures, per lesson 3.

---

## Verification

| Check | Result |
|---|---|
| `python3 tools/validate.py --complete` | `ok`, exit 0 |
| `python3 -m unittest discover -s tools` | 103 tests, OK (no test file touched) |
| `## ` / `### ` headings | none touched (`git diff -U0 -- prompting-wizard/days \| grep '^[+-]#'` → empty) |
| `## Exercise` tier bodies | **none touched** — every day-file hunk is at line 5, 7, 9 or 11 (`## Concept`), plus `days/27.md:21` |
| `## Rubric`, `## Completion` | none touched |
| `## Before / After` | **`days/27.md:21` only** — mandated by FIX-3.20's round-2 re-grade and by checkpoint item 17. Days 22 (`:15-29`), 24 (`:15-23`), 26 (`:15-23`) and 30 (`:15-21`) **unchanged**, per checkpoint items 13, 14, 15, 16 |
| `days/28.md:11` | **not edited** (CONFLICT-07, checkpoint item 5) — verified in file and by empty `git diff -- days/28.md` |
| `days/14.md:9` | **not edited** (CONFLICT-03, checkpoint item 5) — verified the same way |
| `rubrics.md`, `SKILL.md`, `assessment.md`, `tools/`, days 01–21, 23, 25, 28, 29 | untouched |
| `## Concept` 200-word cap | max in range is **192** (days 22 and 26) |

```
 prompting-wizard/days/22.md | 8 ++++----
 prompting-wizard/days/24.md | 4 ++--
 prompting-wizard/days/26.md | 6 +++---
 prompting-wizard/days/27.md | 4 ++--
 prompting-wizard/days/30.md | 6 +++---
 5 files changed, 14 insertions(+), 14 deletions(-)
```

`MASTER-FIX-PLAN.md` also changed — the landed-as notes, the day-28 verdict and the FIX-3.22
amendment required by lesson 5. It is not a day file and is listed separately in the commit.

## Concept word counts (cap 200), recounted

| Day | Before | After | Headroom | Edited |
|---|---|---|---|---|
| 22 | 176 | **192** | 8 | yes |
| 23 | 172 | 172 | 28 | no |
| 24 | 179 | **189** | 11 | yes |
| 25 | 179 | 179 | 21 | no |
| 26 | 179 | **192** | 8 | yes |
| 27 | 177 | **174** | 26 | yes (net −3) |
| 28 | 181 | 181 | 19 | **no — verdict below** |
| 29 | 181 | 181 | 19 | no |
| 30 | 184 | **191** | 9 | yes |

Days 22 and 26 now sit 8 words under the cap and day 30 sits 9 under. Adding to any of the three
requires deleting first.

**Recounted across all thirty concepts, not asserted from the batch reports: sixteen of thirty now
have ten words or less of headroom** — days 02 (199), 15 (198), 07 / 09 / 11 (197), 19 / 21 (196),
05 / 12 (195), 13 (194), 22 / 26 (192), 16 (191), 30 (191), 04 / 06 (190). Day 02 has **one** word
and day 15 has **two**. Wave 4 and wave 5 must budget a deletion for any addition to those sixteen;
FIX-5.01's day-03 and day-06 rows are still affordable (163 and 190, costing zero and one), and that
was checked in the file.

---

## Per day

### Day 22 — `rubrics.md#system-prompts` — 192 words — FIX-3.16, all three sentences

**Anchors now taught, quoted from `rubrics.md`.**

- 3: "Standing behaviour and per-turn request are separated into two blocks, but **two or more lines
  are on the wrong side — in either direction**."
- 4: "…and **exactly one line is on the wrong side — in either direction**."
- 5: "…and **no line is on the wrong side — in either direction**."

**The rung sentence** — the Working tier (`:41`) *mandates* anchor 4's shortfall ("leave **exactly
one** rule that would still be true on a future turn sitting in the per-turn ask"), and the Novice
tier (`:37`) mandates anchor 3's, so three rungs are named. `:9` is now, in full:

> **The rubric counts lines on the wrong side, in either direction: two or more is where this starts;
> exactly one is the climb from there; no line on the wrong side is the top.**

It replaces "Leakage runs both ways: a durable rule restated every turn is redundant, and a
turn-specific detail promoted into the system prompt is **a landmine for the next request**" — the
sentence the rebuilt Novice tier has every bottom-tier learner violate deliberately and twice, read
aloud by `SKILL.md:28` immediately before that tier. The unit is **lines**, not details, because
that is the unit all three anchors count and because wave 2C's round 2 rebuilt `days/22.md:37` on
exactly that distinction.

**`:7`** — the Working tier's mandated state is no longer an instruction against itself. "**Move** a
durable rule into the per-turn slot **and you retype it forever**; **leave** a turn-specific detail in
the system prompt and it silently governs…" became "**A durable rule left in the per-turn slot gets
retyped forever; a turn-specific detail left in the system prompt silently governs requests it was
never written for.**" Both consequences survive; neither is now a prohibition on a state the ladder
scores.

**`:11`** — the second direction was **added**, not disclaimed. The entry offers either; the added
form was chosen because the rebuilt Advanced tier (`:45`) now runs both moves ("if a line repeats in
all three asks, move it up into the system prompt"), so a one-directional test would no longer match
the tier it is the test for:

> Here is the test: read your system prompt line by line and ask, would this be false on some future
> turn? If yes, it belongs in the per-turn ask. **Then the other way: a line you would retype next
> turn belongs in the system prompt.**

**Before / After.** `:15-29` **unchanged**, per FIX-3.16 and checkpoint item 13.

### Day 24 — `rubrics.md#self-critique-loops` — 189 words — FIX-3.17

**Anchors now taught.**

- 3: "A concrete check is named, but **there's no stated action for when it fails**."
- 4: "A check the model can apply to its own output is given, with **an action on failure that names
  no operation ("fix it", "try again")**."
- 5: "…with an action on failure that **names what to do to the failing element**."

**The rung sentence** — the Working tier (`:35`) *mandates* anchor 4's shortfall ("'fix it' or 'try
again', **without naming what to do to the failing element**") and the Novice tier (`:31`) mandates
anchor 3's ("the check only, with nothing said about what to do if it fails"), so three rungs are
named. `:9` is now, in full:

> **A named check with no stated action when it fails is a rung of its own**: the model finds the
> problem and reports it anyway, unfixed. **An action that names no operation — "fix it", "try
> again" — is the climb from there**; "replace it, or flag it as unverified" **names what to do to
> the failing element**, and that is the top.

It replaces "**The loop isn't finished until it says what to do when the check fails.** … without
that line the model finds the problem and reports it anyway, unfixed" — which called both of the two
lower rungs an unfinished loop. Anchor 4 is quoted in the anchor's own two examples; anchor 5 in its
own clause.

**`:11` untouched**, as FIX-3.17 requires — it is a bar on the *check*, not on the action, and is
correct at every rung. **Before / After `:15-23` unchanged**, per checkpoint item 14.

### Day 26 — `rubrics.md#token-economy` — 192 words — FIX-3.18

**Anchors now taught.**

- 3: "Most padding is removed, but **one section is included "just in case"** rather than because the
  task needs it."
- 4: "**Every included token earns its place on inspection**, but the cuts have not been tested
  against the output to confirm accuracy held."
- 5: "Every included token earns its place, and **the cut version was rerun and the output held**."

**The rung sentence** — the Working tier (`:35`) *mandates* anchor 4's shortfall ("Make every cut by
inspection alone: **do not run the two versions and compare**") and the Novice tier (`:31`) mandates
anchor 3's ("**keep the one section you're least sure about**"), so three rungs are named. `:9` now
opens:

> **A section kept "just in case" is a rung of its own. Every token left earning its place on
> inspection is the climb from there; the rerun that confirms the output held is the top.**

It replaces "**The test is the cut, not the eyeballing.**" — the sentence that calls the Working
tier's mandated method a non-test. `:7` is kept, as the entry requires: "Delete a section, rerun, and
compare" now reads as what the top rung buys rather than as the universal method, because `:9` says
so four words in.

`:11` stays pointed at the rerun, as the entry directs, and now says which rung that is: "Whatever
changed tells you what the missing third was doing **— the evidence the top rung asks for.**" See
departure 1.

**Before / After `:15-23` unchanged**, per checkpoint item 15.

### Day 27 — `rubrics.md#failure-diagnosis` — 174 words — FIX-3.20, both halves

**Anchors now taught (unchanged by this batch, and deliberately so).**

- 3: "A lever or technique is named as the cause, but the fix doesn't actually target it."
- 4: "The failing lever or technique is identified by name and the fix changes it, but **it also
  changes a second lever or technique that was not implicated**."
- 5: "The failing lever or technique is identified by name and the fix **targets it and nothing
  else**."

**No rung sentence is added, and that is correct.** Day 27's Working tier leaves anchor 4's shortfall
**silent**, not mandated — wave 2C's ruling, on the ground that instructing a learner to damage a
second lever teaches the opposite of the day. Lesson 1's three-rung form applies where the Working
tier *mandates* the shortfall; here it does not, and `:9`'s "The fix has to target **only** what you
named" stays as a description of the target. **Checkpoint item 17's tracking half is confirmed: that
sentence is unchanged and was not turned into a tier-level demand.**

**`:21` — the mandated edit.** See the Before / After section below.

**`:9` — one unfiled edit, departure 2.** Its closing sentence instructed every learner to predict the
fix, which the Novice tier forbids outright.

### Day 28 — `rubrics.md#prompt-library` — 181 words — **FIX-3.22 verdict: CLEAN, no edit**

The verdict and its evidence are recorded in `MASTER-FIX-PLAN.md` under FIX-3.22, not only here.

**Anchors.**

- 3: "**Saved prompts mark their variable slots, but don't record how they've failed before**."
- 4: "Reusable prompts stored with their slots and at least one failure mode recorded, but **not
  specifically enough for a stranger to recognise it** before running the prompt."
- 5: "…recorded **specifically enough that a stranger would recognise each one** before running the
  prompt."

**Does `days/28.md:9` genuinely supply the rung its Novice tier needs? Yes.** The Novice tier (`:34`)
mandates "every variable part marked as a named slot — **the slots only, nothing yet about how it has
failed**", which is anchor 3 word for word. `:9` opens on exactly that state and scores it as a
position rather than an error:

> **Marking the slot without the failure gets you partway**: a template a stranger could reuse, but
> one still liable to fail the same silent way. The failure note turns reusable into reliable —
> **specific enough that reading it once prevents a repeat**.

"gets you partway" is the rung idiom in the course's own vocabulary, and the second sentence names
what the climb adds in anchor 5's own terms. A compliant Novice hears their mandated state called
*partway* — which is what it is — and not a mistake.

**Two rungs, not three, and that is correct here.** Day 28's Working tier leaves anchor 4's shortfall
**silent** (privative — mandating vagueness is not available), so there is no mandated middle state
for the concept to legitimise and a precise learner may reach 5 from Working. Lesson 1's three-rung
requirement is conditioned on the Working tier mandating the shortfall; it does not.

**`:7` checked too.** "A saved prompt **stays low on the shelf** until two more things are marked" is
positional and comparative, quantified over the whole ladder. It never calls slots-only wrong. Same
form as day 20's `:9`, which FIX-3.22 already ruled clean.

**`:11` untouched** — CONFLICT-07 and checkpoint item 5. A compliant Novice answers "no" to its
second half; that locates them on the ladder rather than condemning them, which is precisely the
ruling CONFLICT-07 made when it dissolved A14. FIX-2.21(b) was not reopened; it remains closed as
rejected by wave 3B.

**The coverage hole is now fully closed: 16 fixed (wave 3B), 20 clean (wave 3B), 28 clean (here).**

### Day 30 — `rubrics.md#capstone` — 191 words — FIX-3.19 (graded high)

**Anchors now taught, all quoted verbatim from `rubrics.md`'s `## Capstone`.**

- 3: "Prompt is **specified and works on varied cases**, but has **no written evaluation criteria**."
- 4: "Prompt is specified, holds on varied cases, and is evaluated against written criteria, with
  **failure modes noted but not specifically enough for someone else to recognise them**."
- 5: "Prompt is specified, **holds on a case it was not designed for**, is evaluated against written
  criteria, and its failure modes are **documented specifically enough that someone else could
  recognise each one**."

**The two dead anchors are gone.** `:9` previously read the last day of the course aloud quoting
"failure modes noted but **not systematically**" and failure modes "**documented**" rather than just
noted — both deleted by FIX-1.27, neither surviving anywhere in `rubrics.md`. `:9` was **replaced,
not extended**, as the entry requires (it is the longest paragraph in the file):

> The rubric's rungs are exact. Day 29's target — "specified and works on varied cases" — sits at
> anchor 3 only because it has "no written evaluation criteria" yet. Add the criteria and note what
> breaks: anchor 4, "**failure modes noted but not specifically enough for someone else to recognise
> them**." **Anchor 5 adds a second axis** — the prompt "**holds on a case it was not designed for**"
> — and asks that its failure modes be "**documented specifically enough that someone else could
> recognise each one**."

Every quoted phrase is now in the file. The **robustness axis** FIX-1.27 carried into both rows is
named at anchor 5, where it discriminates: anchor 4 says "holds on varied cases", anchor 5 "holds on
a case it was not designed for", and that is the difference day 30's Working and Advanced tiers turn
on. "not impressionistic" was dropped from the opening sentence as part of the replacement.

**`:7` — the second collision.** The Novice tier (`:29`) forecloses anchor 4 with "**Record the
scores only; nothing about what broke gets written down at this tier**", while `:7` said "when that
case breaks something, the failure mode **gets written down**, specific enough not to relearn later"
— a universal. Now:

> …and **writing down what that case breaks, specifically enough that someone else would recognise
> it, is the top rung's addition**.

The specificity wording is anchor 5's, and the writing-down is what the ladder climbs to rather than
what every tier does.

**Before / After `:15-21` unchanged**, per FIX-3.19 and checkpoint item 16. **FIX-4.07 is unblocked**
— day 30's tier text and concept are now both settled, so `## Completion`'s "When the revised prompt
passes both" (`:45`) can be reworded by wave 4. It was **not** touched here; `## Completion` is wave
4's per FIX-2.27's blocking note, and under the rebuilt Novice tier there is still no revised prompt
and no second unfamiliar case, exactly as FIX-4.07 argues.

---

## The one `## Before / After` edit — floor and re-derived imitate-the-After

**Day 27 `:21` is the only `## Before / After` hunk in this batch, and it is mandated, not
discretionary.** FIX-3.20's round-2 re-grade files it as **Mandated**, and wave-3 checkpoint item 17
requires it to have landed. Items 13, 14, 15 and 16 declare days 22, 24, 26 and 30's blocks
unchanged, and all four are. Nothing tempted an unsanctioned After edit; the four "do not touch"
instructions and the four checkpoint items agree, and days 24, 26 and 30 were fixed entirely inside
`## Concept`.

**Floor (checkpoint item 18's principle, applied here):** the edit may not change the anchor day 27's
derivation is measured against, which is `wave2c-tiers.md`'s "**Imitate-the-After test:** … caps the
imitator at **3**."

**New After (`days/27.md:21`):**

> The learner names, in writing, which lever or technique they believe was underspecified — before
> anyone touches the prompt or runs anything. **Where the tier also asks for a fix, the change they'd
> make goes in the same writing, still before anything runs.** Only after that prediction is recorded
> does the tutor run the original prompt if it hasn't already been run, confirm what actually broke,
> and check whether the learner's diagnosis, **and any fix**, targeted the thing that was actually
> wrong.

The written prediction is kept intact — the entry forbids removing it, and it is the day's method for
the upper two tiers. **No tier is named**, per `SKILL.md:30` and wave 3A's departure 5: "the tier"
resolves to whichever single tier the learner is shown.

**Imitate-the-After, re-run against the new After.** Novice (`:29`): "Have the learner go lever by
lever through the failed prompt, out loud, until they find the one they'd bet money was
underspecified. Have them name it before anything is run, then run the failed prompt unchanged to
confirm what it produces — **no fix today**."

- **Copy the whole After.** Its first sentence is now the naming step alone, which is what the tier
  asks for. Its second is conditioned on the tier asking for a fix, and this one does not — so a
  learner following the After produces a named lever and no fix. That is anchor **3** ("A lever or
  technique is named as the cause, but the fix doesn't actually target it" — wave 2C's ruling: a
  named cause with no fix is 3). **The route that previously leaked is closed at source**: before this
  edit the After told the learner to write "what they'd change", and only "no fix today" stopped them.
- **Copy the fix clause anyway, ignoring its condition.** Forbidden by name — "no fix today" is
  absolute and is read after the After (`SKILL.md:28`, then `days/27.md:25`'s "per `## Before /
  After`", then the tier). The tier is the later and more specific instruction.
- **Trailing free-form route.** Day 27's Novice writes **no new prompt at all** — its artifact is the
  learner's existing failed prompt, run unchanged — so there is no template, no blank, and no tail
  into which a fix can be smuggled. This is the route days 05 and 09 leaked through and days 15, 16
  and 19 had to close explicitly; on day 27 it does not exist, because the day produces no composed
  artifact to append to. The only free text is the written diagnosis, and "no fix today" is quantified
  over the whole session, not over a slot.
- **Effort gradient.** Naming one lever costs less than naming one lever *and* writing a fix.
  Points the right way.

**Result: imitator 3, unchanged, and strengthened.** The anchor the derivation is measured against
did not move. Ladder 3 / 4 / 5 intact.

---

## Filed into `MASTER-FIX-PLAN.md` (lesson 5 — nothing a later wave must act on is left here)

| Location | What was filed |
|---|---|
| **FIX-3.16** | Landed-as for all three day-22 sentences, with the replaced texts marked do-not-restore and the unfiled `:5` trim. |
| **FIX-3.17** | Landed-as for day 24's `:9` ladder, do-not-restore on the old sentence, and the unfiled `:7` cut. |
| **FIX-3.18** | Landed-as for day 26, the two `:9` deletions marked do-not-restore, the unfiled `:7` cut, and the `:11` scope clause declared as a departure with its reasoning. |
| **FIX-3.19** | Landed-as for day 30's `:9` and `:7`, the unfiled `:5` cut, and confirmation that FIX-4.07 is unblocked and `## Completion` untouched. |
| **FIX-3.20** | Landed-as for `:21` with the re-derived imitator result; explicit confirmation that the `:9` tracking half holds; and the unfiled `:9` fix-prediction edit, marked do-not-restore. |
| **FIX-3.22** | **Day 28's verdict — CLEAN — with all five pieces of evidence**, the hole declared fully closed, and the standing consequence **amended**: it now covers every range, not only 01–21, because day 27 was a live instance outside it. |

**Nothing found stale in wave 4 or wave 5 by these edits.** Checked in the files rather than assumed:
FIX-5.01's normalisation table covers `days/01.md`–`06.md` only and none of its rows is in range —
the "Here is the test:" openers on days 22 and 26 are unchanged, only their tails moved. FIX-4.04
edits `days/28.md:7`, which this batch did not touch, so it remains applicable verbatim; the
sequencing note at "Wave 4 → waves 2 and 3" ("Wave 3 has no day-28 entry") is now confirmed true in
fact and not only by absence. FIX-4.05, FIX-4.07 and FIX-4.13 depend on `days/27.md:17`, `:25` and
`days/30.md:17`, `:25`, `:45`, none of which moved. FIX-5.07 remains the last edit to the repository.

---

## Departures from the plan's literal text

**Three. All substantive; each is recorded in the plan as well as here.**

**1. `days/26.md:11` gained an eight-word scope clause — FIX-3.18 files no `:11` edit.** The entry
says "`:11`'s self-test is the Advanced tier's test and should stay pointed there", which is an
instruction to leave its aim alone, not obviously an instruction to leave its text alone. It was
edited because leaving it silent leaves `SKILL.md:28` reading "Here is the test: cut a third of your
context, **rerun, and compare** outputs side by side" aloud as *the* test of the day, seconds before
a tier that says "**do not run the two versions and compare**". Checkpoint item 15 requires the
concept to say the rerun is what the top rung adds "not what every tier does", and after this edit
`:11` says it too: "— the evidence the top rung asks for." The aim is unchanged, the standard "Here
is the test:" opener is untouched, and day 26 is at 192 of 200.

**2. `days/27.md:9`'s closing sentence was edited — FIX-3.20 files only `:21` and names `:9` as
tracking-only for a different clause.** `:9` closed on "Diagnose on paper first, **predicting the
fix** before you run anything — then run to see if **the prediction** held", read aloud one paragraph
before a Novice tier that ends "**no fix today**". That is the identical collision FIX-3.20's round-2
re-grade mandated the `:21` edit for; scoping `:21` and leaving `:9` would have moved the sentence
that tells a Novice to predict the fix from the After into the concept, one paragraph earlier. Now:
"Diagnose on paper first, before you run anything — then run to see whether **the diagnosis** held."
Cost: −3 words. **The tracking clause FIX-3.20 protects — "The fix has to target only what you named"
— is untouched**, so `failure-diagnosis` anchor 4 stays open; checkpoint item 17's second half holds.
Wave 3B took the identical class of departure on `days/16.md:9`/`:11` and `days/18.md:9`, and wave 3A
on `days/04.md:11`. Filed under FIX-3.20 and under FIX-3.22, which it also amends.

**3. FIX-3.22's standing consequence was widened.** It read "Any wave editing a day file **in the
01–21 range** should re-read that day's `## Concept` against its own tiers." Departure 2 is a live
instance at **day 27** — outside that range, carrying a wave-2C foreclosure, on no FIX-3.21 sub-item,
and defective. The scope clause is now "in any range, not only 01–21", with the day-27 instance
recorded as the evidence. This is a plan amendment rather than a file edit, but it is a departure from
the entry's literal text and is declared as one.

### Five unfiled cuts paid for the additions inside the 200-word cap — non-substantive

Recorded because the standing convention is to record every deviation. None removes an anchor
reference or a worked example.

| Day | Cut | Words | Why it was the cheapest loss |
|---|---|---|---|
| 22 `:5` | "Three of those four **sentences** … you sent **this prompt** again. Only the fourth changes." → "Three of those four … you sent it again; only the fourth changes." | 2 | pure tightening; the quoted four-sentence prompt it refers to is kept in place |
| 24 `:7` | ", one you could point to on a bad day" | 8 | restates "a property the output could plausibly lack" in the same sentence |
| 26 `:7` | "and now you can say which one, instead of assuming" | 9 | restates "that section mattered", four words earlier |
| 26 `:9` | "Neither is obvious from staring at the prompt before you run it." | 12 | with the new ladder above it, this is the same verdict on inspection-only cutting in weaker words — the state the Working tier mandates |
| 30 `:5` | "— not until tested against a case you didn't design for." | 11 | restated by `:7` ("an unfamiliar case tests whether the prompt generalises") and in full by `:11` |

### The rung idiom, applied

**No concept in these nine days names a tier**, per wave 3A's departure 5 and `SKILL.md:30`'s
one-tier rule — including `days/27.md:21`, where the scoping is expressed as "where **the tier** also
asks for a fix". Three rungs are named on the three days whose Working tier *mandates* anchor 4's
shortfall — 22, 24 and 26 — each in the day's own rubric vocabulary and quoting the anchors rather
than paraphrasing them. Days 27 and 28 carry two-rung statements, correctly: both Working tiers leave
their shortfall **silent**, so there is no mandated middle state to legitimise. Day 30's `:9` names
all three anchors explicitly by number, which is day 29's and day 30's established house style for
the capstone rubric and predates this batch.

## Nothing was stopped on

The batch trap was checked before acting rather than after. Checkpoint items 13–16 forbid `## Before /
After` edits on days 22, 24, 26 and 30, and all four days' entries carry a matching "**Do not touch**".
Item 17, by contrast, **requires** the `days/27.md:21` edit, and FIX-3.20's round-2 re-grade files it
as "Mandated" with its reasoning (day 27's After is tutor instruction about the learner's own actions,
not an illustrative model prompt). No entry in range asked for an After edit the checkpoint forbids,
so nothing had to be escalated. Days 23, 25 and 29 were left closed, as the brief directs. FIX-2.21(b)
was not reopened.

---

# Round 2 — two concept-vs-tier collisions closed, FIX-3.22 amended a second time, two minors filed

Both Important items landed. **Two day-file lines changed this round:** `days/17.md:18` and
`days/30.md:11`, plus the two deletions inside `days/30.md:9` that paid for `:11`. Both Minors were
**filed, not taken in file**, with the reasons recorded in the plan.

Day 17 is outside batch C's 22–30 range. It was edited on the coordinator's direct instruction, and
the departure is declared as such below.

## Verification

| Check | Result |
|---|---|
| `python3 tools/validate.py --complete` | `ok`, exit 0 |
| `python3 -m unittest discover -s tools` | 103 tests, OK |
| Round-2 diff scope | `days/17.md` (1 line), `days/30.md` (2 lines), `MASTER-FIX-PLAN.md` — nothing else |
| `## Exercise` tier bodies | **none touched** — hunks are `17.md:18` (inside `## Concept`, which ends at `:18`; `## Before / After` starts at `:20`) and `30.md:9`, `:11` |
| `## Rubric` | none touched |
| `## Before / After` | **none touched this round** — days 17, 22, 24, 26, 30 all unchanged; `days/27.md:21` unchanged since round 1 |
| `## ` / `### ` headings | none touched (grep empty) |
| `days/28.md:11`, `days/14.md:9` | **still untouched** — `git diff --stat` for both files is empty in both rounds |
| `rubrics.md`, `SKILL.md`, `assessment.md`, `tools/` | untouched |
| FIX-3.15 / checkpoint item 12's two conditions | re-verified in the file **after** the edit: `days/17.md:7`'s "shows what an empty value looks like" is unchanged and still a description of the goal, and the `"note": ""` example is not coupled to the Working tier |

## Word counts, recounted with `section()` + `len(split())`

| Day | Round 1 | Round 2 | Headroom | What paid for it |
|---|---|---|---|---|
| 17 | 178 (unedited) | **184** | 16 | **nothing deleted** — the ladder cost 6 words against 22 of headroom, because folding the script question into the top rung removed the duplication between `:18`'s two sentences |
| 30 | 191 | **195** | 5 | `:9`'s "The rubric's rungs are exact." (**5 words**) and "asks that **its failure modes** be" → "asks that **they** be" (**2 words**); `:11` cost 11, net +4 |

Days 22, 24, 26 and 27 are unchanged from round 1 (192, 189, 192, 174).

## Important 1 — `days/30.md:11`

**Confirmed and fixed.** `:11` read "run your day-29 prompt on **a case you didn't build it for**"
while the Novice tier (`:29`) mandates "a close variant, **not a case it was never built for**" —
`SKILL.md:28` reading the instruction aloud, `SKILL.md:30` presenting the tier that negates it in the
tier's own words, on the final day of the course. The gate's diagnosis is right about the process
failure too: I cut a clause from `:5` on the ground that it is "restated by `:11` in full", so the
sentence was read and the check I ran on days 26 and 27 was not run on it.

**Anchors, from `rubrics.md`'s `## Capstone`:** 2 — "works on **a couple of close variants**, but
hasn't been tried on anything unlike the original case"; 5 — "holds on **a case it was not designed
for**".

**Landed** in the shape `:9` already uses one paragraph up:

> Here is the test: run your day-29 prompt on **a close variant, then on a case you didn't build it
> for. The second is the climb** — what breaks there?

The close variant and the unfamiliar case are now two rungs of one test rather than a single
universal instruction. **The deletions that paid for it, named as required:** `:9`'s opening claim
"The rubric's rungs are exact." (5 words) — the three verbatim anchor quotes that follow demonstrate
it without asserting it — and "asks that **its failure modes** be" → "asks that **they** be"
(2 words), where "they" binds to the failure modes named in anchor 4's quote in the preceding
sentence. Net +4; day 30 has 5 words of headroom. The standard "Here is the test:" opener is intact,
so FIX-5.01 is unaffected.

## Important 2 — `days/17.md:18`

**Confirmed and fixed, and the provenance the gate cites is correct in the file:** `git log` puts day
17's Novice foreclosure in `b78e545`, "fix: wave 2B — rebuild tier ladders for days 14-21".

**Anchors, from `rubrics.md`'s `## Output schemas`:** 3 — "**Fields are enumerated, but types, order,
or optionality are left unstated**"; 4 — "An **exact structure** is given, with **one edge (e.g. empty
values) unaddressed**"; 5 — "An exact structure given, **which output can be checked against
mechanically**".

Novice (`:47`) mandates anchor 3 — "as a plain list of field names with **no types and no example
values**". `:18`'s second sentence — "the schema is still **a description, not a contract** — **fill
it with dummy values until it is**" — told that learner their compliant work was not yet a schema and
instructed them to do the one thing `:47` forbids. **Landed:**

> Here is the test: **fields enumerated, with types and order unstated, is a rung of its own**; **an
> exact structure with empty values unaddressed is the climb from there**; **a structure output can
> be checked against mechanically**, without you reading it first, **is the top**.

Three rungs, all three anchors quoted rather than paraphrased. The script question is kept — as the
top rung's content, which is what FIX-3.15's own preservation note already called it ("anchor 5's
text, correctly aimed at the top of the ladder"). No deletion was needed.

**Why it escaped, recorded because it is the generalisable part:** FIX-3.15 is tracking-only and
scoped to `:7` and the `"note": ""` example. Wave 3B verified exactly those two conditions, found them
holding, and closed the file. The entry named some of the day's sentences; the implementer checked
those. That is the same failure mode as my own day-30 `:11` miss, one wave later.

## FIX-3.22 — amended a second time

Filed in the plan, not here. The amendment records: the day list (16, 20, 28) is **not an inventory
and has proved short twice**; six confirmed members (16, 17, 20, 27, 28, 30), of which **three were
defective** (16, 17, 27) plus day 30's `:11`, and **every defect was found by opening the file, not by
following a list**. Days 17 and 30 are the sharpest cases because both *were* named by a wave-3 entry
and survived anyway — so **a day appearing in an entry is not evidence its other concept sentences
were read.**

The standing consequence is now written as **mandatory and unscoped**: any wave opening a day file for
any reason must, before closing it, read **every sentence** of that day's `## Concept` against that
day's **own Novice and Working tier text**, and record the result — clean or fixed — in the plan.
Wave 4 opens `days/17.md` and `days/30.md`; the entry says so, records that both are clean as of this
round, and requires the check to be re-run against any wave-4/5 edit to a concept, self-test or
`## Before / After` on those days.

**Two further plan amendments the round forced:**

- **The wave-3 file list is 22 day files, and `days/17.md` is one.** Day 17 was the sole member of the
  "tracking-only entries mandate nothing, so their days are not listed" exclusion; that exclusion now
  has no members. Recorded with the observation that **this is the second time the "tracking-only"
  label hid a live defect** — FIX-3.20 was the first, re-graded during wave 2C round 2 for the same
  reason. "Tracking only" now reads as "not yet checked against the tiers".
- **The concept-cap census was corrected, not adjusted:** day 30 moves from the 8–10 band to the 4–6
  band at 195, day 17 moves 178 → 184 and stays out of the table at 16. Both recounted after the
  edits.

## The two Minors — filed for wave 5 as **FIX-5.10**, not taken in file

Both were the coordinator's call to make either way. Both were filed, for reasons that are specific
rather than general, and the reasons are in the entry so a wave-5 implementer does not treat either as
a free prose fix.

**(a) `days/03.md:9`/`:11`.** Real, and rubric-wise it is the *inverse* of everything wave 3 fixed:
`adjective`'s anchors are rejection-trigger-based from rung 3 up ("Of the qualities the writer names
as **rejection-triggers**…"), so `:11` is the aligned half and the Novice tier's "two qualities **you
want**" is the loose half. The tier is silent, mandates nothing, and condemns nothing — so it is not
the FIX-3.22 class. **The decisive reason not to edit it in wave 3: `days/03.md:11` is FIX-5.01's one
remaining fully-live row.** Rewriting it now would spend that row exactly as wave 3A spent the day-04
and day-05 rows, and a wave-5 implementer applying FIX-5.01 verbatim afterwards would silently revert
the fix. FIX-5.10(a) carries scoped replacement text that satisfies both, and FIX-5.01's day-03 row
has been amended in place to say "land it with FIX-5.10(a), not alone". Day 03 is at 163 words —
37 of headroom — so both fit.

**(b) `days/10.md:7`.** Weaker, and filed mainly so the one line worth a second read is on the record.
`:7`'s example models a rung above the tier **without condemning it** — the ordinary shape days 23 and
25 were explicitly cleared on — and imitation is structurally impossible: the Novice template is fixed
text with exactly one blank, so a learner copying `:7` cannot bind the second noun. The line I would
not want assumed clean is `:9`'s "**A bare noun next to a bound one is still a gap**", which is the
closest thing on the day to a verdict on the state `:33` mandates. I read it as rung language —
"*still* a gap" names distance left to climb, and one bare noun is anchor 3, a scored rung — and the
gate independently judged `:9` clean. Two readings agreeing is why no edit was made; the entry says
explicitly that this is not a reason to skip re-reading it if wave 5 opens the file. Day 10 is at 178
(22 of headroom) if a scoping clause is ever wanted.

## Departures this round

**One, substantive, and instructed.** `days/17.md` is outside batch C's declared 22–30 range and
outside the "do not touch days 01–21" constraint in the original brief. It was edited on the
coordinator's direct instruction after the gate confirmed the defect and its wave-2B provenance.
Declared here rather than folded into the Important item, because the earlier constraint was explicit
and a reader reconciling the two needs to see which one won and why. Nothing else in days 01–21 was
opened or changed.

The two Minors are **not** departures — the coordinator left the venue to my discretion and both are
filed with reasons.

## Round-2 filings in `MASTER-FIX-PLAN.md`

| Location | What was filed |
|---|---|
| **FIX-3.15** | No longer tracking-only. The `:18` defect, its wave-2B provenance, the landed ladder, do-not-restore on the deleted sentence, and confirmation that both of the entry's own preservation conditions still hold. |
| **FIX-3.19** | Round-2 note: the `:11` collision, the landed text, and the two deletions that paid for it, with the recounted 195. |
| **FIX-3.22** | Second amendment — the six-day table with provenance and verdicts, "an entry naming a day is not evidence its other sentences were read", and the standing consequence rewritten as a mandatory per-file check with wave 4's exposure named. |
| **Wave-3 preamble** | File count corrected to 22; the tracking-only exclusion emptied, with the observation that the label has now hidden a live defect twice. |
| **Wave-3 checkpoint, cap census** | Day 30 moved to the 4–6 band (195); day 17's 184 noted. |
| **FIX-5.01** | Day-03 row re-labelled "live — but land it with FIX-5.10(a), not alone", with the reason and the cost check. |
| **FIX-5.10** (new, wave 5) | Both Minors in full, with replacement text for (a), the reason each was filed rather than edited, the `days/10.md:9` line flagged for a second read, and constraints forbidding tier and `## Before / After` edits on both days. |
