#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["PyYAML"]
# ///
"""Parse api-docs/packagecloud-api.md → OpenAPI 3.1 spec.

The markdown has a very regular shape, which is what we exploit:

    <a id="resource_<name>"></a>
    ## <tag>                            # resource group (tag)

    <a id="resource_<name>_method_<op>"></a>
    ### <op>                            # operation

    Optional short description paragraph(s).

    ```
    <METHOD> /api/v1/...
    ```

    #### URL Params:                    # path params + form/body params
    - `:user_id` String ...             # (names starting with ':' are path)
    - `package[file]` File ...

    #### Query Params:
    - `:q` String ...

    #### Response:
    Array<Thing> Description of the response type.

    #### Example request(s):
    ```curl ... ```

    #### Example response:
    ```< HTTP/1.1 200 OK```
    ```{ "json": "body" }```

Schemas come after operations:

    <a id="object_<Name>"></a>
    ## <Name>

    #### Fields:
    - `name` description of the field.

    #### Example:
    ```{ ... }```
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


def _str_representer(dumper, data):
    """Dump multi-line strings as literal block scalars (``foo: |``) so long
    descriptions and code snippets stay readable instead of turning into
    single-quoted escape soup."""
    if "\n" in data:
        # Literal block style doesn't permit trailing whitespace on lines —
        # strip it per-line so PyYAML doesn't silently fall back to quoting.
        cleaned = "\n".join(line.rstrip() for line in data.split("\n"))
        return dumper.represent_scalar("tag:yaml.org,2002:str", cleaned, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, _str_representer, Dumper=yaml.SafeDumper)


RE_ANCHOR = re.compile(r'^<a id="([^"]+)"></a>\s*$')
RE_H2 = re.compile(r'^## (.+)$')
RE_H3 = re.compile(r'^### (.+)$')
RE_SUBHEAD = re.compile(r'^(#{4,6})\s+(.+?):?\s*$')
RE_CODE_FENCE = re.compile(r'^```')
RE_HTTP_LINE = re.compile(
    r'^(GET|POST|PUT|PATCH|DELETE)\s+(?:https?://[^\s/]+)?(/\S+)\s*$', re.I,
)
RE_PARAM_BULLET = re.compile(r'^-\s+`([^`]+)`\s*(.*)$')
RE_CURL_FILE = re.compile(r"""-F\s+["']?([^'"=\s]+)=@""")
RE_CURL_JSON_HEADER = re.compile(
    r"""-H\s+["']?Content-Type:\s*application/json""", re.I,
)
RE_HTTP_STATUS = re.compile(r'^<\s*HTTP/[\d.]+\s+(\d{3})\b')
RE_LEADING_CODE = re.compile(r'^`([^`]+)`(\s*)')

PRIMITIVE_SCHEMAS = {
    "String": {"type": "string"},
    "Integer": {"type": "integer"},
    "Int": {"type": "integer"},
    "Number": {"type": "number"},
    "Float": {"type": "number"},
    "Boolean": {"type": "boolean"},
    "Bool": {"type": "boolean"},
    "Hash": {"type": "object"},
    "Empty": {"type": "object"},
}

TYPE_KEYWORDS = {"string", "integer", "int", "number", "float",
                 "boolean", "bool", "file", "hash"}


def tokenize(md: str):
    """Yield (kind, value) blocks: anchor | h2 | h3 | h4 | code | text."""
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if (m := RE_ANCHOR.match(line)):
            yield ("anchor", m.group(1)); i += 1; continue
        if (m := RE_H2.match(line)):
            yield ("h2", _unescape(m.group(1))); i += 1; continue
        if (m := RE_H3.match(line)):
            yield ("h3", _unescape(m.group(1))); i += 1; continue
        if (m := RE_SUBHEAD.match(line)):
            yield (f"h{len(m.group(1))}", _unescape(m.group(2)).strip())
            i += 1; continue
        if RE_CODE_FENCE.match(line):
            buf = []; i += 1
            while i < len(lines) and not RE_CODE_FENCE.match(lines[i]):
                buf.append(lines[i]); i += 1
            i += 1  # skip closing fence
            yield ("code", "\n".join(buf))
            continue
        if not line.strip():
            i += 1; continue
        buf = [line]; i += 1
        while i < len(lines) and lines[i].strip() and not (
            RE_ANCHOR.match(lines[i]) or RE_H2.match(lines[i]) or
            RE_H3.match(lines[i]) or RE_SUBHEAD.match(lines[i]) or
            RE_CODE_FENCE.match(lines[i])
        ):
            buf.append(lines[i]); i += 1
        yield ("text", "\n".join(buf))


def _slug(s: str) -> str:
    return re.sub(r'_+', '_', re.sub(r'\W+', '_', s.lower())).strip('_')


