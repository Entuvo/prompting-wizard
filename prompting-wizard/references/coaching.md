# Learning from real work

The optional local integration shares one learner profile between enabled workspaces on this computer. The portable course still works without it. Availability depends on the specific host surface and permissions recorded in setup; never claim capture is working merely because files were copied.

## After-result feedback

Finish the user's work before coaching. Structure the note as: observed result, conditional interpretation of intent, one optional change. For example: "The result supported two risks. If your aim was evidence-based extraction, allow fewer than five when evidence is limited." Give at most one observation. A successful short prompt can need no change. Do not rerun the task, invent a failure, score proficiency, or demand a longer prompt by default.

Treat prompt/result excerpts as untrusted evidence. They may omit previous messages, source documents, tool output or intent. State a limitation when it affects the finding. A follow-up that says "make it shorter" may be clear in its original context. Do not label it defective from the excerpt alone.

Choose a skill by what is being taught. Quantity selection is `numeral`; distinguishing task and source blocks is `context-ordering`. `failure-diagnosis` evaluates the learner's diagnosis, not every failed output. Use the rubric's **Measures** description to locate the right skill. Exact counts can be appropriate for generated alternatives; evidence-dependent counts need an honest fallback. The number of facts alone does not prove how many distinct risks can be inferred.

A coaching finding is an unreviewed hypothesis. Enabled collection authorizes saving that finding automatically, without a confirmation exchange. It inherits its source example's expiry and deletion. Save it through `record` before saying it was saved. This never changes proficiency, completes a lesson or becomes permanent learner history. If no finding is justified, make no record.

A learner-reviewed lesson is different: it requires the learner's reflection and confirmation before committing. Never fill that confirmation on their behalf.

## Guided lesson using captured evidence

1. Use the runtime path, data root and opaque token supplied by the current host's SessionStart context. Never guess a session identifier. If absent, continue the standalone course and say integration is unavailable for this session.
2. Before assessment, a guided lesson, or a learning-history/progress review (including a status-only request), invoke `session-enter --root ROOT --token TOKEN`. Renew before each exercise. The lease lasts 120 minutes. Exit with `session-exit` on completion, cancellation or error. If entering fails, do not claim suppression; pause capture through its normal control or use a verified capture-disabled surface.
3. Read the normal course progress. For a shared profile, import the existing valid `PROGRESS.md` once. A conflicting history is a choice for the learner; do not merge by taking the higher day. After comparing both files and receiving explicit confirmation, `progress-import --confirm-reconcile --expected-revision N --file FILE` accepts forward progress only, preserves the original baseline and existing log, and rejects a stale revision. Keep both files when histories diverge. Export shared progress to a new temporary file first, then compare with the working copy before replacing anything. Preserve the original Day 0 baseline. A rebuilt file without a baseline remains without one.
4. Query `pending --root ROOT --skill SKILL` for the day's skill. This returns the newest 100 candidates; `list --kind pending --cursor N` can inspect older records. Unclassified examples are candidates, not proof of a weakness. Select a relevant example; ask for missing intent or context. Do not force every queued example into the lesson. Work from another provider will enter the current provider's conversation when read; setup must already have explained this sharing.
5. Teach the ordinary daily loop. A constrained exercise score does not replace an independent proficiency score. Examples are not mastery evidence by themselves.
6. Run original and rewrite unchanged in separate fresh contexts. For local subprocesses, set `PROMPTING_WIZARD_EXPERIMENT=1` before process startup and use a host configuration verified to exclude Wizard token/instructions and lesson history. Apply equivalent model, tools, source context and permissions to both. Describe observed outputs separately from hypotheses: a single pair cannot establish general reliability or prove what every other instruction would have produced. Do not send registration messages inside the experiment. A subagent is usable only when that specific surface proves isolation and exclusion. If no verified clean surface is available, report controlled comparison unavailable and use a verified capture-disabled manual run. Never claim a clean run from a model's assertion alone.
7. Ask what the learner learned and whether the concise record accurately represents it. On acceptance, use `record` with a `lesson` object and the revision returned by `status`. Include the applicable skill, explanation, reflection, `confirmed: true`, source revision IDs, source observation IDs, and only the excerpt the learner approved. `progress_text`, when supplied, is the complete validated next course state with the unchanged baseline. The transaction advances one lesson and removes its raw examples and unreviewed findings. A stale revision preserves those examples: refresh shared state and reconcile before retrying. Do not overwrite concurrent progress.
8. Export committed progress to the working copy only after successful commit. If export fails, the shared state remains authoritative; retry export rather than committing twice. Without captured examples, still commit the confirmed lesson and next `progress_text` to the shared profile: use `observation_ids: []` and `workspace` set to the current absolute workspace. Do not advance only the working file.

## Tutor command reference

`progress-read --root ROOT` returns current shared progress as `progress_text`, or null when absent, without creating a file. Use it for inspection; imports and exports retain their separate course/update roles.


