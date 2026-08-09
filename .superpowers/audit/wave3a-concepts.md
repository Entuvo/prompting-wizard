# Wave 3, batch A — concepts, days 01–11

Scope executed: FIX-3.01, FIX-3.02 (both halves plus the mandated day-04 tier re-derivation),
FIX-3.03, FIX-3.04, FIX-3.05, FIX-3.06, and FIX-3.21 sub-items (a) day 2, (b) day 5, (c) day 8,
(d) day 9, (e) day 11, plus the two tracking sub-items (h) day 1 and (i) day 6.
Out of range and untouched: FIX-3.21(f) day 13, (g) day 19, and every entry on days 12–30.

## Verification

| Check | Result |
|---|---|
| `python3 tools/validate.py --complete` | `ok`, exit 0 |
| `python3 -m unittest discover -s tools` | 103 tests, OK (no test file touched) |
| `## ` / `### ` headings | none touched (`git diff -U0 -- prompting-wizard/days \| grep '^[+-]#'` → empty) |
| `rubrics.md`, `SKILL.md`, `assessment.md`, `tools/`, days 12–30 | untouched |
| `## Exercise` tiers edited | `days/04.md:31` only — mandated by FIX-3.02's dependency and checkpoint item 19 |
| `days/14.md:9`, `days/28.md:11` | not edited (CONFLICT-03, CONFLICT-07) |
| grep `exhaustively` across `days/` | one instance, `days/04.md:21`, and it now carries a measure |
| day 06 After word count | 29 words, inside the 40-word budget its own Advanced tier sets |

```
 prompting-wizard/days/01.md |  2 +-
 prompting-wizard/days/02.md |  4 ++--
 prompting-wizard/days/04.md | 10 +++++-----
 prompting-wizard/days/05.md |  2 +-
 prompting-wizard/days/06.md |  6 +++---
 prompting-wizard/days/07.md |  4 +++-
 prompting-wizard/days/08.md |  4 ++--
 prompting-wizard/days/09.md |  4 ++--
 prompting-wizard/days/11.md |  2 +-
 9 files changed, 20 insertions(+), 18 deletions(-)
```

Days 03 and 10 have no filed wave-3 entry and were not edited.

## Concept word counts (cap 200)

| Day | Before | After |
|---|---|---|
| 01 | 129 | 147 |
| 02 | 171 | 199 |
| 03 | 163 | 163 (unedited) |
| 04 | 164 | 190 |
| 05 | 173 | 191 |
| 06 | 185 | 190 |
| 07 | 169 | 197 |
| 08 | 169 | 188 |
| 09 | 179 | 197 |
| 10 | 178 | 178 (unedited) |
| 11 | 187 | 197 |

Days 02, 07, 09 and 11 are within three words of the cap. Any later wave adding a clause to those
four concepts must remove one first.

---

## Per day

### Day 01 — `rubrics.md#noun` — 147 words

**Anchor now taught.** Anchor 4, "The artifact is named unambiguously. Someone reading only the
prompt could describe the finished output", as the day's work; anchor 5, "Named unambiguously and
economically — **no words spent on the artifact beyond what pins it down**", as the rung above.

`:11` now reads: "Nouns compound with counts and formats, but those are later levers. Today, just
name the thing — and the rung above adds economy: no words spent on the artifact beyond what pins it
down."

**Way-station.** Not needed. FIX-3.21(h) is right that no collision exists: `:11`'s "just name the
thing" already supports the Novice tier's "but not the count or the format", and `:9`'s test (name
the physical thing in a noun phrase) is satisfied by a compliant Novice. The economy clause is
scoped, per FIX-3.21(h), to the Advanced rung at `:41` ("in under 15 words total"), not stated as a
universal.

**Before / After.** Unchanged. Floor "unchanged" holds.

### Day 02 — `rubrics.md#verb` — 199 words

**Anchor now taught.** Anchor 3, "An operation is named, but **a nearby operation would satisfy the
same wording just as well**"; anchor 4, "Exactly one operation named, and it is the operation wanted,
but expressed with a generic synonym"; anchor 5, "no verb in the same family names it more narrowly".