def _unescape(s: str) -> str:
    return s.replace(r"\_", "_").replace(r"\*", "*").strip()


def parse(tokens):
    """Walk tokens into a tree of resources (tags→operations) and objects (schemas)."""
    resources: dict[str, dict] = {}
    objects: list[dict] = []
    intro_sections: list[dict] = []

    anchor: str | None = None
    mode = "intro"
    resource = op = obj = None
    intro: dict | None = None
    h4: str | None = None
    h5: str | None = None
    note_pending = False

    def new_op(name: str, anch: str) -> dict:
        return {
            "anchor": anch, "name": name, "description": "", "notes": "",
            "variants": [],  # list of {method, path, label}
            "url_params": [], "query_params": [],
            "response_text": "",
            "example_requests": [], "example_responses": [],
        }

    def flush_op():
        nonlocal op
        if op is not None and resource is not None:
            resource["operations"].append(op)
        op = None

    def flush_obj():
        nonlocal obj
        if obj is not None:
            objects.append(obj)
        obj = None

    for kind, value in tokens:
        if kind == "anchor":
            anchor = value; continue

        if kind == "h2":
            flush_op(); flush_obj(); h4 = None
            if anchor and anchor.startswith("object_"):
                mode = "object"; resource = None; intro = None
                obj = {"anchor": anchor, "name": value, "fields": [],
                       "example": None, "description": ""}
            elif anchor and anchor.startswith("resource_"):
                mode = "resource"; obj = None; intro = None
                resource = resources.setdefault(value, {
                    "anchor": anchor, "tag": value, "operations": [],
                })
            else:
                mode = "intro"; resource = None; obj = None
                intro = {"anchor": anchor or "", "title": value, "blocks": []}
                intro_sections.append(intro)
            anchor = None
            continue

        if kind == "h3":
            flush_op(); h4 = None; h5 = None; note_pending = False
            if mode == "resource" and resource is not None:
                op = new_op(value, anchor or "")
            anchor = None
            continue

        if kind == "h4":
            h4 = value.lower(); h5 = None; note_pending = False
            continue
        if kind == "h5":
            h5 = value; note_pending = False
            continue
        if kind == "h6":
            # H6 markers ("###### Note:") are parenthetical — the next text
            # block is the note, but we must not leave h4 set, or H5 variants
            # that follow the note would be blocked from parsing as operations.
            note_pending = True
            continue

        # content block
        if mode == "resource" and op is not None:
            if note_pending and kind == "text":
                op["notes"] = (op["notes"] + "\n\n" + value).strip()
                note_pending = False
            else:
                _op_block(op, kind, value, h4, h5)
        elif mode == "object" and obj is not None:
            _obj_block(obj, kind, value, h4)
        elif mode == "intro" and intro is not None:
            intro["blocks"].append((kind, value, h4))

    flush_op(); flush_obj()
    return {"resources": list(resources.values()), "objects": objects,
            "intro_sections": intro_sections}


def _op_block(op, kind, value, h4, h5):
    if h4 is None:
        if kind == "code":
            for ln in value.splitlines():
                if (m := RE_HTTP_LINE.match(ln.strip())):
                    op["variants"].append({
                        "method": m.group(1).upper(),
                        "path": m.group(2),
                        "label": h5,
                    })
                    return
        if kind == "text":
            op["description"] = (op["description"] + "\n\n" + value).strip()
        return
    if h4 == "url params" and kind == "text":
        op["url_params"].extend(_parse_bullets(value))
    elif h4 == "query params" and kind == "text":
        op["query_params"].extend(_parse_bullets(value))
    elif h4 == "response" and kind == "text":
        op["response_text"] = (op["response_text"] + "\n" + value).strip()
    elif h4 == "example request(s)" and kind == "code":
        op["example_requests"].append(value)
    elif h4 == "example response" and kind == "code":
        op["example_responses"].append(value)
    elif h4 in {"note", "permissions"} and kind == "text":
        op["notes"] = (op["notes"] + "\n\n" + value).strip()


_JSON_START = re.compile(r'^\s*[\[{]')


def _obj_block(obj, kind, value, h4):
    if h4 == "fields" and kind == "text":
        obj["fields"].extend(_parse_bullets(value))
    elif h4 == "example" and kind == "code":
        if obj["example"] is None:
            obj["example"] = value
    elif kind == "code" and obj["example"] is None and _JSON_START.match(value):
        # Some schema sections (PackageDetails) put the example code fence
        # before the Fields/Example headings rather than under `#### Example:`.
        # Treat any JSON-looking code block in the section as the example.
        obj["example"] = value
    elif h4 is None and kind == "text":
        obj["description"] = (obj["description"] + "\n\n" + value).strip()


