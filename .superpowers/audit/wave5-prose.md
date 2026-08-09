# Wave 5 — prose consistency across the shipped skill

Branch `feat/prompting-wizard-polish`. Thirteen entries, FIX-5.01 through FIX-5.13, all closed:
**ten executed, three ruled** (FIX-5.04, FIX-5.08, FIX-5.10(b)); FIX-5.13(b) ruled and its ruling
written into the file, as its entry required. Nothing is deferred to wave 6.

`rubrics.md`'s 26 anchors are untouched in text. No `## Exercise` tier body was edited on any day. No
`## ` or `### ` heading text changed anywhere. One `# ` title changed — `days/06.md:1`, which is
FIX-5.02's whole content.

## Verification

- `python3 tools/validate.py --complete` → `ok`, exit 0.
- `python3 -m unittest discover -s tools` → **103 tests, OK**.
- Both re-run after FIX-5.07's block move, which is the last shipped edit in the wave.

```
 .superpowers/audit/MASTER-FIX-PLAN.md | 144 ++++++++++++++++++++++++++++++++++
 README.md                             |   2 +-
 prompting-wizard/SKILL.md             |  16 ++--
 prompting-wizard/assessment.md        |   4 +-
 prompting-wizard/days/01.md           |   2 +-
 prompting-wizard/days/02.md           |   2 +-
 prompting-wizard/days/03.md           |   2 +-
 prompting-wizard/days/06.md           |   4 +-
 prompting-wizard/days/07.md           |   2 +-
 prompting-wizard/days/16.md           |  11 ++-
 prompting-wizard/days/17.md           |   4 +-
 prompting-wizard/days/21.md           |   2 +-
 prompting-wizard/days/30.md           |   2 +-
 prompting-wizard/rubrics.md           |  28 +++----
 14 files changed, 189 insertions(+), 36 deletions(-)
```

## The word budget — every concept touched, recounted

Counted with `validate.py`'s own `section(text, "## Concept")` plus `len(str.split())`, before and
after, in the file. Not estimated. `section()` blanks fenced code blocks before counting, which is
why day 17's edit costs nothing.

| Day | Before | After | Δ | What paid for the addition |
|---|---|---|---|---|
| 01 | 147 | **147** | 0 | none needed — `test.` → `test:` is one token either way |
| 02 | 199 | **199** | 0 | none needed — same swap, and nothing else on `:11` was touched |
| 03 | 163 | **179** | +16 | the deleted sentence "If you can't answer, cut the word." (7 words) offsets the added 23-word laddering sentence; 37 words of headroom absorbed the rest |
| 06 | 190 | **191** | +1 | "Test it by removing each lever in turn." (8) → "Here is the test: remove each lever in turn." (9) |
| 07 | 197 | **199** | +2 | "was left open, and rewrite until none of them are." (10) → "was left open; one closed is a rung, all five the climb." (12) — FIX-5.11 candidate C, which predicted 199 and recounts at 199 |
| 16 | 191 | **191** | 0 | edit is in `## Before / After`, outside the counted section |
| 17 | 184 | **184** | 0 | edit is inside the `## Concept` code fence, which `section()` blanks |
| 21 | 196 | **196** | 0 | edit is in the `## Exercise` preamble — this is FIX-5.09's whole reason for deviating from SYS-2 |
| 30 | 195 | **195** | 0 | edit is in `## Completion` |

All twenty-one untouched days recount identical to the wave-3C census. Day 07 now has **one** word of
headroom and day 02 has one; day 03 leaves the tight list.

**One arithmetic correction to the plan.** FIX-5.10(a) describes its suggested `:11` as "one net word
over the FIX-5.01 row". Recounted, it is **+16** over the current line: the FIX-5.01 opener swap is
genuinely cost-neutral (18 words either way), but the sub-item's laddering sentence adds 23 and
removes 7. The entry's own headroom figure — 163, "the second roomiest in the course" — is correct and
covers it with 21 to spare. The text was applied exactly as the entry gives it; only its cost claim
was wrong. **This is the sixth wrong word figure this project has carried.**

## FIX-3.22 — the mandatory per-file check

**Fourteen day files opened, fourteen checks run, all clean. No new member of the class found.** The
per-day evidence is recorded in `MASTER-FIX-PLAN.md` under FIX-3.22's standing consequence, where the
mandate says it belongs; summarised here.

