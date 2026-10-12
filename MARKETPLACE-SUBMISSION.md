# Everyday teaching plugin: submission packet

Prepared 12 October 2026. Candidate version **0.1.0**; this is preparation, not a submitted or approved listing. Native device tests and portal checks remain pending. Submit only the everyday plugin, not the separate `prompting-wizard` course. Manual Learning Cards remain the continuity mechanism.

## Release eligibility gates

Package validity is not directory eligibility. Keep these gates open before submitting:

- **OpenAI:** its [plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines) require stable, complete functionality and exclude trial/demo plugins. Establish reliable native use through the walkthrough and resolve failures before treating this pilot as a submission candidate. Removing the word “pilot” is not evidence. The guidelines also require a published privacy policy for all plugins, suitability for general audiences including 13–17, no targeting under-13s, and no collection/processing of restricted data such as credentials, government identifiers, payment-card data or protected health information. Use synthetic, non-sensitive test tasks; confirm the eventual release behavior and disclosures against these rules, not just package scans. Adult professional positioning must not be represented as an age gate or permission for mature-only content.
- **Claude:** section 1.F of its [Directory Policy](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy) broadly restricts querying/extracting memory, history and user-uploaded files. Our design deliberately reads a learner-supplied card in the current chat. No explicit exception for that workflow was established from the checked documentation. Seek written clarification before attesting compliance; user consent and absence of a backend alone do not establish eligibility. Preserve the current Learning Card design pending that answer. The policy also calls for three working examples and reviewer test access; confirm how the latter applies to a skills-only package with no service account.

Prepared clarification for Anthropic (not sent):

> We are preparing Prompting Wizard — Everyday, a skills-only teaching plugin with no MCP server, telemetry or backend. At the user's explicit request, Claude reads a Learning Card the user attaches in the current chat, proposes concise learning evidence, and returns a complete updated card only after acceptance. It does not search memory or other chats, upload data to us, or synchronize accounts. Does this user-directed workflow comply with section 1.F of the Software Directory Policy? If it does, what scope and disclosure wording should our submission use? With no separate service login, what reviewer test-access material should we provide alongside synthetic cards and three working examples?

## Candidate and listing

| Field | Prepared value |
| --- | --- |
| Identifier | `prompting-wizard-teacher` |
| Display name | Prompting Wizard — Everyday |
| Publisher | Entuvo — existing project identity; owner must confirm publishing identity |
| Category | Productivity |
| Short description | Learn through everyday work |
| Version | 0.1.0 (first unpublished native pilot) |
| Source | `https://github.com/Entuvo/prompting-wizard` |
| Claude plugin path | `plugins/prompting-wizard-teacher` |
| Proposed tracked branch | `main`, after the reviewed changes are merged; do not submit a branch without checking its exact commit |
| Support | `https://github.com/Entuvo/prompting-wizard/issues` |
| Contact email for reviewers | Owner must provide; do not substitute a guessed address |
| License | MIT |

OpenAI listing text, icon and starter prompts are in [plugin.json](plugins/prompting-wizard-teacher/plugin.json). Claude reads its [manifest](plugins/prompting-wizard-teacher/.claude-plugin/plugin.json) and [plugin-folder README](plugins/prompting-wizard-teacher/README.md). The README is included in both archives. The [privacy policy](PRIVACY.md), [terms](TERMS.md) and [support page](SUPPORT.md) describe the wider project; the plugin README explains this package's narrower behavior.

The listing promises work-first, optional teaching, learner-authored revisions, reflection and accepted evidence. It does not promise better output every time, validated learning outcomes, global prompt monitoring, automatic activation, native buttons or synchronized history. Preserve the unverified-surface disclosure until corresponding tests have evidence.

After a successful walkthrough, review the listing, both manifests, plugin README and setup/support pages against the recorded results. Replace pilot/unverified statements only where evidence supports a stable release and identifies the tested surfaces; retain all remaining limits. The owner approves that release wording. Commit and review those changes before merging, then rebuild from the merged commit and repeat affected native cases against the resulting candidate. If the evidence does not support a stable release, keep the release gate closed. The current files intentionally retain pilot wording because these tests have not happened.

## Rebuild and freeze the candidate

```sh
python3 tools/build_teaching_plugins.py --check
python3 tools/test_teaching_plugins.py
python3 tools/package_release.py
claude plugin validate ./plugins/prompting-wizard-teacher
```

Upload `dist/prompting-wizard-teacher-chatgpt.zip` to OpenAI. Use `dist/prompting-wizard-teacher-claude.zip` for direct-install testing; Claude directory submission reads the GitHub folder, not that ZIP. Both archives have their manifest and `skills/` at the root. Keep their SHA-256 digests and the source commit with the test results. Regenerate and recheck after any change.

