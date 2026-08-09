# Wave 2, batch A — tier ladders for days 02–13

Scope: `prompting-wizard/days/02.md` … `days/13.md`, `## Exercise` tier bodies only.
Anchors quoted below are the **settled** text of `prompting-wizard/rubrics.md` as of this commit,
re-derived from the file, not from the plan's line numbers.

## Verification

| Check | Result |
|---|---|
| `python3 tools/validate.py --complete` | `ok`, exit 0 |
| `python3 -m unittest discover -s tools` | 103 tests, OK (no test file touched) |
| `git diff --stat` | days 02–13 only, 12 files, 31 insertions / 31 deletions |
| `### `/`## ` headings | none touched (`git diff -U0 \| grep '^[+-]#'` → empty) |
| "be ready to say" / "be able to say" / "be able to point" riders in 02–13 | none |
| Advanced tier whose added demand is a word or item budget | day 06 only (economy is the anchor-5 clause; rule 1 exception, CONFLICT-14) |

`git diff --stat`:

```
 prompting-wizard/days/02.md | 6 +++---
 prompting-wizard/days/03.md | 6 +++---
 prompting-wizard/days/04.md | 4 ++--
 prompting-wizard/days/05.md | 6 +++---
 prompting-wizard/days/06.md | 4 ++--
 prompting-wizard/days/07.md | 2 +-
 prompting-wizard/days/08.md | 4 ++--
 prompting-wizard/days/09.md | 4 ++--
 prompting-wizard/days/10.md | 8 ++++----
 prompting-wizard/days/11.md | 6 +++---
 prompting-wizard/days/12.md | 6 +++---
 prompting-wizard/days/13.md | 6 +++---
```

Days 01, 14–30 untouched. No edit outside a tier body.

---

## Day 02 — `rubrics.md#verb`

| Tier | Anchor | Anchor text | Why it lands there |
|---|---|---|---|
| Novice | **3** | "An operation is named, but a nearby operation would satisfy the same wording just as well." | The blank now reads "one verb naming what you want done" over `> ________ the correctness issues in {{TASK}}, worst first.` A lazy fill ("review", "list") names an operation a neighbour would satisfy equally. Not 4: nothing requires it be the operation actually wanted. Not lower by default, but "look at" still fits the frame, so anchor 1 remains reachable — rule 3 room to fail. |
| Working | **4** | "Exactly one operation named, and it is the operation wanted, but expressed with a generic synonym (\"check\" instead of \"audit\") where a more specific verb in the same family exists." | Demands one verb and the operation actually wanted, excluding only families ("handle", "deal with"). Not 5: see shortfall below. |
| Advanced | **5** | "Exactly one operation named, it is the operation actually wanted, and no verb in the same family names it more narrowly." | Adds the same-family narrowness check verbatim — "audit" against "check", "rank" against "order" — and requires the narrower verb be used. |

**Working leaves open:** *"expressed with a generic synonym ('check' instead of 'audit') where a more
specific verb in the same family exists."* The tier never asks whether a narrower verb in the same
family exists, so "check" complies and still scores 4. The previous Working explicitly banned
"check" — the anchor's own example — making anchor 4 unreachable.

## Day 03 — `rubrics.md#adjective`

| Tier | Anchor | Anchor text | Why it lands there |
|---|---|---|---|
| Novice | **3** | "Of the qualities the writer names as rejection-triggers, one is in the prompt and a second is not." | "Two qualities you want in the output" over a two-blank frame. The typical fill puts one real rejection-trigger and one decorative word in, leaving the second trigger out. Not 4: no demand that the set be complete or free of non-triggers. "good, professional" still lands at 2 — room to fail. |
| Working | **4** | "Every quality the writer names as a rejection-trigger is in the prompt, and no others are." | "The qualities you would reject the output for missing — usually two — and no others" is anchor 4 word for word, including the exclusion clause FIX-1.04 moved down from 5. |
| Advanced | **5** | "Every rejection-trigger is named and no others are, and each is worded specifically enough that a generic output visibly fails one." | Adds the sole remaining 4→5 discriminator, wording precision, and nothing else. |