| Day | Why opened | Verdict |
|---|---|---|
| 01 | FIX-5.01 | clean — `:11` names counts and formats as "later levers", legitimising the Novice omission by name |
| 02 | FIX-5.01 | clean — `:9` states all three rungs one to one (wave 3A) |
| 03 | FIX-5.01 + FIX-5.10(a) | clean — and the edit *adds* the Novice rung that was missing |
| 04 | FIX-5.01 status check (read-only) | clean — `:11`'s three-rung ladder scopes `:7`'s "a manner word is a mood" |
| 05 | FIX-5.01 status check (read-only) | clean — `:11`'s way-station clause scopes `:9`'s "drop any one" |
| 06 | FIX-5.01 + FIX-5.02 | clean — wave 4's `:11` close call re-confirmed by a third reading; no edit beyond the opener |
| 07 | FIX-5.11 | **was defective at `:7`; fixed.** Clean after |
| 10 | FIX-5.10(b) | clean — third independent reading of `:9`, agreeing with wave 3C and the wave-3 gate |
| 16 | FIX-5.05 | clean — `:11` ladders all three rungs (FIX-3.08) |
| 17 | FIX-5.03 | clean — `:16` and `:18` untouched, so wave 4's re-run trigger never fired; run anyway |
| 21 | FIX-5.09 | clean — `:11` ladders `:35`/`:39`/`:43` one to one (FIX-3.13) |
| 22 | FIX-5.05 (confirmed conforming) | clean — `:9` states all three rungs in the rubric's own counting |
| 30 | FIX-5.12(b) | clean — `:7` scopes the write-down to "the top rung's addition" (FIX-3.19) |

Days 04 and 05 were opened only to confirm FIX-5.01's spent rows and were not edited. They are
checked and recorded anyway, because the mandate reads "for any reason" and because an unrecorded
"we looked and it was fine" is indistinguishable from never having looked — FIX-3.22's own words
about day 20.

**Two close calls carried forward rather than closed by edit**, both re-confirmed rather than
inherited:

- **`days/06.md:11`.** Its deletion test is an Advanced-rung diagnostic presented as "the test" on a
  day whose Novice tier is built to produce levers that fail it, and day 06's concept carries no rung
  language anywhere. Wave 4 ruled it names a property rather than instructing a state; a third
  reading agrees. Not closed by a scoping clause — see departure **D9**.
- **`days/10.md:9`.** "A bare noun next to a bound one is still a gap" is the closest thing on that
  day to a verdict on the state `:33` mandates. Three readings now agree it is positional: "still"
  names distance left to climb, one bare noun is `determiner` anchor 3 — a scored rung — and the
  sentence does not instruct the learner to close it. FIX-5.10(b) filed it precisely so a wave-5
  reader would look rather than assume; looked, and clean.

## Entry by entry

### Executed

**FIX-5.01 — four live rows, two spent rows honoured.**
- `days/01.md:9`, `days/02.md:11` — full stop → colon, sentence bodies untouched. Nothing was
  restored from the entry's table on day 02, whose `:11` wave 3A rewrote and which sits at 199.
- `days/03.md:11` — landed in one edit with FIX-5.10(a), as the entry's Status column requires.
- `days/06.md:11` — "Test it by removing each lever in turn." → "Here is the test: remove each lever
  in turn."
- **`days/04.md:11` and `days/05.md:11` were read and NOT edited.** Both already open "Here is the
  test:". Day 04 carries "would their outputs be the same length and thoroughness?" — `adverb` anchor
  **5**, with no "roughly"; applying the retired row would have dragged it back to anchor 4's
  tolerance language and silently reverted wave 3A. Day 05 carries FIX-3.21(b)'s way-station clause,
  which the retired row would have overwritten. Confirmed in file, not assumed from the Status column.

**FIX-5.02** — `days/06.md:1` → `# Day 6 — Composition: the first five together`. Grepped first: the
old title string appears in no other shipped file, and `validate.py` asserts nothing about `# `
titles. Side effect worth naming: the new title gives day 6 a term, which is what makes FIX-5.12(a)'s
`composition` derivable from the title rule rather than an exception to it.

**FIX-5.03** — `days/17.md:11-12`, `example item one/two` → `sample entry one/two`, matching `:32-33`.

**FIX-5.05** — `days/16.md:19-24` only. Days 17, 18 and 22 were read and already agree; day 22's
`## Before / After` was confirmed conforming and not touched. The boundary-case text carried forward
verbatim from FIX-3.08 — checked character for character against the file before replacing, since the
entry warns this edit can re-introduce the agreeing-examples defect.

**FIX-5.06** — `README.md:5`, "one lever" → "one lever or one technique".

**FIX-5.07 — the last shipped edit made.** `## Preposition` now precedes `## Pronoun` in `rubrics.md`
(`:65-77` and `:79-91` respectively); `assessment.md`'s illustrative `## Levers` block reads
`preposition: 4    pronoun: 2    conjunction: 3`. No heading text changed, so no `rubrics.md#slug`
reference broke — `validate.py --complete` re-run immediately after and returns `ok`.

**FIX-5.09** — one sentence appended to `days/21.md:31`, the `## Exercise` preamble. SYS-2's placement
rule was deliberately not followed, per the entry; the concept was not touched and stands at 196.