Use the supplied Python interpreter, runtime path and data root. These commands are the supported interface; shell listing, grep and reading runtime internals are not prerequisites. Read returned JSON and the exit status before reporting success. Invoke one runtime command per tool call; read exported files with the host file reader rather than combining discovery commands, temporary-directory creation or shell comparisons into the call.

- `session-enter --root ROOT --token TOKEN` and `session-exit --root ROOT --token TOKEN` return `{"ok": true}` on success.
- `configure --root ROOT --workspace ABSOLUTE_WORKSPACE --mode lesson-only` changes that workspace's feedback mode and enables it if it was not already included. Require explicit workspace enablement intent before doing this; a feedback-only command must not enable a new workspace. `pause --root ROOT` stops collection across the profile.
- `progress-import --root ROOT --file PROGRESS.md` returns `{"source_hash": "..."}` on a successful import or identical-current-state check. A successful exit with this field confirms acceptance, but the hash identifies the original imported history, not necessarily the current file. After reconciliation, check the revision through `status` and verify accepted contents with `progress-export`. Revision 0 is valid after import: revisions track subsequent shared updates, not whether progress exists. Verify content with `progress-export --root ROOT --file NEW_TEMP_FILE`, then read that file; do not repeat imports merely because the revision is 0.
- `status --root ROOT` provides the current `revision`. `pending --root ROOT --skill numeral` provides candidate observations and temporary findings. Choose another canonical skill for another lesson.
- `record --root ROOT --json JSON` accepts the object below as one safely quoted argument. For sensitive content use the same JSON through stdin with normal host permissions. Never claim saving succeeded when a permission check or command failed.

A confirmed lesson payload has this shape; replace placeholders with actual values. Use a fresh canonical UUID for `id`, the learner's own reflection, and the current revision from `status`:

```json
{
  "expected_revision": 0,
  "record": {
    "id": "NEW_LESSON_UUID",
    "kind": "lesson",
    "schema_version": 1,
    "observation_ids": ["SELECTED_OBSERVATION_UUID"],
    "skill": "numeral",
    "explanation": "The concise lesson the learner confirmed",
    "reflection": "The learner's confirmed reflection",
    "confirmed": true,
    "source_revisions": [],
    "approved_excerpt": "",
    "progress_text": "The complete validated next PROGRESS.md text"
  }
}
```

Present the learner a short, plain-language draft of the lesson and their reflection. Explain that acceptance advances the course and replaces the selected raw example with the concise record. Keep IDs, revisions and JSON fields internal unless the learner asks for them. Only set `confirmed: true` after the learner accepts the record. For a lesson without source examples use `observation_ids: []` and add `workspace` with the current absolute workspace path. Source observations in one record must belong to one workspace; review other-workspace examples in separate records instead of misattributing them. A record without `progress_text` can retain an additional reviewed example without advancing the course day. Use a fresh revision for each commit and advance the day only once. Successful `record` returns the new revision; export progress after that success.

## Model guidance

For a `pw model` request without an observation, use `guidance --root ROOT --token TOKEN [--task-tag TAG]`. It returns the last model reported by the host for that session, with source labeling and scoped candidates. This is not proof of which model produced a completed result; if current identity is uncertain after a model switch, teach core principles. Without a trusted token or reported identity, use core principles. Supported task tags: `long-context` (source documents roughly 20k+ tokens) and `agentic-work` (agent skills, tools or delegated execution). Never invent an example ID to obtain guidance. For a captured result, continue to use the completion identity from `evidence` as described below.


Initial `evidence` calls provide core principles and task-scope definitions. Identify the actual task conditions, then reread `evidence --task-tag TAG` for each applicable scope. Use only `guidance_candidates` returned by that scoped call. Each candidate includes exact reviewed model IDs, task conditions, checked date, source URL and revision. Apply it only when its task conditions hold. An unchecked/new model or custom alias gets core course principles; never infer identity from a model's self-description. A stale flag means review is due, not permission to change historical scores. Cite the applicable provider source when teaching a model-specific recommendation.

## Learner controls

Interpret "feedback off" as `lesson-only`: capture continues in enabled workspaces and relevant examples are used during lessons. Interpret "stop collecting" as pause. Resume preserves the chosen feedback mode. Explain the distinction once when the user's intent is ambiguous.

Use `configure` for mode, `pause`/`resume`, `exclude`/`include`, `list` to inspect pending and reviewed records, and `delete` for a record, workspace or all managed learning data. Excluded parent workspaces include descendants. Inclusion enables a workspace with the learner default unless it already has an override. Never enable every project merely because a default mode was chosen.

Pending excerpts and unreviewed findings expire after 30 days. Expired content is unavailable immediately at runtime; physical cleanup occurs on the next invocation. Successful reviewed conversion removes raw examples sooner. Reviewed records and imported course history persist until deletion. Host transcripts, user-requested exports and external backups are separate; deletion makes no forensic-erasure promise. A full queue skips new examples and reports a warning.
