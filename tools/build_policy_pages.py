#!/usr/bin/env python3
"""Publish PRIVACY.md, TERMS.md and SUPPORT.md as static pages on the GitHub Pages site.

Plugin directories read the policy URLs with automated checks, so each page is plain HTML with no script
needed to show its text. The Markdown files stay the source; this renders the small subset they use
(headings, paragraphs, "- " lists, `code`, [links](...) and bare URLs) and fails on anything else.
Run:  python3 tools/build_policy_pages.py          (write docs/<page>/index.html)
      python3 tools/build_policy_pages.py --check  (exit 1 when a page is missing or stale)
"""
import hashlib
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = "https://entuvo.github.io/prompting-wizard/"
REPO = "https://github.com/Entuvo/prompting-wizard/blob/main/"
PAGES = {"PRIVACY.md": "privacy", "TERMS.md": "terms", "SUPPORT.md": "support"}
DESCRIPTIONS = {
    "privacy": "How Prompting Wizard handles your data: what it reads, what it stores, and what Entuvo receives.",
    "terms": "The terms for using Prompting Wizard, open source software by Entuvo.",
    "support": "How to get help with Prompting Wizard and report a problem.",
}
INLINE = re.compile(r"`([^`]+)`|\[([^\]]+)\]\(([^)\s]+)\)|(https://[^\s<>()]+[^\s<>().,;:])")


def href(target):
    if target.startswith("https://"):
        return target
    path, _, fragment = target.partition("#")
    if path in PAGES:
        url = f"../{PAGES[path]}/"
    elif path and "/" not in path.strip("./") and not path.startswith(".."):
        url = REPO + path
    else:
        raise ValueError(f"unsupported link target: {target}")
    return url + (f"#{fragment}" if fragment else "")


def inline(text):
    out, last = [], 0
    for m in INLINE.finditer(text):
        out.append(html.escape(text[last:m.start()], quote=False))
        code, label, target, bare = m.groups()
        if code is not None:
            out.append(f"<code>{html.escape(code, quote=False)}</code>")
        elif label is not None:
            out.append(f'<a href="{html.escape(href(target))}">{inline(label)}</a>')
        else:
            out.append(f'<a href="{html.escape(bare)}">{html.escape(bare, quote=False)}</a>')
        last = m.end()
    out.append(html.escape(text[last:], quote=False))
    return "".join(out)


def blocks(markdown):
    """-> (title, sections); each section is a list of HTML blocks, the first headed by its <h2>."""
    title, sections = None, [[]]
    for block in re.split(r"\n\s*\n", markdown.strip()):
        lines = block.splitlines()
        if lines[0].startswith("# ") and len(lines) == 1 and title is None:
            title = lines[0][2:].strip()
        elif lines[0].startswith("## ") and len(lines) == 1:
            sections.append([f"<h2>{inline(lines[0][3:].strip())}</h2>"])
        elif all(line.startswith("- ") for line in lines):
            items = "".join(f"<li>{inline(line[2:].strip())}</li>" for line in lines)
            sections[-1].append(f'<ul class="need">{items}</ul>')
        elif re.match(r"(#|>|\||```|\* |\d+\. |- )", lines[0]) or any(re.match(r"(#|- |\* )", l) for l in lines[1:]):
            raise ValueError(f"unsupported Markdown block: {lines[0][:60]}")
        else:
            sections[-1].append(f"<p>{inline(' '.join(line.strip() for line in lines))}</p>")
    if title is None:
        raise ValueError("missing '# ' title")
    return title, [s for s in sections if s]


def stylesheet(name):
    digest = hashlib.sha256((DOCS / name).read_bytes()).hexdigest()[:8]
    return f'<link rel="stylesheet" href="../{name}?v={digest}">'


def render(source):
    slug = PAGES[source]
    title, sections = blocks((ROOT / source).read_text(encoding="utf-8"))
    page_title = html.escape(f"{title} | Prompting Wizard")
    description = html.escape(DESCRIPTIONS[slug])
    body = "\n".join(f'<section><div class="wrap">\n' + "\n".join(s) + "\n</div></section>" for s in sections)
    nav = "".join(f'<a href="../{s}/">{s.capitalize()}</a>' for s in PAGES.values())
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page_title}</title>
<meta name="description" content="{description}">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:title" content="{page_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{SITE}{slug}/">
<meta property="og:image" content="{SITE}assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<!-- Generated from {source} by tools/build_policy_pages.py; edit the Markdown and rerun. -->
{stylesheet("tokens.css")}
{stylesheet("style.css")}
</head>
<body>
<header class="wrap">
<a href="../"><img class="logo logo-light" src="../assets/logo-on-light.svg" alt="Prompting Wizard" width="336" height="56"><img class="logo logo-dark" src="../assets/logo-on-dark.svg" alt="Prompting Wizard" width="336" height="56"></a>
<div class="hero">
<div>
<h1>{html.escape(title)}</h1>
</div>
</div>
</header>
<main>
{body}
</main>
<footer><div class="wrap">
<nav>{nav}<a href="https://github.com/Entuvo/prompting-wizard">GitHub</a></nav>
<p>Made by <a href="https://www.entuvo.com">Entuvo</a>.</p>
</div></footer>
<!-- Cloudflare Web Analytics: cookie-free visit counts; see PRIVACY.md --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "a182596c5b174373a10af726091943e9"}}'></script>
</body>
</html>
"""


def main(check):
    stale = 0
    for source, slug in PAGES.items():
        page = DOCS / slug / "index.html"
        want = render(source)
        if page.is_file() and page.read_text(encoding="utf-8") == want:
            continue
        if check:
            print(f"docs/{slug}/index.html is stale or missing; run python3 tools/build_policy_pages.py")
            stale += 1
        else:
            page.parent.mkdir(parents=True, exist_ok=True)
            page.write_text(want, encoding="utf-8")
            print(f"docs/{slug}/index.html")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv[1:]))
