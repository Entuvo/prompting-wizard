# Final pass — four fixes before merge

**Status:** all four landed. No invariant traded. Nothing stopped on.

**Files touched:** `prompting-wizard/days/25.md` (Advanced tier only),
`prompting-wizard/rubrics.md` (one added sentence, no anchor text),
`prompting-wizard/days/12.md` (`## Before / After` After only),
`prompting-wizard/SKILL.md` (third bullet of `## Clean-context execution` only).

**Verification:** `python3 tools/validate.py --complete` → `ok` (exit 0);
`python3 -m unittest discover -s tools` → 103 tests, OK.

---

## Item 1 — `days/25.md` Advanced now demands anchor 5's own discriminator

**Edit (`:39`), one clause added, Novice and Working untouched:**

> Write three criteria for {{TASK}} before generating anything, **each specific enough that two
> readers who have not seen the output would produce the same score.** After you see the output,
> score it against exactly those three — don't add a fourth, and don't soften one it narrowly misses.

**Why the old text was insufficient.** "Don't add a fourth, and don't soften one it narrowly misses"
is a rule for the *scorer*, not a property of the *criteria*. `writing-evals` anchor 5 scores the
criteria: "every criterion is specific enough that two readers who have not seen the output would
produce the same score." Nothing in the old Advanced tier demanded it, so a compliant Advanced
learner could write three criteria one of which "could be applied two ways" — anchor 4's shortfall
verbatim — and still comply. wave2c-tiers.md:121 reached 5 by the inference "a criterion that
survives a narrow miss without softening is one that two readers apply identically"; that inference
is about scoring discipline and does not bind the text. The clause now demands the property directly.

### All three tiers re-derived against `rubrics.md#writing-evals`

**Novice (`:31`) → 3.** "Before writing a prompt for {{TASK}}, write three checks you'll apply to
whatever it produces. Only then write the prompt and generate the output."

- Above 1 ("Quality judged by feel; no criteria written down") — three checks are written down.
- Above 2 ("Criteria written, but after the output existed") — "Before writing a prompt", "Only then
  … generate the output" fixes the order; timing is the only thing this rung tests.
- Anchor 3, positive half: *"Criteria written before the output"* — met. Its negative clause, *"but
  at least one names a feeling rather than a checkable property"*, names the shortfall that holds a
  prompt at this rung, not a condition the learner must satisfy (`rubrics.md:6`, added under item 2).
- **Not 4.** Anchor 4 adds *"each naming a checkable property a reader who has not seen the output
  could apply without asking the writer"*. The tier sets no specificity bar at all — "three checks
  you'll apply", applied by the writer — so the least-effort compliant fill ("is it clear? is it
  useful?") names feelings. Floor 3; ceiling open to a learner who volunteers checkable criteria.
- **Unchanged by this edit** (Novice not touched).

**Working (`:35`) → 4.** "Write three criteria for {{TASK}} specific enough that someone else could
apply them without asking you what you meant, then generate the output and score it against them
unchanged."

- Anchor 4's positive half reproduced almost word for word: *"a reader who has not seen the output
  could apply without asking the writer"* ≈ "someone else could apply them without asking you what
  you meant". Timing satisfied by "then generate the output".
- **Not 5.** Anchor 5 requires agreement between two blind readers, not applicability by one. A
  criterion one reader can apply while two would apply it two ways still complies with the tier.
  Floor 4, ceiling open — the permitted 4-or-5 shape wave 2C recorded, and FIX-1.23's standing
  ruling that "apply … without asking" sits at anchor 4, not 5.
- **Unchanged by this edit** (Working not touched, as instructed).

