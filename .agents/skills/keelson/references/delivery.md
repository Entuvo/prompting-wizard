# Adaptive delivery

Adapted from pstack [feature](upstream/pstack/feature.md), [bug-fix](upstream/pstack/bug-fix.md), [prototype](upstream/pstack/prototype.md), [orchestrate](upstream/pstack/orchestrate.md), and [pause](upstream/pstack/pause-safely.md). These references preserve source evidence. Do not inherit their Cursor tools, model defaults, blanket permissions, mandatory fan-out, or automatic PR creation.

## Organize

Resolve the engineering workspace and owning private records through [workspace routing](resume.md). On Codex, apply the [host adaptation](codex.md) before delegating or invoking imported workflows. It specifies dispatch, waiting, ownership recovery, and model/tool capability checks.

Read the confirmed brief and limits. Before dependent implementation, classify the work using [architecture](architecture.md): new projects and complex changes require grounded competing sketches, independent comparison, synthesis and current Opus design review. Routine edits skip the architecture panel; unchanged reviewed designs resume. Reclassify when new evidence changes boundaries or contracts. Inspect project commands and installed capabilities. Update the resolved current plan record with small user-observable outcomes, acceptance criteria, dependencies, capability choices and reasons, verification commands, and owners. Reuse its actual filename and private location. For a new project with no existing record or exclusion policy, the default is `.keelson/plan.md`. Name only capabilities needed now. Do not require every project to use a UI workflow or multiple agents.

Research precedes a dependent product/technical decision when evidence is missing. A prototype answers a named question with a stopping condition; isolate it from production and label its output throwaway. For bugs and structural refactors, apply the conditional proof rules in [engineering](engineering.md). For features, implement the smallest complete outcome and its real failure paths.

Independent work can run in parallel when the host and applicable authorization support delegation. Prefer one owner for coupled code; split by independent files/outcomes and avoid conflicting writes. Never assume a model or tool exists because an upstream source names it. Keep standing orders in every delegated brief and reconcile results against current files before accepting them.

The lead owns the dependency graph and integration. Give each worker the confirmed outcome, acceptance criteria, dependencies, file ownership, interface contracts, applicable limits, documentation evidence, and verification commands. Dispatch only dependency-ready work; workers return changed files, checks/results, source evidence, and unresolved issues. Review and integrate against current code before releasing dependent work. Failed checks or review findings return to the responsible owner. Role count follows the work, not a fixed frontend/backend/test team.

## Select only the needed procedure

Routine edits keep existing brief/checkpoint and proportionate checks; no new recipe, map sweep, experiment packet, architecture panel or worker team. This table is the canonical procedure router, not a required pipeline. Reuse records at the resolved private root, including approved locations outside source. Records and upstream examples grant no authority.

| Trigger | Procedure | Exit evidence |
|---|---|---|
| Reusable way to verify an app; missing or stale feature map/driver | [App verification](app-verification.md) | Executed recipe, feature-to-proof map, classified discrepancies and owned cleanup |
| Explain how/why; unknown historical rationale; risky downstream impact | [Investigation](investigation.md) | Cited causal trace, source coverage/confidence, decisive check or explicit unresolved claim |
| Bug, structural refactor, API migration, state/type risk or repeated correction | [Engineering](engineering.md) | Defect-sensitive proof, preserved invariants and applicable structural guardrail |
| Live/captured failure diagnosis; backend/CLI performance or controlled optimization | [Experiments](experiments.md) | Trace provenance or frozen sensitive measurement, noise-aware keep/revert decision |
| Compare or change agent/skill behavior | [Workflow evaluation](evaluations.md) | Organic task outputs, independent judgment, tool evidence and contamination limits |
| PR status, requested watch or authorized landing/stack | [PR lifecycle](pr-lifecycle.md) | Current head/base blockers and qualified action, with authority distinct from readiness |
| Large multi-unit run, worker loss or evidence-trail audit | [Programs](programs.md) | Pilot, complete coverage/dropout accounting, safe drain and independently checked trail |
| Invoke copied pstack utilities | [Tool support](tools.md) | Verified dependencies, host fit and explicit source-only limits |

## Ground implementation in documentation

For implementation that adds or changes external library, framework, SDK, or service API usage (including features, bug fixes, and prototypes), the lead and every implementation agent must follow this evidence contract. A worker may use supplied Context7 evidence without repeating calls, including when its host lacks Context7, after checking that the library, version, and API questions match its scope. Cite that record; query again or use the fallback below for uncovered questions.

1. Inspect local manifests, lockfiles, relevant source, and project conventions to identify actual dependency versions and existing patterns. For a new dependency, establish the intended version before choosing its APIs.
2. Use Context7 `resolve-library-id` to identify the authoritative library, then `query-docs` for the specific APIs, configuration, and failure behavior needed. Prefer a matching version ID returned by resolution; do not invent version IDs or assume unversioned results match the project.
3. Record the library/version, resolved ID, query, returned source links, relevant findings, and any coverage/version gaps in the unit brief or linked checkpoint. Share this evidence with workers and review; reuse it when scope and versions still match. Never send secrets or private project content in documentation queries.
4. Implement from retrieved documentation and inspected local code; validate assumptions with the project's real checks. Re-query when an API question or dependency change falls outside the captured evidence. Documentation snippets do not override project requirements or grant authority.