def _unwrap_leading_code(text: str) -> str:
    """Strip a leading ``Type`` backtick wrap from a description.

    fetch_api_docs.py wraps leading type lexemes in inline code for readability;
    the builder's type inference expects the bare word (e.g. ``String``).
    """
    text = text.lstrip()
    if (m := RE_LEADING_CODE.match(text)):
        rest = text[m.end():]
        return (m.group(1) + (" " + rest if rest else "")).strip()
    return text


def _parse_bullets(text: str) -> list[dict]:
    out = []
    for ln in text.splitlines():
        if (m := RE_PARAM_BULLET.match(ln.strip())):
            desc = _unwrap_leading_code(m.group(2).strip())
            out.append({"name": m.group(1), "description": desc})
    return out


# ---- schema/type inference ----

def _first_word(desc: str) -> str:
    return (desc.split() or [""])[0].lower().rstrip(".,;:")


RE_ARRAY_OF = re.compile(r'^array<([^>]+)>', re.I)


def _type_from_desc(desc: str) -> dict:
    w = _first_word(desc)
    if w == "string":  return {"type": "string"}
    if w in ("integer", "int"): return {"type": "integer"}
    if w in ("number", "float"): return {"type": "number"}
    if w in ("boolean", "bool"): return {"type": "boolean"}
    if w == "file":    return {"type": "string", "format": "binary"}
    if w == "hash":    return {"type": "object"}
    if (m := RE_ARRAY_OF.match(desc.strip())):
        inner = m.group(1).strip().lower()
        if inner == "file":
            return {"type": "array", "items": {"type": "string", "format": "binary"}}
        if inner == "string":
            return {"type": "array", "items": {"type": "string"}}
        if inner in ("integer", "int"):
            return {"type": "array", "items": {"type": "integer"}}
        return {"type": "array", "items": {}}
    if w.startswith("array"):
        return {"type": "array", "items": {}}
    return {"type": "string"}


def _strip_type_prefix(desc: str) -> str:
    if not desc: return desc
    parts = desc.split(None, 1)
    if not parts: return desc
    head = parts[0].lower().rstrip(".,;:")
    if head in TYPE_KEYWORDS or head.startswith("array"):
        return parts[1] if len(parts) > 1 else ""
    return desc


def _value_schema(v):
    if v is None: return {"type": "string", "nullable": True}
    if isinstance(v, bool): return {"type": "boolean"}
    if isinstance(v, int):  return {"type": "integer"}
    if isinstance(v, float): return {"type": "number"}
    if isinstance(v, str):  return {"type": "string"}
    if isinstance(v, list):
        return {"type": "array", "items": _value_schema(v[0]) if v else {}}
    if isinstance(v, dict):
        props = {k: _value_schema(val) for k, val in v.items()}
        return {"type": "object", "properties": props} if props else {"type": "object"}
    return {}


def _best_json(blocks: list[str]):
    """Return the first code block that parses as JSON (stripping leading '<HTTP/...' line)."""
    for b in blocks:
        s = re.sub(r'^<\s*HTTP/[^\n]+\n?', '', b.strip())
        try:
            return json.loads(s)
        except Exception:
            continue
    return None


def _openapi_path(doc_path: str) -> str:
    return re.sub(r':([A-Za-z_][A-Za-z0-9_]*)', r'{\1}', doc_path)


def _path_params(openapi_path: str) -> set[str]:
    return set(re.findall(r'\{([^}]+)\}', openapi_path))


def _operation_id(anchor: str, tag: str, name: str) -> str:
    if anchor.startswith("resource_") and "_method_" in anchor:
        resource, method = anchor[len("resource_"):].split("_method_", 1)
        return f"{resource}_{method}"
    return re.sub(r'\W+', '_', f"{tag}_{name}").strip("_")


RESPONSE_PATTERNS = [
    (re.compile(r'^\[([A-Za-z_]\w*)\]\(#object_\1\)'), "ref"),
    (re.compile(r'^Array<([A-Za-z_]\w*)>'),            "array"),
    (re.compile(r'^<([A-Za-z_]\w*)>'),                 "ref"),
    (re.compile(r'^Hash<String,\s*([A-Za-z_]\w*)>'),   "hash"),
    (re.compile(r'^([A-Z][A-Za-z0-9_]*)\b'),           "ref"),  # fallback: bare name
]


