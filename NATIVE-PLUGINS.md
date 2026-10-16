# Prompting Wizard plugin setup

Prompting Wizard ships as **one plugin**, `prompting-wizard` (version 1.5.0), for Claude (app, Cowork, Claude Code) and for ChatGPT and Codex. It carries three skills: **learn** (everyday learning and the in-app export review), **prompting-wizard** (the optional 30-lesson course and `pw history`) and **pw** (commands). It also bundles the teaching guide, rubrics and an empty Learning Card.

Everyday coaching in the ChatGPT and Claude apps is a pilot. The walkthrough below still needs to establish installation, activation and manual card transfer on each surface. Neither directory submission nor publication has occurred.

## Downloads

Each [GitHub Release](https://github.com/Entuvo/prompting-wizard/releases/latest) attaches two plugin files, built from that release's tag:

| File | For | Manifest |
| --- | --- | --- |
| `prompting-wizard-claude.zip` | Claude app, Cowork, Claude Code | `.claude-plugin/plugin.json` |
| `prompting-wizard-openai.zip` | ChatGPT and Codex | root `plugin.json` (Agent Plugins), plus the legacy `.codex-plugin/plugin.json` for the Codex CLI |

Both have their manifest and `skills/` at the archive root and contain no learner history, hooks, MCP servers or credentials. Two manual-setup files are attached too: `prompting-wizard-native-guide.md` and `prompting-wizard-learning-card.md` (see [manual setup](NATIVE-APPS.md)). A release download is not a directory listing. Build them yourself with `python3 tools/package_release.py`.

What runs where: the course's Python scripts (local progress storage and `pw history`) run only in Claude Code or Codex. In the ChatGPT and Claude apps, everyday learning, the in-app export review and the course with an attached `PROGRESS.md` work without them.

## Claude installation

On a paid plan, open **Customize → Plugins** on the web or desktop and upload `prompting-wizard-claude.zip`. Plugins added there are saved to your account and sync to Cowork and to Claude Code when you sign in with the same account. In Claude Code you can instead run `/plugin marketplace add Entuvo/prompting-wizard` and install **prompting-wizard**. Use an approved marketplace or administrator-provided plugin when workspace policy requires it.

Start a new conversation and say:

> Use Prompting Wizard to teach me through my work; no interview. Keep tips occasional. My task is: [your task].

Confirm that the coach can read the bundled guide. If it cannot, use the [manual setup](NATIVE-APPS.md). Account installation does not prove the skill activates in every new chat. Skills and commands work in Claude chat; hooks and local MCP servers run only in Cowork and Claude Code (this plugin ships neither). See [Claude plugins](https://support.claude.com/en/articles/13837440-use-plugins-in-claude).

## ChatGPT and Codex installation

**Workspace:** a workspace admin adds the plugin and publishes it with **Plugins → Personal → plugin menu → Publish**, then grants the intended roles access. Members get it on web, desktop and mobile. This is workspace distribution, not public publication. See [workspace publishing](https://developers.openai.com/plugins/build/plugins#publish-a-local-plugin-to-your-workspace).

**Codex:** run `codex plugin marketplace add Entuvo/prompting-wizard` and install **prompting-wizard**.

**Public:** the publisher uploads `prompting-wizard-openai.zip` through the [OpenAI plugin submission portal](https://developers.openai.com/plugins/deploy/submission); one listing covers ChatGPT and Codex. Publish only after approval. OpenAI's guidelines exclude trial plugins, so the pilot label has to be resolved by the walkthrough first.

Once installed, start a new chat, select the plugin with `@` if necessary, and use the start request above.

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

## Maintainers

The plugin tree `plugins/prompting-wizard/` is generated; never hand-edit it. Its canonical sources are:

- `prompting-wizard/` (course skill), `pw/SKILL.md` and `learn/SKILL.md`;
- `prompting-wizard/.claude-plugin/plugin.json`, `packaging/plugin.json` (Agent Plugins) and `packaging/openai-plugin.json` (legacy Codex);
- `packaging/README.md` (the plugin's README); the guide and empty card are generated from `prompting-wizard/references/`.

```sh
python3 tools/sync_codex_plugin.py          # regenerate the tree
python3 tools/sync_codex_plugin.py --check  # CI: stale, missing or unexpected files
python3 tools/package_release.py            # build the two downloads
```

All three manifests share the course version in `prompting-wizard/VERSION.md`. Skill descriptions must stay within claude.ai's 200-character limit, and frontmatter within the Agent Skills fields. Never place learner cards or progress in the plugin tree. Current OpenAI submission rules do not accept plugins with lifecycle hooks or app references; keep the optional coaching hooks a separate install.

Documentation checked 16 October 2026 (Claude plugins and Claude Code plugin reference; OpenAI Plugins build and submission guides).
