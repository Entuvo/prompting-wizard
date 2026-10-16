# Privacy policy

Last updated: 16 October 2026

Prompting Wizard is published by Entuvo. It is a set of files you install into an AI assistant you already use. Entuvo does not operate a Prompting Wizard account system or website backend. The course itself sends Entuvo nothing.

## What we collect

We do not collect personal information, lesson answers, prompts, scores, or `PROGRESS.md` contents.

The standalone course uses a local or attached `PROGRESS.md`. Optional local coaching stores learner data in an owner-only SQLite profile directory you choose. Entuvo receives neither file.

## The website

The website (entuvo.github.io/prompting-wizard) counts visits with Cloudflare Web Analytics. It sets no cookies and does not identify you. Cloudflare records page views, the referring site, and coarse device and country information, so Entuvo can see which pages and which links bring people to the course. The site is hosted by GitHub Pages, which keeps its own server logs under GitHub's policies. Videos load from YouTube only when you press play.

## Optional local coaching

Only explicitly enabled workspaces are captured. Prompts and results are bounded to 16 KiB each, with truncation and incomplete-context labels. At most 1,000 completed pending examples are stored; a full queue skips new ones with a health warning. Pausing stops collection. Exclusion covers the selected workspace and descendants.

Raw examples and unreviewed findings expire after thirty days. Expired evidence is unavailable on runtime reads; physical cleanup happens on the next runtime invocation. A learner-confirmed lesson removes its source raw examples and findings earlier, retaining only the approved concise record. Reviewed records and imported course history remain until deleted. Original Day 0 baselines are preserved.

Both local hosts can use the same directory. When a lesson reads examples from another host, those excerpts enter the current provider's conversation and are subject to its policies. After-result coaching adds model inference and quota use; lesson-only collection does not. There is no Prompting Wizard cloud sync, account or telemetry service.

Use the runtime to inspect, exclude, pause or delete managed learning data. Deletion includes associated pending findings and drafts. Host transcripts, terminal/tool histories, process arguments, explicit exports and external backups are separate; the project cannot erase them or promise forensic erasure. Use stdin rather than command arguments for sensitive record text. See [controls and setup](COACHING.md).

## Learning from past work history

`pw history` runs only when you ask, one time. It reads one of the following:

- your Claude Code or Codex sessions, through that host's documented SDK, skipping workspaces excluded from local coaching;
- a ChatGPT or Claude data export that you downloaded and chose to supply.

It never parses private transcript files. An export archive is read in memory and never extracted. You confirm twice: once before anything is read, and again before scoring.

Scoring sends a sample of your prompts and the assistant's replies (300 by default) through the AI provider you are already using, under its terms, and uses your quota. Each provider's history is reviewed only by that provider's hosts: Claude Code and the Claude app review only Claude exports, and Codex and ChatGPT review only ChatGPT exports. Another provider's export is declined without review. In a coding host, the runtime's shape check runs on your machine and stops before anything reaches the model. In the ChatGPT and Claude apps, though, uploading a file sends it to that app's provider before the plugin can decline it, so upload only that app's own export. Secrets that look like API keys, tokens, long hex strings or email addresses are masked before anything is written or sent. Pattern masking cannot catch everything.

In Claude Code and Codex, results are written under `history/` in a local data directory you choose, with owner-only permissions. They include verbatim prompts, the casebook pages and an aggregate baseline. Runs are deleted 30 days after they are written, on the next runtime invocation, or sooner with `delete`.

In the ChatGPT and Claude apps, nothing is stored by Prompting Wizard. Findings appear in the reply, and the uploaded file stays in that chat under the provider's retention.

Nothing is added to `PROGRESS.md`, a Learning Card, CLAUDE.md, AGENTS.md or any settings file unless you accept it. A Learning Card entry contains a paraphrase, never an excerpt. Entuvo receives nothing. Host transcripts and provider exports are governed by their own retention, and this project cannot delete them.

## What the course may fetch

A locally loaded copy may read the public `VERSION.md` file from this GitHub repository to see whether a newer version exists. Automatic checks happen at most once every seven days. An explicit "check for updates" request, or a missing or unreadable last-check date, can fetch again sooner. That request goes to GitHub, not to an Entuvo server.

The `prompting-wizard-openai.zip` download has no update check and makes no such fetch; it updates only through the app's plugin manager.

Marketplace-managed and skills-CLI installs still apply updates through those hosts. They may also make the same read-only `VERSION.md` fetch when a check is due.

GitHub, Claude, OpenAI, the skills CLI, and any other host you use may collect their own logs or install telemetry under their policies. Those are not Entuvo services.

## Practice prompts

Lesson prompts run in your AI assistant, with that assistant's file and network access. Outputs stay in that session unless you save them.

## Contact

Questions about this policy: open an issue at https://github.com/Entuvo/prompting-wizard/issues

## Portable Learning Cards

The everyday pilot contains no Wizard cloud service or background native-chat capture. A card contains only accepted learning evidence and preferences; avoid secrets and raw work excerpts. Attaching it to ChatGPT or Claude sends it to that provider under your account settings and its terms. Exporting it does not update or erase older uploads, chat history, backups or provider memory. Corrections/retractions affect the card you retain; delete other copies separately. Existing local coaching capture, retention and opt-in remain unchanged.

The native teaching plugins bundle instructions, rubric references and an empty card. They contain no MCP service, lifecycle hooks, local database or telemetry. They do not read other chats. Selected work and attached cards are processed by the host provider. Installing or removing a plugin does not save or delete your retained cards or prior provider uploads.