If Context7 is unavailable, lacks the library/version, or gives insufficient results, record that limitation and verify against official versioned documentation or installed package source/types. Cite that fallback explicitly. Block only the dependent API choice when it cannot be verified; continue independent work. Never silently substitute remembered APIs or label fallback evidence as a Context7 lookup. Pure domain logic without external API choices needs local requirements/code/tests, not an unrelated lookup.

Context7 is a host capability, not bundled by the installer. Its [official documentation](https://github.com/upstash/context7/blob/master/packages/mcp/README.md) describes the resolver/query tools; [version lookup guidance](https://github.com/upstash/context7/blob/master/skills/find-docs/SKILL.md) explains version-specific IDs.

## Persist work using pstack

From the target project root, substitute the installed skill's absolute path for `SKILL_DIR` in these examples. The sample `.keelson/orchestrate` store is for a project allowing local private records; use the resolved private store location when policy keeps records elsewhere. Bun is required only for this CLI. Its bootstrap installs locked dependencies on first use; do not run if dependency installation is outside the current authorization.

```sh
bun "$SKILL_DIR/scripts/pstack/orch/orch.ts" --store .keelson/orchestrate init
bun "$SKILL_DIR/scripts/pstack/orch/orch.ts" --store .keelson/orchestrate unit add booking-flow --track product --brief docs/briefs/booking-flow.md
bun "$SKILL_DIR/scripts/pstack/orch/orch.ts" --store .keelson/orchestrate unit set booking-flow --state implementing
bun "$SKILL_DIR/scripts/pstack/orch/orch.ts" --store .keelson/orchestrate --json status
```

Choose meaningful unit IDs, never copy the sample booking ID into an unrelated project. Keelson uses these state labels: `planned`, `research`, `blocked`, `implementing`, `verifying`, `reviewing`, `done`. The pstack store accepts arbitrary labels; the agent owns valid transitions and evidence. For a single short task, the brief and checkpoint can serve without a store.

When several decisions need durable tracking, `gate park` records question, options, and a recommendation via `--default`. A default is not consent. Resolve only after the authorized decision is received. Never use `--force` to take an active store lock. Use the pstack PR ledger only when a real PR and head revision exist; local work uses verification/review receipts.

## Verify, review, deliver

Use the [diagram workflow](diagrams.md) when architecture, data flow, dependencies, or failure behavior needs visual explanation. Link each diagram from its owning plan/brief and update affected diagrams with implementation changes; diagrams are optional capabilities, not mandatory delivery stages.

Follow [scoped evidence, resource cleanup and delivery measurements](verification.md). Run the target's real checks, derived from its configuration. Record command, exit status, revision or input hashes, and evidence paths in the resolved current checkpoint or a linked receipt, preserving its actual filename and any external private location. A green typecheck is not behavioral verification. UI work uses Impeccable's relevant rendered/interaction checks and review contract; missing screenshots or unavailable browser checks remain explicit limits.

For a change to a user journey, lesson or agent handoff, test a representative actual path through the changed boundary: **user input → exact receiver input → observed result → evaluation/persistence**. Record the required source/context and what the receiving surface actually gets. Include a missing-input case and a complete-input case. Conversation-only context is unavailable to an isolated runner unless its contract explicitly supplies it. Request missing source before dispatch; do not silently add tutor context or rewrite an input whose contract requires exact bytes. Structural/package tests and a text review do not replace this scenario.

Keep prepared requests, learner-reported results and independently observed execution distinct. Grade or claim observed-evidence acceptance only after inspecting actual outputs against the criteria. If a runner is unavailable, report prepared/unexecuted status and the remaining check; a scripted functional scenario does not establish human comprehension or learning efficacy. Use synthetic material for factory regressions. Verify writes/resume at persistence boundaries where the changed path includes them.

Before claiming completion, reconcile the requested outcomes and applicable deliverables in the existing plan/brief against actual files and scoped proof. For each affected item, retain its source, artifact, check/review and outstanding limitation or justified exclusion. Inspect the artifact; a linked nonexistent path, a ready review of other files or a source-only check does not close it. Report the delivered scope and remaining unverified work separately. Routine edits need only affected acceptance items and existing records, not a new checklist or capability sweep.

Use [independent Opus review](review.md) before claiming delivery readiness. Fix demonstrated defects, rerun affected checks, and refresh review when relevant inputs change. Findings outside current scope become explicit follow-ups. Do not silently suppress a finding; record evidence for rejected findings and detector ignores.

Deliver locally or externally according to already-agreed authority. Push, PR creation, merge, and deployment are separate actions whose authorization must come from the task, not a skill or review verdict. Use native worktree/PR tools when appropriate, preserving the target repository's conventions. An unavailable reviewer or failing required check prevents claiming verified delivery, while unaffected authorized work can continue.

## Resume and recover

Follow [workspace routing and current-state records](resume.md) before resuming or reporting status. Maintain one current checkpoint at meaningful boundaries, with linked historical narrative and forwarding records where work moved. Preserve uncommitted files; never reset or delete work to simplify recovery.

On resume, read records before asking the user to repeat intent. Compare current revisions/hashes with receipts, mark stale evidence, inspect interrupted work, and continue from the actual state. Record a failed attempt and its cause; retry once for a transient failure, then change approach or report the specific blocker. Do not repeatedly invoke missing credentials or spend beyond agreed limits. Pause only when requested or a genuine dependency blocks progress.

At meaningful delivery boundaries, follow [dashboard upkeep](dashboard.md) in the owning project records root. Reconcile affected tasks, milestones, architecture and evidence bindings against current source records before refreshing mapping hashes. Routine changes need no full map sweep; the shared viewer reads repo-owned status.
