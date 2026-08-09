# Test suite for `tools/validate.py`

Suite: `tools/test_validate.py` — 82 tests, stdlib `unittest` only, no new
dependencies and no build step. Fixtures are built in
`tempfile.TemporaryDirectory` and `validate.SKILL` is repointed per test via
`addCleanup`, so nothing reads or mutates `prompting-wizard/`.

`tools/validate.py` was not modified.

## How to run

```
$ python3 -m unittest discover -s tools
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 0.178s

OK
```

`python3 tools/test_validate.py` runs the same 82 tests with per-test names.

Note: bare `python3 -m unittest discover` from the repo root finds **0 tests** —
`tools/` is not a package, and Python 3.11 dropped namespace-package discovery.
`-s tools` is required. Adding `tools/__init__.py` would fix it but restructures
`tools/`, so it was not done.

## What is covered

| Target | Tests | Notes |
|---|---|---|
| Shipped contract | 8 | `TOP_FILES`, 11 levers, 15 techniques, day sections, tiers, word cap, allowlist — pinned as literals so widening a rule is a visible test change |
| `slugify` | 10 | real cases (`Few-shot examples`, `Agent and tool prompting`), separator runs, trimming, digits, empty, punctuation-only, non-ASCII; all 26 rubric slugs round-trip from a prose heading |
| `strip_fences` | 14 | backtick and tilde, non-greedy separation, longer/shorter closers, cross-type closers ignored, line-count preservation, unterminated, blockquoted, indented |
| `section` | 10 | `##` spans `###` but stops at `##`/`#`; `###` stops at `###`; absent heading; last-section-to-EOF; fenced `#` does not truncate; empty section; duplicate headings; heading at EOF without newline |
| `h2_slugs` | 4 | headings found, fenced headings ignored, `#`/`###` ignored, empty |
| `read_text` | 4 | success, missing file, undecodable bytes, appends without discarding — never raises |
| `check` | 28 | clean fixture; each failure mode in isolation asserted as *exactly one* message; allowlist; `require_all_days`; unreadable files |
| CLI | 4 | `ok`/exit 0, `N problem(s)` on stdout with detail on stderr/exit 1, `--complete` |

Each `check` failure mode asserts the full problem list equals one expected
string, so a fix that produces the right message plus a spurious second one
fails.

The CLI tests copy `validate.py` into a temp dir beside a fixture skill tree and
run it as a subprocess, so the `ok` / exit-code contract that the ten build
tasks gate on is verified without depending on real content.

## Coverage reached

100% line coverage of `tools/validate.py` — 95 executable lines, all executed:
66 in-process (measured with `sys.monitoring`), 23 import-time definitions, and
the 6-line `__main__` block via the subprocess CLI tests.

Line coverage is weak evidence on its own, so the suite was mutation-tested
against a disposable copy. **12 of 12 mutants killed:**

| Mutation | Result |
|---|---|
| `CONCEPT_MAX_WORDS` 200 → 300 | 2 failures |
| drop `capstone` from `TECHNIQUES` | 3 failures |
| drop `AGENTS.md` from `TOP_FILES` | 1 failure, 2 errors |
| drop `## Rubric` from `DAY_SECTIONS` | 1 failure |
| `FENCE` made greedy (`.*?` → `.*`) | 1 failure |
| `section` lookahead → `^#{1,6} ` | 7 failures |
| `ABS_PATH_ALLOWED` emptied | 2 failures |
| `slugify` loses `.strip("-")` | 3 failures |
| `read_text` swallows the error | 5 failures |
| `strip_fences` stops preserving line count | 9 failures |
| `require_all_days` ignored | 2 failures |
| both `FENCE` line anchors removed | 3 failures (the gap tests) |

The first pass had two survivors, both fixed: the word-cap tests derived their
fixtures from `CONCEPT_MAX_WORDS` (so they adapted to any cap) and no test
pinned the shipped constants. Hence `ContractTests` and literal 200/201 word
fixtures. Removing only the *opening* `^` anchor is a genuinely equivalent
mutant — the closing fence stays anchored, so blockquoted fences are still not
stripped — which is why the both-anchor mutant is listed instead.

## What remains uncovered

- **Real skill content.** Deliberate, per constraint. `python3 tools/validate.py --complete` against `prompting-wizard/` is still a separate manual gate (currently `ok`).
- **`OSError` variants other than `FileNotFoundError`.** Permission-denied and `IsADirectoryError` (a directory named `*.md` under the skill) take the same `except` arm but are untested; the message would read `unreadable (IsADirectoryError)`.
- **CRLF line endings.** `\r` is a `\s` and a `[^a-z0-9]`, so behaviour is plausible but unverified. A Windows-authored day file is untested.
- **Problem ordering** is asserted only for `require_all_days`; elsewhere tests assert set membership or single-element lists.
- **`rglob` traversal edge cases** — symlinks, symlink loops, non-`.md` files.
- **Unicode beyond the one `café` case** (em-dashes, smart quotes in headings).