def _response_schema(text: str, known: set[str], example=None) -> dict:
    """Resolve the response schema.

    Priority: known schema refs (Array<Thing>, <Thing>, Hash<String, Thing>,
    [Thing](#object_Thing)) > JSON example inference > bare-primitive text
    (String/Integer/…) > plain object.

    Docs quirk: many list endpoints declare the element type (e.g.
    ``[PackageFragment](#object_PackageFragment) A JSON array of …``) rather
    than ``Array<PackageFragment>``. When the text continues with "array"/
    "list" or the example itself is a list, upgrade a plain ref to
    ``array<ref>``.
    """
    text = _unwrap_leading_code((text or "").strip())
    for pat, kind in RESPONSE_PATTERNS:
        if (m := pat.match(text)) and m.group(1) in known:
            ref = {"$ref": f"#/components/schemas/{m.group(1)}"}
            if kind == "ref":
                rest = text[m.end():]
                if isinstance(example, list) or re.search(r'\b(array|list) of\b', rest, re.I):
                    return {"type": "array", "items": ref}
            if kind == "array": return {"type": "array", "items": ref}
            if kind == "hash":  return {"type": "object", "additionalProperties": ref}
            return ref
    if example is not None:
        return _value_schema(example)
    first = (text.split(None, 1) or [""])[0].rstrip(".,;:")
    if first in PRIMITIVE_SCHEMAS:
        return dict(PRIMITIVE_SCHEMAS[first])
    return {"type": "object"}


def _extract_response_status(example_responses: list[str], default: str) -> str:
    for block in example_responses:
        for ln in block.splitlines():
            if (m := RE_HTTP_STATUS.match(ln.strip())):
                return m.group(1)
    return default


def _extract_curl_data(ex: str):
    """Pull the first balanced `{...}` block following a curl `-d` flag and
    try to parse it as JSON. Handles nested braces that trip regex matching."""
    m = re.search(r'-d\s+[\'"]?\{', ex)
    if not m:
        return None
    start = m.end() - 1  # position of the opening '{'
    depth = 0
    for i in range(start, len(ex)):
        if ex[i] == '{':
            depth += 1
        elif ex[i] == '}':
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(ex[start:i + 1])
                except Exception:
                    return None
    return None


def _json_request_body(example_requests: list[str]) -> dict | None:
    for ex in example_requests:
        if not RE_CURL_JSON_HEADER.search(ex):
            continue
        data = _extract_curl_data(ex)
        if data is None:
            continue
        return {
            "required": True,
            "content": {
                "application/json": {
                    "schema": _value_schema(data),
                    "example": data,
                },
            },
        }
    return None


RE_NESTED_FIELD = re.compile(r'^([A-Za-z_]\w*)\[([A-Za-z_]\w*)\]$')


RE_IDENTIFIER = re.compile(r'^[A-Za-z_]\w*$')


def _field_ref_from_desc(desc: str, known: set[str]) -> tuple[dict | None, str]:
    """If a field description starts with a known schema reference
    (Array<Foo>, <Foo>, Hash<String, Foo>, [Foo](#object_Foo), or bare Foo),
    return (ref-shaped schema, remaining description text)."""
    for pat, kind in RESPONSE_PATTERNS:
        if (m := pat.match(desc)) and m.group(1) in known:
            ref = {"$ref": f"#/components/schemas/{m.group(1)}"}
            if kind == "array": schema = {"type": "array", "items": ref}
            elif kind == "hash": schema = {"type": "object", "additionalProperties": ref}
            else: schema = ref
            return schema, desc[m.end():].lstrip()
    return None, desc


def _build_schema(obj, known: set[str] = frozenset()) -> dict:
    example = _best_json([obj["example"]] if obj["example"] else [])
    example_obj = example[0] if isinstance(example, list) and example else example

    # Free-form map: docs declared no fields and the example's keys aren't
    # identifier-shaped (SeriesValue is keyed by date strings like 20160221Z).
    # Emit `additionalProperties` with a uniform value schema when possible.
    if (isinstance(example_obj, dict) and example_obj and not obj["fields"]
            and all(not RE_IDENTIFIER.match(k) for k in example_obj.keys())):
        value_schemas = [_value_schema(v) for v in example_obj.values()]
        all_same = all(s == value_schemas[0] for s in value_schemas)
        out: dict = {
            "type": "object",
            "additionalProperties": value_schemas[0] if all_same else True,
        }
        if isinstance(example, (dict, list)):
            out["example"] = example
        if obj["description"]:
            out["description"] = obj["description"]
        return out

    props: dict = {}
    nested: dict[str, dict[str, str]] = {}

    for f in obj["fields"]:
        name = f["name"]
        if (m := RE_NESTED_FIELD.match(name)):
            # `paths[self]` groups into `paths: {properties: {self: ...}}`.
            outer, inner = m.group(1), m.group(2)
            nested.setdefault(outer, {})[inner] = f["description"]
            continue
        if "[" in name:
            continue
        desc = f["description"]
        ref_schema, desc = _field_ref_from_desc(desc, known)
        if ref_schema is not None:
            schema = ref_schema
        else:
            schema = (_value_schema(example_obj[name])
                      if isinstance(example_obj, dict) and name in example_obj
                      else {"type": "string"})
        if desc:
            schema = {**schema, "description": desc}
        props[name] = schema

    for outer, inners in nested.items():
        if outer in props:
            continue
        ex_val = example_obj.get(outer) if isinstance(example_obj, dict) else None
        if isinstance(ex_val, dict):
            schema = _value_schema(ex_val)
            inner_props = schema.get("properties") or {}
            for inner, desc in inners.items():
                if inner in inner_props and desc:
                    inner_props[inner] = {**inner_props[inner], "description": desc}
            props[outer] = schema
        else:
            props[outer] = {
                "type": "object",
                "properties": {
                    inner: ({"type": "string", "description": desc}
                            if desc else {"type": "string"})
                    for inner, desc in inners.items()
                },
            }

    # Fold in keys the docs' Fields list forgot — the example is the source of
    # truth for wire format, and the bulleted Fields list is occasionally
    # out of date with the real response shape (ReadToken is missing `id`,
    # Repository is missing `package_count_human`, etc.).
    if isinstance(example_obj, dict):
        for key, val in example_obj.items():
            if key not in props:
                props[key] = _value_schema(val)

    out = {"type": "object"}
    if props:
        out["properties"] = props
    if isinstance(example, (dict, list)):
        out["example"] = example
    if obj["description"]:
        out["description"] = obj["description"]
    return out


