# Wave 2, batch B — tier ladders for days 14–21

Scope: `prompting-wizard/days/14.md` … `days/21.md`, `## Exercise` tier bodies only.
Every anchor quoted below is the **settled** text of `prompting-wizard/rubrics.md`, read from the
file. Where the plan's quoted anchor differs from the file, the file wins and the difference is
recorded under "Discrepancies".

## Verification

| Check | Result |
|---|---|
| `python3 tools/validate.py --complete` | `ok`, exit 0 |
| `python3 -m unittest discover -s tools` | 103 tests, OK (no test file touched) |
| `git diff --stat` | days 14–21 only, 8 files, 19 insertions / 19 deletions |
| `## ` / `### ` headings | none touched (`git diff -U0 -- prompting-wizard/days \| grep '^[+-]#'` → empty) |
| "be ready to" / "be able to say" / "be able to point" / "if asked" riders in 14–21 | **none** (grep clean; days 15, 19 and 20 each had one, all removed) |
| Advanced tier whose added demand is a word or item budget | **day 14 only** ("under 60 words total"; economy is literally noun-5 / adjective-5, CONFLICT-14 / rule-1 exception) |
| `## Concept` or `## Before / After` edited | none |

```
 prompting-wizard/days/14.md | 2 +-
 prompting-wizard/days/15.md | 4 ++--
 prompting-wizard/days/16.md | 6 +++---
 prompting-wizard/days/17.md | 4 ++--
 prompting-wizard/days/18.md | 4 ++--
 prompting-wizard/days/19.md | 6 +++---
 prompting-wizard/days/20.md | 6 +++---
 prompting-wizard/days/21.md | 6 +++---
```

Days 01–13 and 22–30 untouched. No edit outside a tier body.

---

## Day 14 — all eleven lever rubrics (review day)

| Tier | Anchor | Anchor text (the two that carry 4→5 here) | Why it lands there |
|---|---|---|---|
| Novice | **1–3** | noun 3: "The artifact is recognisable, but a reasonable reader could still deliver two different things." | Now produces a prompt: the eleven-lever inventory, then "rewrite **only those three** into the prompt, leaving the other eight exactly as they are, and send that version." Eight levers stay wherever the learner's original left them, so the prompt sits in the review-day 1–3 band — the same shape as day 07's Novice. **Not 4**: nothing requires the other eight be set at all. |
| Working (unchanged) | **4** | noun 4: "The artifact is named unambiguously. Someone reading only the prompt could describe the finished output." | "Revise their prompt so every one of the eleven levers is deliberately set" — presence and deliberateness across all eleven, nothing about words spent. |
| Advanced (unchanged) | **5** | noun 5: "Named unambiguously and **economically** — no words spent on the artifact beyond what pins it down." / adjective 5: "…each is worded specifically enough that a generic output visibly fails one." | "Sets all eleven levers **in under 60 words total**." The budget is the verification device for the economy clause that *is* noun anchor 5 — the rule-1 exception, one of the three days (01, 06, 14) where it is legitimate. |

**Working leaves open:** *"and economically — no words spent on the artifact beyond what pins it
down"* (noun 5) and adjective 5's wording-precision clause. Working asks only that each lever be
*set*. **Left silent** — the tier says nothing about economy, so a terse learner may reach 5.

T12 closed: the tier that previously produced nothing but a spoken inventory now produces the
artifact `SKILL.md:32` runs and `SKILL.md:34` scores.

## Day 15 — `rubrics.md#role-framing` (model ladder — repaired, not moved)

**Before wave 2B, against the settled anchors, this ladder read 4 / 4 / 4.** Wave 1's FIX-1.13 moved
anchor 4 to a *disjunctive, at-least-one, text-based* bar and anchor 5 to *role text says how*;
neither wave-1 nor wave-2 planning re-derived day 15 against that. Novice's closing clause was
anchor 4's positive content verbatim, and Advanced's "be ready to name both" was a rule-7 rider that
anchor 5 no longer credits. Two edits restore 3 / 4 / 5. **Round 2 revised the Working tier as well —
see the round-2 section below; the table row here is the round-1 state.**