**Advanced (`:39`, as edited) → 5.** Anchor 5's two requirements are now both mandated in the tier
text: *"Criteria written before the output"* ("before generating anything") and *"every criterion is
specific enough that two readers who have not seen the output would produce the same score"* (lifted
from the anchor, distributed over each of the three by "each"). **Not 4:** anchor 4's shortfall is
"at least one could be applied two ways", which the new clause is the exact negation of, so a
compliant Advanced prompt cannot sit at 4. The scoring-discipline sentence survives byte-identical
and still does its own work — it is simply no longer load-bearing for the 4→5 step.

**Ladder: 3 / 4 / 5, strictly rising.** CONFLICT-08's constraint (day 25 must land 3/4/5) holds.

### Imitate-the-After, day 25 Novice — **unchanged at 3**

The test (wave2c-tiers.md:32-34): `SKILL.md:32` presents `## Before / After` immediately before the
exercise, so the realistic bottom-rung learner copies the worked example — which anchor does a
compliant learner reach?

Neither the After (`:21`) nor the Novice tier (`:31`) was touched by this edit, and `SKILL.md:34`
shows the learner exactly one tier, so the Advanced clause is never in a Novice learner's view.
Re-derived from the file rather than assumed: the After's three checks ("every claim traces to a
source, no paragraph exceeds five sentences, and the conclusion appears in the first paragraph") are
checkable properties written before the output — anchor 4 at least, and wave 2C read them as anchor
5. Imitating them is more work than complying with the tier, and the rung the tier *tests* is
timing, which the After also models and which imitation cannot shortcut, so the **least-effort
compliant path stays at 3** — wave 2C's recorded verdict, still true of the shipped file. A learner
who does copy the criteria verbatim lands **above** their tier, not below: the healthy direction, and
the reason wave 2C proposed no edit. That verdict is untouched here.

---

## Item 2 — a written convention for privative anchor clauses

**Added to `rubrics.md` after line 5, as its own paragraph. No anchor text changed.**

> Where an anchor carries a negative clause — "but has no written evaluation criteria", "but at least
> one could be applied two ways" — that clause names the shortfall which holds a prompt at that rung
> rather than a condition the prompt has to satisfy, so score the highest anchor whose positive
> requirements are met.

Both quoted fragments are byte-exact substrings of live anchors (`capstone` 3 and `writing-evals` 4),
so the sentence teaches the convention from the file's own text. Voice matches the surrounding
paragraphs (imperative to the scorer, em dashes, straight double quotes, as at `:142` and `:169`).

**What it unblocks — day 30 Novice, re-derived.** `days/30.md:29` mandates three written checks, a
close-variant run, and "Record the scores only; nothing about what broke gets written down at this
tier." A literal tutor was stuck: `capstone` anchor 3 says "but has **no** written evaluation
criteria", which is now false of the prompt, while anchor 4 needs "failure modes noted", which the
tier forecloses. Under the convention: anchor 4's positive set is incomplete (failure modes are a
positive requirement of anchor 4, foreclosed by the tier), and anchor 3's positive requirement
("Prompt is specified and works on varied cases") is met, so the highest anchor whose positives are
met is **3**. Working → 4 and Advanced → 5 are unaffected (both turn on positives the tier mandates,
not on negatives). **Day 30 ladder holds at 3 / 4 / 5**, and is now derivable rather than stuck.

**Day 25 Novice** is the second stuck case and resolves the same way — see item 1's Novice
derivation, which cites `rubrics.md:6` directly.