**Working leaves open:** *"each is worded specifically enough that a generic output visibly fails
one."* Working says nothing about how the qualities are worded, so "blunt, actionable" stated loosely
complies and stays at 4. The old Working demanded that wording test and so sat at 5.

## Day 04 — `rubrics.md#adverb`

| Tier | Anchor | Anchor text | Why it lands there |
|---|---|---|---|
| Novice | **3** | "Depth or manner is set for part of the task, but another part is left to guess." | New frame `> Review {{TASK}} ________, and for ________ specifically, ________.` sets a manner word for the whole and a measure for **one named part** only. Not 4: no measure across the whole task. A bare manner word with no measure still lands at 2. |
| Working (unchanged) | **4** | "Depth and manner set with a measure attached across the whole task, but attached as a stated tolerance rather than a fixed figure, so two competent readers would land inside that tolerance rather than on the same length." | "Set clearly enough that you could predict **roughly** how long the output would be" is a stated tolerance across the task — anchor 4's operational form. |
| Advanced (unchanged) | **5** | "Depth and manner set with a measure attached to every part, so two competent readers would produce the same length and thoroughness." | Two depths for two parts, "and the prompt says which and by how much" — a measure on every part, as a figure. |

**Working leaves open:** *"attached as a stated tolerance rather than a fixed figure, so two competent
readers would land inside that tolerance rather than on the same length."* "Roughly how long" is
exactly a tolerance; the tier never asks for a fixed figure, and never asks for per-part coverage.

## Day 05 — `rubrics.md#preposition`

| Tier | Anchor | Anchor text | Why it lands there |
|---|---|---|---|
| Novice | **3** | "Most of scope, audience and exclusion are set, but one relation is left implicit." | Frame reduced to two blanks (`> Fix the ________ problems in {{TASK}}, for ________.`) — scope and audience set, exclusion left implicit. That is anchor 3's definition. |
| Working (unchanged) | **4** | "Boundaries, audience and exclusions are all set, but at least one could be satisfied two ways." | "All three, none left to the model's default" is presence of all three and nothing more. |
| Advanced | **5** | "Boundaries, audience and exclusions all set so each admits exactly one reading — in what, for whom, without what." | Rewritten to demand exactly that: "each worded so it admits exactly one reading — a reader looking for a second way to satisfy any one of the three should not find one." |

**Working leaves open:** *"but at least one could be satisfied two ways."* Working requires the three
relations be present and non-default; it never tests how many readings any of them admits. The
previously missing exclusion is now what Working adds over Novice, so demand rises at both steps.

## Day 06 — `rubrics.md#noun`, `#verb`, `#adjective`, `#adverb`, `#preposition`

| Tier | Anchor | Anchor text (noun / adjective, the two that carry 4→5 here) | Why it lands there |
|---|---|---|---|
| Novice (unchanged) | **3** | noun 3: "The artifact is recognisable, but a reasonable reader could still deliver two different things." | Adds one lever at a time with no quality bar beyond "the sentence still reads naturally", so each lever arrives at whatever setting comes first to hand. Generic fills ("clearly", "the code") still land at 2. |
| Working | **4** | noun 4: "The artifact is named unambiguously. Someone reading only the prompt could describe the finished output." | All five levers set deliberately in one integrated sentence rather than five stitched clauses. The economy sentence has been **removed** from this tier. |
| Advanced | **5** | noun 5: "Named unambiguously and economically — no words spent on the artifact beyond what pins it down." / adjective 5: "…each is worded specifically enough that a generic output visibly fails one." | "…in under 40 words total, with every word doing one lever's job and none spent on anything else." The 40-word budget is the **verification device** for the economy clause that literally *is* noun anchor 5 — the rule 1 exception (CONFLICT-14), not an off-rubric rider. |

**Working leaves open:** *"and economically — no words spent on the artifact beyond what pins it
down"* (noun 5). Working previously carried "Every word should be doing one lever's job", which is
that clause restated, putting Working at 5 on two of the day's five rubrics and leaving Advanced's
word count as a restatement. That sentence now sits only in Advanced.

## Day 07 — `rubrics.md#noun`, `#verb`, `#adjective`, `#adverb`, `#preposition` (model ladder; FIX-2.06 only)

