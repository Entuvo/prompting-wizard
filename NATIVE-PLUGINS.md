# Prompting Wizard plugin setup

Prompting Wizard ships as **one plugin**, `prompting-wizard` (version 1.5.3), for Claude (app, Cowork, Claude Code) and for ChatGPT and Codex. It carries three skills: **learn** (everyday learning and the in-app export review), **prompting-wizard** (the optional 30-lesson course and `pw history`) and **pw** (commands). It also bundles the teaching guide, rubrics and an empty Learning Card.

Everyday coaching has passed the walkthrough below in Claude on the web ([record](#walkthrough-record)). ChatGPT and the Claude desktop and phone apps have not been through it yet. It is not listed in any public directory. OpenAI's plugin directory rejected the 1.5.1 submission on 16 October 2026 (see [OpenAI directory review](#openai-directory-review)).

## Downloads

Each [GitHub Release](https://github.com/Entuvo/prompting-wizard/releases/latest) attaches two plugin files, built from that release's tag:

| File | For | Manifest |
| --- | --- | --- |
| `prompting-wizard-claude.zip` | Claude app, Cowork, Claude Code | `.claude-plugin/plugin.json` |
| `prompting-wizard-openai.zip` | ChatGPT and Codex | root `plugin.json` (Agent Plugins), plus the legacy `.codex-plugin/plugin.json` for the Codex CLI. It leaves out the update check and the local session-history readers. |

Both have their manifest and `skills/` at the archive root and contain no learner history, hooks, MCP servers or credentials. Two manual-setup files are attached too: `prompting-wizard-native-guide.md` and `prompting-wizard-learning-card.md` (see [manual setup](NATIVE-APPS.md)). A release download is not a directory listing. Build them yourself with `python3 tools/package_release.py`.

What runs where: the course's Python scripts (local progress storage and `pw history`) run only in Claude Code or Codex. `pw history` on Claude Code or Codex sessions needs the marketplace install or the Claude download; the OpenAI download reads app data exports only. In the ChatGPT and Claude apps, everyday learning, the in-app export review and the course with an attached `PROGRESS.md` work without them.

## Claude installation

On a paid plan, open **Customize → Plugins** on the web or desktop and upload `prompting-wizard-claude.zip`. Plugins added there are saved to your account and sync to Cowork and to Claude Code when you sign in with the same account. In Claude Code you can instead run `/plugin marketplace add Entuvo/prompting-wizard` and install **prompting-wizard**. Use an approved marketplace or administrator-provided plugin when workspace policy requires it.

Start a new conversation and say:

> Use Prompting Wizard to teach me through my work; no interview. Keep tips occasional. My task is: [your task].

Confirm that the coach can read the bundled guide. If it cannot, use the [manual setup](NATIVE-APPS.md). Account installation does not prove the skill activates in every new chat. Skills and commands work in Claude chat; hooks and local MCP servers run only in Cowork and Claude Code (this plugin ships neither). See [Claude plugins](https://support.claude.com/en/articles/13837440-use-plugins-in-claude).

## ChatGPT and Codex installation

**Personal (ChatGPT desktop), macOS or Linux:** run this in Terminal.

```sh
curl -fsSL https://raw.githubusercontent.com/Entuvo/prompting-wizard/v1.5.3/install-chatgpt.sh | sh
```

The script is pinned to one release. It uses `~/Downloads/prompting-wizard-openai.zip` if that file matches the release checksum, and otherwise downloads the zip from that release. It stops if the checksum does not match. It then copies the plugin to `~/.codex/plugins/prompting-wizard/` and adds one entry to `~/.agents/plugins/marketplace.json`. Other entries in that file stay as they are, and the old file is backed up first. To install a zip you already have, run `sh install-chatgpt.sh --zip PATH`. To remove the plugin, run `sh install-chatgpt.sh --uninstall`. Then quit and reopen the ChatGPT desktop app, open **Plugins → Personal** and install **Prompting Wizard**.

**Manual steps (and Windows):** a downloaded zip does not appear in ChatGPT by itself. ChatGPT has no zip upload for personal plugins. Register the zip as a local plugin, following [OpenAI's manual install](https://developers.openai.com/plugins/build/plugins#install-a-local-plugin-manually):

1. Unzip `prompting-wizard-openai.zip` to `~/.codex/plugins/prompting-wizard/` (on Windows, `%USERPROFILE%\.codex\plugins\prompting-wizard\`).
2. Add this entry to the `plugins` list in `~/.agents/plugins/marketplace.json`. The path is relative to your home folder and must start with `./`. If the file does not exist, create it with a top-level `"name"` (for example `"personal"`) and a `"plugins"` list.

   ```json
   {
     "name": "prompting-wizard",
     "source": { "source": "local", "path": "./.codex/plugins/prompting-wizard" },
     "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
     "category": "Productivity"
   }
   ```

3. Quit and reopen the ChatGPT desktop app and install **Prompting Wizard** under **Plugins → Personal**.

The app installs a copy into its own cache. After you install a newer zip, install the plugin again in the app.

**Workspace:** to share it, a workspace admin opens the plugin's menu under **Personal**, chooses **Publish**, and grants the intended roles access. Members then get it on web, desktop and mobile. This is workspace distribution, not public publication. See [workspace publishing](https://developers.openai.com/plugins/build/plugins#publish-a-local-plugin-to-your-workspace). An admin can instead import this repository's marketplace from GitHub under **Admin → Plugins → Add → Import marketplace**, pinned to a release tag. See [plugin management](https://learn.chatgpt.com/docs/enterprise/plugin-management).

**Codex:** run `codex plugin marketplace add Entuvo/prompting-wizard` and install **prompting-wizard**.

**Public:** the publisher uploads `prompting-wizard-openai.zip` through the [OpenAI plugin submission portal](https://developers.openai.com/plugins/deploy/submission); one listing covers ChatGPT and Codex. It is not listed: see [OpenAI directory review](#openai-directory-review). OpenAI's guidelines also exclude trial plugins, so the ChatGPT walkthrough is still to be done before resubmission.

Once installed, start a new chat, select the plugin with `@` if necessary, and use the start request above.

## OpenAI directory review

Entuvo submitted `prompting-wizard-openai.zip` (1.5.1) to OpenAI's plugin directory. It was rejected on 16 October 2026 with five findings:

1. Skills-only plugins are not currently accepted. Unresolved: the plugin has no app or MCP server.
2. The name or description referred to another assistant, model or platform. Fixed in 1.5.2: the OpenAI listing fields name none, and `tools/sync_codex_plugin.py` fails if one does.
3. The category was not confirmed. Fixed in 1.5.2: `Education & Research`, from OpenAI's accepted list in its [submission errors reference](https://developers.openai.com/plugins/deploy/submission-errors).
4. The privacy policy failed the automated assessment. Fixed in 1.5.2: privacy, terms and support are static pages at https://entuvo.github.io/prompting-wizard/privacy/, `/terms/` and `/support/`, built from the Markdown files by `tools/build_policy_pages.py`.
5. A skill could install or load code from an untrusted or mutable source. Fixed in 1.5.2: the OpenAI download leaves out the update check (which fetched `VERSION.md` from GitHub and could replace skill files) and `history_hosts.py` (which needed SDKs installed with pip). Its history guide, command table, `learn` skill and README describe only the export route. `tools/package_release.py` fails if the download contains `raw.githubusercontent`, `pip install`, `curl`, `git clone`, `npx`, `Update check`, `--host claude-code` or `--host codex`.

Resubmit only once OpenAI accepts skills-only plugins.

## Keep teaching and continuity separate

The plugin supplies the guide, so successful loading removes the need to attach that guide each time. It does **not** supply your learning history. Attach the current `LEARNING.md` in each new chat that needs it. Without a card, learning can begin from the current task without claiming past progress.

After meaningful practice, the coach proposes a learning record. Accept only an accurate description. Ask for the complete updated card, save it yourself and carry it to the next chat or provider. Replace an old project upload deliberately. An exported artifact is not proof of a durable save or account sync. Keep the previous file if validation or preservation is uncertain. Reading an example or following a hint does not establish independent skill.

To learn from past chats, export your data from the same app's settings (ChatGPT: Data controls → Export data; Claude: Settings → Privacy → Export data) and upload `conversations.json` or a few conversations to that app. Each app reviews only its own provider's history and declines the other provider's export without reviewing it. The upload itself still reaches that app's provider, so upload only that app's own export. Then ask the coach to review them. It reads up to 30 recent conversations and says how much it covered. It reports your most common gaps, with up to three of your own cases, and proposes card records that you accept or reject. Nothing is stored beyond that chat.

Occasional is the default; frequent or on-request can be chosen. More/less/pause affects this chat. Accepted card preferences travel only when the card is supplied. Installation cannot promise automatic coaching in every ordinary chat. Existing account instructions and the plugin should yield one invitation, not two; coding-host local feedback retains its ownership and opt-in rules.

The package contains no background observer, hosted storage or automatic cross-provider synchronization. See [privacy](PRIVACY.md).

## Walkthrough before claiming device compatibility

Use disposable chats and synthetic material. Record provider, account plan, app version, surface and date. Run these checks separately on web, desktop, iOS and Android:

1. Install through the chosen supported route; start a fresh chat and verify the skill and bundled guide are available. Record whether explicit selection is needed.
2. With no card, request normal work and teaching. Check work comes first, no interview occurs and no past history is claimed. Try Later and on-request.
3. Choose Practice, provide your own edit and a separate prediction, and choose whether to retry. Check the prediction is excluded, same-chat comparison is labeled exploratory, and no external action is repeated.
4. Accept an accurate record. Inspect the complete returned card, retain it, and attach it to a fresh chat in the other provider. Check profile ID and prior events are preserved and the next opportunity uses that evidence.
5. Try a missing guide, malformed card and conflicting card copies. Expect an honest limitation with originals preserved, not a fabricated save or merge.
6. Start an ordinary new chat without mentioning Wizard. Record whether it activates. A pass after explicit selection does not establish automatic activation.

Local package tests and model simulations do not establish these native results or human learning effectiveness.

### Walkthrough record

| Provider and surface | Plan | App version | Date | 1 Install | 2 Work first | 3 Practice | 4 Card to other app | 5 Bad card | 6 Ordinary new chat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Claude, web | Max | web | 2026-10-16 | pass | pass | pass | pass | pass | started on its own |
| ChatGPT, macOS desktop | — | desktop | 2026-10-17 | pass (`install-chatgpt.sh`, then Plugins → Personal) | not run | not run | not run | not run | not run |

Surfaces not listed have not been through the walkthrough.

## Maintainers

The plugin tree `plugins/prompting-wizard/` is generated; never hand-edit it. Its canonical sources are:

- `prompting-wizard/` (course skill), `pw/SKILL.md` and `learn/SKILL.md`;
- `prompting-wizard/.claude-plugin/plugin.json`, `packaging/plugin.json` (Agent Plugins) and `packaging/openai-plugin.json` (legacy Codex);
- `packaging/README.md` (the plugin's README); the guide and empty card are generated from `prompting-wizard/references/`.

```sh
python3 tools/sync_codex_plugin.py          # regenerate the tree
python3 tools/sync_codex_plugin.py --check  # CI: stale, missing or unexpected files
python3 tools/package_release.py            # build the two downloads
python3 tools/build_policy_pages.py         # rebuild docs/privacy, docs/terms, docs/support after editing the Markdown
```

The OpenAI download differs from the tree in exact edits listed in `OPENAI_EDITS` and `OPENAI_OMIT` in `tools/package_release.py`. When you change the Update check section of `prompting-wizard/SKILL.md`, the local-session lines of `references/history.md`, the `history` row of `references/commands.md`, the closing line of `learn/SKILL.md`'s export section, or the past-work lines of `packaging/README.md`, the build fails until those edits match again. OpenAI listing text must not name another assistant, model or platform.

All three manifests share the course version in `prompting-wizard/VERSION.md`. Skill descriptions must stay within claude.ai's 200-character limit, and frontmatter within the Agent Skills fields. Never place learner cards or progress in the plugin tree. Current OpenAI submission rules do not accept plugins with lifecycle hooks or app references; keep the optional coaching hooks a separate install.

`install-chatgpt.sh` sits at the repository root and is not part of either download. Its `version=` line and the one-liners in `README.md` and this file must match `prompting-wizard/VERSION.md`; `tools/validate.py` fails otherwise. The script downloads `prompting-wizard-openai.zip` and `SHA256SUMS` from the release with that tag, so every release must attach both. `tools/test_install_chatgpt.py` covers it.

Documentation checked 17 October 2026 (Claude plugins and Claude Code plugin reference; OpenAI Plugins build, submission and plugin management guides).
