#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
#     "beautifulsoup4",
#     "markdownify",
# ]
# ///
"""Fetch https://packagecloud.io/docs and convert it to Markdown.

This is the general documentation page (packaging concepts, repository setup,
config files, the master-token/read-token/API-token model, CLI usage, etc.) —
the conceptual companion to the per-endpoint reference parsed by
``fetch_api_docs.py``. Unlike the API page, this content does not feed the
OpenAPI build; it is kept as a human-readable reference under ``api-docs/``.
"""

import argparse
import html as htmllib
import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

URL = "https://packagecloud.io/docs"
SITE_ROOT = "https://packagecloud.io"

# Same-page links on /docs show up as "/docs", "/docs#frag", "#frag", or the
# fully-qualified equivalents. NOTE: "/docs/api#..." is a *different* page and
# must not be collapsed to a fragment — handled by the exact/"#"-suffix checks
# below rather than a naive prefix match.
SAME_PAGE_PREFIXES = (
    "https://packagecloud.io/docs",
    "http://packagecloud.io/docs",
    "/docs",
)


class DocsConverter(MarkdownConverter):
    """Tweaks:
    - Fenced code blocks.
    - Same-page links rewritten to bare "#frag".
    - Remaining site-relative links (e.g. "/docs/api#...") absolutized to
      https://packagecloud.io/... so the standalone markdown's links resolve.
    - Empty <a name="X"> anchors emitted as raw HTML <a id="X"></a> so
      fragment links in the markdown actually resolve.
    """

    def convert_a(self, el, text, parent_tags):
        href = el.get("href") or ""
        anchor = el.get("name") or el.get("id")
        if not href:
            return f'<a id="{anchor}"></a>' if anchor else (text or "")
        for prefix in SAME_PAGE_PREFIXES:
            if href == prefix:
                el["href"] = "#"
                break
            if href.startswith(prefix + "#"):
                el["href"] = href[len(prefix):]
                break
        else:
            # Not a same-page link. Absolutize bare site-relative hrefs.
            if href.startswith("/"):
                el["href"] = SITE_ROOT + href
        return super().convert_a(el, text, parent_tags)

    def convert_pre(self, el, text, parent_tags):
        code = el.find("code")
        body = (code.get_text() if code else el.get_text()).rstrip("\n")
        return f"\n\n```\n{body}\n```\n\n"


# --- The per-distribution "Push/Yank string" table ---------------------------
#
# The OS/version table is an AngularJS template
# (``<div class="distros-container" ng-repeat=...>``) whose data lives inline in
# the page as ``generalDocApp.config.allDist`` and is rendered client-side. The
# static HTML carries only the ``{{ ... }}`` placeholders, so we parse the data
# ourselves and reproduce exactly what the template would emit. The helper
# functions below mirror the originals from the page's JS bundle:
#
#   pythonOrNode(key)     -> "Node.js"/"Python" groups are skipped (ng-if);
#                            they have their own static sections above.
#   distAnchorName(d)     -> "anchor-" + os_dist.split("/")[0]
#   packageFileName(type) -> sample artifact filename per package type
#   amzInfoLink(item)     -> display_name, with an Amazon Linux note on EL 6.0


def _extract_alldist(html: str):
    """Pull the ``allDist`` JSON array out of the inline ``generalDocApp`` config."""
    m = re.search(r"allDist\s*:\s*", html)
    if not m:
        return None
    try:
        data, _ = json.JSONDecoder().raw_decode(html, m.end())
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, list) else None


def _package_file_name(package_type: str) -> str:
    return {
        "rpm": "test-1.0-2.el6.x86_64.rpm",
        "deb": "testpkg_1.0-2_amd64.deb",
        "alpine": "test-0.7.4-r7.apk",
    }.get(package_type, "<package_name>")


def _version_cell(item: dict) -> str:
    name = htmllib.escape(item.get("display_name", ""))
    # The page links Enterprise Linux 6.0 to the Amazon Linux note.
    if item.get("display_name") == "Enterprise Linux 6.0":
        return f"{name} / <a href=\"#amazon-info\">Amazon Linux</a>"
    return name