| Tier | Anchor | Anchor text | Why it lands there |
|---|---|---|---|
| Novice (unchanged) | **1–3** | noun 3: "The artifact is recognisable, but a reasonable reader could still deliver two different things." | One lever named as missing and rewritten in; the other four stay as the learner originally left them, so the prompt sits wherever the original did on those. Review-day 1–3 band, per the pattern table. |
| Working (unchanged) | **4** | noun 4: "…Someone reading only the prompt could describe the finished output." | All five levers set, each checked explicitly against the original. |
| Advanced | **5** | noun 5: "…no words spent on the artifact beyond what pins it down." / adjective 5: "…each is worded specifically enough that a generic output visibly fails one." | The load-bearing-clause test, now with one added sentence naming **where** it is scored: "The artifact phrase and the quality words are where this bites hardest: neither may carry a word that isn't pinning something down." |

**Working leaves open:** the economy clause of noun 5 and the wording-precision clause of adjective 5
— Working asks only that each lever be *set*, never that no word be spent beyond what pins it down.

Per CONFLICT-13, `rubrics.md#token-economy` was **not** added to `days/07.md`'s Rubric line.

## Day 08 — `rubrics.md#pronoun`

| Tier | Anchor | Anchor text | Why it lands there |
|---|---|---|---|
| Novice (unchanged) | **3** | "Exactly one pronoun still requires the reader to guess; the rest resolve." | Takes a prompt with an unbound pronoun and replaces **that one** pronoun with its noun phrase. Nothing is said about the rest, so a real prompt typically keeps one still-guessable reference. Not 4: no requirement that *every* reference resolve. |
| Working | **4** | "Every reference resolves inside the prompt or to a quoted block, but at least one antecedent sits more than a sentence away from its pronoun." | "Every pronoun has exactly one possible antecedent inside the prompt or in a block you quote, **even if the reader has to look back a sentence or two to find it**" — the scope condition FIX-1.06 moved down to 4, with distance explicitly tolerated. |
| Advanced | **5** | "Every reference resolves inside the prompt or to a quoted block, and each pronoun's antecedent is the nearest preceding noun phrase." | Demands nearest-preceding-noun-phrase, and forbids the degenerate escape: "Keep the pronouns — replacing them with nouns is not the exercise." |

**Working leaves open:** *"but at least one antecedent sits more than a sentence away from its
pronoun."* The tier licenses that distance in so many words. The old Working negated it outright
("no re-reading required to confirm which one"), which is the rule-2 anti-pattern the plan quotes.
The old Advanced ("zero pronouns") scored 5 vacuously over an empty reference set — removed.

## Day 09 — `rubrics.md#conjunction`

| Tier | Anchor | Anchor text | Why it lands there |
|---|---|---|---|
| Novice | **3** | "Branches and conditions are named, but the fallback (the otherwise) is missing." | Frame reduced to `> Update {{TASK}}. If ________, ________.` — condition and outcome, no `otherwise`. A vague outcome still lands at 2. |
| Working (unchanged) | **4** | "Each branch stated with its condition and its fallback, though the wording leaves the order of checks ambiguous." | One condition, its outcome, and an explicit fallback for everything else. The fallback is now what Working *adds*, not what the scaffold already handed over. |
| Advanced (unchanged) | **5** | "Each branch stated with its condition and its fallback, in an order that resolves without ambiguity." | Two branches "ordered so a reader checks them in a fixed sequence with no overlap between them" — the only tier where check order can be tested at all. |

**Working leaves open:** *"though the wording leaves the order of checks ambiguous."* A single branch
fixes no check order and the tier never asks for one, so the ordering property anchor 5 requires is
untouched at Working.

## Day 10 — `rubrics.md#determiner`