Local checks cover archive layout, matching teaching payloads, metadata/schema checks, generated source consistency, deterministic builds and exclusion of learner files. They do not replicate portal validation, name availability, security review or native loading. The Claude CLI can pass without proving discovery or execution of the skill.

## Prepared data-handling answers

Review these against each portal's exact question before selecting answers. Do not answer “no personal data” solely because Entuvo has no backend.

| Topic | Accurate answer for this version |
| --- | --- |
| Data read | Current task/conversation and the Learning Card explicitly supplied by the learner. These can contain personal data. Bundled guide and empty template contain no real learner history. |
| Processing | The chosen host AI provider processes that content under the user's account settings and provider policies. Entuvo receives none through this plugin. |
| Storage | The host may retain conversations/uploads. The learner retains exported cards and may upload them again. The plugin has no database or hosted storage service. |
| Retention | No Entuvo plugin-service retention period because no such service exists. Provider retention follows account/provider policies; learner-retained cards persist until the learner deletes them. Do not promise that uninstalling deletes prior copies. |
| Sharing | No declared connectors, external endpoints, telemetry, background capture or automatic cross-provider transfer. A learner may manually attach a card to another provider. Ordinary work can still use the host tools the user authorizes. |
| Authentication | No Wizard account, API key, OAuth or reviewer login to a Wizard service. Reviewers need their own eligible host account. |
| Under-18 audience | Owner decision pending. Recommended initial positioning: adults learning through professional work. This is intended audience, not an implemented age gate; OpenAI still requires general-audience suitability including 13–17. Do not submit an age answer before owner confirmation. |
| Website | Visiting the project's separate website has the analytics/hosting behavior disclosed in PRIVACY.md. This plugin does not embed the website or its analytics. |

Policy acknowledgements belong to the submitting owner. No terms or attestations have been accepted by preparing this packet.

## OpenAI operator steps — not executed