**No ladder is lifted by it.** The convention is the reading every wave report already applied; it
changes no derivation, only writes one down where the tutor reads. Checked against the two tiers most
exposed to it: day 25 Working stays at 4 (held there by anchor 5's *positive* not being demanded, not
by anchor 4's negative — wave2c-tiers.md:123 already recorded it as silent on that clause), and day
30 Novice stays at 3 as above.

**Integrity after the edit:** 26 `## ` headings, byte-identical to HEAD (diff of heading text: no
change); all 156 anchor-table rows byte-identical; 26 slugs, and all 49 `rubrics.md#slug` references
across the skill resolve.

---

## Item 3 — `days/12.md`'s After now demonstrates what it claims

**Edit (`:21`), a line break inside the blockquote, in the house style already used at
`days/17.md:29`:**

> Review {{TASK}} for correctness and style. … Summarise your findings in five bullets at the end.
>
> IMPORTANT: do not suggest changing the public API — it's frozen for this release.

Before the edit the marker was the last sentence of a single-line blockquote — `interjection` anchor
3 ("the marker sits inline in a paragraph with other instructions rather than on a line of its own"),
the rung the rubric explicitly names as *lower* — while `:23` glossed it as "moved to stand alone at
the end". The After now reaches anchor 5 ("Exactly one marker in the prompt, on the instruction the
writer names as highest-stakes, standing alone as its own line"), which is what the gloss asserts.
`:23` is left byte-identical and is now true. The `## Concept` is untouched, so FIX-3.11(a)'s
keep-verbatim sentence at `:7` survives.

### Imitate-the-After, day 12 Novice — **derived, and still capped at 3**

**Novice tier (`:31`), verbatim:** "Write a five-sentence prompt for {{TASK}} as a single paragraph,
containing one instruction you'd be angriest to see ignored. Mark that instruction IMPORTANT: where
it sits — inline in the paragraph, not moved and not on a line of its own — then send the completed
prompt."

- **Above 1.** Anchor 1 is "All instructions carry equal weight; the critical one is buried
  mid-paragraph." The tier mandates a marker on the critical instruction, so weights are no longer
  equal.
- **Not 2.** Anchor 2 is a priority word "attached to something other than the instruction the writer
  names as the one they would be angriest to see ignored." The tier mandates the marker on exactly
  that instruction.
- **Anchor 3, exactly.** "The critical instruction is marked, but the marker sits inline in a
  paragraph with other instructions rather than on a line of its own." The tier mandates "inline in
  the paragraph … not on a line of its own", and "five-sentence prompt … as a single paragraph"
  guarantees the other instructions share that paragraph.
- **Not 4.** Anchor 4 needs the instruction "marked and stands alone rather than sitting
  mid-paragraph" — negated by "not on a line of its own" in the anchor's own words — and additionally
  a second marked item, where the tier mandates one.
- **Not 5.** Anchor 5 needs "standing alone as its own line" — negated by the same clause.

**Cap: 3.** **Proof that the edit cannot lift it.** The cap is produced entirely by the tier's
foreclosure clause, which is untouched, and which negates the discriminating clause of anchors 4 and
5 in those anchors' own words. A learner who reproduces the After's new own-line formatting is by
construction *non-compliant* with the tier, so they are not the compliant imitator this test
measures. The edit therefore strengthens wave 2D's derivation rather than changing it: before, only
"not moved" was violated by copying (wave2d-sweep.md:565-571); now "not on a line of its own" is
violated too, so copying is visibly non-compliant on two independent grounds instead of one.

**Checkpoint item 18's floor holds** — no `## Before / After` edit may change the anchor its day's
derivation is measured against; it may rise, it may not fall. Day 12's After rises from anchor 3 to
anchor 5. Day 12's tiers were not touched, so the 3 / 4 / 5 ladder is unaffected.

---

## Item 4 — `SKILL.md` discloses whenever the envelope does not prevent writes

**The gap (day15-trace.md §5, A1).** `:49` ("a sandbox setting exists → set it") and `:50` ("no
setting exists → dispatch and disclose") were mutually exclusive, and only the `:50` branch told the
learner their prompt can write to disk. This harness's dispatch tool offers settings that narrow
capability per call — a subagent type, a worktree isolation flag — but delivers neither read-only
filesystem access nor anything preventing writes (`Bash` survives every option). A tutor taking the
`:49` branch on a partial setting silently dropped the disclosure.

**The fix.** The third bullet's trigger is now the *achieved* restriction rather than the *existence*
of a setting. Bullet 2 keeps its function unchanged (set the most restrictive available setting on
the dispatch call); bullet 3 keeps both of its functions (the one-time disclosure and the offer of
the fallback) and now fires on the partial case as well as the none case. **The bullets were located
by content, not by line number.**

**`## Clean-context execution`, in full, as it now reads:**

> ## Clean-context execution
>
> The learner's prompt must run with no lesson history in context. Lesson context contaminates the output and destroys the comparison the exercise depends on.
>
> - If this harness can dispatch an isolated agent, dispatch the prompt there and capture the output verbatim. Detect this by whether an isolated-agent dispatch tool is actually available to you, not by inspecting configuration — Codex, for example, can expose a `spawn_agent` tool with no corresponding entry in `~/.codex/config.toml`, so a missing config entry does not mean dispatch is unavailable.
> - Isolation is a property of the dispatch, not of the prompt. If the dispatch tool accepts a sandbox, permission, or tool-allowlist setting, dispatch with the most restrictive one that still lets the prompt run — read-only filesystem access by default. Set it on the dispatch call, never in the message: the message is the learner's prompt verbatim and nothing else. Apply the same setting to the rewrite's run, so both runs are constrained identically and the comparison stays fair. If the dispatch tool exposes a nesting depth or concurrency limit, set it to the minimum that lets the prompt run.
> - Restriction is what the settings achieve, not what they are named. Unless the settings you applied actually prevent the prompt from writing — because the tool offers none, or because the ones it offers only narrow capability, a subagent type or a workspace flag, while leaving some tool in the envelope able to write — dispatch anyway, but say once, before the first run of the course: "Your prompt will run for real, with the file and network access this session has, in this directory." If the learner would rather it did not, use the fallback below instead.
> - If it cannot, or if dispatch fails, print the prompt in a fenced block and ask the learner to run it in a fresh chat and paste the output back. This is a fallback for when dispatch is unavailable, not a safety measure: the prompt still runs, in a session you cannot observe and possibly with broader access than this one, and the learner then pastes untrusted output back into this context.
>
> Never run the learner's prompt in the lesson context. A contaminated run is worse than no run.
>
> Run the rewritten prompt in a **separate** clean context from the learner's. Reusing one context primes the second run with the first run's output.

**Verbatim rule — four sites extracted and byte-compared, all identical.** `sed -n '36p;49p;59p;60p'`
before and after hash to the same SHA-256 (`1ac42b23…0cf918`), and the four lines still sit at 36,
49, 59 and 60 because the edit replaced one line with one line:

- `:36` "Execute the learner's prompt **verbatim** in a context containing no lesson history."
- `:49` "…never in the message: the message is the learner's prompt verbatim and nothing else."
- `:59` "Never improve the learner's prompt before running it."
- `:60` "Never add an instruction, a constraint, or a reminder to the learner's prompt — including a
  safety one."

Nothing in the new bullet wraps, prepends to, or amends the learner's prompt: the disclosure is
addressed to the learner, once, before the first run, and never enters the dispatched message.

---

## FIX-3.22 per-file check — every day file opened

Two day files were opened and edited: **12** and **25**. Both checked sentence by sentence, the
`## Concept` against that day's own Novice and Working tier text, `## Before / After` included.

### `days/12.md` — **CLEAN**, one close call recorded, no edit proposed

- **`:5`** — condemns the *unmarked* must-not-fail instruction in a row of five. That is anchor 1,
  *below* the Novice rung; the tier mandates the instruction be marked. No collision.
- **`:7`** — **the close call.** "But marking alone isn't enough: buried mid-paragraph, it still
  competes for attention" describes precisely the state the Novice tier mandates (marked, inline,
  mid-paragraph). It clears on the day-20 / day-28 test — positional, not verdictive — and `:9`
  settles it explicitly: "Marked inline among its neighbours **is where this starts**". A concept
  that names the state as the bottom rung of its own ladder is not condemning it, so "isn't enough"
  reads as "isn't the top". Same resolution as `days/15.md:5` and `days/28.md:9`. The third sentence
  ("Standing alone, the same sentence becomes the hardest thing to have missed") is FIX-3.11(a)'s
  keep-verbatim line and is untouched.
- **`:9`** — the three-rung ladder mapping anchors 3/4/5 in the day's idiom; it is what clears `:7`.
  "If everything is IMPORTANT, nothing is" does not condemn the Working tier's mandated two markers:
  "everything" is not two of five, and the same sentence names the two-marker state as "the climb
  from there". This is FIX-3.11(b) landed correctly. No collision.
- **`:11`** — "count the markers in your prompt, and ask whether the one you'd be angriest to see
  ignored stands alone on its own line." A compliant Novice answers "no". It is a question, not a
  verdict, and `:9` has already ruled that answer a rung rather than a failure — the same shape as
  `days/15.md:11`, ruled clean. Recorded, not filed.
- **`## Before / After` (`:17`, `:21`, `:23`)** — Before is anchor 1; After is now anchor 5, a state
  the Novice tier forecloses. That is the normal shape for every day carrying a foreclosure clause
  (days 15, 16, 22 …) and is governed by the imitate floor, derived above, not by FIX-3.22. The
  gloss at `:23` is byte-identical and is now accurate.
- Concept **195 words**, unchanged (cap 200). The edit is outside `## Concept`.

### `days/25.md` — **CLEAN**, one close call recorded, no edit proposed

- **`:5`** — condemns "Make sure it is good" as naming a feeling. The Novice tier is **silent** on
  checkability, not mandating a feeling-criterion, so nothing mandated is condemned. This is the
  `days/03.md` ruling (MASTER-FIX-PLAN.md:4349): silence is not a mandate.
- **`:7`** — states anchor 5's property as what three written checks achieve. Aspirational, naming
  the bar without calling anything below it wrong — the ground on which `days/15.md:7` and
  `days/28.md:7` were both cleared.
- **`:9`** — condemns criteria written *after* the output, which is anchor 2, below the Novice rung.
  "You don't get to relax one because this attempt came close" states the Advanced discipline to all
  tiers but forecloses nothing the Novice tier mandates.
- **`:11`** — **the close call.** "Show your criteria to someone who hasn't seen the output. Could
  they score it without asking you what you meant?" poses the *Working* bar (anchor 4) to every tier,
  and day 25's concept — unlike day 12's `:9` — carries no sentence naming the write-it-first-but-
  not-yet-specific state as a rung of its own. It asks rather than verdicts, so it is not a FIX-3.22
  collision, but a Novice learner has no in-concept sentence telling them "no" is a legitimate
  answer. Recorded so the next reader need not re-derive it. **No edit proposed** — day 25 is a
  reference ladder and this pass is not authorised to rewrite its concept.
- Concept **179 words**, unchanged (cap 200). The edit is inside `## Exercise`.

---

## Scope

```
 prompting-wizard/SKILL.md   | 2 +-
 prompting-wizard/days/12.md | 4 +++-
 prompting-wizard/days/25.md | 2 +-
 prompting-wizard/rubrics.md | 2 ++
 4 files changed, 7 insertions(+), 3 deletions(-)
```

Confirmed by mechanical diff against HEAD, not by reading:

- **Tier bodies:** all 90 tier sections across the 30 day files extracted and compared — exactly one
  changed, `days/25.md ### Advanced`. No other tier body moved.
- **`## Rubric` sections:** all 30 extracted and compared — none changed.
- **Rubric anchors:** all 156 table rows byte-identical.
- **Rubric headings:** 26, byte-identical; all slugs resolve, and all 49 `rubrics.md#slug` references
  across the skill resolve.
- **Concepts:** none touched; the two opened days sit at 195 and 179 words against the 200 cap.
- **Verbatim-rule sites:** four, byte-identical (same SHA-256 before and after).