| Tier | Anchor | Anchor text | Why it lands there |
|---|---|---|---|
| Novice | **3** | "Most nouns are bound, but one noun is left bare where swapping \"the\" for \"any\" would change what gets done." | Frame reduced to one blank: `> Fix ________ correctness issue in {{TASK}}. Leave style issues alone.` — "style issues" stays bare, and "any style issue" vs "the style issues" changes what is left alone. Previously **both** bindable nouns had blanks, so the least work on the day produced anchor 4–5. |
| Working | **4** | "Each noun is bound — the, a, each, every, any — but one binding could be read two ways without changing what gets done." | "Every noun is bound with a determiner chosen deliberately … none left bare" now matches anchor 4's "**Each** noun is bound". The old Working bound only "the two or three nouns that most affect scope", capping a compliant Working learner *below* a Novice one. |
| Advanced | **5** | "Each noun is bound — the, a, each, every, any — and swapping any determiner would change what gets done." | The swap test, with the corrective action stated: "If a swap changes nothing, that binding isn't doing work — rewrite it." |

**Working leaves open:** *"but one binding could be read two ways without changing what gets done."*
Working requires deliberate binding but never applies the swap test, so a determiner that changes
nothing when swapped complies and holds the prompt at 4.

## Day 11 — `rubrics.md#numeral`

| Tier | Anchor | Anchor text | Why it lands there |
|---|---|---|---|
| Novice | **3** | "Every countable dimension is bounded, but at least one bound is vague enough to need judgement (\"a few\", \"several\")." | `> Give me ________ options for {{TASK}}, each ________.` — both dimensions must be filled, but "a few" and "fairly short" fit as readily as "three" and "under 40 words". The pre-written "exactly" and "under ___ words" are gone, so the lazy fill no longer arrives numerically bounded. |
| Working (unchanged) | **4** | "Every countable dimension is bounded, and every bound is a number, but at least one is a range or an approximation rather than an exact count." | "Bounds every countable dimension … with a number instead of a vague quantifier" is anchor 4's positive content exactly. |
| Advanced | **5** | "Every countable dimension is bounded, and every bound is an exact count or length, checkable without judgement." | Rewritten to name the discriminator: "makes each bound an exact count or an exact length rather than a range or an approximation — no \"three to five\", no \"about 40 words\"". |

**Working leaves open:** *"but at least one is a range or an approximation rather than an exact
count."* "A number" admits "3–5 options" and "about 40 words", both of which comply with Working and
sit at 4.

## Day 12 — `rubrics.md#interjection` (was 5/5/5)

| Tier | Anchor | Anchor text | Why it lands there |
|---|---|---|---|
| Novice | **3** | "The critical instruction is marked, but the marker sits inline in a paragraph with other instructions rather than on a line of its own." | "Mark that instruction IMPORTANT: **where it sits, without moving it**" — the repositioning step that previously satisfied every clause of anchor 5 is gone. A learner who marks the wrong sentence lands at 2 ("attached to something other than the instruction the writer names…"). |
| Working | **4** | "The must-not-fail instruction is marked and stands alone rather than sitting mid-paragraph, but competes with one other marked item." | Two marked instructions, the must-not-fail one standing alone on its own line. Anchor 4 was previously **structurally impossible**: all three tiers mandated exactly one marker while anchor 4 requires a competing second. |
| Advanced | **5** | "Exactly one marker in the prompt, on the instruction the writer names as highest-stakes, standing alone as its own line." | Exactly one marker, on the instruction you'd be angriest to see ignored, standing alone, "Every other instruction carries no marker." |

**Working leaves open:** *"but competes with one other marked item."* Working **mandates** the
competing second marker, so anchor 5's "Exactly one marker in the prompt" cannot be reached from this
tier by any compliant learner. That is what makes anchor 4 the ceiling here rather than the floor.