| Tier | Anchor | Anchor text | Why it lands there |
|---|---|---|---|
| Novice | **3** | "The role implies a standard or a body of knowledge, but the prompt doesn't say which parts to draw on." | A role "with a concrete stake — something it's responsible for, something that happens if it's wrong", sent "**without saying anywhere in it what the output should include, exclude, or assume differently**." The stake implies the standard; the added clause forecloses anchor 4 in anchor 4's own words. **Reaches 1–2** if the learner writes "you are a world-class expert" — rule-3 room to fail preserved. |
| Working (round-1 state — **superseded in round 2**) | **3-or-4** | "The role text names **at least one** thing the output includes, excludes **or** assumes because of the role, but not how the role produces it." | Round 1 left this tier at "A reader should be able to name at least two things the output does because of the role" — an inference test against a text anchor, so a bare stance with a naming-free role text sat at **3**. Round 2 re-aimed it at the text. |
| Advanced | **5** | "The role text names what the output includes, excludes **and** assumes because of the role, **and says how the role produces each**." | "Whose role text names one thing the output includes, one it excludes, and one it assumes because of the role — and **says, in the prompt itself, how the role produces each of the three**." All three dimensions plus the mechanism, in the text, where `rubrics.md:5` can see it. |

**Working leaves open:** *"but not how the role produces it."* The tier never asks for the mechanism.
**Left silent** — it also never forbids it, so a learner who volunteers the mechanism reaches 5.

**Ladder, before and after: 3 / 4 / 5 → 3 / 4 / 5.** It lands where the census recorded it. The edits
undo a drift introduced by wave 1, they do not re-pitch the day. Filed as FIX-3.14 so wave 3 knows
the day's self-test and After are now the stale halves.

## Day 16 — `rubrics.md#few-shot-examples`

| Tier | Anchor | Anchor text | Why it lands there |
|---|---|---|---|
| Novice | **3** | "Examples show variety, but none demonstrates a boundary or a near-miss." | "Two examples that show different kinds of item — **both ordinary cases, neither one you'd hesitate over yourself** — each with a one-line reason." Variety without a boundary, stated in the day's own words for a boundary case (`days/16.md:9`, "the best boundary case is one you'd hesitate over yourself"). **Reaches 2** if the two examples are near-identical typical cases — room to fail. **Not 4**: the boundary case is forbidden here. |
| Working | **4** | "Examples cover the boundary case but not a genuine failure case." | "Two examples that disagree, one of them a **boundary case** — the case you'd hesitate over yourself." The boundary case arrives; the failure case is never asked for. |
| Advanced | **5** | "Examples cover the boundary case **and the failure case**." | "A boundary case, and a **failure case you have watched the model actually produce on this task** rather than one you invented. **Say in the prompt what it got wrong.**" The failure case is the whole 4→5 gap; the observed-and-stated bar makes it ungameable and lands it in the prompt text (rule 7). |

**Working leaves open:** *"but not a genuine failure case."* **Left silent** — anchor 4's shortfall is
an *omission*, so the tier simply does not ask for a failure case; a learner who adds one anyway
reaches 5, which is the permitted 4-or-5 shape.

## Day 17 — `rubrics.md#output-schemas`

| Tier | Anchor | Anchor text | Why it lands there |
|---|---|---|---|
| Novice | **3** | "Fields are enumerated, but types, order, or optionality are left unstated." | "Names every field the output must contain, **as a plain list of field names with no types and no example values**." Fields enumerated, everything else unstated. **Not 4**: anchor 4 opens "An exact structure is given" — a plain name-list with no types and no dummy values is not a structure. **Reaches 2** if the learner writes "as a table" and leaves the fields un-enumerated. |
| Working | **4** | "An **exact structure** is given, with one edge (e.g. empty values) **unaddressed**." | "Whose schema is a fenced code block **filled with dummy values**, naming every field, **its type, and the order the fields come in**." Exact structure; empty values never mentioned. |
| Advanced (unchanged) | **5** | "An exact structure given, which output can be **checked against mechanically**." | "Every field typed, **every optional value shown filled and shown empty**, no field left to prose description." Closing the empty-value edge is exactly what makes the structure mechanically checkable. |