def _classify_url_params(url_params, used_path):
    path_p, body_p = [], []
    for p in url_params:
        if p["name"].startswith(":"):
            stripped = p["name"][1:]
            (path_p if stripped in used_path else body_p).append(
                {**p, "name": stripped}
            )
        else:
            body_p.append(p)
    return path_p, body_p


def _param_entry(p, where, required=None):
    schema = _type_from_desc(p["description"])
    entry = {
        "name": p["name"].lstrip(":"),
        "in": where,
        "required": required if required is not None else (where == "path"),
        "schema": schema,
    }
    desc = _strip_type_prefix(p["description"])
    if desc:
        entry["description"] = desc
    return entry


def _file_schema(name: str, existing: dict) -> dict:
    """Binary schema for a file-upload param, preserving description + array shape."""
    is_array = name.endswith("[]") or existing.get("type") == "array"
    out = ({"type": "array", "items": {"type": "string", "format": "binary"}}
           if is_array else {"type": "string", "format": "binary"})
    if "description" in existing:
        out["description"] = existing["description"]
    return out


def _is_file_schema(t: dict) -> bool:
    if t.get("format") == "binary":
        return True
    items = t.get("items") or {}
    return items.get("format") == "binary"


def _curl_file_params(example_requests: list[str]) -> set[str]:
    names: set[str] = set()
    for ex in example_requests:
        names.update(RE_CURL_FILE.findall(ex))
    return names


def _request_body(body_params: list[dict], file_names: set[str] = frozenset()) -> dict | None:
    if not body_params:
        return None
    props = {}
    for p in body_params:
        schema = dict(_type_from_desc(p["description"]))
        desc = _strip_type_prefix(p["description"])
        if desc:
            schema["description"] = desc
        if p["name"] in file_names:
            schema = _file_schema(p["name"], schema)
        props[p["name"]] = schema
    has_file = any(_is_file_schema(s) for s in props.values())
    body_schema = {"type": "object", "properties": props}
    media = "multipart/form-data" if has_file else "application/x-www-form-urlencoded"
    return {"required": True, "content": {media: {"schema": body_schema}}}


def _synthesize_api_tokens(parsed) -> None:
    """The `## API Tokens` section documents GET /api/v1/token.json inline rather
    than as a resource. Pull the HTTP line and examples out of its intro blocks
    and append a synthetic resource so the endpoint shows up in the spec."""
    section = next((s for s in parsed["intro_sections"]
                    if s["anchor"] == "api_tokens"), None)
    if section is None:
        return

    method = path = None
    example_request = None
    example_response = None
    for kind, value, _h4 in section["blocks"]:
        if kind != "code":
            continue
        for ln in value.splitlines():
            if (m := RE_HTTP_LINE.match(ln.strip())):
                method, path = m.group(1).upper(), m.group(2)
                break
        if value.lstrip().startswith("curl") and path and path in value and example_request is None:
            example_request = value
        if example_response is None:
            try:
                parsed_json = json.loads(value.strip())
                if isinstance(parsed_json, dict) and "token" in parsed_json:
                    example_response = parsed_json
            except Exception:
                pass
    if not method or not path:
        return

    op = {
        "anchor": "resource_api_tokens_method_get_token",
        "name": "get_token",
        "description": (
            "Retrieve your API token programmatically. Authenticate with your "
            "packagecloud account email address (as the basic-auth username) and "
            "password (as the basic-auth password); be sure to URL-encode the "
            "username and password if you embed them in the URL."
        ),
        "notes": "",
        "variants": [{"method": method, "path": path, "label": None}],
        "url_params": [], "query_params": [],
        # Leading `APIToken` resolves to a $ref via _response_schema, giving
        # client codegen a named type. The rest of the line becomes the
        # response description.
        "response_text": (
            "APIToken A JSON hash mapping the key `token` to your API token."
        ),
        "example_requests": [example_request] if example_request else [],
        "example_responses": [json.dumps(example_response)] if example_response else [],
        "security_override": [{"emailPassword": []}],
    }
    parsed["resources"].append({
        "anchor": "resource_api_tokens",
        "tag": "api_tokens",
        "operations": [op],
    })