The Advanced "be ready to say in one sentence why none of the other instructions needed one" rider is
deleted (SYS-2, rule 7). Working's "Say which of the two is the one that must not fail" is **not** a
rider of that class — it supplies the elicitation anchors 2, 4 and 5 all depend on ("the instruction
the writer names as…"), exactly as the rubric's fastest fix requires.

## Day 13 — `rubrics.md#particle`

| Tier | Anchor | Anchor text | Why it lands there |
|---|---|---|---|
| Novice | **3** | "The phrasal verb is close to right, but a stricter synonym would remove a small remaining ambiguity." | "A phrasal verb naming what you want done" over `> ________ each external call in {{TASK}} and check it against its documented contract.` — a habitual "look over" or "go through" fits, and a stricter synonym ("look up") would remove the ambiguity. Previously read "whose particle names the exact operation you want", which is anchor 4–5 from a scaffold. |
| Working | **4** | "Each phrasal verb present was chosen deliberately, but at least one could be swapped for a plain verb without changing the task." | "Choosing its particle deliberately rather than by habit: swapping the particle for a plausible alternative should visibly change the task" — deliberate choice, demonstrated against **other particles**. |
| Advanced | **5** | "Each phrasal verb present is load-bearing and no plain verb would have served — swapping any particle changes the task." | Both tests: swap the particle, and replace the whole phrasal verb with a plain verb; keep it only if both swaps change the task, "if the plain verb serves just as well, use the plain verb instead" — which is `days/13.md:11`'s own rule, and which FIX-1.01's N/A clause now covers. |

**Working leaves open:** *"but at least one could be swapped for a plain verb without changing the
task."* The tier tests the particle only against other **particles**, never against a plain verb, so
"look up each external call" complies at Working even though "consult the documentation for each
external call" would have served. The old Advanced changed nothing but the count (two phrasal verbs
instead of one) — SYS-2's item-budget variant, removed.

---

## Departures from the plan, and why

Seven. Each is a case where the plan entry conflicts with the brief's bar or with the settled
`rubrics.md`, and the plan entry loses.

1. **FIX-2.02 (day 03 Advanced) carries a rule-7 rider.** Its proposed text ends "For each, be able
   to point at the output it rules out." That explanation never enters the prompt and cannot be
   scored — the exact defect SYS-2 catalogues. Dropped. Anchor 5's content is fully carried by the
   surviving wording clause.

2. **FIX-2.12 (day 13 Working) carries the same rider** — "you should be able to say what the
   particle adds." Replaced with the particle-swap test. The plan's *Why* rejects the swap test on
   the grounds that it "forecloses anchor 4, whose defining feature is that only *cosmetic*
   substitutions exist" — but that reasons from the **pre-wave-1** anchor 4. Settled anchor 4 reads
   "Each phrasal verb present **was chosen deliberately**, but at least one could be swapped for a
   **plain verb**", so the particle-swap test is now anchor 4's positive content and the plain-verb
   test is the 4→5 discriminator. See discrepancy (a) below.

3. **Day 13 Novice, not addressed by the plan.** It read "a phrasal verb whose particle names the
   exact operation you want" — anchor 4–5 from a two-second fill, the identical defect FIX-2.01 fixes
   on day 02. Left alone the day would have been 4–5 / 4 / 5. Lowered to anchor 3 with day 02's
   wording.

4. **FIX-2.10 puts day 11's Novice at anchor 2** ("Removing both puts Novice at anchor 2"). That
   yields a 2/4/5 ladder with anchor 3 unoccupied, which the brief's bar forbids. Novice keeps two
   blanks but drops the pre-written "exactly" and "each under ___ words", so both dimensions arrive
   bounded and at least one may be vague — anchor 3.

5. **FIX-2.10 says "do not touch `:43`" (day 11 Advanced).** That instruction was written against the
   pre-FIX-1.09 anchor 4 ("awkward to verify without counting carefully"), for which "verifiable
   without judgement" *was* the discriminator. Against the settled anchor 4 ("a range or an
   approximation rather than an exact count") a prompt saying "3–5 options" satisfies the old
   Advanced text while sitting at 4. Advanced now names exact-count/exact-length directly.

6. **FIX-2.04 declares day 05's Advanced correct** via "in that order, and in no more words than the
   boundaries need". Word economy is scored by `noun`, `adjective` and `token-economy`, not by
   `preposition`; ordering is scored by `context-ordering` (day 21). Neither is `preposition`'s 4→5
   discriminator, and day 05 is not one of the rule-1 budget exceptions (01, 06, 14). Applied the
   plan's own stated fallback — the one-reading test — and removed both riders.

7. **FIX-2.03's replacement Novice for day 04 dropped "then send the completed line as your
   prompt."** Re-added (rule 4: every tier produces a sendable prompt), otherwise verbatim.

## Discrepancies between the plan's quoted anchors and the settled file

The file wins in both cases; wave 1 is settled.