def render_distros_html(distros: list) -> str:
    """Reproduce the ``.distros-container`` template, one block per distro group.

    Grouping mirrors AngularJS ``groupBy: 'distro_name'`` (first-seen group
    order, original order within a group); table rows mirror ``orderBy: 'id'``;
    the anchor/heading/examples use the group's first entry, as the template's
    ``value[0]`` does.
    """
    groups: dict[str, list] = {}
    for item in distros:
        groups.setdefault(item.get("distro_name", ""), []).append(item)

    blocks = ["<div>"]
    for key, value in groups.items():
        if key in ("Node.js", "Python"):  # pythonOrNode(key)
            continue
        first = value[0]
        anchor = "anchor-" + str(first.get("os_dist", "")).split("/")[0]
        display = htmllib.escape(first.get("display_name", ""))
        os_dist = htmllib.escape(first.get("os_dist", ""))
        pkg_file = htmllib.escape(_package_file_name(first.get("package_type", "")))

        rows = "".join(
            f"<tr><td>{_version_cell(item)}</td>"
            f"<td>{htmllib.escape(item.get('os_dist', ''))}</td></tr>"
            for item in sorted(value, key=lambda i: i.get("id", 0))
        )
        blocks.append(
            f'<a name="{anchor}"></a>\n'
            f"<h3>{htmllib.escape(key)}</h3>\n"
            "<table>\n"
            "<thead><tr><th>Version</th><th>Push/Yank string</th></tr></thead>\n"
            f"<tbody>{rows}</tbody>\n"
            "</table>\n"
            f"<p><i>Example: pushing a package to {display}:</i></p>\n"
            f"<pre>package_cloud push user/repo/{os_dist} {pkg_file}</pre>\n"
            f"<p><i>Example: yanking a package from {display}:</i></p>\n"
            f"<pre>package_cloud yank user/repo/{os_dist} {pkg_file}</pre>\n"
        )
    blocks.append("</div>")
    return "\n".join(blocks)


def inject_distros(node, html: str) -> bool:
    """Replace the ``.distros-container`` template with the rendered table."""
    container = node.select_one("div.distros-container")
    if container is None:
        return False
    distros = _extract_alldist(html)
    if not distros:
        print("WARNING: could not extract allDist data; dropping distros table",
              file=sys.stderr)
        container.decompose()
        return False
    rendered = BeautifulSoup(render_distros_html(distros), "html.parser")
    container.replace_with(rendered)
    return True


def extract_main(soup: BeautifulSoup):
    # ``.docs-content`` is the article body; ``main`` also wraps the top nav
    # and a large inline <script>, so prefer the tighter container.
    for selector in (".docs-content", "main", "article", "#content", ".content"):
        node = soup.select_one(selector)
        if node:
            return node
    return soup.body or soup


def clean(node):
    for tag in node.select("script, style, noscript, nav, header, footer, aside"):
        tag.decompose()
    # Any AngularJS template we didn't explicitly render would otherwise leak
    # raw `{{ ... }}` placeholders into the markdown — drop the leftovers.
    for tag in node.select("[ng-repeat]"):
        tag.decompose()
    return node


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-o", "--output", default="api-docs/packagecloud-docs.md",
                        help="Output markdown path (default: %(default)s)")
    parser.add_argument("-u", "--url", default=URL, help="Source URL")
    parser.add_argument("--html-cache", default="api-docs/packagecloud-docs.html",
                        help="Path to cached raw HTML; reused if present, otherwise fetched and saved (default: %(default)s)")
    parser.add_argument("--refresh", action="store_true",
                        help="Ignore any existing HTML cache and re-download from --url.")
    args = parser.parse_args()

    cache = Path(args.html_cache)
    if cache.exists() and not args.refresh:
        html = cache.read_text(encoding="utf-8")
        print(f"Using cached {cache} ({len(html)} chars)", file=sys.stderr)
    else:
        resp = requests.get(args.url, timeout=30, headers={"User-Agent": "packagecloud-rs-docs-fetcher"})
        resp.raise_for_status()
        html = resp.text
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(html, encoding="utf-8")
        print(f"Fetched {args.url} → {cache} ({len(html)} chars)", file=sys.stderr)

    soup = BeautifulSoup(html, "html.parser")
    main_node = extract_main(soup)
    # Render the dynamic distros table before clean() strips the <script> that
    # carries its data.
    inject_distros(main_node, html)
    main_node = clean(main_node)

    md = DocsConverter(heading_style="ATX", bullets="-", code_language="").convert_soup(main_node)
    md = "\n".join(line.rstrip() for line in md.splitlines())
    while "\n\n\n" in md:
        md = md.replace("\n\n\n", "\n\n")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md.strip() + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(md)} chars)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