## Bugs and surprising behaviour found

Each is pinned by a test that asserts **current** behaviour and is marked
`DOCUMENTED GAP` in its name or docstring. None were fixed.

### 1. Blockquoted fences are not stripped (known; now pinned)

`FENCE` is anchored at column 0, so `> ` + backticks keeps its prefix and the
block is treated as prose. Live example: `prompting-wizard/days/17.md:30-35`.

- `StripFencesTests.test_blockquoted_fence_is_not_stripped`
- `CheckConceptWordCapTests.test_blockquoted_fence_counts_toward_the_cap_unlike_a_plain_fence`

The second test is the one that matters: it writes the *same* 400-word sample
twice, plainly fenced and blockquote-fenced, and shows the plain one passes
while the quoted one fails the 200-word cap. A day written in the days/17.md
house style is charged for sample JSON it should never have been charged for.
Section boundaries are safe — a `## ` inside a blockquote is not at column 0
either — so the word cap is the live consequence.

### 2. Indented fences are not stripped

Same column-0 anchor. A fence nested under a list item survives.
`StripFencesTests.test_indented_fence_is_not_stripped`

### 3. A shorter closing fence closes a longer opening fence

CommonMark requires the closer to be at least as long as the opener. Here
`` `{3,} `` backtracks to three backticks when no equal-length closer exists, so
` ````` ` … ` ``` ` closes. `StripFencesTests.test_shorter_closing_fence_also_closes_a_longer_opening_fence`

Low impact today — a correctly closed ` ```` ` wrapper around inner ` ``` `
blocks still works (`test_longer_fence_wrapping_inner_fences_is_stripped_as_one_block`) —
but a *mis*-closed long fence silently ends early instead of being left alone.

### 4. A heading on the last line without a trailing newline reads as missing

`section`'s pattern requires a `\n` after the heading line, so a file ending
`## Rubric` with no final newline reports `missing '## Rubric'` for a heading
that is plainly there. With a trailing newline the same empty section returns
`""` and passes. This is the most likely of these to bite a real author, since
plenty of editors will save without a trailing newline.

`SectionTests.test_heading_on_the_final_line_without_a_trailing_newline_returns_none`
(and `test_empty_section_returns_empty_string_not_none` for the contrast)

### 5. An unreadable file is reported twice

The day loop and the `rglob` absolute-path scan both call `read_text` on the
same file, so one undecodable day file emits two identical problems and inflates
the count printed by the CLI.
`CheckUnreadableFileTests.test_unreadable_day_file_is_reported_twice`

### 6. Duplicate headings: only the first copy is validated

`section` returns the first match, so a day file containing two `## Concept`
blocks validates the first and ignores the second entirely — including its word
count. `SectionTests.test_only_the_first_of_two_identical_headings_is_returned`

### 7. Absolute paths inside fenced code blocks are still flagged

The absolute-path scan runs on raw text; every other check strips fences first.
An example transcript in a code block therefore cannot show a home path. This
may well be intended — it is the one check where a code block is not an excuse —
but the inconsistency is undocumented.
`CheckAbsolutePathTests.test_absolute_path_inside_a_fenced_block_is_still_reported`

### 8. `slugify` drops non-ASCII letters rather than transliterating

`café` → `caf`, because `[^a-z0-9]+` treats `é` as a separator and it collapses
into the trailing hyphen that is then trimmed. Harmless for the current
all-ASCII headings; a rubric heading with an accent would produce a slug no
`rubrics.md#…` reference would plausibly match.
`SlugifyTests.test_non_ascii_letters_are_dropped_rather_than_transliterated`

## Suggested follow-up (not done here)

Priority order if the module is ever opened for fixes:

1. **High** — #4, heading-at-EOF. Produces a false "missing" on valid content.
2. **High** — #1/#2, fence anchoring. Allow optional `> ` and leading whitespace before the fence, keeping line-count preservation.
3. **Medium** — #5, dedupe problems before returning, or skip files already read.
4. **Medium** — #6, report a duplicated required heading rather than silently taking the first.
5. **Low** — #3, #7, #8.

Every one of these would be caught by the existing suite as a deliberate,
visible test change: the `DOCUMENTED GAP` tests are written to fail the moment
the behaviour is corrected.
