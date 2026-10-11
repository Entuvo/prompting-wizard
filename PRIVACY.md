# Privacy policy

Last updated: 11 October 2026

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

## What the course may fetch

A locally loaded copy may read the public `VERSION.md` file from this GitHub repository to see whether a newer version exists. Automatic checks happen at most once every seven days. An explicit "check for updates" request, or a missing or unreadable last-check date, can fetch again sooner. That request goes to GitHub, not to an Entuvo server.

Marketplace-managed and skills-CLI installs still apply updates through those hosts. They may also make the same read-only `VERSION.md` fetch when a check is due.

GitHub, Claude, OpenAI, the skills CLI, and any other host you use may collect their own logs or install telemetry under their policies. Those are not Entuvo services.

## Practice prompts

Lesson prompts run in your AI assistant, with that assistant's file and network access. Outputs stay in that session unless you save them.

## Contact

Questions about this policy: open an issue at https://github.com/Entuvo/prompting-wizard/issues