**FIX-5.10(a)** — landed in the same edit as FIX-5.01's day-03 row, per the entry.

**FIX-5.11** — candidate C, the recommended one. `days/07.md:7`'s third sentence now ladders the
one-lever rung the Novice tier mandates against the five-lever climb, in `:11`'s own idiom. 197 → 199,
matching the entry's counted prediction exactly.

**FIX-5.12** — all six sub-items. (a) field-2 clause naming `composition`/`review`/`review`; (b)
`days/30.md:45` now defers to `SKILL.md` instead of restating a time; (c) forward pointer added to
`## Every session` step 6; (d) `SKILL.md`'s Completion step reordered, no content change; (e) rebuild
output specification added and the five failure rules broken into a four-row sub-list; (f)
`SKILL.md:32` now defers to the substitution rule at `:28` instead of stating it differently.

**FIX-5.13(a) and (c)** — the day-0 half-integer rule, and one sentence preparing a learner for a
visible day-15 demotion.

### Ruled

**FIX-5.04 — the recommended no-op, taken.** The entry conditions spending an edit on FIX-5.05
changing day 17's surrounding form. FIX-5.05 touched day 16 only, so the condition never fired. Day
17's Concept fence stays bare and its After fence stays quoted.

**FIX-5.08 — closed under (a), accepted.** Full reasoning in the entry. In short: raising absolute
difficulty across days 22–28 requires raising tier demand, which the entry declares inadmissible;
option (b) was considered on the merits and rejected because reordering breaks a real dependency
chain (22 → 23, 25 → 30, 27 and 28 presume the full technique vocabulary) and would desynchronise
every day-number reference in the plan, all audit reports, and `SKILL.md:63`'s day list, while
tutor-side additions would put unscored demand on seven consecutive days — the shape SYS-2 exists to
constrain. **No tier body was touched on any of days 22–28.** Recorded as accepted, not deferred.

**FIX-5.10(b) — re-read, clean, no edit.** Day 10's concept stands at 178 of 200 and its 22 words of
headroom were not spent.

**FIX-5.13(b) — ruled acceptable and written into the file, not fixed with a state field.** The entry
says closing it properly needs a state field recording which levers have ever been exercised, and
that (b) "may need a state field rather than a clause — if so, rule and file rather than inventing
contract". No field was invented. `SKILL.md:24` now says the day-14 mean is over all eleven entries,
says how that differs from day 0's, names the one surviving case — a lever imputed at day 0 and N/A
again on the day-14 prompt — and states that the case is narrow enough to accept rather than track.
The residue the entry called out ("the two means now differ and nothing explains why") is closed.

## Departures from the plan's literal text

Thirteen, four substantive (D2, D4, D6, D9).

**D1 — FIX-5.10(a)'s cost claim is wrong; the text was applied anyway.** "One net word over the
FIX-5.01 row" recounts as +16. Not substantive: the entry's headroom figure is right and covers it.
Recorded because five wrong word figures preceded it.

**D2 — FIX-5.09's disclaimer was reworded. Substantive.** The entry's suggested sentence asserts
"every tier forbids deleting a word". `days/21.md:39` and `:43` do say "without deleting a word";
**`:35`, the Novice tier, does not** — it says "leaving every constraint exactly where it falls",
which is a placement rule, not a deletion rule. Shipping the entry's wording would have put a false
universal in a file, which is the class of defect this wave exists to remove. Landed as "every tier
is a reorder", true of all three tiers and consistent with `:9`'s "This is a pure reorder, not a
trim". The rest of the sentence, including day 23's "useful habit, not a scored one" form and the
`context-ordering`-alone claim, is the entry's verbatim.

**D3 — FIX-5.05's replacement block was de-quoted one level.** The entry renders its replacement
inside its own `>` quoting, so taken literally it would give day 16 a blockquoted label and a
doubly-nested example. Landed at one level less, which is what "standardise on day 18's and day 22's
form: a plain-text label, then a separate blockquote" actually names — verified against `days/18.md:21-31`
and `days/22.md:21-27`. Non-substantive; the entry's own text is unchanged word for word.

**D4 — FIX-5.12(e)'s rebuild specification says where the values come from. Substantive.** The entry
asks only for what a rebuilt file must contain. A list of required contents with no source is a
specification the tutor cannot meet: a stated day number supplies `current_day` and nothing else,
while `## Levers`, `## Tasks` and `level` have no derivation. One clause was added — the day number
supplies only `current_day`, ask the learner for the rest, and tell them the lever scores are their
own estimate until day 14 rescores all eleven. **No new stop condition and no new field**; every
requirement listed is one `SKILL.md:14`'s checks already enforce, and the day-14 fact is
`SKILL.md:24`'s existing re-derivation.