PAGINATION_PARAM_NAMES = {
    "page": "#/components/parameters/pageParam",
    "per_page": "#/components/parameters/perPageParam",
}
PAGINATION_HEADER_REFS = {
    "Link": "#/components/headers/LinkHeader",
    "Total": "#/components/headers/TotalHeader",
    "Per-Page": "#/components/headers/PerPageHeader",
    "Max-Per-Page": "#/components/headers/MaxPerPageHeader",
}

COMPONENTS_PARAMETERS = {
    "pageParam": {
        "name": "page", "in": "query", "required": False,
        "schema": {"type": "integer", "minimum": 1},
        "description": "One-based page index.",
    },
    "perPageParam": {
        "name": "per_page", "in": "query", "required": False,
        "schema": {"type": "integer", "minimum": 1},
        "description": ("Items per page (default 30). Values above the server's "
                        "Max-Per-Page are clamped; inspect the Max-Per-Page "
                        "response header for the effective cap."),
    },
}

COMPONENTS_HEADERS = {
    "LinkHeader": {
        "description": ("RFC-5988 pagination links for this response "
                        "(rel=\"next\", \"prev\", \"last\")."),
        "schema": {"type": "string"},
    },
    "TotalHeader": {
        "description": "Total number of items in the underlying collection.",
        "schema": {"type": "integer"},
    },
    "PerPageHeader": {
        "description": "Number of items returned on this page.",
        "schema": {"type": "integer"},
    },
    "MaxPerPageHeader": {
        "description": ("Maximum number of items the server will return on a "
                        "single page."),
        "schema": {"type": "integer"},
    },
}


def _is_paginated(op: dict) -> bool:
    """GETs with an array response are paginated per the global pagination
    convention in the docs. Also catches the stats map-endpoints (series)
    whose docs explicitly mention pagination but whose response is a map."""
    for resp in (op.get("responses") or {}).values():
        for body in (resp.get("content") or {}).values():
            s = body.get("schema") or {}
            if s.get("type") == "array":
                return True
    desc = op.get("description") or ""
    return bool(re.search(r'\bpagination\b', desc, re.I))


IN_ORDER = {"path": 0, "header": 1, "query": 2, "cookie": 3}


def _sort_parameters(paths: dict, components_params: dict) -> None:
    """Canonicalize parameter order so regen output doesn't shuffle.

    Path params come first in URL-template order (explicitly, not relying on
    insertion order which is contaminated by set-difference iteration in the
    path-filler logic). Then header, then query, then cookie; within those
    non-path groups, sort alphabetically by name. ``$ref`` params are
    resolved against the components-parameters map to find their in/name.
    """
    for path_template, methods in paths.items():
        path_order = {n: i for i, n in enumerate(
            re.findall(r'\{([^}]+)\}', path_template)
        )}

        def key(p: dict):
            if "$ref" in p:
                ref_name = p["$ref"].rsplit("/", 1)[-1]
                resolved = components_params.get(ref_name, {})
                p_in = resolved.get("in", "query")
                p_name = resolved.get("name", ref_name)
            else:
                p_in = p.get("in", "query")
                p_name = p.get("name", "")
            if p_in == "path":
                # Unknown path params (shouldn't happen) sort last among
                # path params, still before any non-path param.
                return (0, path_order.get(p_name, len(path_order)), p_name)
            return (IN_ORDER.get(p_in, 99), 0, p_name)

        for op in methods.values():
            if not isinstance(op, dict):
                continue
            params = op.get("parameters")
            if params:
                op["parameters"] = sorted(params, key=key)