**Working leaves open:** *"with one edge (e.g. empty values) unaddressed."* **Left silent** — the tier
neither requires nor forbids showing an empty value, so a thorough learner may reach 5.

## Day 18 — `rubrics.md#task-decomposition`

| Tier | Anchor | Anchor text | Why it lands there |
|---|---|---|---|
| Novice (round-1 state — **superseded in round 2**) | **3 on one branch, 5 on the other** | "Tasks are split into steps, but one step's output isn't a clean input to the next." | Round 1 read "summarised in your own words **or pasted, whichever is easier**". The summarised branch is anchor 3; the pasted branch is anchor 5, and it was the easier one. Round 2 removed the branch — see the round-2 section. |
| Working | **4** | "Work split so each step has one output, and the next step's input is the previous step's output **plus exactly one added instruction or re-explanation**." | "Each step's input is the previous step's output **plus exactly one line of added instruction. Nothing from the original task may be re-explained.**" Anchor 4's state, mandated exactly — see below. |
| Advanced (unchanged) | **5** | "…each step's input is **verbatim** the previous step's output — nothing added, nothing re-explained." | The only tier now demanding the verbatim seam, and its adversarial constraint (the last step must cite a detail that only survives an unparaphrased hand-off) becomes the *test* of that seam rather than an extra. |

**Working leaves open:** *"plus exactly one added instruction or re-explanation."* **Mandated**, not
silent: "exactly one line of added instruction". Anchor 4's shortfall here is a *positive state* — a
thing present in the seam — and the FIX-2.17 round-2 correction forbids "at most one", which admits
zero and therefore anchor 5. Anchor 4 is Working's ceiling, not its floor.
**Wave-3 entry filed: FIX-3.12** — `days/18.md:7` still reads "Splitting into three prompts **only
fixes this** if each step's input is exactly the last step's output", which the Working tier now
contradicts.

## Day 19 — `rubrics.md#reasoning-scaffolds`

| Tier | Anchor | Anchor text | Why it lands there |
|---|---|---|---|
| Novice | **3** | "Some intermediate steps are named, but one that the task actually depends on is missing." | "Naming **two or three** specific things the answer depends on in place of 'step by step'." A fixed small count over an unbounded dependency list leaves something out by construction. **Reaches 2** if the named things are generic. **Not 4**: no set-match is demanded. |
| Working | **4** | "The reasoning steps asked for match the ones the task requires, **but the prompt does not fix the order they are produced in**." | "Names the intermediates the answer actually depends on — no more, no fewer — **in any order**." The set-match is anchor 4's positive content; ordering is explicitly released. |
| Advanced | **5** | "…match the ones the task requires, **in the order the task requires them produced**." | "**States in the prompt** the order they must be produced in — which comes first, and which cannot start until an earlier one is done." Ordering is the only 4→5 discriminator after FIX-1.17, and it now lands in the prompt text rather than in the learner's readiness. |

**Working leaves open:** *"but the prompt does not fix the order they are produced in."* **Left
silent** — "in any order" releases the requirement without forbidding a learner from stating one, so
Working scores 4-or-5 by learner. The "be ready to say what breaks…" rider is gone.

## Day 20 — `rubrics.md#negative-constraints`

