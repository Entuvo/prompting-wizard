# SDD ledger — plan: docs/superpowers/plans/2026-08-09-prompting-wizard.md
branch: feat/prompting-wizard
base: 63574e1

Task 1: review clean on spec (commits 63574e1..532f879); quality Approved
Task 1: 2 Important findings labeled plan-mandated — awaiting human ruling
  (a) section()/h2_slugs are fence-unaware: a `# ` line inside a fenced block truncates a section
  (b) read_text() unguarded: non-UTF8/permission error crashes harness with bare traceback
Task 1: minor (deferred): ABS_PATH_ALLOWED exempts the whole line, not the match
Task 1: fix round 1/5 (3 addressed, 0 open; commits 532f879..0ff6c40)
Task 1: minor (deferred): section() re-strips fences on every call (perf nit)
Task 1: minor (deferred): closing fence must start at col 0; CommonMark allows 3-space indent
Task 1: complete (commits 63574e1..0ff6c40, review clean)
Task 2: review spec-compliant on structure (26/26 slugs, 26 five-row tables); quality Needs fixes
Task 2: 1 Important — ## Verb moved brief's score-5 anchor to score-4, invented new score-5
Task 2: minor (deferred): Adverb-3 "part of the task" undefined
Task 2: minor (deferred): Determiner 4/5 boundary hinges on "minor reading left open"
Task 2: fix round 1/5 (4 addressed, 0 open; commits 276ac5f..9041425)
Task 2: complete (commits 0ff6c40..9041425, review clean)
Task 3: complete (commits 9041425..dc3f9be, review clean, no fix round)
Task 4: complete (commits dc3f9be..a992fbd, review clean, no fix round)
  MILESTONE: validator green (ok, exit 0) — scaffolding complete, content remains
Task 5: complete (commits a992fbd..844f9e7, review clean, no fix round)
  template locked: 4 H2 sections, 3 H3 tiers, rubrics.md#slug ref, {{TASK}} token, concept 129w
Task 5: minor (deferred): reviewer trusted reported word count instead of counting it
Task 6: complete (commits 844f9e7..2b76a83, review clean, no fix round)
  days 02-07 written; concepts 163-185w; concept-rubric alignment verified per day
Task 6: minor (deferred): day 04 concept least distinctive of the six (not a defect)
Task 7: complete (commits 2b76a83..db858ff, review clean, no fix round)
  days 08-14 written; all 11 lever slugs now have a lesson (verified); concepts 169-187w
Task 7: minor (deferred): days 09/11 run 5 concept paragraphs vs batch norm of 4
Task 7: minor (deferred): day 09 third paragraph syntactically dense
Task 7: minor (deferred): day 14 title spells "eleven"; brief table says "11"
PROJECT GAP (for Task 10): no .gitignore; tools/__pycache__/ left untracked
Task 8: review spec-compliant on structure; 4 Important findings (reviewer summary said
  "Approved" but Importants govern -> fix loop entered)
  (1) day 19 concept teaches gating; rubrics.md#reasoning-scaffolds never scores it
  (2) day 20 before-seed has a generic exclusion; brief specified "no exclusions"
  (3) day 17 After schema uses prose type-descriptions, not dummy values; not valid JSON
  (4) day 21 report claimed ~280 words; actual 217 (file fine, report inaccurate)