**Way-station** (Novice `:31` mandates the anchor-3 shortfall — "a verb loose enough that a nearby
operation would satisfy your wording just as well"):

- `:9` — "A verb a nearby operation would satisfy just as well is where this starts; the operation
  you actually want is the climb from there."
- `:11` — "If they can narrow it to a nearby operation, you are partway."

The stranger test itself is unchanged and its failing examples ("help", "look at") are anchors 1–2,
below the Novice rung, so the test now discriminates rungs instead of condemning the tier.

**Before / After.** Unchanged. Floor "unchanged" holds.

### Day 04 — `rubrics.md#adverb` — 190 words — **FIX-3.02, full re-derivation below**

**Anchor now taught.** Anchor 3, "Depth or manner is set for part of the task, but another part is
left to guess"; anchor 4, "Depth and manner set with a measure attached **across the whole task**,
but attached as a stated tolerance rather than a fixed figure"; anchor 5, "a measure attached to
every part, so two competent readers would produce the same length and thoroughness".

**Edits.**

- `:9` — FIX-3.02(b) applied verbatim.
- `:11` — rewritten (**not in any filed entry**; see departures): "Here is the test: if two competent
  people followed this manner word, would their outputs be the same length and thoroughness?
  Measuring the one part where depth matters most and leaving the rest to guess is a rung of its own;
  a measure across the whole task is the climb from there, and one on every part is the top."
- `:21` (After) and `:23` (gloss) — FIX-3.02(a), with one departure (see below).
- `:31` (Novice tier) — foreclosure clause added, per FIX-3.02's dependency and checkpoint item 19.

**Way-station.** `:11`'s "Measuring the one part where depth matters most and leaving the rest to
guess is a rung of its own". Without it the concept's two-reader test condemns, aloud, the exact state
the strengthened Novice tier now mandates.

### Day 05 — `rubrics.md#preposition` — 191 words

**Anchor now taught.** Anchor 3, "Most of scope, audience and exclusion are set, but **one relation
is left implicit**"; anchor 5, "Boundaries, audience and exclusions all set so each admits exactly
one reading — in what, for whom, without what".

**Way-station** (Novice `:31` mandates "a scope and an audience — those two only, with nothing ruled
out"): `:11` — "Two answers of three leaves one open boundary the model will set for you, which is a
rung of its own; all three, each admitting exactly one reading, is the top."

**Before / After.** Unchanged. Floor "unchanged" holds.

### Day 06 — `#noun`, `#verb`, `#adjective`, `#adverb`, `#preposition` — 190 words

**Anchor now taught at `:7`.** `preposition` anchor 5, "Boundaries, audience and exclusions all set
so each admits exactly one reading — **in what, for whom, without what**". `:7` now reads "The
preposition says where it stops, who it's for, and what it must not touch" (FIX-3.04, verbatim).

**Way-station.** Not needed, per FIX-3.21(i), and confirmed in the file: `:9` states what the Working
tier demands, `:11`'s remove-each-lever test is tier-independent, and nothing in the concept asserts
the property `:31` now mandates as absent. The concept was **not** re-coupled to the rebuilt tiers.

**Before / After — sanctioned exception. Floor: must not fall below `noun` 5 or `adjective` 5.**

New After (29 words):

> Rank the correctness issues in {{TASK}} into a blunt, jargon-free list, one bullet per issue with
> none omitted, for a reader new to the codebase, without proposing API changes.

Re-scored against all five cited rubrics:

| Rubric | Before | After | Anchor |
|---|---|---|---|
| noun | 5 | **5** | "a blunt, jargon-free list, one bullet per issue" — a reader can describe the finished output, and no word is spent on the artifact beyond what pins it down. Floor held. |
| verb | 5 | **5** | "Rank" — one operation, nothing narrower in its family. Untouched. |
| adjective | 5 | **5** | "blunt, jargon-free" — untouched by both edits. Floor held. |
| adverb | **2** | **5** | "one bullet per issue with none omitted" — a measure attached to every part of the one-part task, so two competent readers produce the same length. |
| preposition | **3** | **5** | scope ("correctness issues in {{TASK}}"), audience ("for a reader new to the codebase") and exclusion ("without proposing API changes"), each admitting one reading. |

**Imitate-the-After, re-derived.** Novice `:31` mandates "the first word that comes to hand for each
… so someone reading your finished prompt still could not describe the artifact it produces". Copying
the new After produces a describable artifact, so an imitator is non-compliant with the tier and is
not what the tier is scored on. A compliant learner stays at **2–3**, unchanged from wave 2D. The
bottom rung is held down by the tier's own clauses, not by any weakness in the After, exactly as
FIX-3.21's preamble states — so raising the After from 2/3 to 5 on two rubrics does not re-open the
leak. Ladder 2–3 / 4 / 5 intact.

### Day 07 — `#noun`, `#verb`, `#adjective`, `#adverb`, `#preposition` — 197 words

**Anchor now taught.** The closing test scores `noun` anchor 5 ("no words spent on the artifact
beyond what pins it down") and `adjective` anchor 5 ("each is worded specifically enough that a
generic output visibly fails one") through the deletion test, and anchor 4 coverage across the five
levers through the lever-goes-unset half.

New fourth paragraph:

> Here is the test: delete one clause from your rewrite and read it again. If a lever goes unset,
> that clause was load-bearing; if the sentence still says exactly what you meant, it was decoration.
> Setting all five levers is the climb; leaving no clause whose deletion changes nothing is the rung
> above.

Day 07 now has four paragraphs and a closing self-test, closing P03 and P05.

**Way-station.** "Setting all five levers is the climb; leaving no clause whose deletion changes
nothing is the rung above" — the Novice tier rewrites one lever in and the Working tier sets five
without the decoration test, which `:9` previously stated as the universal target.

**Before / After.** Unchanged, and unchangeable in the relevant sense: day 07's block is tutor
instruction, not a worked prompt (wave-2D imitator result: N/A).

### Day 08 — `rubrics.md#pronoun` — 188 words

**Anchor now taught.** Anchor 3, "**Exactly one pronoun still requires the reader to guess**; the
rest resolve"; anchor 4, "Every reference resolves inside the prompt or to a quoted block, but at
least one antecedent sits more than a sentence away"; anchor 5, "each pronoun's antecedent is the
nearest preceding noun phrase".

**Way-station** (Novice `:31` mandates "leaving exactly one pronoun that still requires the reader to
guess"): `:11` — "One you can't point at, with the rest resolving, is partway. Replacing that last
one is the climb; putting each antecedent next to its pronoun is the rung above."

**Before / After — sanctioned exception. Floor: the After at `:21` must keep every reference
resolving, anchor 4 or above.** The After prompt is **unchanged**; only the gloss at `:23` was
replaced, with FIX-3.06's text verbatim. The After remains `pronoun` anchor 4 ("it" binds to the
diff, a sentence back), which is the floor. Imitator result unchanged at **3**: copying the After
gives a prompt where every reference resolves, which is non-compliant with the Novice mandate.

**Optional half declined.** FIX-3.06's optional fenced diff under `:21` was not added — it is
explicitly optional, and the replacement gloss no longer claims a quoted block exists, so the defect
it was offered against is closed without it. Recorded so a later wave can still take it if it wants a
worked instance of the anchors' "quoted block" clause.

### Day 09 — `rubrics.md#conjunction` — 197 words

**Anchor now taught.** Anchor 3, "Branches and conditions are named, but **the fallback (the
otherwise) is missing**"; anchor 4/5 differ only on order of checks.

**Way-station** (Novice `:33` mandates "the outcome only, with no fallback for everything the
condition doesn't match"):

- `:9` — "or the fallback can be missing, which gets you partway, with everything the condition
  doesn't match still left for the model to invent."
- `:13` — "the answer names the rung you are on, and the fallback is the last one to close."

**Before / After.** Unchanged. Floor "unchanged" holds.

### Day 11 — `rubrics.md#numeral` — 197 words

**Anchor now taught.** Anchor 3, "Every countable dimension is bounded, but **at least one bound is
vague enough to need judgement** ('a few', 'several')"; anchor 4, "every bound is a number, but at
least one is a range or an approximation"; anchor 5, "an exact count or length".

**Way-station** (Novice `:33` mandates "a number for the count, and words rather than a number for
the length"): `:13` — "Bounding the count but leaving the length in words is partway; a number on
every dimension is the rung above."

**Before / After.** Unchanged. Floor "unchanged" holds.

---

## FIX-3.02 — day 04, full re-derivation (checkpoint item 19)

### The After, as landed

> Review {{TASK}} exhaustively for correctness — every function against its callers, one line per
> issue found — then for style in exactly three sentences, flagging only tone and word choice.

`adverb` anchor **5**: a measure is attached to both parts ("one line per issue found"; "exactly
three sentences"), so two competent readers produce the same length and thoroughness. Before the fix
it was anchor 3 — a measure on the style half only.

### The Novice tier, as landed

> Fill the blanks with a manner word, the one part of the task where depth matters most, and a
> measure for that part only — **leave the manner word itself bare, with no measure attached across
> the whole task, so the depth of everything else is still left to guess** — then send the completed
> line as your prompt.

The added clause negates anchor 4's positive content ("a measure attached **across the whole task**")
in that anchor's own words, and keeps the measure scoped to the one named part the template already
isolates. Proven shape, matching days 02, 05, 08, 09, 11.

### Imitate-the-After, re-run against the **new** After

Template (`:33`, untouched): `> Review {{TASK}} ________, and for ________ specifically, ________.`

Copying the new After requires putting "— every function against its callers, one line per issue
found" into blank 1, where it attaches to the manner word and covers the correctness pass — i.e. a
measure across the whole task. The Novice mandate now forbids exactly that, so an imitator of the new
After is **non-compliant** and is not what the tier is scored on, the same standard wave 2D applied
on the other eight template days.

A compliant learner produces, e.g., `Review {{TASK}} carefully, and for correctness specifically, one
line per issue found.` — manner word bare across the whole task, measure on one named part, the rest
left to guess. That is anchor **3** word for word. The effort gradient points the right way: one bare
word plus one measure costs less than two measures.

### Ladder after the fix

| Tier | Text | Anchor |
|---|---|---|
| Novice `:31` | bare manner word, measure for one named part only | **3** — "Depth or manner is set for part of the task, but another part is left to guess." |
| Working `:37` | "set clearly enough that you could predict **roughly** how long the output would be" | **4** — measure across the whole task, as a stated tolerance rather than a fixed figure. |
| Advanced `:41` | "two different depths for two different parts … says which and by how much" | **5** — a measure attached to every part. |

3 / 4 / 5, imitator 3. The leak FIX-3.02(a) opened is closed.

---

## OPEN-3.01 — ruling (checkpoint item 8)

**Explicitly deferred to wave 4, with a recommended resolution recorded. Nothing was changed on day
9's tiers or on `conjunction`'s anchors.**

Both candidate resolutions named in OPEN-3.01 are out of batch A's reach by construction: the rubric
side is a wave-1-class edit to settled anchors, and the day side is a wave-2-class edit to a settled
ladder. Batch A's charter forbids both. Ruling on the *semantics* without editing either file would
put the ruling nowhere a tutor reads it — `rubrics.md:7`'s not-applicable rule is the only place the
convention could live, and that is `rubrics.md`.

Recommended resolution for wave 4, for whoever re-opens it: take the **rubric side**. Make plurality
explicit in `conjunction` anchors 4 and 5 ("Two or more branches, each stated with its condition and
its fallback, …"), and let `rubrics.md:7` absorb genuinely single-branch tasks. It repairs every
single-branch prompt in the course rather than day 9 alone, it is the same shape as FIX-1.12's
treatment of `particle` over an empty set, and it leaves day 9's rebuilt ladder untouched — which
matters, because the day side would move a Working tier wave 2A verified.

Interaction with FIX-3.21(d), as that entry requires: (d) was applied on the reading OPEN-3.01 itself
records as the status quo — that anchor 5's ordering clause is **vacuous, not satisfied**, over one
branch, so day 9's Working sits at 4. The concept text landed above says only that the fallback is
"the last one to close" and does not assert where a one-branch prompt lands on the 4/5 boundary, so
either resolution of OPEN-3.01 leaves day 9's concept correct as written. No rework is created.

---

## Departures from the plan's literal text

Eleven, five of them substantive.

**1. FIX-3.01's literal replacement was not used — substantive, and required by FIX-3.21(h).** The
plan's text is "Today, just name the thing — in as few words as pin it down", which teaches `noun`
anchor 5's economy clause to every tier including a Novice tier foreclosed below anchor 4.
FIX-3.21(h) forbids exactly that. Landed instead as "— and the rung above adds economy: no words
spent on the artifact beyond what pins it down", which scopes it to `days/01.md:41` and quotes the
anchor rather than paraphrasing it.

**2. FIX-3.02(a)'s After carries one change beyond the plan's replacement text — substantive.** The
plan's replacement keeps "then for style in **three sentences at most**". Under FIX-1.05's rebuilt
anchors that is a *stated tolerance*, which is anchor 4's discriminator word for word — "attached as
a stated tolerance rather than a fixed figure, so two competent readers would land inside that
tolerance rather than on the same length". The plan's literal text therefore lands the day-04 After at
**anchor 4**, and checkpoint item 3 requires every edited After to score **5**; FIX-3.02's own *Why*
says the same ("not the 5 a model answer must score"). The plan contradicts itself here. Resolved by
changing "in three sentences at most" to "in **exactly** three sentences", the minimum edit that
satisfies both. The gloss at `:23` quotes the new wording to match.

**3. `days/04.md:11`'s self-test was rewritten — substantive, filed by no entry.** Once FIX-3.02's
mandated foreclosure lands, day 04's Novice tier *instructs* the learner to leave the manner word
bare, while `:11` told them, aloud, that a manner word two readers would follow differently "isn't
doing its job". Same class as every FIX-3.21 sub-item, on a day FIX-3.21 does not list, because day
04's tier was strengthened by this wave rather than by wave 2D. Rewritten to present the one-measured-
part state as a scored rung.

**4. FIX-3.05's added paragraph does not fit the 200-word cap — substantive.** *(Figures corrected in
round 2; see "Important 1" below for the method and the errors.)* The entry asserts "Day 7's concept
currently runs short … so there is headroom". It ran at 169 words, leaving **31**; the paragraph the
entry specifies is **50**. Landed as a **53**-word paragraph carrying the same two halves (deletion
test, five-lever coverage), and paragraph 3 was compressed from **46** words to **21**, a saving of
**25** — its last sentence ("The rewrite you're aiming for is the opposite: every clause, if removed,
visibly weakens the result") was removed because the new self-test states the same thing
operationally, and the remaining sentence was tightened. 169 − 25 + 53 = **197** words.

**5. Tier framing uses the course's "rung / partway" idiom rather than naming tiers — substantive,
applied across FIX-3.21(a)–(e).** Several sub-items give directions of the form "name the stranger
test as what **Working and Advanced** are graded on". No concept in the thirty days names a tier, and
`SKILL.md:30` shows a learner exactly one tier, so naming the other two aloud tells a Novice learner
about rungs they cannot see. The established device — `days/28.md:9` "gets you partway",
`days/29.md:5-9` "bottom rung / the rung above", `days/23.md:7` "clears the middle rungs" — says the
same thing tier-agnostically and is what the brief names as the model. Used everywhere.

**6. FIX-3.03's gloss instruction was extended — non-substantive.** The entry says only to replace
`"exhaustively" the adverb` with the new phrase. Because FIX-3.04's exclusion clause lands in the same
sentence and the gloss enumerates one phrase per lever, the preposition's entry was also updated to
name the exclusion ("— audience and exclusion, not audience alone"). Leaving it would have left the
gloss claiming "nothing is left for the model to invent" while silently omitting a clause the After
now carries.

**7. Self-test openers normalised on days 04 and 05 — non-substantive, and it overlaps FIX-5.01.**
Both sentences were being rewritten in full for other reasons, and the brief requires the established
"Here is the test:" idiom. FIX-5.01 (wave 5, P01/P02) normalises days 1–6; days 01, 02, 08, 09 and 11
already used the idiom, so after this batch only `days/03.md:11` and `days/06.md:11` remain for it.
Flagged so wave 5 does not treat the entry as unstarted.

**8. `days/09.md:9`'s "exactly as underspecified as no branching at all" was deleted, not just
softened — substantive.** FIX-3.21(d) quotes the clause without saying it is false. It is: a stated
condition and outcome with no fallback is `conjunction` anchor **3**, and no branching at all is
anchor **1**. The clause was flatly wrong against the rubric independently of any tier collision, and
survives nowhere in the replacement.

**9. FIX-3.06's optional fenced diff was declined — non-substantive.** Recorded under day 08 above.

**10. `days/02.md:11` lost one of its three failing examples — non-substantive.** `or "consider"` was
cut to buy the four words the way-station clause needed inside the cap. "help" and "look at" remain,
and "look at" is the day's own Before.

**11. Day 05's `:11` says "which is a rung of its own" rather than repeating "partway" — non-
substantive.** Pure variation; days 02, 08, 09 and 11 use "partway", days 01, 04, 05, 07 and 08 use
"the rung above". Both are the established idiom.

## Checkpoint items closable from batch A

- **Item 1** — validator `ok`. Of the days it names, 4, 6 and 7 are in range and all pass; 15, 19, 21
  belong to batch B.
- **Item 2** — day 06's After is 29 words.
- **Item 3** — both known before-state failures re-scored: day 04 was 3, now **5**; day 06 was adverb
  2 / preposition 3, now **5 / 5**, with noun, verb and adjective held at 5. Day 04's 5 depends on
  departure 2.
- **Item 4** — one surviving "exhaustively" in `days/`, at `days/04.md:21`, and it carries a measure.
- **Item 5** — `days/14.md` and `days/28.md` untouched.
- **Item 8** — OPEN-3.01 explicitly deferred to wave 4, above.
- **Item 18** — the in-range half: days 2, 5, 8, 9 and 11 landed; day 1 (h) applied in the scoped
  form; day 6 (i) not re-coupled. **No `## Before / After` edit on days 1, 2, 5, 9 or 11 was made at
  all**; day 6's rose (adverb 2→5, preposition 3→5) with the noun-5 and adjective-5 floor held; day
  8's After prompt is unchanged at anchor 4, its floor. Days 13 and 19 are batch B's.
- **Item 19** — FIX-3.02 landed and day 04 re-derived above against the new After, not by inspection
  of the tier.

## Nothing was stopped on

Every filed entry in range was executed. The four plan defects found (departures 1–4, plus 8) were
each resolvable in-file without contradicting a settled anchor or a settled ladder.

---

# Round 2 — corrections, filings, and four prose minors

Six items from the gate. All six landed. No `## Before / After` block and no `## Exercise` tier body
was touched this round; the only day files changed are `days/01.md`, `days/02.md` and `days/05.md`,
each named by a minor. Days 03, 04, 06, 07, 08, 09 and 11 are unchanged from round 1.

## Verification

| Check | Result |
|---|---|
| `python3 tools/validate.py --complete` | `ok`, exit 0 |
| `python3 -m unittest discover -s tools` | 103 tests, OK |
| `## ` / `### ` headings | none touched |
| `## Before / After` blocks | none touched this round |
| `## Exercise` tier bodies | none touched this round |
| `rubrics.md`, `SKILL.md`, `assessment.md`, `tools/`, days 12–30 | untouched |

Concept word counts, all recounted with `validate.py`'s own `section()` plus `len(split())`, not by
eye:

| Day | Round 1 | Round 2 | Change |
|---|---|---|---|
| 01 | 147 | **147** | Minor 1, cost-neutral |
| 02 | 199 | **199** | Minors 2 and 4, paid for by three cuts |
| 03 | 163 | 163 | unchanged |
| 04 | 190 | 190 | unchanged |
| 05 | 191 | **195** | Minor 3 |
| 06 | 190 | 190 | unchanged |
| 07 | 197 | 197 | unchanged |
| 08 | 188 | 188 | unchanged |
| 09 | 197 | 197 | unchanged |
| 10 | 178 | 178 | unchanged |
| 11 | 197 | 197 | unchanged |

## Important 1 — departure 4's figures, recomputed

Recomputed with `validate.py`'s `section()` and `len(str.split())` against `git show HEAD~1` for the
before-state. Three of the four figures in round 1's departure 4 were wrong.

| Figure | Round 1 said | Correct | Method |
|---|---|---|---|
| FIX-3.05's specified paragraph | 51 | **50** | `len(plan_text.split())` |
| Landed paragraph | 47 | **53** | paragraph 4 of the new `## Concept` |
| Day 07 paragraph 3, before | 30 | **46** | paragraph 3 of `HEAD~1`'s `## Concept` |
| Day 07 paragraph 3, after | 21 | 21 | correct |
| Saving on paragraph 3 | 9 | **25** | 46 − 21 |
| Headroom before the edit | 169 → 31 | 169 → 31 | correct |

Paragraph vectors, for the record: before `[73, 50, 46]` = 169; after `[73, 50, 21, 53]` = 197.

Round 1's 30 counted only the two sentences it went on to rewrite, not the whole paragraph — the
deleted sentence ("The rewrite you're aiming for is the opposite…", 16 words) was left out of its own
before-figure. The 47 was an eye-count of a draft that was revised once more before it landed.

**The conclusion is unchanged and the arithmetic still closes.** FIX-3.05 specifies a 50-word
paragraph into 31 words of headroom, so the entry's "there is headroom" claim is false and a
substitution was required; 169 − 25 + 53 = 197, inside the cap.

The report's departure 4 has been corrected in place.

## Important 2 — OPEN-3.01 filed into the plan as FIX-4.22

Round 1's ruling lived only in this report, which is the failure mode `wave2d-sweep.md:536` names —
"wave 3's implementer reads the plan, not this report" — and the reason FIX-3.02's dependency was
moved into the plan in the first place. Corrected:

- **`MASTER-FIX-PLAN.md`, new entry FIX-4.22** — "Make `conjunction` anchors 4 and 5 require two or
  more branches — resolves OPEN-3.01, deferred here by wave 3A — severity: medium". Placed after
  FIX-4.21, at the end of wave 4's entries. It carries the exact anchor replacement text, the
  reasoning for taking the rubric side over the day side, the flag that it re-opens a wave-1 file and
  needs a re-opening ruling, the note that **no day file changes either way** because day 09's landed
  concept is correct under both outcomes, and a stated fallback if the entry is rejected: write the
  vacuous-vs-unsatisfied convention into `rubrics.md:7` instead. Silence is ruled out as an outcome.
- **`MASTER-FIX-PLAN.md`, new wave-4 checkpoint item 7** — OPEN-3.01 is closed, not deferred again;
  `days/09.md` must be confirmed unedited; if FIX-4.22 lands, re-read `conjunction` against
  `days/09.md:39` and `:43` and confirm the ladder still reads 3 / 4 / 5.

## Important 3 — FIX-5.01 de-staled

Confirmed both hazards the gate named, in the file. The old `days/04.md:11` row's replacement text
carried "would their outputs be **roughly** the same length and thoroughness?" — `adverb` anchor 4's
tolerance language — against a line round 1 deliberately moved to anchor 5's wording. The old
`days/05.md:11` row would have overwritten FIX-3.21(b)'s way-station clause. Both would have been
silent reverts of wave-3 alignment fixes, applied by an implementer following the table verbatim.

Amended:

- The table gains a **Status** column. `days/04.md:11` and `days/05.md:11` are marked **spent — DO NOT
  APPLY**, each with a one-line reason naming what applying it would revert; both lines already open
  "Here is the test:".
- `days/03.md:11` and `days/06.md:11` remain **live** and unchanged.
- `days/01.md:9` and `days/02.md:11` are marked **live, punctuation only** — both still use a full
  stop where the idiom uses a colon, so P01's half survives; but their sentence bodies are no longer
  what the old table said, and day 02's may not be restored from it.
- A **cost check** paragraph was added: the day-06 row costs **one** word (190 → 191), the day-03 row
  is cost-neutral, both inside the cap.
- The **Sequencing** paragraph was rewritten — it read as a forward dependency on wave 3 ("apply wave
  3 first"), which is now spent; it is a de-staling notice pointing at this report.
- The days-01-and-02 note records that `days/02.md` sits at 199 words, one under the cap, so the
  colon swap is the only change its concept can absorb.

## Minors

**Minor 1 — `days/01.md:11`, "the rung above" → "the top rung".** Endorsed and applied. For a Novice
learner at `noun` anchor 3 the rung above is anchor 4 (describability), not anchor 5 (economy), so
"the rung above" pointed at the wrong rung for the reader most likely to hear it. "The top rung" is
unambiguous and matches `days/29.md:5`'s vocabulary. Cost-neutral: 147 → 147.

**Minor 2 — `days/02.md:11`, the two-way reading.** Was: "If they can narrow it to a nearby operation,
you are partway" — readable as the stranger *succeeding* at narrowing. Now: "If they name the
neighbourhood but not the operation, you are partway." Exactly as long as the clause it replaces, and the
intended sense — the stranger reaches the family, not the member — is the only available reading.
This is anchor 3's content ("a nearby operation would satisfy the same wording just as well"), which
`:9` already states in the anchor's own phrasing, so the two lines now agree.

**Minor 3 — `days/05.md:11`, agreement error and a coverage gap.** Was: "Two answers of three leaves
one open boundary…" — a plural subject with a singular verb, read aloud verbatim by `SKILL.md:28` —
and it scored only the two-of-three state, leaving one-of-three (`preposition` anchor 2, "One boundary
is given … but others are missing") uncovered. Now:

> Each answer you cannot give is a boundary the model will set for you; two of three answered is a
> rung of its own, and all three, each admitting exactly one reading, is the top.

The general rule leads, the way-station follows it as a case, and any number of missing answers is
covered. 191 → 195.

**Minor 4 — `days/02.md`, anchor 5's discriminator. Done in the file, not deferred.** The gate left
the call open. Deferring it would have put an *alignment* gap — the concept never naming the property
its top anchor scores — into wave 5, a prose wave, on the same day the plan already judged worth
fixing on day 01 (A13 / FIX-3.01). `:9` now reads:

> One prompt, one verb. A verb a nearby operation would satisfy just as well is where this starts;
> the operation you actually want is the climb from there; the narrowest verb in its family is the
> top.

Three rungs, in order, matching anchors 3, 4 and 5 — the last quoting anchor 5's discriminator, "no
verb in the same family names it more narrowly", in the concept's own register.

**The nine words this cost were paid for by three cuts, listed because no entry authorises them:**

| Line | Was | Now | Saved |
|---|---|---|---|
| `:5` | "The model has to invent a verb" | "The model must invent a verb" | 1 |
| `:5` | "the easiest one: summarise, probably, because summarising is the safe default when nothing else is specified" | "the easiest one: summarise, the safe default when nothing else is specified" | 4 |
| `:7` | "leave the model to pick a member of the family, same as no verb at all" | "leave the model to pick one, same as no verb at all" | 4 |

All three are tightenings that remove repetition — "summarise … summarising", "family … family" —
rather than teaching. No example verb, no anchor reference and no sentence was lost. Nine words cut,
nine words added at `:9`, Minor 2 cost-neutral: **199 → 199**, verified by recount, not by
arithmetic.

**Day 02 is now at 199 of 200 words and has one word of headroom.** Any later entry adding a clause to
it must delete first. FIX-5.01's amended entry says so at the point of use.

## Departures this round

Two, both non-substantive, both invited by the gate's own wording.

1. **Minor 4 was taken in-file rather than filed to wave 5.** The gate offered either; the reasoning
   for choosing the file is above. It carries three unauthorised prose cuts on `days/02.md:5` and
   `:7`, tabulated.
2. **FIX-5.01's days-01 and -02 rows were relabelled "live, punctuation only" rather than "spent".**
   The gate's instruction was to leave only days 03 and 06 live and mark the other rows spent with a
   reason. Marking days 01 and 02 flatly spent would have discarded P01 — those two lines genuinely
   still use a full stop where the idiom uses a colon, and wave 3A did not touch `days/01.md:9` at
   all. They are marked live for the opener alone, with an explicit warning that their sentence bodies
   in the table are stale. This preserves the finding while closing the revert hazard, which is what
   the instruction was for.
