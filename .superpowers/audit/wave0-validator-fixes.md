# Wave 0 — validator defect fixes

Fixes the eight gaps recorded in [`validator-tests.md`](./validator-tests.md).
Seven were bugs and are fixed; one (#7) was ruled intended and is now documented
as such in the module.

Files changed: `tools/validate.py`, `tools/test_validate.py`. **Nothing under
`prompting-wizard/` was touched** — verified with `git diff --stat -- prompting-wizard/`
(empty).

Method for each bug: change the pinning test to assert the correct behaviour,
watch it fail, change the module, watch it pass. Every changed and added
assertion was replayed against the unmodified `HEAD` copy of `validate.py` to
confirm it genuinely goes red there (24 failures/errors); see
[Red evidence](#red-evidence).

## Results

| | Before | After |
|---|---|---|
| `python3 -m unittest discover -s tools` | 82 pass | **103 pass** |
| `python3 tools/validate.py --complete` | `ok`, exit 0 | **`ok`, exit 0** |
| Pyright on `tools/` | 10 errors (all `reportArgumentType`) | **0 errors** |
| Mutation check | 12/12 killed | **20/20 killed** |

No `DOCUMENTED GAP` label remains in the suite. No test was deleted.

---

## 1. Blockquoted fences were not stripped

**Before** — `FENCE` was anchored at column 0, so `> ` + backticks kept its
prefix and the block was read as prose. The live case is
`prompting-wizard/days/17.md:30-35`, a JSON sample inside a blockquoted `After`
example.

**Module** — `FENCE` gained an optional, backreferenced blockquote prefix:

```
QUOTE_PREFIX = r"(?:[ ]{0,3}>[ ]?)*"
```

The closing fence must repeat the *same* prefix text (`(?P=quote)`), so a quoted
fence is only closed at the same quote depth. That matters: without the
backreference a stray `> ` + fence could pair with an unrelated column-0 fence
far below and blank out real headings between them.

**Test** — `StripFencesTests.test_blockquoted_fence_is_not_stripped` became
`test_blockquoted_fence_is_stripped` (`"> ```\n> [...]\n> ```\n"` → `"\n\n\n"`).
`CheckConceptWordCapTests.test_blockquoted_fence_counts_toward_the_cap_unlike_a_plain_fence`
became `test_blockquoted_fence_is_exempt_from_the_cap_like_a_plain_fence`: the
same 400-word sample now costs the same whether or not it is quoted, and both
forms produce zero problems. Added: nested `>> ` fences, and two tests pinning
that quote depth must match in both directions.

**After** — a day file written in the days/17.md house style is no longer
charged for sample JSON against the 200-word Concept cap.

## 2. Indented fences were not stripped

**Before** — same column-0 anchor; a fence under a list item survived.

**Module** — `[ ]{0,3}` before the fence run, on both the opening and the
closing line, per CommonMark. Opening and closing indentation need not match.

**Test** — `test_indented_fence_is_not_stripped` became
`test_indented_fence_is_stripped`. Its fixture moved from four spaces to three,
because four spaces is an indented code block in CommonMark, not a fence; that
boundary is now pinned by a new `test_fence_indented_four_spaces_is_not_a_fence`,
so the fixture change is visible rather than silent. Added
`test_opening_and_closing_fence_indentation_need_not_match` and
`CheckConceptWordCapTests.test_indented_fence_is_exempt_from_the_cap`.

## 3. A short closing fence closed a long opening fence

**Before** — `` `{3,} `` backtracked. Given a 5-backtick opener with no
5-backtick closer, the group gave back two backticks to `[^\n]*` (the info
string) and a 3-backtick line closed the block.

**Module** — the fence run is now `(?P<fence>(?P<char>[`~])(?P=char){2,})`
followed by `(?!(?P=char))`. The negative lookahead forces a maximal munch, so
the group cannot give characters back. `(?P=char)` also makes the run
homogeneous, so the closer must be the same fence character as well as at least
as long.

**Test** — `test_shorter_closing_fence_also_closes_a_longer_opening_fence`
became `test_shorter_closing_fence_does_not_close_a_longer_opening_fence`:
`"`````\nA\n```\nafter\n"` is now left untouched, because the block is
unterminated. Added `test_equal_length_closing_fence_closes_a_longer_opening_fence`
so the fix does not simply break long fences. The pre-existing
`test_longer_fence_wrapping_inner_fences_is_stripped_as_one_block` and
`test_closing_fence_longer_than_the_opening_still_closes_the_block` still pass
unchanged.

**After** — a mis-closed long fence is left alone instead of silently ending
early and blanking the wrong lines.

## 4. A heading on the final line with no trailing newline read as missing

**Before** — `section`'s pattern was `^{heading}\s*$\n(...)`. A file ending
`## Rubric` with no final newline reported `missing '## Rubric'` for a heading
that is plainly there.

**Module** — `\n` → `\n?`. Greedy `\s*` still swallows intervening blank lines,
so every existing section body is byte-identical.

**Test** — `test_heading_on_the_final_line_without_a_trailing_newline_returns_none`
became `..._is_found` and asserts `""` (matching the trailing-newline case
pinned by `test_empty_section_returns_empty_string_not_none`). Added
`test_final_heading_with_a_body_but_no_trailing_newline_is_found`.

## 5. An unreadable file was reported twice

**Before** — the day loop and the `rglob` absolute-path scan both called
`read_text` on the same path, so one undecodable day file emitted two identical
problems and inflated the CLI's count.

**Module** — `check` now holds a per-run `cache` and reads each path through a
`load(path, label)` closure, so `read_text` fires at most once per file. This
also dedupes `rubrics.md`, which was read twice for the same reason.
`read_text` itself is unchanged.

**Test** — `test_unreadable_day_file_is_reported_twice` became
`..._is_reported_once` and asserts a single-element list. Added
`test_unreadable_rubrics_file_is_reported_once`.

## 6. Duplicate headings were silently ignored

**Before** — `section` returns the first match, so a second `## Concept` was
invisible: never validated, and its words never counted against the cap.

**Module** — new `heading_occurrences(text, heading)` counts own-line
occurrences after stripping fences. `check_day` uses the count for both arms:

```
count == 0  ->  "days/01.md: missing '## Concept'"
count > 1   ->  "days/01.md: duplicate '## Concept' (2 occurrences)"
```

`section` still returns the first copy, which is now harmless because the
duplicate is reported. Scope is the four required day sections: a general
"no repeated heading anywhere" rule would fire on legitimately repeated
sub-headings, and the required sections are where the ruling's failure mode
(uncounted Concept words) actually lives.

**Test** — `SectionTests.test_only_the_first_of_two_identical_headings_is_returned`
lost its GAP label and now asserts both halves of the corrected behaviour:
`section` returns `"first\n\n"` *and* `heading_occurrences` returns 2. Added
`HeadingOccurrencesTests` (6 tests), plus
`CheckDaySectionTests.test_duplicate_day_section_is_reported`,
`test_each_required_day_section_is_checked_for_duplication` (subTest over all
four), and `test_a_duplicate_heading_inside_a_fenced_block_is_not_counted`.

## 7. Absolute paths inside fenced blocks — intended, unchanged

Ruled intended: a fenced install snippet is exactly where a machine-specific
path hides, so a code block is not an excuse. **No behaviour change.**

The scan moved into a named `check_absolute_paths(text, label, errors)` whose
docstring records why this is the one check that reads raw text while every
other check strips fences first.
`CheckAbsolutePathTests.test_absolute_path_inside_a_fenced_block_is_still_reported`
keeps its assertions; its docstring now opens `"""Intended, not a gap: ..."""`
and points at that docstring.

## 8. `slugify` dropped non-ASCII letters

**Before** — `[^a-z0-9]+` treated `é` as a separator, so `café` → `caf`.

**Module** — `[\W_]+`. In Python's `str` mode `\W` is Unicode-aware, so the
class means "not a letter or digit"; `_` is added back because `\W` alone would
keep it, and `_` was a separator before.

**After** — `café` → `café`. Output is unchanged for every ASCII heading, which
is every heading in `rubrics.md` today: the existing round-trip test over all 26
rubric slugs (`test_every_expected_rubric_slug_round_trips_from_a_prose_heading`)
and the hyphen/whitespace/digit/punctuation tests all pass untouched.

**Test** — `test_non_ascii_letters_are_dropped_rather_than_transliterated`
became `test_non_ascii_letters_are_kept_not_dropped`. Added
`test_non_ascii_letters_are_kept_mid_heading`,
`test_underscore_is_still_a_separator` (guards the `_` in the new class), and
`test_em_dash_and_smart_quotes_are_separators`.

---

## Effect on real content

Fixes 1-3 change what counts as fenced content, so `## Concept` word counts
could move. They did not:

- The only blockquoted fence in the skill is `days/17.md:30-35`, and it sits in
  `## Before / After`, which has no word cap. The fix is preventative there.
- No file contains an indented fence (1-3 spaces), a 4+-space fence, or a fence
  longer than three characters.
- Comparing `section(text, "## Concept")` word counts across all 30 day files
  under the old and new modules: **zero differences.**
- No duplicate heading exists in any shipped `.md` file, so fix 6 adds no
  errors.

### `--complete` output

```
$ python3 tools/validate.py --complete
ok
$ echo $?
0
```

Nothing was stopped on; no file under `prompting-wizard/` was edited.

## Typing noise in the test suite

`section()` returns `str | None` and was passed straight into
`assertIn`/`assertNotIn`, which Pyright reports as `reportArgumentType`
(10 errors on the `HEAD` version, all in `SectionTests`).

Added a module-level helper:

```python
def body_of(text, heading):
    body = validate.section(text, heading)
    if body is None:
        raise AssertionError(f"fixture has no {heading!r} section")
    return body
```

`raise AssertionError` rather than `self.assertIsNotNone` because Pyright does
not narrow through a unittest method call, but does narrow past a `raise`. It
is also better hygiene: an unexpected `None` now fails with
`fixture has no '## Concept' section` instead of
`TypeError: argument of type 'NoneType' is not iterable`.

Applied at the five call sites that fed a `section()` result into a membership
check (10 such assertions). Pyright on `tools/`: 10 errors → **0**, with no
diagnostics of any rule remaining.

## Red evidence

The finished suite run against the unmodified `HEAD` copy of `validate.py`:

```
Ran 103 tests
FAILED (failures=17, errors=7)
```

All 24 are the tests whose assertions this change corrects (the 7 errors are
calls to `heading_occurrences`, which does not exist on the old module). The
tests that pass against both modules are deliberate regression guards for
behaviour that was already right — the 4-space-indent boundary, quote-depth
mismatch in both directions, equal-length long closers, and the intended
abs-path-in-fence behaviour.

## Mutation check

Re-ran the 12 mutants from `validator-tests.md` plus 8 new ones aimed at the
fixes, each applied to a disposable copy of the module.

| Mutation | Result |
|---|---|
| `CONCEPT_MAX_WORDS` 200 → 300 | killed (2) |
| drop `capstone` from `TECHNIQUES` | killed (3) |
| drop `AGENTS.md` from `TOP_FILES` | killed (1 failure, 2 errors) |
| drop `## Rubric` from `DAY_SECTIONS` | killed (1) |
| `FENCE` made greedy | killed (1) |
| `section` lookahead → `^#{1,6} ` | killed (7) |
| `ABS_PATH_ALLOWED` emptied | killed (2) |
| `slugify` loses `.strip("-")` | killed (3) |
| `read_text` swallows the error | killed (6) |
| `strip_fences` stops preserving line count | killed (13) |
| `require_all_days` ignored | killed (2) |
| both `FENCE` line anchors removed | killed (2) |
| **fix 1/2**: quote prefix dropped from opener | killed (6) |
| **fix 1/2**: opener indentation dropped | killed (3) |
| **fix 1**: closer quote depth not backreferenced | killed (2) |
| **fix 3**: maximal-munch lookahead removed | killed (1) |
| **fix 4**: heading newline made mandatory again | killed (1) |
| **fix 5**: read cache removed | killed (2) |
| **fix 6**: duplicate branch removed | killed (5) |
| **fix 8**: `slugify` back to `[^a-z0-9]+` | killed (2) |

**20 of 20 killed.** Every fix is pinned by at least one test that dies if the
fix is reverted.

## What remains uncovered

Carried forward from `validator-tests.md`, still true:

- `OSError` variants other than `FileNotFoundError` (permission denied,
  `IsADirectoryError`).
- CRLF line endings.
- Problem ordering, except for `require_all_days`.
- `rglob` traversal edge cases — symlinks, symlink loops.

New, introduced by these fixes:

- A blockquote prefix must match the closing fence *exactly as text*, so
  `> ```` opened and `>```` closed (marker without its space) does not pair.
  CommonMark would pair them. Not worth the regex.
- Duplicate detection covers the four required day sections only; a repeated
  `## Noun` in `rubrics.md` would still merge silently into `h2_slugs`.
- Fence detection has no list-context awareness, so a fence indented four or
  more spaces inside a deeply nested list item is not stripped.
