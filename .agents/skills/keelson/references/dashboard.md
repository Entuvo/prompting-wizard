# Project-owned dashboard

The owning project records root owns `.keelson/dashboard/map.json`, architecture, milestones, tasks and evidence. Never save another project's alignment or mapping in the Keelson factory. Preserve established private/public boundaries: a shared viewer may read a separate engineering root, but private records stay in their owning workspace.

Installation creates an explicitly unverified map only when absent and registers it in the machine-local `~/.local/share/keelson/dashboard/registry.json`. Existing maps and registration metadata are preserved. A legacy registered map is copied into its owning repo only if no conflicting map exists; conflicts stop setup without overwriting either map. Registry absolute paths and server tokens must not be committed. `--registry PATH` selects a separate registry; its viewer must use that same path.

## Onboarding

Read current project instructions, routing, confirmed intent, architecture/ADRs, plans and evidence. Populate the repo map from those records as part of onboarding; a scaffold alone is incomplete onboarding. Reuse existing maps. Do not invent a stack, solution, milestone acceptance or working behavior to fill the canvas. For discovery-only projects map established intent and explicit unknowns; for design-only projects label proposed architecture and planned implementation. Onboarding grants no product implementation authority and requires no new questionnaire or approval stage.

Map actual components and connections, capability/journey overlays, milestones and tasks to existing source records. Bind checks/reviews only to their tested scope. Keep unknowns unverified, explicit dependencies blocked with an owner/action, and merely future work planned. Source presence, a completed task and Opus's source review do not prove runtime behavior. Keep human acceptance separate from evidence. Use `scopeNote` to explain coverage and omissions.

The schema is implemented by `scripts/dashboard/model.py:validate_map`; the factory's `docs/operator-dashboard.md` describes all fields. Component `sources` are engineering-relative; task `source` uses the owning records root when present, otherwise the engineering root. Evidence receipts are records-relative. Preserve existing registration roots and receipt directories.

After inspecting and reconciling the map, from the owning records root run:

```sh
python3 .agents/skills/keelson/scripts/dashboard_setup.py . --reconcile --source .keelson/checkpoint.md
```

Replace the example `--source` with actual authoritative files; repeat it for additional product/plan/routing sources. Component/task source files are included automatically. Do not create a checkpoint merely for this command. It records SHA-256 dependencies in `mappingInputs.engineering` and `mappingInputs.records`; it cannot establish that map content is accurate. Never run `--reconcile` simply to clear a warning. Reconciliation retains prior explicit dependencies; remove a retired dependency from the map only after reconciling why it no longer applies.

## Delivery and resume

At meaningful delivery boundaries, update affected map tasks, milestones, evidence bindings and architecture when their source records change. On resume inspect the map alongside current routing and evidence; reconcile stale claims before reporting status. Routine edits need only affected rows and proportionate checks, not a full inventory, new panel or rediscovery. Preserve unrelated current work and decisions.

The viewer polls records every two seconds. Changed declared source files make `mappingStatus` stale, display a warning and prevent project release readiness. Missing source hashes mean mapping unverified and also prevent release readiness. These checks detect declared dependency changes, not uncited new scope or semantic errors; the agent must still reconcile coverage. Evidence freshness is evaluated independently. A source-current map is not a runtime pass.

For an existing installation, `dashboard_setup.py .` registers/migrates without refreshing hashes or overwriting map content. For a separate private records root, invoke the installed/factory helper with that owning root; retain the existing engineering-root pointer. Start the shared viewer with `python3 .agents/skills/keelson/scripts/dashboard.py` and open its authenticated localhost URL. A registry change appears without restart; code updates require restarting the viewer. The viewer observes files; it does not edit maps, run agents, schedule work or install a startup service.

## Interrupted setup

A busy registry reports its `registry.json.lock/owner.json`. It records PID, hostname and acquisition time. On the recorded host inspect that PID with the system process viewer (on macOS/Linux: `ps -p <pid> -o lstart=,command=`). Do not remove a lock while that setup process is alive. If the process is absent, or the PID has demonstrably been reused after the recorded time, remove only `owner.json` and the empty lock directory, then inspect records and retry. Missing/invalid owner metadata requires establishing that no setup process is running first. No automatic stale-lock deletion occurs; concurrent project work must remain protected. Existing parent aliases such as macOS `/tmp` resolve to their physical directory; the registry file itself and project destinations must not be symlinks.