- **(a) `particle` anchor 4.** FIX-2.12 and FIX-1.12 quote "Each phrasal verb present is
  load-bearing, but at least one plain verb would have served as well." The file reads "**Each
  phrasal verb present was chosen deliberately**, but at least one could be swapped for a plain verb
  without changing the task." The difference is load-bearing (pun intended): the settled text puts
  *deliberate choice* at 4 and reserves *load-bearing* for 5, which is what makes departure 2 above
  correct rather than a regression.

- **(b) `numeral` anchor 5.** FIX-1.09 says "Leave rows 1, 2 and 5 as written" and quotes row 5 as
  "Every countable dimension bounded, and the bounds checkable without judgement." The file reads
  "Every countable dimension is bounded, and **every bound is an exact count or length**, checkable
  without judgement." Row 5 was tightened in round 2; the added clause is precisely what departure 5
  above targets.

## Notes for wave 3 (not fixed here — concepts are out of scope)

- **`days/12.md:7`** still reads "Position matters as much as the word." FIX-1.10 deliberately made
  interjection anchor 4 **position-independent** to resolve the interjection/context-ordering
  contradiction, and anchor 5 now turns on exclusivity plus standing alone as its own line, not on
  where in the prompt that line sits. The concept's emphasis on position no longer matches what the
  rubric scores. The After (`:21`) and gloss (`:23`) are fine — FIX-1.10 was written to keep them.
- **`days/06.md:31`** (Novice) is the least crisp anchor-3 target in this batch: it asks for all five
  levers with no quality bar, so where it lands depends more on the learner than on the tier. No
  census finding covers it and the plan does not call for a change, so it is untouched. If wave 3
  revisits day 06, consider giving it an explicit "set each lever with the first word that comes to
  hand" framing so the anchor-3 target is stated rather than emergent.
- **`days/13.md:11`** ("If it didn't, use a plain verb instead") is now reproduced in the Advanced
  tier. That is deliberate — it is the anchor-5 discriminator — but it means a compliant Advanced
  learner may hand in a prompt with zero phrasal verbs, scored N/A under the preamble's
  not-applicable rule. Worth a sentence in the day's Concept if wave 3 touches it.

---

# Round 2 — the day 12 Novice formatting leak

Two edits, both tier body, both in scope. Days 02–11 and 13 were **not** touched this round
(`git diff --stat` for round 2 lists `days/04.md`, `days/12.md` and `MASTER-FIX-PLAN.md` only).

## The leak, and why round 1 missed it

Round 1's Novice closed the *positional* reading ("where it sits, without moving it") but said nothing
about **line breaks**. A five-sentence prompt written as five lines — an ordinary prompt shape, and
the very shape round 1's own Working tier presupposes when it says "standing alone on its own line" —
produces a marked instruction that is the only marker in the prompt, on the highest-stakes
instruction, standing alone as its own line. That is `interjection` anchor 5 clause for clause, from
the lowest tier. For any learner who happens to format that way the ladder read **5 / 4 / 5**, an
inversion, and the same class of defect FIX-2.11 was escalated to remove.

The paragraph reading was the intended one and the day's Before / After at `:17,21` writes the
five-sentence prompt as a single paragraph, so the day supports it — but the tier text never said it,
and the tier text is what the learner is given.

**Fixed at `days/12.md:31`:**

> Write a five-sentence prompt for {{TASK}} as a single paragraph, containing one instruction you'd be angriest to see ignored. Mark that instruction IMPORTANT: where it sits — inline in the paragraph, not moved and not on a line of its own — then send the completed prompt.

Two independent closures, deliberately belt-and-braces: "as a single paragraph" fixes the shape up
front, and "not on a line of its own" forecloses the own-line reading even if a learner ignores the
first. The clause now negates the *exact* words shared by anchors 4 and 5 — "stands alone",
"standing alone as its own line" — rather than the position, so there is no ordinary formatting under
which the completed prompt reaches either.

## Day 12 re-derived against `rubrics.md` `## Interjection`