def _apply_pagination(paths: dict, operation_overrides: dict | None = None) -> None:
    operation_overrides = operation_overrides or {}
    for methods in paths.values():
        for method, op in methods.items():
            if method != "get":
                continue
            if (operation_overrides.get(op.get("operationId")) or {}).get("pagination") is False:
                continue
            if not _is_paginated(op):
                continue
            existing = {
                p.get("name") for p in (op.get("parameters") or [])
                if isinstance(p, dict) and p.get("in") == "query"
            }
            params = op.setdefault("parameters", [])
            for pname, ref in PAGINATION_PARAM_NAMES.items():
                if pname not in existing:
                    params.append({"$ref": ref})
            for resp in (op.get("responses") or {}).values():
                headers = resp.setdefault("headers", {})
                for name, ref in PAGINATION_HEADER_REFS.items():
                    headers.setdefault(name, {"$ref": ref})


def _apply_operation_overrides(paths: dict, operation_overrides: dict,
                               known: set[str]) -> None:
    """Patch generated operations with per-endpoint overrides.

    Currently supports ``response_schema``: a type expression matching the
    same grammar as response_text (``ReadToken``, ``Array<ReadToken>``,
    ``Hash<String, License>``, etc.). Routed through ``_response_schema`` so
    the override uses the same resolver as the rest of the builder.
    """
    if not operation_overrides:
        return
    by_id = {}
    for path, methods in paths.items():
        for method, op in methods.items():
            by_id[op.get("operationId")] = op

    for op_id, ov in operation_overrides.items():
        op = by_id.get(op_id)
        if op is None:
            continue
        rs = ov.get("response_schema")
        if rs is not None:
            # String form → resolved via the grammar (Array<Foo>, <Foo>, …).
            # Dict form → used verbatim (arbitrary OpenAPI schema object).
            new_schema = rs if isinstance(rs, dict) else _response_schema(rs, known)
            for resp in (op.get("responses") or {}).values():
                content = resp.get("content") or {}
                for media in content.values():
                    if isinstance(media, dict) and "schema" in media:
                        media["schema"] = new_schema
        # `pagination: false` is consumed downstream by _apply_pagination,
        # which consults operation_overrides directly. Nothing to strip here.


def _apply_schema_overrides(schemas: dict, overrides: dict) -> None:
    """Patch generated schemas with empirical corrections.

    Defaults every declared property to required, then subtracts entries in
    `optional`. Supports a ``replace`` key that swaps the entire schema for
    the provided dict (used when the docs' inferred shape is structurally
    wrong, e.g. SeriesValue's real wire format wraps the date map in a
    ``value`` key). See ``api-docs/schema-overrides.yaml`` for the format.
    """
    for name, ov in (overrides or {}).items():
        if "replace" in ov:
            schemas[name] = ov["replace"]
            continue
        schema = schemas.get(name)
        if schema is None:
            continue
        props = schema.setdefault("properties", {})

        for prop in ov.get("remove_properties") or []:
            props.pop(prop, None)

        for prop, sub in (ov.get("add_properties") or {}).items():
            props[prop] = {**sub}

        for prop in ov.get("nullable") or []:
            if prop in props:
                props[prop] = {**props[prop], "nullable": True}

        optional = set(ov.get("optional") or [])
        required = [p for p in props.keys() if p not in optional]
        if required:
            schema["required"] = required