Task 8: minor (deferred): day 15 tier progression uneven (2 things -> 1 -> 2)
NOTE: fence-strip fix still unexercised; day 17 schema is JSON with no # comment lines
Task 8: minor (deferred): validator FENCE regex anchored at col 0 — blockquoted fences
  ("> ```", as in days/17.md:30-35) are NOT stripped. No current defect (no # lines inside),
  but widens the earlier col-0 deferred minor. For final review triage.
Task 8: fix round 1/5 (6 addressed, 0 open; commits 74d1156..3e48ea7)
Task 8: minor (deferred): day 17 dummy-value vocabulary differs between its two blocks
Task 8: minor (deferred): day 19 Advanced tier escalates harder than batch norm
Task 8: complete (commits db858ff..3e48ea7, review clean)
Task 9: review spec ❌ — 4 Important concept-rubric misalignments; quality Needs fixes
  (1) day 30 "add criteria and it clears 3" inverts capstone anchor 3 (defined by their absence)
  (2) day 29 concept teaches lever rubrics, not capstone axis; day-29 work caps at anchor 3
  (3) day 23 teaches ordering; rubric scores presence/gameability. PLAN CONFLICT: brief's
      Advanced constraint IS the ordering line (which is rubrics.md's fastest-fix heuristic,
      not a scored anchor). Implementer put it in Novice and invented un-gameable Advanced.
  (4) day 28 closing test checks cross-prompt slot vocabulary; rubric scores a single prompt
  baseline gap CONFIRMED: day 14 re-scores all 11 levers, so day-0 values are lost by day 14
Task 9: minor (deferred): day 26 After cuts ~90% not "a third" (tiers grade correctly)
Task 9: fix round 1/5 (6 addressed, 1 new breakage: day 29 self-contradiction; commits 18ed1e2..bd184dd)
Task 9: fix round 2/5 (3 addressed, 0 open; commits bd184dd..ce4eb74)
Task 9: complete (commits 3e48ea7..ce4eb74, review clean)
  ALL 30 DAYS WRITTEN. validator --complete green.
Task 9: minor (deferred): day 28 Working tier reads at anchor-5 completeness, not anchor-4
Task 9: minor (deferred): reviewer recounts (179/179/179) differ slightly from implementer's
  (181/181/184); both well under cap, different counting methods, not worth a round
Task 10: 4/6 verifications passed; 2 found REAL SKILL.md defects (found by behavioural trace,
  missed by nine tasks of structural review):
  (A) SKILL.md:26 presents ## Exercise with no {{TASK}} substitution -> learner sees raw token
  (B) SKILL.md:13 absent PROGRESS.md silently runs assessment -> mid-course loss restarts at day 1
  Both contradict the plan's own Error Handling / Lesson-format sections. Ruled: implementation
  bugs, not plan-vs-finding conflicts. Plan amended (Task 4 Step 1b). Fix dispatched.
Task 10: Codex parity statically verified 4/4; live run pending (user running it manually)
Task 10: fix round 1/5 (2 addressed, 0 open, 9 behavioural rules verified intact; c013a37..66ddd97)
Task 10: complete (commits ce4eb74..66ddd97, review clean)
  OUTSTANDING: live Codex parity run — user executing manually, report expected at
  .superpowers/sdd/2026-08-09-prompting-wizard/codex-parity-report.md
CODEX LIVE RUN #1: fixture corrupted in paste (## Tasks + ## Log replaced by cmux task-panel
  render). Codex behaved CORRECTLY given the corrupt file: named ## Tasks as failed field,
  stopped, refused to infer, never ran anything in lesson context. Error-handling path verified.
  Daily loop still unverified in Codex. Fixture rewritten directly; re-run pending.
TWO REAL DEFECTS from the live run (only a live run could find these):
  (C) SKILL.md:38 claims Codex needs multi_agent=true in [features] to dispatch. FALSE —
      Codex 0.147.0 exposed spawn_agent with no such entry. Tutor would wrongly fall to Tier B.
      Fix: detect by tool availability, not by inspecting config.
  (D) SKILL.md:14 recovery "accept a day number the learner states" is over-broad — a day
      number cannot repair a missing ## Tasks section. Needs per-field recovery.
FINAL WHOLE-BRANCH REVIEW (opus): verdict "Merge with fixes". 0 Critical, 8 Important.
  Confirmed both Codex defects (C, D). Ruled the fence-regex gap structurally unreachable
  (a blockquoted fence can never contain a col-0 heading) — closed, not merely deferred.
PARKED (human ruling): systemic anchor-5 Working-tier compression on days 02, 08, 16, 17, 18,
  24, 26, 27, 28 — Working written at anchor-5 language, so anchor 4 unreachable and
  Working/Advanced score identically. Real, systemic, NOT fixed in this wave. Deliberate
  follow-up pass required; reviewer's guidance was to fix the sweep or accept the pattern,
  never to fix day 28 alone. Ruling: accept for now, sweep later.
STILL UNVERIFIED at merge: day 15 traced on neither harness; Codex daily loop (re-run pending).
FINAL FIX WAVE: 9 findings addressed in one dispatch (commits 66ddd97..09a9a88, 9 files).
  Scoped re-review clean: 9/9 addressed, 9 behavioural rules intact, parked sweep untouched
  on days 16/18/27, no new breakage. FINAL REVIEW GATE PASSED.
BRANCH READY: feat/prompting-wizard @ 09a9a88, 21 commits off 63574e1. validator --complete ok.
CODEX LIVE RUN #2 (full day-1 loop, real spawn_agent, two separate clean agents): CONFIRMED
  working — {{TASK}} substituted into tier, exactly 1 of 2 eligible weak levers, noun anchor
  quoted verbatim, separate clean contexts, never ran in lesson context. Tier A verified.
FOUR NEW FINDINGS (behavioural, only a live full-loop run could surface these):
  (E) IMPORTANT: pedagogy can invert. Vague prompt exploited workspace context and returned
      MORE than the precise one, which stalled for a missing artifact. SKILL.md's "rubric only,
      no freelance criticism" then FORBIDS the tutor explaining the confounder.
  (F) {{TASK}} substitution is grammatically broken — ## Tasks entries are gerund phrases:
      "Help me with Reviewing PRs on the payments service". Affects all 30 days.
  (G) secondary weak-lever constraint is added but never scored or discussed anywhere.
  (H) "update any lever scores the day changed" — overwrite/average/other is undefined.
  (also noted) clean conversation context != isolated filesystem; spawned agent shares workspace.
STATUS: branch feat/prompting-wizard @ 09a9a88 ready to land; findings E-H NOT fixed.
