#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
#     "beautifulsoup4",
#     "markdownify",
# ]
# ///
"""Fetch https://packagecloud.io/docs/api and convert it to Markdown."""

import argparse
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

URL = "https://packagecloud.io/docs/api"


# The `/api/v1/token.json` endpoint returns a tiny object the source page
# never names. Declaring it as `APIToken` means client codegen gets a
# proper named type instead of an anonymous inline object.
API_TOKEN_SECTION = '''
<a id="object_APIToken"></a>

## APIToken

#### Fields:

- `token` Your packagecloud API token, used for HTTP basic authentication on subsequent requests.

#### Example:

```
{"token":"f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0"}
```

#### See Also:

The [docs](#api_tokens) on API tokens.
'''


# The `/api/v1/licenses/:license_key/license.json` endpoint returns a tiny
# object the docs only describe as "Hash" — synthesize a named `License`
# type so codegen produces an explicit struct.
LICENSE_SECTION = '''
<a id="object_License"></a>

## License

#### Fields:

- `license` The packagecloud:enterprise license data (YAML-encoded string).
- `signature` The GPG signature of the license data, verifiable against the packagecloud GPG key.

#### Example:

```
{
  "license": "---\\n:company_name: company-2\\n:company_domain: www.domain2.com\\n",
  "signature": "-----BEGIN PGP SIGNATURE-----\\n...\\n-----END PGP SIGNATURE-----\\n"
}
```

#### See Also:

The [docs](#resource_licenses_method_index) on the licenses API.
'''


# The `/api/v1/distributions` endpoint's response type is named
# `Hash<String, Distribution>`, but `Distribution` itself is never defined
# under ``Objects`` in the source docs. Synthesize both `Distribution` and
# its `DistroVersion` element type so the response can resolve to
# ``additionalProperties: {$ref: Distribution}`` and client codegen produces
# proper named types. Field list is inferred from real API responses (see
# ``dists.json``).
DISTRIBUTION_SECTION = '''
<a id="object_DistroVersion"></a>

## DistroVersion

#### Fields:

- `id` The numeric id of this version. Used as the `distro_version_id` value on package-upload requests.
- `display_name` Human-readable name for the version (e.g. "5.10 Breezy Badger").
- `index_name` Short canonical name used in repository paths (e.g. "breezy").
- `version_number` The version number portion when applicable (e.g. "5.10").

#### Example:

```
{
  "id": 4,
  "display_name": "5.10 Breezy Badger",
  "index_name": "breezy",
  "version_number": "5.10"
}
```

<a id="object_Distribution"></a>

## Distribution

#### Fields:

- `display_name` Human-readable name for the distribution (e.g. "Ubuntu").
- `index_name` Short canonical name used in repository paths (e.g. "ubuntu").
- `versions` Array<DistroVersion> The known versions of this distribution.

#### Example:

```
{
  "display_name": "Ubuntu",
  "index_name": "ubuntu",
  "versions": [
    {
      "id": 4,
      "display_name": "5.10 Breezy Badger",
      "index_name": "breezy",
      "version_number": "5.10"
    }
  ]
}
```

#### See Also:

The [docs](#resource_distributions) on the distributions API.
'''


# The `packages_contents` endpoint is documented as returning a `PackageContents`
# object, but the source page never defines that type. Synthesize a schema
# section from the example response so the OpenAPI builder can resolve the
# reference. The field list and example match the shape the API actually
# returns (see the Example response on the packages_contents endpoint).
PACKAGE_CONTENTS_SECTION = '''
<a id="object_PackageContents"></a>

## PackageContents

#### Fields:

- `files` An array of file entries referenced by the source package; each entry has a `filename`, `size`, and `md5sum`.

#### Example:

```
{
  "files": [
    {
      "filename": "jake_1.0.orig.tar.bz2",
      "size": 1108,
      "md5sum": "a7a309b55424198ee98abcb8092d7be0"
    },
    {
      "filename": "jake_1.0-7.debian.tar.gz",
      "size": 1571,
      "md5sum": "0fa5395e95ddf846b419e96575ce8044"
    }
  ]
}
```

#### See Also:

The [docs](#resource_packages_method_contents) on the Package Contents API.
'''


SAME_PAGE_PREFIXES = (
    "https://packagecloud.io/docs/api",
    "http://packagecloud.io/docs/api",
    "/docs/api",
)


