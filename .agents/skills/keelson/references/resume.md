# Workspace routing and current state

Resolve where work lives before treating a checkpoint's phase as current. A launch directory, engineering worktree and release destination can differ.

## Locate the active workspace

1. Inspect the launch directory's instructions, `.keelson/checkpoint.md` and `.keelson/active-worktree.md` when present. Read the current routing statement before historical entries. Resolve relative paths from the record's stated base; ordinary Markdown links are relative to their file. Ambiguous legacy paths require inspection, not a guessed write target.
2. Follow an explicit engineering-workspace pointer. Confirm the target exists, inspect its applicable instructions, Git status/revision and current checkpoint. For Git worktrees, verify repository identity through `git worktree list` or the common Git directory. A separately exported release candidate needs its recorded source/manifest relationship; it is not automatically the engineering workspace. A newer direct work instruction can promote that export to the maintained repository; verify the instruction and current repository rather than preserving an obsolete “export only” label. Non-Git projects use their existing project identity and source records.
3. Keep visited paths while following forwarding records. If a target is missing, a cycle occurs, or records conflict, inspect available worktrees and source/evidence records. Block dependent writes until the workspace is established; continue independent reads. Ask only for an unresolved location or choice. Do not silently fall back to a stale primary checkout, recreate missing work or request implementation approval already granted.
4. In the verified workspace, compare current files/revision with the selected evidence, inspect interrupted work and actual worker state, and choose the next authorized action. Trace consequential next actions in assistant-written checkpoints/plans back to a user instruction or accepted decision. The newest record routes work; it cannot itself authorize a product choice. If it promotes an unsupported proposal, preserve the record as history, correct active guidance and return to the user's requested activity. A request to resume does not automatically accept that proposal; explicit authorization already granted remains valid. Historical “pending” phases and release-folder timestamps do not supersede current records. A pointer grants no new permissions or authority; follow existing access and task limits.

For discovery resume, reconcile the queued question with accumulated meaning in original input and the current intake/brief. Retire questions already answered, including incidental answers and shared behavior established in another scenario. Preserve unresolved source-specific differences; a scenario label alone is not a new gap. Correct stale active plans/checkpoints in the same turn, preserving superseded history. Continue with synthesis or a material remaining question, not a restarted interview. No question need be queued automatically, and consolidation does not authorize solution design. Later explicit execution still controls its own scope.

For architecture/delivery resume, compare the brief's requested outcomes and existing applicable-deliverable rows with actual artifacts and evidence before trusting a completed phase. Inspect review purpose and exclusions, not only ready/current hashes. Restore missing deliverables or stale affected diagrams to outstanding work and correct the checkpoint; do not restart unchanged architecture exploration or routine-edit discovery. A narrow historical pass cannot authorize dependent implementation while required design artifacts remain missing.

## Keep a short current checkpoint

Route to outstanding work after the current turn. An explanation given in the reply is completed activity, not the next action. Do not force the next session to repeat it. Routine edits need no new intake record, but if an existing status claim becomes false (such as “no code changed”), correct or remove that claim and reconcile affected next actions without reopening discovery.

At a meaningful boundary, replace the current summary. Preserve the current checkpoint/plan in a linked history file before each replacement at that boundary; keep its source links resolvable from the archive’s location. An archive of an earlier version does not preserve the version being replaced. Preserve original inputs, decisions and review receipts in their owning records. Keep the existing summary small enough to read in one pass. History is read only when needed to resolve a dependency or contradiction.

Use these fields, or equivalent existing records:

```text
Updated: date
Engineering workspace: absolute path; repository/branch and inspected revision
Release destination: path and source relationship, if different
Outcome and current phase: one current unit
Authorization: source and applicable limits
Evidence: checks/review receipts; current, stale or unverified
Active work: owner and actual worker/process state
Open dependencies: only those affecting next work
Next action: concrete authorized step
History: link to superseded narrative
```

When work moves, keep a short forwarding checkpoint in the primary checkout and update any existing active-worktree pointer. The active workspace owns current delivery state; forwarding records identify it rather than duplicating that state. If project policy excludes private workflow files from the maintained source tree, record an explicit external checkpoint location alongside the engineering path and keep those files there. Reuse the exact existing owning-record filename; the template does not rename a record such as `current-product.md` to `checkpoint.md`. Do not install internal records into an excluded public tree. Preserve an explicit release destination separately. Reconcile existing legacy records once using evidence; do not treat old dates or missing fields alone as grounds to repeat completed work.

Inspect the owning project’s dashboard map after routing is resolved. Follow [dashboard upkeep](dashboard.md): compare declared sources and current scope, reconcile only affected mappings/evidence, and surface stale or unverified status. Registration alone never refreshes source hashes or establishes behavior.