| Tier | Anchor | Anchor text | Why it lands there |
|---|---|---|---|
| Novice | **3** | "One real failure mode is excluded, but a second, equally likely one is not." | Generic exclusion replaced with "a **single** specific exclusion naming one failure you've actually seen the model make on this task — **one exclusion only, even if a second failure comes to mind**." Anchor 3 word for word. **Reaches 2** if the replacement stays generic. **Not 4**: anchor 4 describes a set of exclusions; the tier forecloses the second. |
| Working | **4** | "Exclusions are specific and each names the failure it prevents, but at least one is speculative rather than observed, **or names its failure without citing the incident in the prompt**." | "Exactly two exclusions, each naming a specific failure you have actually watched the model make on this task." Observed, specific, and uncited — anchor 4's second disjunct. |
| Advanced | **5** | "Exclusions are specific, and each **cites in the prompt** the incident it prevents." | "Each exclusion names the incident it prevents **inside the prompt itself** — 'do not X; last time you did X and it cost Y' — so a reader who wasn't there can see what it is guarding against." The plan's un-softenable phrase, kept verbatim; it is exactly what `days/20.md:21`'s After already models. |

**Working leaves open:** *"or names its failure without citing the incident in the prompt."* **Left
silent** — the tier asks for the observed failure to be *named*, never for the incident to be
recounted in the prompt. The "be ready to say when and how each one happened" rider is gone.

## Day 21 — `rubrics.md#context-ordering` (the course's worst single defect)

| Tier | Anchor | Anchor text | Why it lands there |
|---|---|---|---|
| Novice | **3** | "Instruction is findable, but constraints are **scattered** rather than grouped at the end." | The 200-word burial is still written and still read back — that is the demonstration — but the tier now ends "then have them **move the instruction to the top**, leaving every constraint exactly where it falls, and **send that version as their prompt**." The writing step is also amended to "with the constraints **scattered through the material rather than grouped**", which forecloses the escape where a learner happens to draft their constraints together at the end and reaches 4 or 5 from the lowest tier. **Not 1**: the scored artifact is no longer the buried draft. |
| Working | **4** | "Task first, material second, with constraints grouped last **except for one placed early**." | "Group their constraints at the end — without deleting a word — **leaving exactly one constraint where it currently sits mid-material**." Anchor 4's state, mandated. |
| Advanced | **5** | "Task first, material second, constraints grouped last." | "Task first, material second, and **every constraint grouped last with none left early** — without deleting a word." Exactly the one clause that separates 4 from 5, nothing else. |

**Working leaves open:** *"except for one placed early."* **Mandated**, not silent: anchor 4's
shortfall is a positive state (a constraint present early), and any silent formulation — "group your
constraints at the end" — is anchor 5. **Wave-3 entry filed: FIX-3.13**, covering both the concept
collision and the re-homing of the prediction test.

T18 closed: a compliant Novice learner no longer hands `SKILL.md:34` a prompt that is anchor 1 by
instruction, and `SKILL.md:20` no longer records a guaranteed 1.

---

## Departures from the plan, and why

Six. Each is a case where the plan entry conflicts with the brief's bar or with the settled
`rubrics.md`, and the plan entry loses.

1. **FIX-2.14 (day 15 Working) rejected outright.** Its premise — "Anchors 4 and 5 are conjunctive —
   *included, excluded and assumed*, all three, every time" — is false against the settled file.
   FIX-1.13's own replacement text, and `rubrics.md` as shipped, put **"includes, excludes **or**
   assumes"** and **"at least one thing"** at anchor 4; only anchor 5 is conjunctive. The stated harm
   ("a learner who names two inclusions and no exclusion … can still be capped at 3") therefore
   cannot occur: two inclusions clear anchor 4. Applying it would have tightened a model day's
   Working tier for no scoring gain.

2. **Day 15 Novice and Advanced edited although no plan entry asked for it.** This is the third
   defect class the brief warns about, and it is the largest finding in this batch: measured against
   the settled anchors, day 15 — one of the six model ladders — was reading **4 / 4 / 4**, because
   FIX-1.13 lowered anchor 4 under Novice's feet and raised anchor 5 out of reach of Advanced's "be
   ready to name both" rider. The brief's day-15 condition is that the three tiers "still land where
   they did"; 3 / 4 / 5 is where they did, and two minimal edits restore it. The alternative —
   leaving it — would also have failed the brief's own verification that no "be ready to"-class rider
   survives in 14–21.