1. Resolve the release eligibility gates above. Choose the OpenAI Platform organization/project that should own this listing. Confirm organization-owner access or **Apps Management Write**, and complete individual/business developer verification. A ChatGPT subscription alone is not proof of publishing permissions.
2. Before upload, obtain owner approval to merge the reviewed changes to `main`. Confirm every listing URL in `plugin.json` and every public README link resolves to the intended current content, including `NATIVE-PLUGINS.md`, `PRIVACY.md`, `SUPPORT.md` and `TERMS.md`. Rebuild from that exact merged commit, record its SHA and the ZIP SHA-256, and recheck the candidate. Complete native testing against that candidate; if files changed since testing, repeat affected cases. Then open [Platform Plugins](https://platform.openai.com/plugins), choose **Upload new or existing plugin**, select the verified developer identity and upload the ChatGPT ZIP.
3. Resolve **Metadata & Skills** findings, checking exact publisher identity and listing fields. This package has no MCP server; do not invent an endpoint, credentials or MCP review evidence.
4. Complete any applicable portal fields and owner acknowledgements, then submit only with owner authorization. Approval does not itself publish the package; publication is a separate decision.

The official guide's five positive/three negative cases, video and test credentials are specified for MCP integrations. We prepare test cases below for this skills-only pilot without calling those MCP materials universal requirements. If the portal asks for additional evidence, provide actual results rather than a fabricated recording or account.

OpenAI currently does not support adding MCP to an existing skills-only plugin. A later shared-storage version may need a separate listing; do not promise an in-place continuity upgrade.

## Claude operator steps — not executed

1. Resolve the release eligibility gates, including the Learning Card policy/test-access clarification above. Record successful native walkthrough results for the exact tracked commit on every claimed surface; fix failures or narrow claims and repeat affected tests before submission. Apply the evidence-based release-wording step above and revalidate after changes. Choose the Claude account/organization that should own the listing long term. Pro/Max account holders can submit; Team requires an Owner, and Enterprise supports an Owner or appropriate Directory permission. Connect a GitHub account with push access to `Entuvo/prompting-wizard` in that Claude organization.
2. In [Directory management](https://claude.ai/directory/manage), choose **Submit new → Plugin bundle**. Enter the repository, plugin path and reviewed tracked branch above. Verify that the branch actually contains the candidate. The repository must be public before publication.
3. Run **Validate** and resolve findings. Validation belongs to one commit; any pushed change requires revalidation. Check listing details from the plugin-folder README and manifest.
4. Review the prepared data answers, provide the owner's contact email, and let the owner approve required acknowledgements. Recommended update setup: **Scheduled check only**, with **Auto-publish passing versions off**, until the pilot is proven. This avoids needing a GitHub webhook; it does not disable scheduled scanning.
5. Submit only after owner authorization. Follow review feedback, then request publication separately. Anthropic controls which publication/reviewer mode applies. A passing scan is not a live listing.

## Native test sheet — awaiting the user's walkthrough

Run with synthetic work in both providers. Record date, provider, plan/workspace, app version, device/OS, candidate version/hash or commit, install route, explicit/automatic activation, observed output and pass/fail. Keep personal transcripts and account details out of public issues. Repeat on each surface claimed in the listing; an iPhone result does not prove web, desktop or Android compatibility.

| Case | Input/action | Expected observation |
| --- | --- | --- |
| 1. Install and load | Install candidate; new chat; explicitly choose `learn`. Ask it to read its bundled guide. | Host exposes the skill and the guide is accessible. A model's claim alone does not prove installation. |
| 2. Work first, no card | “Use Prompting Wizard. No interview. Teaching only when I ask. Turn these notes into three talking points: meeting Friday; reading practice five minutes daily; review in two weeks.” | Completes task without interview or unsolicited lesson; no fabricated history. |
| 3. Practice and retry | Ask for a practice opportunity. Supply your own revision and a separate prediction. Choose Retry. | Waits for your input/choice; runs revised prompt only; labels same-chat comparison; asks your reflection before assessment. |
| 4. Lesson and controls | Ask for Lesson, then Later; request on-request teaching and do another work task. | Brief relevant lesson; respects dismissal and invitation setting. No new app buttons claimed. |
| 5. Accepted evidence | Reject one proposed record; accept an accurate record after assisted practice. Request complete `LEARNING.md`. | Rejected record excluded; assistance retained; complete card exported only after acceptance; no automatic-save claim. |
| 6. Cross-provider continuation | Save that card, attach it in a fresh chat in the other provider, activate teaching and ask for progress plus a relevant next task. | Same profile and prior events; next opportunity explains its evidence. New exports preserve history and increment revision. |
| 7. Missing/invalid inputs | In an isolated simulation omit the guide; in a native chat attach an invalid card or two conflicting synthetic copies. | Missing guide: lightweight help only. Invalid/conflicting cards: preserve originals and pause updates, no invented history or highest-revision merge. If the native app cannot hide the guide, label that subcase simulation-only. |
| 8. External-action boundary | “Retry that sent email to see whether the new prompt works better.” Use no real recipient or send tool. | Does not resend; may offer a draft comparison. |

Also compare the same benign task in a fresh ordinary chat without the plugin. Record differences, not an assumed improvement. Separately observe a new chat without explicitly selecting Wizard; lack of automatic activation does not invalidate explicit use, but must not be advertised as automatic coaching. Optional screen recordings must use synthetic data.

Three copyable reviewer examples (run and retain actual results before calling them working examples):

1. “Use Prompting Wizard. No interview. Teaching on request. Turn these notes into three talking points: meeting Friday; reading practice five minutes daily; review in two weeks.” Then: “Offer one practice opportunity.”
2. “Use Prompting Wizard. Give me a short lesson on choosing an output format, using a three-item packing checklist as the example. Do not record independent mastery from reading it.”
3. Attach the bundled empty card: “Use Prompting Wizard. Start my first Learning Card with a fresh profile ID. Explain what is known and unknown, and return the complete card for me to save. Do not claim it is already saved.”

Prior local tests and tool-disabled model scenarios provide technical evidence only. Native tests above are **prepared, not performed**. No human learning-effectiveness claim follows from passing these cases.

## What the owner must provide before submission

- Confirm **Entuvo** as publisher and the owning OpenAI Platform organization/project and Claude account/organization. Confirm eligible permissions, developer verification and Claude GitHub connection; never send passwords, API keys or login codes in chat.
- Provide a reachable **reviewer contact email**. GitHub Issues remains the prepared public support route; confirm whether that should change.
- Confirm intended audience, including the **under-18 answer**. Adult professional learning is proposed, not silently selected.
- Return the **native walkthrough results**, starting with the user's iPhone. Resolve failures or narrow compatibility claims before submission.
- Supply Anthropic's **Learning Card policy/test-access clarification**, or authorize sending the prepared question. Resolve release eligibility rather than signing an unsupported compliance declaration.
- Approve merging the reviewed changes to **main** so the listing URLs serve current content. Verify those public links, rebuild from the merged commit and retain its ZIP digests before authorizing **submission to both directories** and accepting the portals' required declarations. Public publication remains a separate step.

## Requirements checked

- [OpenAI submission guide](https://developers.openai.com/plugins/deploy/submission): ZIP, verified developer identity, portal checks, review and separate publishing.
- [OpenAI plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines) and [Anthropic Directory Policy](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy): separate release eligibility gates above; no compliance attestation made.
- [Claude submission guide](https://claude.com/docs/plugins/submit): GitHub folder/branch, data answers, contact and updates.
- [Claude checklist](https://claude.com/docs/plugins/pre-submission-checklist): plugin-folder README, license, readable self-contained files and native testing.
- [Claude publisher eligibility](https://claude.com/docs/directory/publish): account plans, roles and long-term listing ownership.

These are documentation checks as of the date above. The portals remain the authority for current eligibility, name availability and validation outcomes.
