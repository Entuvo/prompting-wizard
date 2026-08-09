# Wave 2, batch D — the imitate-the-After sweep over days 01–21

Scope: `prompting-wizard/days/01.md` … `days/21.md`, `## Exercise` tier bodies only. Every anchor
quoted below is the **settled** text of `prompting-wizard/rubrics.md`, read from the file and quoted
by text, never by line number.

This batch applies retroactively the test batch C invented and applied only forward. Grep confirms
neither `wave2a-tiers.md` nor `wave2b-tiers.md` contains "imitate" or "copying the After": the
standard improved mid-wave and days 01–21 were reviewed without it.

## The test, as applied

`SKILL.md:28` reads the day's `## Before / After` aloud immediately before the exercise, so a learner
copying the worked example they were just shown is the realistic least-effort path. For each day:
**if a learner imitates that day's After, which anchor do they reach?** A Novice tier whose compliant
imitator reaches anchor 4 or 5 fails. Two supporting criteria, both from batch C:

- **The effort gradient must point the right way.** A sound Novice asks for *less* than the After. If
  complying costs more than copying, the learner copies. (This is what cleared days 23 and 25.)
- **Anchor transfer.** Copying only lifts the score if the property the rubric scores is *textual*.
  Where anchors 4 and 5 are relative to something the rubric elicits from the writer — their own
  rejection-triggers, their own task's dependencies — the example's words do not carry its anchor
  across to a different task. This is the distinction that separates day 02 (fails) from day 03
  (passes), and it is stated for every day below.

A third structural fact decides several days: **whether the Novice template is the After's own
sentence minus the blank.** Where it is (days 01, 02, 03, 04, 09, 11, 13), filling the blank with the
After's word reproduces the After. Where the template is *truncated* relative to the After (days 05,
09, 10), the missing relation cannot be reached by filling a blank — but on days 05 and 09 it can be
**smuggled into the trailing free-form blank**, which is the day-22-round-2 defect, and both were
closed.

---

## Verification

| Check | Result |
|---|---|
| `python3 tools/validate.py --complete` | `ok`, exit 0 |
| `python3 -m unittest discover -s tools` | 103 tests, OK (no test file touched) |
| `git diff --stat` | days 01, 02, 05, 06, 08, 09, 11, 13, 19 only — 9 files, 11 insertions / 11 deletions |
| `## ` / `### ` headings | none touched (`git diff -U0 -- prompting-wizard/days \| grep '^[+-]#'` → empty) |
| `## Concept`, `## Before / After`, `## Rubric` edited | none — every edit is inside a `### Novice` or `### Working` body |
| Days 03, 04, 07, 10, 12, 14, 15, 16, 17, 18, 20, 21 | **not edited** — derivations below |
| Days 22–30, `rubrics.md`, `SKILL.md`, `assessment.md`, `tools/` | untouched |
| "be ready to" / "be able to" / "if asked" / "able to point" riders in 01–21 | none added; none present |
| Advanced tier whose added demand is a word or item budget in 01–21 | days 01, 06, 14 only — the three sanctioned exceptions, all pre-existing, none touched |
| Every Novice ends by sending a prompt | now true on days 06 and 08, which previously did not; days 07 and 14 produce a revision, which `SKILL.md:32` runs |

```
 prompting-wizard/days/01.md | 2 +-
 prompting-wizard/days/02.md | 2 +-
 prompting-wizard/days/05.md | 2 +-
 prompting-wizard/days/06.md | 4 ++--
 prompting-wizard/days/08.md | 2 +-
 prompting-wizard/days/09.md | 2 +-
 prompting-wizard/days/11.md | 2 +-
 prompting-wizard/days/13.md | 2 +-
 prompting-wizard/days/19.md | 4 ++--
```

---

## All 21 days

Anchors are Novice / Working / Advanced. "Imitator" is the anchor a **compliant** learner reaches by
copying the day's After — compliant, because a learner who disobeys the tier is not what the tier is
scored on.

| Day | Rubric | Anchors (after) | Imitator | Verdict |
|---|---|---|---|---|
| 01 | noun | 3 / 4 / 5 | 3 (was **5**) | **FAILED — fixed** |
| 02 | verb | 3 / 4 / 5 | 3 (was **5**) | **FAILED — fixed** |
| 03 | adjective | 3 / 4 / 5 | 2–3 | pass |
| 04 | adverb | 3 / 4 / 5 | 3 | pass |
| 05 | preposition | 3 / 4 / 5 | 3 (was **4** by smuggle) | **FAILED — fixed** |
| 06 | noun, verb, adjective, adverb, preposition | 2–3 / 4 / 5 | 2–3 (was **5**) | **FAILED — fixed** |
| 07 | same five (review day) | 1–3 / 4 / 5 | N/A — After supplies no prompt | pass |
| 08 | pronoun | 3 / 4 / 5 | 3 (was **5**) | **FAILED — fixed** |
| 09 | conjunction | 3 / 4 / 5 | 3 (was **4**, by smuggle) | **FAILED — fixed** |
| 10 | determiner | 3 / 4 / 5 | 3 | pass |
| 11 | numeral | 3 / 4 / 5 | 3 (was **5**) | **FAILED — fixed** |
| 12 | interjection | 3 / 4 / 5 | 3 | pass (closed by batch A round 2) |
| 13 | particle | 3 / 4 / 5 | 3 (was **4**) | **FAILED — fixed** |
| 14 | all eleven (review day) | 1–3 / 4 / 5 | N/A — After supplies no prompt | pass |
| 15 | role framing | 3 / 4 / 5 | 3 | pass (closed by batch B) |
| 16 | few-shot examples | 3 / 4 / 5 | 3 | pass (closed by batch B) |
| 17 | output schemas | 3 / 4 / 5 | 3 | pass (closed by batch B) |
| 18 | task decomposition | 3 / 4 / 5 | 3 | pass (closed by batch B round 2) |
| 19 | reasoning scaffolds | 3 / 4-or-5 / 5 | 3 (was **5**) | **FAILED — fixed** (inversion) |
| 20 | negative constraints | 3 / 4 / 5 | 3 | pass |
| 21 | context ordering | 3 / 4 / 5 | 3 | pass |