class DocsConverter(MarkdownConverter):
    """Tweaks:
    - Fenced code blocks with language hints when present.
    - Same-page <a href="/docs/api#X"> links rewritten to "#X".
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
        return super().convert_a(el, text, parent_tags)

    def convert_pre(self, el, text, parent_tags):
        code = el.find("code")
        lang = ""
        if code and code.get("class"):
            for cls in code["class"]:
                if cls.startswith("language-"):
                    lang = cls[len("language-"):]
                    break
                if cls.startswith("lang-"):
                    lang = cls[len("lang-"):]
                    break
        body = (code.get_text() if code else el.get_text()).rstrip("\n")
        body = repair_json_example(body)
        return f"\n\n```{lang}\n{body}\n```\n\n"


JSON_START_RE = re.compile(r'^\s*[\[{]')
JSON_ELLIPSIS_LINE_RE = re.compile(r'^\s*\.\.\.\s*,?\s*$', re.MULTILINE)
JSON_TRAILING_COMMA_RE = re.compile(r',(\s*[}\]])')


def repair_json_example(body: str) -> str:
    """Make the docs' JSON examples actually parse.

    The source pages include trailing commas (``},\\n]``) and literal ``...``
    placeholder lines to elide content — both invalid JSON. We leave non-JSON
    blocks (curl commands, HTTP status lines, etc.) untouched.
    """
    if not JSON_START_RE.match(body):
        return body
    body = JSON_ELLIPSIS_LINE_RE.sub('', body)
    body = JSON_TRAILING_COMMA_RE.sub(r'\1', body)
    return body


def extract_main(soup: BeautifulSoup):
    for selector in ("main", "article", "#content", ".docs-content", ".content"):
        node = soup.select_one(selector)
        if node:
            return node
    return soup.body or soup


# A type lexeme: a word, optionally with an <...> generic containing
# comma-separated words (Array<GPGKey>, Hash<String, Distribution>).
TYPE_LEXEME = r'\w+(?:<\w+(?:,\s*\w+)*>)?'
PARAM_TYPE_RE = re.compile(
    r'^(\s*-\s+`[^`]+`\s+)(' + TYPE_LEXEME + r')(\s+[A-Z])',
)
RESPONSE_TYPE_RE = re.compile(
    r'^(\s*)(' + TYPE_LEXEME + r')(\s+[A-Z])',
)
H4_RE = re.compile(r'^#{4,6}\s+(.+?):?\s*$')
H1_3_RE = re.compile(r'^#{1,3}\s+')

# Single-letter "A" and "An" are English indefinite articles, not types.
# ``A JSON hash of ...`` should stay as prose, not become `` `A` JSON hash ...``.
ARTICLE_LEXEMES = {"A", "An"}


def _wrap_type_match(m):
    prefix, lexeme, suffix = m.group(1), m.group(2), m.group(3)
    if lexeme in ARTICLE_LEXEMES:
        return m.group(0)
    return f"{prefix}`{lexeme}`{suffix}"


def wrap_type_expressions(md: str) -> str:
    """Wrap API type expressions in inline backticks.

    Two places they show up:
    - In `URL Params`/`Query Params`/`Body Params` bullets: after the
      backticked param name (e.g. ``- `:user_id` String The username.``).
    - In a `Response:` section's first paragraph (e.g. ``Empty An empty JSON
      hash.`` or ``Array<GPGKey> An array of ...``).

    The lexeme matches a bare word or a generic like `Array<GPGKey>`; we only
    wrap when the next word starts with a capital letter, which filters out
    prose like ``The GPG key type`` (next word ``type`` is lowercase).
    """
    out: list[str] = []
    current_h4 = None
    pending_response = False
    for line in md.splitlines():
        if (m := H4_RE.match(line)):
            current_h4 = m.group(1).strip().lower()
            pending_response = (current_h4 == "response")
            out.append(line); continue
        if H1_3_RE.match(line):
            current_h4 = None; pending_response = False
            out.append(line); continue

        if current_h4 in {"url params", "query params", "body params"} and line.lstrip().startswith("- `"):
            out.append(PARAM_TYPE_RE.sub(_wrap_type_match, line)); continue

        if pending_response and line.strip():
            out.append(RESPONSE_TYPE_RE.sub(_wrap_type_match, line))
            pending_response = False
            continue

        out.append(line)
    return "\n".join(out)


def clean(node):
    for tag in node.select("script, style, noscript, nav, header, footer, aside"):
        tag.decompose()
    # Parameter names are marked with <span class="name">; re-tag as <code>
    # so markdownify emits them as inline `backticks`. Skip spans inside <pre>
    # (pygments uses other class names anyway, but be defensive).
    for span in node.select('span.name'):
        classes = span.get("class", [])
        if classes != ["name"]:  # skip "name success"/"name failure" status tags
            continue
        if span.find_parent("pre"):
            continue
        # SeriesValue's Fields bullet authors the word "A" as a name span
        # even though the sentence ("A JSON hash of Dates and values") starts
        # with the English article. Unwrap so it doesn't become `` `A` ``.
        if span.get_text(strip=True) in ARTICLE_LEXEMES:
            span.unwrap()
            continue
        span.name = "code"
        del span["class"]
    return node


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-o", "--output", default="api-docs/packagecloud-api.md",
                        help="Output markdown path (default: %(default)s)")
    parser.add_argument("-u", "--url", default=URL, help="Source URL")
    parser.add_argument("--html-cache", default="api-docs/packagecloud-api.html",
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
    main_node = clean(extract_main(soup))

    md = DocsConverter(heading_style="ATX", bullets="-", code_language="").convert_soup(main_node)
    md = "\n".join(line.rstrip() for line in md.splitlines())
    md = wrap_type_expressions(md)
    md = md.rstrip() + "\n\n" + API_TOKEN_SECTION.strip() + "\n"
    md = md.rstrip() + "\n\n" + LICENSE_SECTION.strip() + "\n"
    md = md.rstrip() + "\n\n" + DISTRIBUTION_SECTION.strip() + "\n"
    md = md.rstrip() + "\n\n" + PACKAGE_CONTENTS_SECTION.strip() + "\n"
    while "\n\n\n" in md:
        md = md.replace("\n\n\n", "\n\n")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md.strip() + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(md)} chars)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