| Tier | Anchor | Anchor text (verbatim from the file) | Why it lands there, and not a rung higher or lower |
|---|---|---|---|
| Novice | **3** | "The critical instruction is marked, but the marker sits inline in a paragraph with other instructions rather than on a line of its own." | The tier now instructs literally this: a single paragraph, marked where it sits, inline, not on a line of its own. **Not 4**: anchor 4 requires the instruction to "stand alone rather than sitting mid-paragraph", which the tier now forbids in as many words. **Not 5**: anchor 5 requires "standing alone as its own line", forbidden by the same clause. **Reaches 2** if the learner marks a sentence other than the one they name as the one they'd be angriest to see ignored — rule 3 room to fail, preserved. |
| Working | **4** | "The must-not-fail instruction is marked and stands alone rather than sitting mid-paragraph, but competes with one other marked item." | Two marked instructions, the must-not-fail one standing alone on its own line, plus one other marker. Every clause of anchor 4, including the competing item. **Not 5**: see shortfall below. **Not 3**: the critical marker no longer sits inline. |
| Advanced | **5** | "Exactly one marker in the prompt, on the instruction the writer names as highest-stakes, standing alone as its own line." | Exactly one marker, on the instruction you'd be angriest to see ignored, standing alone as its own line, "Every other instruction carries no marker" — all four clauses, nothing added. |

**Working leaves open:** *"but competes with one other marked item."* The tier **mandates** the second
marker, so anchor 5's opening clause — "Exactly one marker in the prompt" — is unreachable from this
tier by any compliant learner. Anchor 4 is Working's ceiling, not its floor.

Strictly rising, each anchor occupiable, no two tiers on the same anchor, and no ordinary formatting
choice moves any tier off its rung.

## Minor — `days/04.md:31`

"Fill **the blank**" governed a three-blank frame (inherited from FIX-2.03's replacement text).
Pluralised, and each blank named so the mapping to the frame is unambiguous:

> Fill the blanks with a manner word, the one part of the task where depth matters most, and a measure for that part only — then send the completed line as your prompt.

Anchor unchanged at **3** — "Depth or manner is set for part of the task, but another part is left to
guess" — since the measure is still explicitly scoped to one named part. Naming the blanks makes that
scoping harder to misread, if anything reinforcing the rung.

## Wave-3 entries filed in `MASTER-FIX-PLAN.md`

Both added after FIX-3.10, with the wave-3 file list and checkpoint updated to match.

- **FIX-3.11 — Day 12: reconcile the concept with the rebuilt tier ladder** (severity: high). Three
  collisions documented with current text and required direction: `:7` position (anchor 4 is
  position-independent after FIX-1.10 — but keep "Standing alone, the same sentence becomes the
  hardest thing to have missed", which is the property anchor 4 now measures); `:9` the one-marker
  absolute versus a Working tier that mandates two, with the `SKILL.md:30` single-tier-visibility
  consequence spelled out and the required reframing as a *scored way-station*; `:11` "move it or
  mark it" versus the Novice tier's "not moved". Carries an explicit **do not touch** on the Before /
  After and gloss at `:17,21,23`, and a note about the 200-word `## Concept` cap.
- **OPEN-3.01 — Day 9's Working tier may be scoreable at `conjunction` anchor 5** (question, not a
  fix). Logged with the anchor text, the tier text, and the reasoning: anchors 4 and 5 differ only by
  order-of-checks ambiguity, and a single condition plus fallback is one check whose order is
  trivially unambiguous, so day 9 is 3/4/5 only under the reading that anchor 5's ordering clause is
  *vacuous* rather than *satisfied* at one branch — a reading `rubrics.md` does not state. Two
  candidate resolutions recorded (rubric side, day side) with the trade-off, plus the contrast with
  `interjection`'s mirror-image defect that explains why this is a question rather than a fix. Marked
  **do not change the rubric — wave 1 is settled**, and added to the wave-3 checkpoint so it cannot
  be closed without a ruling.

## Round 2 verification

| Check | Result |
|---|---|
| `python3 tools/validate.py --complete` | `ok`, exit 0 |
| `python3 -m unittest discover -s tools` | 103 tests, OK |
| Round-2 diff scope | `days/04.md` (1 line), `days/12.md` (1 line), `MASTER-FIX-PLAN.md` — days 02–11 and 13 untouched |
| Day 12 ladder | 3 / 4 / 5, Novice admits no anchor-5 reading under any ordinary formatting |
| Headings | none touched |
