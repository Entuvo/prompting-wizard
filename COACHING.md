# Optional local coaching

Prompting Wizard keeps the portable 30-day course and an optional local integration. The integration uses your host model to explain one useful prompting lesson after a result. Both hosts can use the same local learner profile. There is no account service or cross-device sync.

Choose **after-result** for a short coaching note, or **lesson-only** to collect examples for guided lessons without extra inference after each task. **Pause** stops collection. Only workspaces you explicitly enable are collected.

Compatibility evidence comes from the synthetic checks below. It does not establish support across host versions or demonstrate human learning outcomes.

## Compatibility checked on 8 October 2026

| Surface | Observed behavior | Limits |
| --- | --- | --- |
| Claude Code 2.1.293–2.1.294, isolated print sessions | Main-session capture, result then one continuation, evidence read and temporary finding saved | Needs scoped command permissions. Default print permissions denied access. Heredoc saving was rejected; direct `record --json` succeeded. Hook payloads omitted model ID, so use general guidance. |
| Codex CLI 0.159.3, interactive local session | Normal hook trust, capture, result then continuation, evidence read and finding saved | Tested in a synthetic workspace under workspace-write; shared home profile needs a narrow `--add-dir` grant. Completion events supplied `gpt-6-astra`. |
| Codex CLI 0.159.3, `exec` | Task ran, but tested invocations emitted no hook callbacks | Automatic capture is not supported by this evidence. Do not infer interactive compatibility applies here. |
| Codex desktop, browser Claude/ChatGPT, remote/cloud sessions, Windows | Not verified | No automatic-capture support claim. Portable lessons remain separate. |

Both observed hosts can emit a genuine new user submission while `stop_hook_active` remains true. Those results are retained for a later lesson without starting another feedback loop. Parent main-session callbacks did not contain separate child submissions in the tested child runs. That does not establish clean-context execution for every subagent surface.

Python storage, CLI, installer and packaging tests use disposable files. Guidance tests check source selection and validation; they do not establish educational efficacy. Model self-report does not establish clean-context isolation. Do not run controlled lesson comparisons on an unverified surface.

## Setup

Use a checked-out source repository and Python 3.9 or newer. Local checks ran on macOS with Python 3.9.6 and 3.14.6; CI targets Python 3.12. Windows installation is not implemented.

First review the proposed installation. The data root must be outside enabled workspaces and outside skill/plugin caches.

```sh
PW_DATA_ROOT="$HOME/.prompting-wizard"
python3 tools/install_coaching.py --host claude --root "$PW_DATA_ROOT" --config "$HOME/.claude/settings.json" --dry-run
python3 tools/install_coaching.py --host codex --root "$PW_DATA_ROOT" --config "$HOME/.codex/hooks.json" --dry-run
```

Use `--install` in place of `--dry-run` for each host you choose. This adds only owned handlers, copies a versioned runtime, and leaves unrelated settings intact. Use normal host controls to review and trust the exact hooks. Refused or absent trust means inactive collection; copying files does not prove activation. One registration per host/profile avoids duplicate hooks.

The review output identifies the installed runtime. Invoke its `scripts/wizard.py` with Python. Configure a default, then explicitly include a workspace, or assign a workspace override:

```text
wizard.py configure --root ROOT --mode after-result
wizard.py include --root ROOT --workspace ABSOLUTE_WORKSPACE
wizard.py configure --root ROOT --workspace ABSOLUTE_WORKSPACE --mode lesson-only
wizard.py status --root ROOT
```

The installer does not enable workspaces or grant tool permissions. For after-result mode, use normal narrowly scoped host grants for the installed runtime's `evidence` and `record` commands against this data root. Review those commands; do not grant general shell access to make coaching work. Claude print mode can require explicit grants even when hooks themselves run. If ongoing prompts interrupt feedback, select lesson-only explicitly or keep capture paused while resolving access.

Verify activation with a synthetic prompt and `list --kind pending`. Check that result precedes feedback, one finding is saved, and no loop occurs. Avoid using private work as a setup test. An empty queue is not proof of failure or success: exclusions, pause, suppressed lessons, expiry and unsupported host surfaces also produce no records.