**D5 — FIX-5.12(a) landed as a title-rule clause, not an exception.** After FIX-5.02, all three
titles contain their term (`Composition`, `Review`, `Review`), so the sentence says they take the
term from their titles and log `composition`/`review`/`review` — which keeps `SKILL.md:79`'s
recoverability claim literally true rather than true-with-an-exception. The entry asked only for "one
clause naming what they log".

**D6 — FIX-5.13(a)'s rounding direction was chosen, not inherited. Substantive.** The entry says
"Round, or say which way, in one clause" and leaves the direction open. Landed as **round down**: a
two-score median that falls between whole numbers takes the lower. Reason, stated in the file: the
`## Levers` contract is integer throughout. Reason not stated in the file but recorded here — it
agrees with `rubrics.md:5` ("score the prompt as written, not the intent behind it") and routes a
borderline lever into secondary practice under `SKILL.md:34` rather than out of it. A future wave
wanting round-half-up should know this was a choice, not a finding.

**D7 — FIX-5.13(b)'s explanation says more than "the two means differ".** It also names the exact
surviving case and states that it is accepted. The entry asked for the difference to be explained;
explaining it without naming the case would leave the next reader re-deriving the window.

**D8 — FIX-5.13(c) landed in `SKILL.md:24`**, the first of the two sites the entry offers ("or in
what the tutor says").

**D9 — day 06's `:11` scoping clause was NOT added, though wave 4 left nine words for it.
Substantive, and a refusal rather than an omission.** Wave 4 round 2 recorded the close call against
FIX-5.01's day-06 row and said nine words are available after the opener swap. The shortest candidate
that is both accurate and in the course's idiom — "Levers that fail this test are where this starts."
— is exactly nine words and lands day 06 at **200 of 200**. Zero headroom on a day the plan already
lists as tight was judged a worse trade than a re-confirmed close call on a line no entry requires
changing, and the alternative — inventing a shorter rung mapping for a deletion test that maps onto no
single anchor of the five rubrics day 6 scores — is tier-derivation work, not prose work. Day 06
stands at 191.

**D10 — FIX-5.12(b)'s day-30 sentence cites a location, not a time.** "Carry this out when
`SKILL.md` calls for it — after step 6 of `## Every session`, never before". The entry says "make the
day file defer explicitly rather than restate a time"; naming step 6 is the deferral's address, and
without it the sentence points at a document rather than a step. `SKILL.md:42` uses the same
identifier.

**D11 — FIX-5.01's day-04 and day-05 rows were not applied.** Honouring the Status column rather than
departing from it, but recorded because it is the one place in this wave where the plan's own table
carries text that must not be shipped.

**D12 — FIX-5.12(e)'s sub-list gives `## Tasks` two rows.** The original paragraph named `## Tasks`
once among "any other field → re-run the assessment" and then narrowed the fewer-than-three case to
Part 3. Both rules are preserved exactly and neither was merged; the list simply makes the narrowing
visible as its own row. Non-substantive, recorded because a re-reader will notice the repetition.

**D13 — two copy-edits in `SKILL.md` named by no entry.** The (e) insertion put a second "Say plainly"
in the same bullet as the existing one, changed to "tell them"; and the (b) sentence first landed as
"It means over all eleven…", which parses as "it signifies", corrected to "Its mean is taken over all
eleven…". Non-substantive.

## Stale text found in the audit corpus, corrected nowhere but recorded here

- **`census-prose.md` DEFECT-P03 and P05** — "Day 7 has no closing self-test at all" and "day 7 runs
  one paragraph short" are both stale. FIX-3.05 added `days/07.md:11`, and the wave-5 preamble already
  records P03 and P05 as closed by FIX-3.05. The census row is not being edited; noted so a later
  reader does not treat the census as current.
- **`census-prose.md`'s day-04 row** quotes `:11` as "would their outputs be **roughly** the same
  length and thoroughness?". Wave 3A removed "roughly". This is the exact stale text FIX-5.01's
  day-04 row was retired for carrying.

## What wave 6 inherits

Recorded in `MASTER-FIX-PLAN.md` under "Wave 5 — result", not here, per the standing rule that
anything a later step must act on goes in the plan.

- Every `rubrics.md:NN` reference in the plan and in all seven audit reports is stale after FIX-5.07.
- Every `SKILL.md:NN` reference below `:14` is off by three after FIX-5.12(e). Wave 6's cited lines
  `:13`, `:20`, `:28`, `:44`, `:53` are now `:13`, `:24`, `:32`, `:48`, `:57` — verified by grep, not
  computed.
- The concept-cap table is republished there with day 03 removed and days 03 and 07 restated.
- Wave 6 touches `SKILL.md`, `README.md` and `assessment.md` only, so it trips no FIX-3.22 day-file
  trigger — but the mandate still binds if it opens one.