3. **FIX-2.15 puts day 16 at 4 / 5 / 5.** Its own *Why* says so: "Novice at anchor 4 (boundary only),
   Working at anchor 5 (boundary plus failure)." That leaves anchor 3 unoccupied and both upper tiers
   on the same rung — the defect the wave exists to remove. Retargeted to 3 / 4 / 5: Novice gets
   variety without a boundary (anchor 3), Working gets the boundary case (anchor 4), Advanced gets
   the failure case (anchor 5). Advanced keeps the plan's observed-failure bar, which is now a
   concrete reading of anchor 4's word "**genuine**" rather than an off-rubric extra, and it lands in
   the prompt ("Say in the prompt what it got wrong").

4. **FIX-2.16's replacement Novice for day 17 lands at anchor 4, not 3.** As drafted it keeps "as a
   fenced code block filled with dummy values" and only drops the empty-value clause — but a fenced
   block of dummy values *with field names and types* **is** "an exact structure … with one edge
   unaddressed", i.e. anchor 4, which is where the plan also puts Working. Novice was rewritten to
   produce a plain list of field names with no types and no example values, which is anchor 3's text
   exactly and cannot be read as a structure. This is the typographic-escape class: the code block,
   not the wording, was doing the anchor-4 work.

5. **FIX-2.19 puts day 20's Novice at anchor 4** (one observed exclusion plus one speculative one is
   anchor 4's first disjunct in so many words). Same defect as (3): anchor 3 unoccupied and the
   Novice tier level with Working. Novice retargeted to a single observed exclusion, which is anchor
   3 verbatim ("One real failure mode is excluded, but a second, equally likely one is not"), and the
   second exclusion becomes what Working adds. Working and Advanced are the plan's text.

6. **FIX-2.21(a)'s Advanced tier carries two off-rubric riders; both removed.** (i) "Fix the three
   levers named as weakest wherever they surface in the reordered material" is scored by nothing —
   `days/21.md:47` cites `#context-ordering` alone, and the brief forbids requiring levers the day's
   `## Rubric` does not cite. FIX-2.21(b), which would have added them, edits the `## Rubric` body
   and is outside this batch's scope. (ii) "Predict, before running it, what changes about the
   output. Check the prediction against the real run" never lands in the prompt text, so
   `rubrics.md:5` cannot see it and `SKILL.md:32-34` scores nothing for it — rule 7. Advanced is now
   the 4→5 discriminator and nothing else. Both removals are recorded in **FIX-3.13**, including the
   fact that wave 2's checkpoint item 6 is left open by design rather than by oversight.

## Discrepancies between the plan's quoted anchors and the settled file

The file wins in all three; wave 1 is settled.

- **(a) `role-framing` anchor 4 — the consequential one.** FIX-2.14 asserts anchors 4 and 5 are both
  conjunctive and cites `rubrics.md:170-171`. The file reads, at 4: "The role text names **at least
  one** thing the output includes, excludes **or** assumes because of the role, but not how the role
  produces it." Disjunctive and at-least-one. This inverts the fix: the day needed no Working edit
  at all, and needed Novice and Advanced edits the plan never contemplated. See departures 1 and 2.
- **(b) `negative-constraints` anchor 4.** FIX-2.19 and CONFLICT-11 reason from "with one still
  speculative" as anchor 4's sole shortfall. The file carries a **second disjunct** added in wave 1
  round 2: "…**or names its failure without citing the incident in the prompt**." That disjunct is
  what lets the plan's Working tier (all exclusions observed, none cited) sit at 4 — the plan's own
  conclusion is right, but only because of a clause it never quotes.
- **(c) `few-shot-examples` anchor 3.** FIX-2.15 never quotes it, and treats anchor 4 as the bottom
  of the ladder. The file's anchor 3 — "Examples show variety, but none demonstrates a boundary or a
  near-miss" — is a perfectly occupiable rung and is what day 16's Novice now targets.

## Wave-3 entries filed in `MASTER-FIX-PLAN.md`

Added after OPEN-3.01, with the wave-3 file list and the wave-3 checkpoint updated to match.