**Nine days failed. Nine were fixed.** Six were named by the reviewer (01, 02, 06, 08, 11, 13, 19 —
seven, counting day 19's inversion); days **05** and **09** were found by this sweep and were named
by nobody.

---

## Days edited

Each entry gives the before text, the after text, the anchor each tier now lands on, and the
imitate-the-After result after the fix.

### Day 01 — `rubrics.md#noun`. The reference implementation carried the flaw.

**The After** (`:21`): `Produce a five-bullet review of {{TASK}}, one bullet per correctness issue.`
Eleven words. Named unambiguously — a reader can describe the finished output — and economically:
every word pins something down. That is `noun` anchor **5**, "Named unambiguously and economically —
no words spent on the artifact beyond what pins it down." It also satisfies day 01's own Advanced
tier, "names the artifact unambiguously in under 15 words total", with four words to spare.

**The template** (`:33`) is `> Produce ________ for {{TASK}}.` — the After's own frame, with the
whole artifact phrase blanked and no truncation anywhere. There is no structural foreclosure at all:
filling the blank with the After's noun phrase reproduces the After's noun phrase exactly, and the
noun rubric scores nothing but the noun phrase. The old Novice instruction — "a noun phrase naming
**exactly** what you want back" — pointed at it: "exactly what you want back" is anchor 4's
describability restated as the demand.

**So it leaks, and the leak is anchor 5 from the bottom rung, against a Working tier at 4 and an
Advanced tier at 5.** It is milder than day 02's only in that the copy needs re-phrasing around
"for" instead of "of"; the substance transfers whole.

Two independent confirmations that this is not a new reading:

- `MASTER-FIX-PLAN.md`'s **rule 3** cites this very template as its worked illustration and concedes
  the range: it "admits 'a summary' (anchor 2) as readily as 'a five-bullet review' (**anchor 4**)".
  Rule 3 asks only whether a *lazy* learner can still score 2 — which they can, so rule 3 passes.
  The imitate test asks a different question, and the plan's own sentence answers it.
- **FIX-3.01**, filed in wave 1, states it outright: "The After (`:21`) does score 5, so **the ceiling
  is currently reachable only by imitation, not by instruction**." That is the wave-2D finding,
  written down in wave 1, and no wave acted on it because no wave had the test.

**Before** (`:31`):

> Fill the blank with a noun phrase naming exactly what you want back, then send the completed line as your prompt.

**After** (`:31`):

> Fill the blank with a noun phrase naming what you want back and what it covers — but not the count or the format, so a reader could still deliver two different things — then send the completed line as your prompt.

| Tier | Anchor | Anchor text (verbatim) | Why it lands there, and not a rung higher or lower |
|---|---|---|---|
| Novice | **3** | "The artifact is recognisable, but a reasonable reader could still deliver two different things." | The tier now states anchor 3's own clause as the demand, and negates anchor 4 by naming the two things that would satisfy it — the count and the format. **Not 4**: anchor 4 is "Someone reading only the prompt could describe the finished output", which the tier forbids in the same words its own Working tier uses. **Not 2**: "what it covers" pushes past the bare category anchor 2 illustrates ("a review", "some notes"). **Reaches 2** anyway if the learner writes only "a review" — rule 3's room to fail, unchanged. |
| Working (unedited) | **4** | "The artifact is named unambiguously. Someone reading only the prompt could describe the finished output." | Anchor 4's text, near-verbatim, as it has always been. |
| Advanced (unedited) | **5** | "Named unambiguously and economically — no words spent on the artifact beyond what pins it down." | "in under 15 words total. Precision without length is the constraint" — the sanctioned budget-as-verification-device for the economy clause that *is* anchor 5. |

**Working leaves open:** the economy clause of anchor 5. **Left silent** — Working says nothing about
words spent, so a terse learner may reach 5. Permitted 4-or-5 shape.

**Imitate-the-After test, after the fix:** the After carries a count ("five-bullet") and a format
("one bullet per correctness issue"). Both are now forbidden by name, so a learner copying it is
visibly non-compliant, and a compliant imitator lands at **3**. The effort gradient also inverts back
the right way: writing "a review of the correctness issues" is less work than reproducing the After.

**Shape and voice preserved.** The tier is still one sentence, still opens "Fill the blank with a noun
phrase" and still closes "then send the completed line as your prompt". The template is untouched.
Only the qualifier between those bookends changed.

**Downstream days written against day 01's Novice shape** — the fill-a-blank-then-send form — are
days **02, 03, 05, 09, 10, 11, 13**. Of those, **02, 11 and 13** carried the same leak and are fixed
here; **05 and 09** carried a weaker smuggle-route version and are fixed here; **03, 04 and 10** are
sound, for the reasons given below. The flaw was in the exemplar, and it propagated to five of the
seven days that copied it.

### Day 02 — `rubrics.md#verb`

**The After** (`:21`): `Rank the correctness issues in {{TASK}} by blast radius, worst first.`
**The template** (`:33`): `> ________ the correctness issues in {{TASK}}, worst first.` — the After's
sentence minus its verb. Filling "Rank" costs one word and reproduces the After's verb, and the verb
is the only thing this rubric scores. The day's **own Advanced tier** certifies the result:
"check it against the nearest more specific verb in the same family — 'audit' against 'check',
**'rank' against 'order'**" — i.e. "rank" is the narrower member of its pair. Anchor **5**: "no verb
in the same family names it more narrowly." Working is at 4. Inverted.

Anchor transfer is total here: `verb` anchors 3, 4 and 5 are properties of the verb as written, with
no elicited referent, so the example's verb carries its anchor to any task.

**Before** (`:31`):

> Fill the blank with one verb naming what you want done, then send the completed line as your prompt.

**After** (`:31`):

> Fill the blank with one verb naming roughly what you want done — a verb loose enough that a nearby operation would satisfy your wording just as well, not the narrowest one you could find — then send the completed line as your prompt.

| Tier | Anchor | Anchor text (verbatim) | Why it lands there |
|---|---|---|---|
| Novice | **3** | "An operation is named, but a nearby operation would satisfy the same wording just as well." | Anchor 3's clause is now the demand, word for word, and the learner can apply it mechanically: could "list" or "summarise" satisfy this sentence? For "Rank … worst first" the answer is no, so the copy is non-compliant. **Not 4**: anchor 4 needs "exactly one operation named, and it is the operation wanted", which a verb admitting a nearby operation is not. **Not 5**: "not the narrowest one you could find" negates anchor 5's clause. **Reaches 2** on "handle" or "deal with" — room to fail preserved. |
| Working (unedited) | **4** | "Exactly one operation named, and it is the operation wanted, but expressed with a generic synonym ('check' instead of 'audit') where a more specific verb in the same family exists." | "exactly one verb, naming the operation you actually want rather than a family of operations like 'handle' or 'deal with'." |
| Advanced (unedited) | **5** | "Exactly one operation named, it is the operation actually wanted, and no verb in the same family names it more narrowly." | The same-family narrowness check, with the narrower verb required. |

**Working leaves open:** *"expressed with a generic synonym … where a more specific verb in the same
family exists."* **Left silent**, unchanged from batch A.

**Imitate-the-After test, after the fix:** a compliant imitator cannot use "Rank" — the tier's own
stated test rejects it — and lands at **3**.

### Day 05 — `rubrics.md#preposition`

Not named by the reviewer. Found by asking whether the template's *truncation* is a real foreclosure
or only an apparent one.

**The After** (`:21`): `Fix the correctness problems in {{TASK}}, for a reader who has not seen the
codebase, without introducing new dependencies.` **The template** (`:33`):
`> Fix the ________ problems in {{TASK}}, for ________.` — the After minus the exclusion. Batch A's
derivation is that "exclusion left implicit … is anchor 3's definition", and structurally that is
right for the scope blank. But the **audience blank is the last thing in the sentence and is
free-form**, and the After's text after "for " is one continuous tail: "a reader who has not seen the
codebase, without introducing new dependencies." A learner copying that tail into the second blank
lands all three relations — anchor **4**, level with Working. This is exactly the smuggling route
`wave2c-tiers.md` round 2 closed on day 22 ("the two lines … cannot ride down with the request").

**Before** (`:31`):

> Fill the blanks with a scope and an audience, then send the completed line as your prompt.

**After** (`:31`):

> Fill the blanks with a scope and an audience — those two only, with nothing ruled out — then send the completed line as your prompt.

| Tier | Anchor | Anchor text (verbatim) | Why it lands there |
|---|---|---|---|
| Novice | **3** | "Most of scope, audience and exclusion are set, but one relation is left implicit." | Two of three relations, and the third now foreclosed by name ("with nothing ruled out") rather than only by the template's shape. **Not 4**: anchor 4 opens "Boundaries, audience and exclusions are **all** set". **Reaches 2** if the scope blank is filled with something that bounds nothing. |
| Working (unedited) | **4** | "Boundaries, audience and exclusions are all set, but at least one could be satisfied two ways." | "all three, none left to the model's default." |
| Advanced (unedited) | **5** | "Boundaries, audience and exclusions all set so each admits exactly one reading — in what, for whom, without what." | "each worded so it admits exactly one reading — a reader looking for a second way to satisfy any one of the three should not find one." |

**Working leaves open:** *"but at least one could be satisfied two ways."* **Left silent**, unchanged.

**Imitate-the-After test, after the fix:** the After's third relation is now forbidden by name, so it
cannot ride into the audience blank. Compliant imitator: **3**.

### Day 06 — `rubrics.md#noun`, `#verb`, `#adjective`, `#adverb`, `#preposition`

The reviewer's finding is confirmed and is worse than stated: day 06 fails the imitate test **and**
has no rubric-visible separation between Novice and Working.

**Separation.** Before this batch, Novice ended with all five levers set (added one at a time) and
Working ended with all five levers set (in one sentence). The only stated difference — "without
writing five separate clauses stitched together" — is a property of **sentence structure**, which
none of the five cited rubrics measures. Batch A's own report says so in its wave-3 notes:
`days/06.md:31` "asks for all five levers with no quality bar, so where it lands depends more on the
learner than on the tier", and it recommended exactly the fix applied here. FIX-2.05 moved the
economy sentence out of Working and never examined Novice; economy is `noun` anchor 5 and belongs to
Advanced, so the separation had to come from anchor 4's own content instead.

**Imitation.** The After (`:21`) — `Rank the correctness issues in {{TASK}} into a blunt, jargon-free
list, exhaustively, for a reader new to the codebase.` — is twenty words with, in the day's own
gloss, "every word above doing exactly one lever's job". That is `noun` anchor 5 and the Advanced
tier's demand minus the arithmetic. The old Novice, whose end state was "all five levers set", did
not forbid producing it.

**Before** (`:31`, Novice):

> Take a one-line prompt for {{TASK}} with none of the five levers set, then rewrite it adding one lever at a time — noun, verb, adjective, adverb, preposition — checking after each addition that the sentence still reads naturally.

**After** (`:31`):

> Take a one-line prompt for {{TASK}} with none of the five levers set, then rewrite it adding one lever at a time — noun, verb, adjective, adverb, preposition — using the first word that comes to hand for each and checking only that the sentence still reads naturally, so someone reading your finished prompt still could not describe the artifact it produces. Send that version.

**Before** (`:35`, Working):

> Write a single prompt for {{TASK}} that sets all five levers — noun, verb, adjective, adverb, preposition — without writing five separate clauses stitched together.

**After** (`:35`):

> Write a single prompt for {{TASK}} that sets all five levers — noun, verb, adjective, adverb, preposition — without writing five separate clauses stitched together, and so that someone reading only your prompt could describe the finished artifact.

| Tier | Anchor | Anchor text (verbatim) | Why it lands there |
|---|---|---|---|
| Novice | **2–3** | noun 3: "The artifact is recognisable, but a reasonable reader could still deliver two different things." | "the first word that comes to hand for each" is the anchor-3 target *stated* rather than emergent, and the closing clause negates noun anchor 4 in anchor 4's own words. **Not 4 or 5** on noun. On `adverb` a bare manner word with no measure is anchor 2, and on `adjective` a decorative quality is anchor 2 — which is why the band is 2–3 rather than a single rung, as batch A already recorded. |
| Working | **4** | noun 4: "The artifact is named unambiguously. Someone reading only the prompt could describe the finished output." | Anchor 4's clause is now *stated* — the same sentence day 01's Working carries — instead of being hoped for. This is what makes the rise from Novice visible to a cited rubric. |
| Advanced (unedited) | **5** | noun 5: "Named unambiguously and economically — no words spent on the artifact beyond what pins it down." | "under 40 words total, with every word doing one lever's job and none spent on anything else" — the CONFLICT-14 / rule-1 budget exception, unchanged. |

**Working leaves open:** noun 5's economy clause and adjective 5's wording-precision clause. **Left
silent** — Working asks that each lever be set and the artifact be describable, never that no word be
spent beyond what pins it down.

**Rule 4** is also satisfied for the first time: the old Novice ended on a check step and named no
artifact to hand over. "Send that version." was added, as batches A and B did on days 04, 14, 18
and 19.

**Imitate-the-After test, after the fix:** the After is describable and economical, both now
forbidden at Novice. Compliant imitator: **2–3**.

### Day 08 — `rubrics.md#pronoun`

The reviewer's finding is confirmed, and there is a second, unreported half: this day fails the
imitate test too.

**The reviewer's half.** The old Novice replaced *"the pronoun"* — singular, the one the seed carries
— with its noun phrase. Do that and every reference resolves, which is anchor **4** at least, and
anchor 3 ("Exactly one pronoun still requires the reader to guess; the rest resolve") is vacated by
instruction. Batch A's defence — real prompts carry several unbound pronouns so one survives — is a
statement about the learner's raw material, not about the tier, and the tier is what is scored. The
seed at `:17` is "Look at this and fix it", which carries exactly two; fix "the pronoun" and one
remains, fix both and nothing does.

**The unreported half.** The After (`:21`) is `Read the diff below. Fix the null-handling bug it
introduces in the payment handler.` Its single pronoun "it" resolves to "the null-handling bug", the
nearest preceding noun phrase — anchor **5** verbatim. Its shape (quote the material, then bind one
pronoun to the noun immediately before it) is trivially reusable on any task, and Working is mandated
down to 4 ("even if the reader has to look back a sentence or two"). Inversion.

**Before** (`:31`):

> Take a prompt for {{TASK}} that uses a pronoun with no antecedent, then rewrite it by replacing the pronoun with the exact noun phrase it should have meant.

**After** (`:31`):

> Take a prompt for {{TASK}} that uses at least two pronouns with no antecedent, then rewrite it by replacing all but one of them with the exact noun phrase each should have meant — leaving exactly one pronoun that still requires the reader to guess — and send the rewritten prompt.

| Tier | Anchor | Anchor text (verbatim) | Why it lands there |
|---|---|---|---|
| Novice | **3** | "Exactly one pronoun still requires the reader to guess; the rest resolve." | Anchor 3's clause is now the mandated end state, in the anchor's own words. **Not 4 or 5**: both open "Every reference resolves inside the prompt or to a quoted block", which the surviving unbound pronoun contradicts. **Not N/A**: the rubric's not-applicable rule fires only when the task has no instance of the property; a pronoun requiring a guess is an instance, so the degenerate N/A the reviewer feared is now impossible by construction. **Reaches 2** if the learner leaves two unresolvable ("More than one reference is unresolvable"). |
| Working (unedited) | **4** | "Every reference resolves inside the prompt or to a quoted block, but at least one antecedent sits more than a sentence away from its pronoun." | "even if the reader has to look back a sentence or two to find it" — the distance explicitly tolerated. |
| Advanced (unedited) | **5** | "Every reference resolves inside the prompt or to a quoted block, and each pronoun's antecedent is the nearest preceding noun phrase." | Nearest-preceding-noun-phrase, plus "Keep the pronouns — replacing them with nouns is not the exercise", which forbids the vacuous escape. |

**Working leaves open:** *"but at least one antecedent sits more than a sentence away from its
pronoun."* **Left silent** (in fact licensed), unchanged from batch A.

**Imitate-the-After test, after the fix:** the After resolves every reference; the tier now requires
exactly one that does not. Compliant imitator: **3**. Rule 4's send step was also added — the old
tier had none.

### Day 09 — `rubrics.md#conjunction`

Not named by the reviewer. Same class as day 05.

**The After** (`:23`): `Update {{TASK}}. If the input is empty, return an empty result rather than
erroring; otherwise process every row.` **The template** (`:35`):
`> Update {{TASK}}. If ________, ________.` FIX-2.08 removed the fallback blank, and batch A treated
the removal as the foreclosure. But the outcome blank is the last thing in the sentence and is
free-form, and the After's text after "If the input is empty," is one continuous tail ending in the
`otherwise` clause. Pasting the tail is *less* work than composing an outcome, and it lands condition
+ outcome + fallback — anchor **4**, level with Working.

**Before** (`:33`):

> Fill the blanks with a condition and its outcome, then send the completed line as your prompt.

**After** (`:33`):

> Fill the blanks with a condition and its outcome — the outcome only, with no fallback for everything the condition doesn't match — then send the completed line as your prompt.

| Tier | Anchor | Anchor text (verbatim) | Why it lands there |
|---|---|---|---|
| Novice | **3** | "Branches and conditions are named, but the fallback (the otherwise) is missing." | Anchor 3's clause, now stated rather than merely unscaffolded, with anchor 4's "and its fallback" negated in the anchor's own word. **Reaches 2** if the outcome is vague ("handle it") — "One branch is acknowledged but its condition or its outcome is missing." |
| Working (unedited) | **4** | "Each branch stated with its condition and its fallback, though the wording leaves the order of checks ambiguous." | "one condition, its outcome, and an explicit fallback for everything else." |
| Advanced (unedited) | **5** | "Each branch stated with its condition and its fallback, in an order that resolves without ambiguity." | "two branches … ordered so a reader checks them in a fixed sequence with no overlap between them" — the only tier on which check order can be tested at all. |

**Working leaves open:** *"though the wording leaves the order of checks ambiguous."* **Left silent**,
unchanged. **OPEN-3.01 is untouched and still open** — this batch does not rule on whether a single
branch plus fallback satisfies anchor 5's ordering clause vacuously; the Novice fix is independent of
that ruling either way, and FIX-3.21(d) records the dependency.

**Imitate-the-After test, after the fix:** the After's `otherwise` clause is now forbidden by name.
Compliant imitator: **3**.

### Day 11 — `rubrics.md#numeral`

**The After** (`:23`): `Give me exactly three options for {{TASK}}, each under 40 words, ranked by
cost.` **The template** (`:35`): `> Give me ________ options for {{TASK}}, each ________.` — the
After minus its two bounds. Filling "exactly three" and "under 40 words" gives an exact count and an
exact length: anchor **5**, "every bound is an exact count or length, checkable without judgement",
against a Working tier that asks only for "a number instead of a vague quantifier" (anchor 4).
Inversion, exactly as reported. Batch A removed the *pre-written* "exactly" and "under ___ words" but
left the bounds merely *permitted* to be vague; permission is not foreclosure, which is the lesson of
day 22's round 2.

**Before** (`:33`):

> Fill the blanks with how many you want and how long each should be, then send the completed line as your prompt.

**After** (`:33`):

> Fill the blanks with how many you want and how long each should be — a number for the count, and words rather than a number for the length ("fairly short", "a paragraph or so") — then send the completed line as your prompt.

| Tier | Anchor | Anchor text (verbatim) | Why it lands there |
|---|---|---|---|
| Novice | **3** | "Every countable dimension is bounded, but at least one bound is vague enough to need judgement ('a few', 'several')." | Both dimensions arrive bounded, and exactly one is guaranteed vague. Anchor 3, clause for clause. **Not 4**: anchor 4 needs "every bound is a number". **Not 5**: same. **Reaches 2** if a blank is left doing no bounding work at all. |
| Working (unedited) | **4** | "Every countable dimension is bounded, and every bound is a number, but at least one is a range or an approximation rather than an exact count." | "bounds every countable dimension … with a number instead of a vague quantifier." |
| Advanced (unedited) | **5** | "Every countable dimension is bounded, and every bound is an exact count or length, checkable without judgement." | "an exact count or an exact length rather than a range or an approximation — no 'three to five', no 'about 40 words'." |

**Working leaves open:** *"but at least one is a range or an approximation rather than an exact
count."* **Left silent**, unchanged.

**Why the count keeps its number.** The alternative — mandating vagueness on both dimensions — would
have put Novice at anchor 3 too, but would have taught nothing, and would have risked anchor 2
("One quantity is given … but other countable dimensions are open") on any sloppy fill. Splitting the
two blanks lets the bottom rung practise the day's actual move on the count while the length holds
the tier down, and it makes copying "each under 40 words" visibly non-compliant.

**Imitate-the-After test, after the fix:** an imitator may still copy "exactly three" — that is
compliant and does not lift the score, because the length bound is mandated vague. Compliant
imitator: **3**.

### Day 13 — `rubrics.md#particle` — with one disagreement with the reviewer

**The After** (`:21`): `Look up each external call in {{TASK}} and check it against its documented
contract.` **The template** (`:33`): `> ________ each external call in {{TASK}} and check it against
its documented contract.` — the After minus two words. Filling "Look up" reproduces the After
verbatim, and the tier is scored on the phrasal verb alone.

**Where I disagree.** The reviewer says the day's own gloss "certifies that particle as load-bearing
— anchor 5". The gloss (`:23`) is "'Over' means skim; 'up' means retrieve and compare. Swapping one
word turned a glance into a check against documentation" — which certifies the *particle swap*
changes the task. That is `particle` anchor 4's positive content ("Each phrasal verb present **was
chosen deliberately**") plus half of anchor 5. Anchor 5 is conjunctive and its second half is "**no
plain verb would have served**", and batch A's derivation — which I checked against the file and
agree with — is that "look up" fails it: "consult the documentation for each external call" would
have served, which is why day 13's own Advanced tier makes the plain-verb substitution the test.
So the imitator lands at **4**, not 5.

**The finding stands regardless.** Anchor 4 from the bottom rung is a failure by batch C's stated
standard, it is level with Working rather than below it, and it costs two copied words against a
tier that asks the learner to think of a phrasal verb. Fixed.

**Before** (`:31`):

> Fill the blank with a phrasal verb naming what you want done, then send the completed line as your prompt.

**After** (`:31`):

> Fill the blank with the phrasal verb you'd reach for by habit rather than one whose particle you've chosen deliberately — close to right, with a small ambiguity a stricter synonym would remove — then send the completed line as your prompt.

| Tier | Anchor | Anchor text (verbatim) | Why it lands there |
|---|---|---|---|
| Novice | **3** | "The phrasal verb is close to right, but a stricter synonym would remove a small remaining ambiguity." | Anchor 3's clause is the demand, word for word. **Not 4**: anchor 4 opens "Each phrasal verb present **was chosen deliberately**", and the tier requires the opposite in the anchor's own word — and in the same vocabulary its own Working tier uses ("choosing its particle deliberately rather than by habit"). **Not 5**: anchor 5 needs the verb load-bearing, which a habitual choice is not. **Reaches 2** on a genuinely loose "look over" whose particle swap would change the task without the writer noticing. |
| Working (unedited) | **4** | "Each phrasal verb present was chosen deliberately, but at least one could be swapped for a plain verb without changing the task." | "choosing its particle deliberately rather than by habit: swapping the particle for a plausible alternative should visibly change the task" — deliberate choice, tested against other **particles** only. |
| Advanced (unedited) | **5** | "Each phrasal verb present is load-bearing and no plain verb would have served — swapping any particle changes the task." | Both tests: the particle swap **and** the plain-verb substitution. |

**Working leaves open:** *"but at least one could be swapped for a plain verb without changing the
task."* **Left silent**, unchanged.

**Imitate-the-After test, after the fix:** "look up" is the deliberate, tested choice the day itself
holds up; the tier now asks for the habitual one. Compliant imitator: **3**.

### Day 19 — `rubrics.md#reasoning-scaffolds` — the inversion

Confirmed, and it is the most serious of the nine.

**The After** (`:21`): `For {{TASK}}: list the assumptions the answer would depend on that aren't
stated in the material, **then** check each against what's actually given. Answer citing which of
those assumptions it relies on and whether each was confirmed.` The day's own gloss says "The rewrite
names **the two intermediates the answer actually depends on**" — so the After's set *matches*, and
the "then" fixes the order they are produced in. Both clauses of anchor **5**: "The reasoning steps
asked for match the ones the task requires, **in the order the task requires them produced**."

**The old Novice** said only "naming two or three specific things the answer depends on in place of
'step by step'". Batch A/B's derivation was that a fixed small count "leaves something out by
construction" — but that is a heuristic, not a guarantee, and the day's own After demonstrates a
two-item set that matches. Nothing in the tier said anything about order, and the After's ordering
clause is a reusable shape ("list X, then check each against Y") that transfers to any task. So an
imitating Novice reached **5**, above their own Working tier — the inversion.

**Working's half.** Working read "names the intermediates the answer actually depends on — no more,
no fewer — **in any order**." The reviewer reads that as pinning Working at anchor 4; batch B read it
as releasing the requirement. Both readings are available from the text, which is itself the problem.
The standing rule prefers silence to a mandate whenever the shortfall is **privative**, and anchor
4's shortfall here is an absence ("the prompt does not fix the order they are produced in"), so
silence is the correct form and the phrase is removed.

**Before** (`:31`, Novice):

> Write a "think step by step" prompt for {{TASK}}, then rewrite it, naming two or three specific things the answer depends on in place of "step by step", and send the rewritten version.

**After** (`:31`):

> Write a "think step by step" prompt for {{TASK}}, then rewrite it, naming two or three specific things the answer depends on in place of "step by step" — two or three only, even if the answer depends on more, so at least one thing it depends on goes unnamed — and send the rewritten version.

**Before** (`:35`, Working):

> Write a prompt for {{TASK}} that names the intermediates the answer actually depends on — no more, no fewer — in any order.

**After** (`:35`):

> Write a prompt for {{TASK}} that names the intermediates the answer actually depends on — no more, no fewer.

| Tier | Anchor | Anchor text (verbatim) | Why it lands there |
|---|---|---|---|
| Novice | **3** | "Some intermediate steps are named, but one that the task actually depends on is missing." | Anchor 3's clause is now mandated rather than hoped for. **Not 4**: anchor 4 opens "The reasoning steps asked for **match** the ones the task requires", and the tier guarantees they do not. **Not 5**: anchor 5 is conjunctive on that same set-match, so ordering cannot lift the tier — which is precisely what closes the inversion, since an imitator may copy the After's "then" and still score 3. **Reaches 2** if the named things are generic ("the intermediate steps expected aren't named"). |
| Working | **4**, 5 by learner | "The reasoning steps asked for match the ones the task requires, but the prompt does not fix the order they are produced in." | The set-match is anchor 4's positive content and the whole of what the tier asks. The ordering shortfall is now **silent**: a learner who volunteers an order reaches 5, which is the permitted 4-or-5 shape used on days 14, 16, 17, 20 and 28. |
| Advanced (unedited) | **5** | "The reasoning steps asked for match the ones the task requires, in the order the task requires them produced." | "states in the prompt the order they must be produced in — which comes first, and which cannot start until an earlier one is done." Ordering is the sole 4→5 discriminator after FIX-1.17, and it lands in the prompt text. |

**Imitate-the-After test, after the fix:** a compliant imitator may reproduce the After's two-step
ordered shape and must still leave one dependency unnamed, so anchor 4's set-match fails and anchor 5
with it. Compliant imitator: **3**. **Ladder: 3 / 4 / 5, strictly rising, inversion closed.**

---

## Days not edited — derivations

Every day below was run through the same test and passed. Each entry names the After's anchor, the
compliant imitator's anchor, and the mechanism that holds the imitator down.

### Day 03 — `rubrics.md#adjective`. Imitator: **2–3**.

The template is the After minus its two adjectives, so structurally this is day 02's shape. It passes
on **anchor transfer**. `adjective` anchors 3, 4 and 5 are all relative to an elicited fact — "the
qualities **the writer names** as rejection-triggers" — so copying "blunt, jargon-free" onto a
different recurring task does not make them that writer's rejection-triggers. Anchor 4 requires every
one of the writer's triggers to be present "and no others"; a borrowed pair satisfies that only by
coincidence, and the ordinary result is anchor 3 ("one is in the prompt and a second is not") or 2.
The effort gradient is flat, not inverted: two borrowed words cost the same as two of your own.
Anchor 5's second clause (wording precision) *is* textual and does transfer, but anchor 5 is
conjunctive with anchor 4's elicited clause, so it cannot lift the score alone. A diligent
non-imitating learner may reach 4 — the permitted 3-or-4-by-learner shape, per day 23.

There is also no smuggle route: the second blank sits *before* "summary", so the After's trailing
"that a new joiner could act on" cannot be pasted into it grammatically.

### Day 04 — `rubrics.md#adverb`. Imitator: **3**.

The rare case where the After is itself an anchor-3 prompt, so imitating it is compliant *and*
correct. `Review {{TASK}} exhaustively for correctness, then for style in three sentences at most…`
attaches a measure to the style pass and none to the correctness pass — "exhaustively" is, in the
day's own gloss, "an open-ended, thorough pass". That is anchor 3 exactly: "Depth or manner is set
for part of the task, but another part is left to guess." The three-blank template maps onto the
After one-to-one and produces the same rung. (Note that FIX-3.02 proposes attaching a measure to
"exhaustively" in the After; if wave 3 applies it, **this derivation must be re-run** — the After
would move to anchor 4 or 5 and the template would need the same treatment days 02 and 11 got.
Recorded here rather than in the plan because FIX-3.02 already exists and this is a consequence of
it, not a new fix.)

### Day 07 — the five levers, review day. Imitator: **N/A**.

`## Before / After` is tutor instruction, not a worked prompt: "The tutor does **not** supply a
rewrite yet. The learner attempts their own rewrite first." There is nothing to imitate. Novice sits
in the review-day 1–3 band (one lever rewritten in, the other four left as the learner's original had
them); Working is 4; Advanced is 5. The tier produces a revision, so rule 4 is satisfied without a
send clause, exactly as `MASTER-FIX-PLAN.md`'s rule 4 says of this day.

### Day 10 — `rubrics.md#determiner`. Imitator: **3**.

The strongest structural foreclosure in the course, and worth naming as the pattern the other
template days should have used. The After is `Fix every correctness issue in {{TASK}}. Leave **each**
style issue alone.` The template is `> Fix ________ correctness issue in {{TASK}}. Leave style issues
alone.` — the second bindable noun sits in **fixed text the learner is not filling**. An imitator can
copy "every" into the blank and still leaves "style issues" bare, which is anchor 3 word for word
("one noun is left bare where swapping 'the' for 'any' would change what gets done"). Reaching 4
requires editing outside the blank, which is not what the tier asks. No smuggle route exists because
the free text follows the blank in a *separate sentence*.

### Day 12 — `rubrics.md#interjection`. Imitator: **3**.

Closed by batch A round 2, which found this exact defect class before the test had a name. The Novice
tier mandates "as a single paragraph … marked IMPORTANT: where it sits — inline in the paragraph,
**not moved and not on a line of its own**". The After moves the marked instruction to the end;
copying it violates "not moved", and reaching anchors 4 or 5 additionally requires the own-line
formatting the tier forbids in those anchors' own words.

### Day 14 — all eleven levers, review day. Imitator: **N/A**.

Same as day 07: `## Before / After` is tutor instruction and supplies no prompt. Novice is 1–3 (three
levers rewritten in, eight left exactly as they are, and the version sent), Working 4, Advanced 5.

### Day 15 — `rubrics.md#role-framing`. Imitator: **3**.

Already carries the negative clause, added by batch B: the tier sends the prompt "**without saying
anywhere in it what the output should include, exclude, or assume differently**" — anchor 4's
positive content negated in anchor 4's own words. The After does exactly that ("Flag anything you
wouldn't want your name attached to, and call out any assumption you can't verify"), so copying it is
visibly non-compliant.

### Day 16 — `rubrics.md#few-shot-examples`. Imitator: **3**.

Already carries the clause: "**both ordinary cases, neither one you'd hesitate over yourself**". The
After is a labelled boundary case plus a labelled failure case — anchor 5 — and both are forbidden by
name at Novice.

### Day 17 — `rubrics.md#output-schemas`. Imitator: **3**.

Already carries the clause: "**as a plain list of field names with no types and no example values**".
The After is a fenced JSON block with dummy values, types and an empty value shown — anchor 5 — and
the code block, the types and the values are each forbidden. This is also the day batch B identified
as the typographic-escape case: the fenced block, not the wording, was doing the anchor-4 work.

### Day 18 — `rubrics.md#task-decomposition`. Imitator: **3**.

Closed by batch B round 2, on this test in all but name: the After writes every seam as
`[Prompt 1's output, unedited]`, and the tier now reads "summarised in your own words **rather than
pasted** — a paraphrase at every seam, **not the actual text**", negating anchor 5's "verbatim" in
the rubric's own vocabulary and closing the partial reading with "at every seam".

### Day 20 — `rubrics.md#negative-constraints`. Imitator: **3**.

The After carries two exclusions, each citing its incident — anchor 5. The Novice tier mandates
"**one exclusion only, even if a second failure comes to mind**", and the one-exclusion state *is*
anchor 3 ("One real failure mode is excluded, but a second, equally likely one is not"). The
interesting sub-case: an imitator could copy a **single** one of the After's exclusions *with* its
incident clause, which looks like anchor 5's text ("each cites in the prompt the incident it
prevents"). It does not score 5, because anchors 4 and 5 both describe a *set* of exclusions and
anchor 3's distinguishing clause — the unexcluded second failure — is true by mandate. Same reasoning
batch B used to keep the tier off anchor 4.

### Day 21 — `rubrics.md#context-ordering`. Imitator: **3**.

Two independent reasons. The material is the learner's own 200+ words, not the After's, so there is
nothing to copy; and the tier mandates "**leaving every constraint exactly where it falls**", which
the After's grouped `Constraints:` block violates.

---

## Disagreements with the reviewer

Two, both recorded with evidence. Neither changes what was fixed.

1. **Day 13 lands the imitator at anchor 4, not anchor 5.** The reviewer says the day's gloss
   "certifies that particle as load-bearing — anchor 5". The gloss certifies that swapping the
   *particle* changes the task, which after FIX-1.12 is anchor **4**'s content ("chosen
   deliberately") — settled anchor 5 additionally requires that "**no plain verb would have
   served**", and "consult the documentation for each external call" serves. That is batch A's
   reading, it is why day 13's Advanced tier exists in its current form, and I checked it against the
   file rather than the plan (whose FIX-1.12 / FIX-2.12 quotations of anchor 4 are pre-wave-1 and
   wrong — see batch A's discrepancy (a)). The tier still failed and is still fixed; only the
   severity label changes.

2. **Day 08's defect is larger than reported.** The reviewer frames it as an anchor-3 vacancy created
   by the Novice tier's own instruction, with an N/A risk. Both are real. But the day also fails the
   imitate test on its own terms: the After binds its single pronoun to the nearest preceding noun
   phrase, which is anchor **5** verbatim, and the shape is reusable on any task. The fix closes both
   halves with one clause, and the N/A risk is closed by construction rather than by argument about
   what real prompts contain.

I did **not** disagree with the reviewer on days 02, 11, 19 or 06 — all four verify exactly as
reported, and day 19's inversion is the most serious of the nine.

## Two failures nobody named

**Days 05 and 09.** Both were cleared by batches A and B on the ground that the Novice *template* had
been truncated — day 05's exclusion blank and day 09's fallback blank were removed by FIX-2.04 and
FIX-2.08 respectively — so the missing relation could not be filled in. That is true of the blanks
and false of the sentence: on both days the last blank is free-form and sits at the end, and on both
days the After's corresponding text is one continuous tail that ends in the missing relation. Pasting
the tail is *less* work than composing the shorter answer, which is the effort-gradient failure
exactly. This is the defect batch C's round 2 found on day 22 — "the unit the tier counted was not
the unit the rubric counts" — in its other form: the *shape* the tier counted was not the shape the
learner types. Both closed by naming the forbidden relation in the tier text.

## Departures from literal plan text, non-substantive

Recorded because the standing convention is to record every deviation, not only the consequential
ones. Neither changes an anchor.

- **`days/06.md:31`** — rule 4's send step ("Send that version.") added, as batches A and B did on
  `days/04.md:31`, `14.md:29`, `18.md:41`, `19.md:31`, `22.md:37`, `24.md:31`, `26.md:31,35` and
  `28.md:34`. No plan entry proposes text for this line.
- **`days/08.md:31`** — same addition ("and send the rewritten prompt"). FIX-2.07 proposes no text
  for the Novice tier at all; it addresses Working and Advanced only.

Day 07's Novice was inspected for the same gap and left alone: it produces a rewrite
("rewrite only that lever in"), and `MASTER-FIX-PLAN.md`'s rule 4 cites it as the example of a tier
that satisfies the rule without a send clause.

## Wave-3 entry filed in `MASTER-FIX-PLAN.md`

**FIX-3.21 — Days 1, 2, 5, 6, 8, 9, 11, 13, 19: the concept states as universal the thing the rebuilt
Novice tier now mandates as absent** (medium; nine sub-items graded individually, seven mandated and
two tracking-only). Filed as a single entry rather than nine because every sub-item is the same
collision class as FIX-3.11/3.12/3.13/3.16/3.17/3.18 and takes the same resolution — reframe the
concept's absolute as what the upper rungs add, in day 29's self-cap shape.

Mandated: **(a) day 2** `:9,:11`, **(b) day 5** `:11`, **(c) day 8** `:11`, **(d) day 9** `:9,:13`,
**(e) day 11** `:13`, **(f) day 13** `:9,:11`, **(g) day 19** `:11`. Tracking only: **(h) day 1**,
which has no collision today but **constrains FIX-3.01** — its proposed "in as few words as pin it
down" is `noun` anchor 5's economy clause and must be scoped to the Advanced rung, not taught to a
Novice tier now foreclosed below anchor 4; and **(i) day 6**, which records that `:31` now mandates
"the first word that comes to hand" and `:35` now carries anchor 4's describability clause.

Sub-items (b) and (d) are declared as **pre-existing** collisions that wave 2D only made explicit —
FIX-2.04 and FIX-2.08 created them — rather than as new damage. Sub-items (e), (f) and (g) are
genuinely new.

The wave-3 file list is updated from **16 to 21 day files** (`days/02.md`, `05`, `09`, `11`, `13`
added; `08` and `19` gain a second, independent entry; `01` and `06` were already listed), the
counting convention paragraph is unchanged and still governs, and the wave-3 checkpoint gains
**item 18**, which requires the seven mandated sub-items to have landed, the two tracking-only ones to
have been checked, and — explicitly — **no `## Before / After` on days 1, 2, 5, 6, 8, 9, 11, 13 or 19
to have been edited**, since each is the worked example every derivation above is measured against.

## The pattern section is stale, in more places than four

Not fixed — `MASTER-FIX-PLAN.md`'s "The correct-tier pattern" is a wave-0 artifact and the brief says
the file beats the plan. Recorded so the next reader does not inherit a dead citation. Beyond the
four the brief names:

- **Rule 1's day-23 citation** quotes an Advanced tier reading "whose stop condition is
  **un-gameable**"; `days/23.md:39` now reads "State one way a model could satisfy it without doing
  the real work, then rewrite the condition so that shortcut no longer counts as done."
- **Rule 2's day-15 illustration** quotes a Working tier ("name at least two things the output does
  because of the role") that batch B round 2 replaced, and an anchor-4 shortfall ("the mechanism is
  only implied, not stated") that is not the settled wording.
- **Rule 2's day-08 anti-pattern** quotes `rubrics.md:72` as "the resolution takes a re-read to
  confirm". FIX-1.06 replaced that row; settled anchor 4 reads "at least one antecedent sits more
  than a sentence away from its pronoun", and day 08's Working tier now *licenses* the distance
  rather than negating it — so the day cited as the anti-pattern is no longer an instance of it.
- **Rule 3's day-01 illustration** is the one this batch acted on: it concedes the template "admits …
  'a five-bullet review' (anchor 4)" and treats that as acceptable because a lazy learner can still
  score 2. Both halves are true; the imitate test is a different question and the plan never asked
  it.
- **The pattern table's day-01 row** (3 / 4 / 5) survives this batch unchanged — but it survived by
  repair, not by having been right.

## Nothing was stopped on

Three candidates were considered and resolved rather than escalated.

- **Day 01 is the pattern's own exemplar and I changed it.** The brief authorises the fix if the leak
  is genuine and requires the finding be stated plainly, which the day-01 section does. The
  constraint that its shape and voice not change is met: same opening, same closing, same template,
  one added qualifier. Nineteen days were modelled on it and five of the seven that copied its
  fill-a-blank form inherited the flaw, which is recorded above and is the strongest argument that
  the fix belonged at the exemplar rather than only at the copies.
- **Day 03 looks like day 02 and is not.** Both templates are the After minus the blanks. They differ on
  anchor transfer, which is the criterion batch C used to clear days 23 and 25, and the derivation is
  written out in full above so a reviewer can overrule it cheaply.
- **Day 06's Working tier was edited although the reviewer only flagged the Novice/Working gap.**
  Lowering Novice alone would have left the two tiers separated by a property no cited rubric can
  see. Stating anchor 4's describability clause in Working is the minimum that makes the rise
  visible, and it is the same sentence day 01's Working has always carried.