def build_openapi(parsed, overrides: dict | None = None) -> dict:
    _synthesize_api_tokens(parsed)
    known = {o["name"] for o in parsed["objects"]}
    schemas = {o["name"]: _build_schema(o, known) for o in parsed["objects"]}
    _apply_schema_overrides(schemas, (overrides or {}).get("schemas") or {})

    paths: dict[str, dict] = {}
    tags_seen: list[str] = []

    for res in parsed["resources"]:
        tag = res["tag"]
        if not res["operations"]:
            continue
        if tag not in tags_seen:
            tags_seen.append(tag)
        for op in res["operations"]:
            if not op["variants"]:
                continue
            base_id = _operation_id(op["anchor"], tag, op["name"])
            multi = len(op["variants"]) > 1
            for variant in op["variants"]:
                method = variant["method"]
                oa_path = _openapi_path(variant["path"])
                used = _path_params(oa_path)
                path_ps, body_ps = _classify_url_params(op["url_params"], used)

                parameters = [_param_entry(p, "path") for p in path_ps]
                # Fill in any path params referenced in the URL but not documented.
                documented = {p["name"] for p in path_ps}
                for missing in used - documented:
                    parameters.append({
                        "name": missing, "in": "path", "required": True,
                        "schema": {"type": "string"},
                    })
                # Skip query-param bullets that name an URL path placeholder —
                # the docs occasionally file path params under "Query Params"
                # (e.g. packages_index lists ``:arch`` as a query param even
                # though ``{arch}`` is in the URL template).
                parameters += [_param_entry({**p, "name": p["name"].lstrip(":")},
                                            "query", required=False)
                               for p in op["query_params"]
                               if p["name"].lstrip(":") not in used]

                file_names = _curl_file_params(op["example_requests"])
                json_body = (_json_request_body(op["example_requests"])
                             if method in {"POST", "PUT", "PATCH"} else None)
                has_form_body = (method in {"POST", "PUT", "PATCH"}
                                 and body_ps and json_body is None)
                request_body = (json_body
                                or (_request_body(body_ps, file_names)
                                    if has_form_body else None))
                if body_ps and method not in {"POST", "PUT", "PATCH"}:
                    # For GET/DELETE with form-ish params, fall back to query.
                    parameters += [_param_entry(p, "query", required=False)
                                   for p in body_ps]

                default_status = {"POST": "201", "DELETE": "204"}.get(method, "200")
                example = _best_json(op["example_responses"])
                status = _extract_response_status(op["example_responses"], default_status)
                schema = (op.get("response_schema_override")
                          or _response_schema(op["response_text"], known, example))
                content_schema = {"schema": schema}
                if example is not None:
                    content_schema["example"] = example
                resp_desc = _unwrap_leading_code(
                    " ".join(op["response_text"].split())
                )
                responses = {
                    status: {
                        "description": resp_desc or "Successful response",
                        "content": {"application/json": content_schema},
                    },
                }

                full_desc = "\n\n".join(filter(None, [op["description"], op["notes"]])).strip()
                if op["example_requests"]:
                    full_desc = (full_desc + "\n\n**Example request:**\n\n```\n"
                                 + op["example_requests"][0] + "\n```").strip()

                label = variant["label"]
                op_id = f"{base_id}_{_slug(label)}" if multi and label else base_id
                summary = f"{op['name']} ({label})" if multi and label else op["name"]
                op_obj: dict = {
                    "operationId": op_id,
                    "tags": [tag],
                    "summary": summary,
                }
                if full_desc:
                    op_obj["description"] = full_desc
                if parameters:
                    op_obj["parameters"] = parameters
                if request_body:
                    op_obj["requestBody"] = request_body
                if op.get("security_override"):
                    op_obj["security"] = op["security_override"]
                op_obj["responses"] = responses

                paths.setdefault(oa_path, {})[method.lower()] = op_obj

    op_overrides = (overrides or {}).get("operations") or {}
    _apply_operation_overrides(paths, op_overrides, known)
    _apply_pagination(paths, op_overrides)
    _sort_parameters(paths, COMPONENTS_PARAMETERS)

    return {
        "openapi": "3.1.0",
        "info": {
            "title": "packagecloud API",
            "version": "1.0.0",
            "description": ("REST API for managing packagecloud repositories. "
                            "Generated from https://packagecloud.io/docs/api."),
        },
        "servers": [{"url": "https://packagecloud.io"}],
        "security": [{"apiToken": []}],
        "tags": [{"name": t} for t in tags_seen],
        "paths": paths,
        "components": {
            "securitySchemes": {
                "apiToken": {
                    "type": "http", "scheme": "basic",
                    "description": ("HTTP basic auth: provide your API token as the "
                                    "username, leave the password empty."),
                },
                "emailPassword": {
                    "type": "http", "scheme": "basic",
                    "description": ("HTTP basic auth using your packagecloud account "
                                    "email as the username and password as the password. "
                                    "Used by the token-retrieval endpoint."),
                },
            },
            "parameters": COMPONENTS_PARAMETERS,
            "headers": COMPONENTS_HEADERS,
            "schemas": schemas,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-i", "--input", default="api-docs/packagecloud-api.md")
    ap.add_argument("-o", "--output", default="openapi.yaml")
    ap.add_argument("-f", "--format", choices=["yaml", "json"], default=None)
    ap.add_argument("--overrides", default="api-docs/schema-overrides.yaml",
                    help="Path to schema overrides YAML (skipped if missing).")
    args = ap.parse_args()

    md = Path(args.input).read_text(encoding="utf-8")
    parsed = parse(tokenize(md))

    overrides = {}
    overrides_path = Path(args.overrides)
    if overrides_path.exists():
        overrides = yaml.safe_load(overrides_path.read_text(encoding="utf-8")) or {}

    spec = build_openapi(parsed, overrides)

    fmt = args.format or ("json" if args.output.endswith(".json") else "yaml")
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "json":
        out.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
    else:
        out.write_text(
            yaml.safe_dump(spec, sort_keys=False, width=100, allow_unicode=True) + "\n",
            encoding="utf-8",
        )

    n_paths = len(spec["paths"])
    n_ops = sum(len(v) for v in spec["paths"].values())
    n_schemas = len(spec["components"]["schemas"])
    print(f"Wrote {out}: {n_paths} paths, {n_ops} operations, {n_schemas} schemas",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