- **FIX-3.12 — Day 18: reconcile the concept with a Working tier that mandates one added line**
  (medium). `:7`'s "only fixes this if … nothing added, nothing re-explained" and `:11`'s verbatim
  self-test now contradict the tier a Working learner is shown; carries an explicit **do not touch**
  on the Before / After at `:15-33` and a note on the 200-word cap.
- **FIX-3.13 — Day 21: reconcile the concept with the rebuilt ladder, and re-home the prediction
  test** (medium). Covers (a) the mandated early constraint versus `:7`'s single-move recipe, (b) the
  prediction test at `:11` now living in no tier and needing a day-23-style "not a scored one"
  declaration, and (c) **FIX-2.21(b) left unapplied** — wave 2's checkpoint item 6 is explicitly
  open and must be closed one way or the other rather than silently.
- **FIX-3.14 — Day 15: the ladder was repaired against FIX-1.13's anchors, and the concept's test no
  longer matches** (medium). Records the 4/4/4 before-state with its cause, the rejection of
  FIX-2.14, and the three consequences for wave 3 — `:11`'s two-item output-effect self-test matches
  no rung, `:21`'s After is now load-bearing for FIX-3.07, and wave 3's checkpoint item 6 must not
  move the Working tier to three properties.

## Departures from literal plan text, non-substantive

Listed separately from the six above because none of them changes an anchor, but the rule is to
record every deviation from the plan's quoted replacement text, not only the consequential ones.
All three are rule 4 ("every tier produces a written prompt") applied to a plan text that omitted the
send step — the same change batch A made to FIX-2.03's day-04 Novice.

- **`days/14.md:29`** — FIX-2.13's replacement ends "…leaving the other eight as they are." Added
  "**and send that version**", and changed "as they are" to "exactly as they are" so the eight
  untouched levers are unambiguously untouched rather than merely unmentioned.
- **`days/18.md:41`** — FIX-2.17's replacement ends "…summarised or pasted, whichever is easier."
  Added "**and send the three prompts**" (and, in round 2 below, replaced the branch itself).
- **`days/19.md:31`** — FIX-2.18's replacement ends "…in place of 'step by step'." Added "**and send
  the rewritten version**", which also disambiguates which of the two prompts the learner wrote is
  the scored artifact.

## Nothing was stopped on

Day 15 was the one candidate for a stop-and-report. The brief's condition is that a plan entry must
not *move* day 15's ladder; FIX-2.14 would not have moved it (Working stays at 4 either way), and the
edits actually made restore the ladder to the 3 / 4 / 5 the census recorded rather than re-pitching
it. The finding that made them necessary is a wave-1 consequence, not a wave-2 judgement call, and it
is filed as FIX-3.14 with the full before-state so it can be reviewed independently.

---

# Round 2 — the day 18 branch leak and the day 15 Working inference test

Two tier-body edits, both in scope. Days 14, 16, 17, 19, 20 and 21 were **not** touched this round
(round-2 `git diff --stat`: `days/15.md` 1 line, `days/18.md` 1 line, `MASTER-FIX-PLAN.md`).

## Critical — `days/18.md:41` offered anchor 5 by name

Round 1's Novice read "…the previous prompt's output — summarised in your own words **or pasted,
whichever is easier**". The justification I wrote covered the summarised branch and was silent on the
other, which is the leak: pasting is the easier branch *and* the shape the learner has just been
shown, because `SKILL.md:28` presents `## Before / After` before the exercise and day 18's After at
`:25-31` writes every seam as `[Prompt 1's output, unedited]`. A learner taking that branch hands in
three prompts each carrying the previous output verbatim — `task-decomposition` anchor 5 — from the
bottom rung, while Working is mandated down to 4. Least-effort compliant path: **5 / 4 / 5**. Same
inversion class as day 12's own-line leak in batch A, and precisely what FIX-2.17 exists to remove.

**Fixed at `days/18.md:41`:**