## Controls

Use the `pw` skill for conversational controls: `/prompting-wizard:pw` in the Claude plugin, `$prompting-wizard:pw` in the Codex plugin, or `/pw` (Claude) / `$pw` (Codex) with both standalone skills installed. `help` lists actions. The table below is the underlying runtime interface.

Explicit leading pw invocations are excluded from work capture. A command interrupting unfinished work discards that unfinished capture pair. Tutor mode suppresses follow-up command and lesson conversations. Pausing stops work evidence collection; installed hooks still supply a session token so `resume` works in a new chat.


Every command requires `--root ROOT`. `ROOT` denotes the shared data directory, not the installed skill directory.

| Command | Effect |
| --- | --- |
| `status [--workspace PATH]` | Report pause/default mode, shared-progress presence, and optional workspace override, exclusion and effective mode. |
| `configure --mode after-result` or `--mode lesson-only` | Set learner default; add `--workspace PATH` for an override. |
| `pause` / `resume` | Stop/resume collection, preserving modes. |
| `exclude --workspace PATH` | Stop collection in that workspace and descendants. |
| `include --workspace PATH` | Enable that workspace with its previous override or the learner default. |
| `list --kind all\|pending\|reviewed [--cursor N]` | Inspect records in bounded pages. |
| `delete --id UUID [--kind observation\|finding\|lesson]` / `--workspace PATH` / `--all` | Delete selected managed learning data. |
| `progress-read` | Read shared course state without creating an export. |
| `guidance --token TOKEN [--task-tag TAG]` | Read scoped guidance for the last host-reported session model; not a completed-result identity. |
| `progress-import --file PROGRESS.md` | Validate and preserve course state; reject conflicting history. After learner confirmation, add `--confirm-reconcile --expected-revision N` to accept forward state that retains the baseline and prior log. |
| `progress-export --file DESTINATION` | Export current shared course state atomically. |

Read [privacy](PRIVACY.md) before enabling capture. Reading Claude examples in a Codex lesson, or the reverse, sends those selected excerpts to the current host/provider. After-result feedback uses additional model quota. Lesson-only capture performs no additional inference.

Remove integration with `tools/install_coaching.py --host HOST --root ROOT --config CONFIG --remove`. Edited owned handlers cause a conflict; resolve deliberately instead of forcing an overwrite. Removing hooks preserves learner data. Delete learning data separately when wanted. Configuration backups are removed after success or successful rollback; failed recovery preserves them. They contain no learner database copies. Writes detect changed preimages; arbitrary editors that ignore file locks cannot be given a universal atomic compare-and-swap guarantee.

## Runtime and contributor contracts

`store.py` owns SQLite transactions, retention and learner records. `wizard.py` validates host events, provides learner controls, selects reviewed guidance and requests one continuation. The host model produces the feedback; there is no background model service. `install_coaching.py` owns registration receipts and code installation. One explicit course-file allowlist drives archives, generated copies and validation. Public course archives contain neither lifecycle hooks nor learner data.

An observation is bounded raw evidence. A coaching finding is a temporary hypothesis, never a score. A reviewed lesson requires learner reflection and confirmation; committing it removes its source observations and findings in the same transaction. Shared course updates use a revision check and preserve the original Day 0 baseline. Conflicts do not merge by selecting the higher day.

Add a host only with official event documentation, sanitized live callbacks, pairing/steering/loop tests and ordinary permission/trust probes. Never parse undocumented private transcripts. Add model guidance only with exact documented model identifiers, task scope, official source URL, checked date and revision. Unknown identities fall back to core principles; a source refresh never rewrites past scores silently.

`record` accepts bounded JSON on stdin. For short paraphrased findings, `record --json JSON` accepts one quoted argument with identical validation. Arguments can appear in process listings and host tool logs; use stdin for sensitive text. Hooks never put captured prompt/result text into shell commands. See the tutor procedure in [coaching.md](prompting-wizard/references/coaching.md).