> Write a single chained prompt for {{TASK}} with three asks in it, then split it into three prompts where each one's input is the previous prompt's output summarised in your own words rather than pasted — a paraphrase at every seam, not the actual text — and send the three prompts.

Two independent closures, deliberately belt-and-braces, and both borrowed from the higher anchor's own
wording so there is no gap between what is forbidden and what is scored. "Summarised in your own words
**rather than pasted**" removes the branch; "**a paraphrase at every seam, not the actual text**"
negates anchor 5's discriminator (`rubrics.md:215`, "each step's input is **verbatim** the previous
step's output") in the same language day 18's own self-test uses (`:11`, "**verbatim** … not a
paraphrase, the actual text"). "At every seam" closes the partial reading — one pasted seam among
three is still a pasted seam.

## Important — `days/15.md:35` tested inference, not text

FIX-1.13 made the rubric a text property twice over: the Measures line is "whether **the prompt says**
what the role changes" (`rubrics.md:167`) and anchor 4 opens "**The role text names** at least one
thing…" (`:172`). Round 1 carried that correction to Novice and Advanced and diagnosed the cause in
FIX-3.14, but left Working reading "A reader should be able to **name at least two things the output
does** because of the role" — an inference test. A prompt whose role text is only "Answer as a
reviewer who will be paged if it breaks" satisfies it: a reader infers two output effects while the
role text names none, which is anchor 3 ("the role implies a standard … but the prompt doesn't say
which parts to draw on"). So Working was 3-or-4 by learner, and for the inferring learner the day was
flat at 3 across its bottom two rungs.

**Fixed at `days/15.md:35`:**

> Write a prompt for {{TASK}} whose role text names at least one thing the output includes, excludes, or assumes because of the role — named in the prompt, not left for a reader to infer from the role.

FIX-2.14 remains rejected — its premise is still false against the file. The disjunction is kept
("includes, excludes, **or** assumes", "at least one") and the mechanism is left unasked, so Advanced
retains the whole 4→5 gap.

**One deliberate deviation from the suggested wording.** The suggestion ended "— without saying how
the role produces it." I left the mechanism *silent* rather than *forbidden*, per rule 2's preference,
because the mandate buys nothing here: anchor 5 requires all three dimensions ("includes, excludes
**and** assumes"), so a Working learner scoped to "at least one" cannot reach 5 by volunteering a
mechanism. Adding a prohibition would have capped the tier for no scoring gain and put a fourth
concept-versus-tier collision into wave 3. The clause that *is* load-bearing — "named in the prompt,
not left for a reader to infer" — is the one that closes the reported defect, and it is in.

## Days 15 and 18 re-derived against the settled anchors

`rubrics.md` `## Role framing`:

| Tier | Anchor | Anchor text (verbatim from the file) | Why it lands there, and not a rung higher or lower |
|---|---|---|---|
| Novice | **3** | "The role implies a standard or a body of knowledge, but the prompt doesn't say which parts to draw on." | A role with a concrete stake implies the standard; the tier then forecloses the rung above in anchor 4's own vocabulary — "without saying anywhere in it what the output should include, exclude, or assume differently". **Not 4**: anchor 4 needs the role text to name at least one such thing, which the tier forbids. **Reaches 1–2** on "you are a world-class expert" — room to fail preserved. |
| Working | **4** | "The role text names at least one thing the output includes, excludes or assumes because of the role, but not how the role produces it." | Anchor 4's positive content, in the anchor's own words, with the inference escape shut. **Not 3**: the naming is required to be in the prompt. **Not 5**: see shortfall below. |
| Advanced | **5** | "The role text names what the output includes, excludes and assumes because of the role, and says how the role produces each." | One included, one excluded, one assumed — all three dimensions — "and says, **in the prompt itself**, how the role produces each of the three". Every clause of anchor 5, nothing added. |

**Working leaves open:** *"but not how the role produces it."* **Left silent**, and the silence is
safe: "at least one" scopes the tier to a single dimension, and anchor 5 needs all three, so no
compliant Working prompt reaches 5 whether or not the learner volunteers a mechanism.

`rubrics.md` `## Task decomposition`:

| Tier | Anchor | Anchor text (verbatim from the file) | Why it lands there, and not a rung higher or lower |
|---|---|---|---|
| Novice | **3** | "Tasks are split into steps, but one step's output isn't a clean input to the next." | A paraphrase at every seam is the definition of an unclean input. **Not 4**: anchor 4 requires the input to *be* the previous output plus one addition; a paraphrase is not the previous output. **Not 5**: anchor 5's "verbatim … the actual text" is negated word for word. **Reaches 1–2** if the learner never really splits the three asks — room to fail. |
| Working | **4** | "Work split so each step has one output, and the next step's input is the previous step's output plus exactly one added instruction or re-explanation." | "The previous step's output plus **exactly one line of added instruction**. Nothing from the original task may be re-explained." Anchor 4's state, mandated — "at most one" would admit zero and therefore anchor 5. |
| Advanced (unchanged) | **5** | "…each step's input is **verbatim** the previous step's output — nothing added, nothing re-explained." | The only tier demanding the verbatim seam; its adversarial constraint (the last step must cite a detail that survives only an unparaphrased hand-off) is now the *test* of that seam. |

**Working leaves open:** *"plus exactly one added instruction or re-explanation."* **Mandated** —
anchor 4's shortfall here is a positive state, not an omission. Wave-3 entry **FIX-3.12** was filed
in round 1 for the resulting concept collision and still stands.

**Day 18 Novice admits no anchor-5 reading under either branch, because there is no longer a second
branch.** The tier states the required form positively ("summarised in your own words"), rules out
the alternative explicitly ("rather than pasted"), and then negates anchor 5's discriminator in the
rubric's own words ("a paraphrase at every seam, not the actual text"). The only way to reach anchor 5
from this tier is to disobey it.

## Round-2 minors folded in

- **Wave-3 checkpoint renumbered.** It read 1,2,3,4,5,6,9,10,7,8 after round 1's insertions; it now
  runs 1–12 in sequence, with the two new items appended as 11 and 12.
- **Three unreported departures added** to the report's departures list, under a new heading
  "Departures from literal plan text, non-substantive" — the "send" clauses added to `days/14.md:29`,
  `18.md:41` and `19.md:31`, none of which appears in the plan's replacement text.
- **FIX-3.09 amended.** `days/19.md:9` calls gating "useful, but **secondary** to getting the list
  right". That was true against the pre-wave-1 anchors; after FIX-1.17 ordering-and-gating *is* the
  scored 4→5 discriminator and wave 2B's Advanced tier demands exactly it, so the concept now tells
  the learner aloud (`SKILL.md:28`) that the property separating their tier from full marks is
  secondary. The entry's old "confirmed already fixed, do not re-touch" note on `:9` is replaced with
  the required direction and the 200-word cap warning. New checkpoint item 11.
- **FIX-3.15 filed** — day 17, low, tracking only. The concept's schema example at `:11` contains
  `"note": ""` and `:16` glosses it, which is the anchor-4→5 property wave 2B assigned to Advanced.
  Nothing is broken: neither Novice nor Working *requires* it, so no tier is lifted. Filed because
  day 17 was on no wave-3 list and a wave-3 editor could couple the concept and the Working tier
  without noticing. New checkpoint item 12.

## Round 2 verification

| Check | Result |
|---|---|
| `python3 tools/validate.py --complete` | `ok`, exit 0 |
| `python3 -m unittest discover -s tools` | 103 tests, OK |
| Round-2 diff scope | `days/15.md` (1 line), `days/18.md` (1 line), `MASTER-FIX-PLAN.md` — days 14, 16, 17, 19, 20, 21 untouched |
| `## ` / `### ` headings | none touched |
| Day 15 ladder | 3 / 4 / 5, and Working now fails on the text, not on a reader's inference |
| Day 18 ladder | 3 / 4 / 5, with no branch in Novice that reaches anchor 5 |
| Riders in 14–21 | still none |
| Advanced word/item budgets in 14–21 | still day 14 only |
