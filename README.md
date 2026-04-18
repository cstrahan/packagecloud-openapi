# packagecloud-openapi

An unofficial OpenAPI 3.1 spec for the [packagecloud.io](https://packagecloud.io)
HTTP API, derived from the public [API documentation page](https://packagecloud.io/docs/api).

packagecloud does not publish a machine-readable spec. This repo generates one
by parsing the docs page into markdown, then lifting the markdown into an
OpenAPI document suitable for client codegen.

## Layout

```
api-docs/
  packagecloud-api.html   Cached raw HTML from https://packagecloud.io/docs/api
  packagecloud-api.md     Markdown conversion of the docs page
  schema-overrides.yaml   Empirical corrections applied on top of the generated spec
openapi.yaml              Generated OpenAPI 3.1 spec
scripts/
  fetch_api_docs.py       Download the docs page → api-docs/packagecloud-api.md
  build_openapi.py        Build openapi.yaml from the markdown + overrides
```

## Regenerating the spec

Both scripts are [uv](https://docs.astral.sh/uv/) single-file scripts with
inline dependency declarations — no separate install step.

```sh
# 1. Fetch and convert the docs page. Uses api-docs/packagecloud-api.html as a
#    cache; pass --refresh to force a re-download.
./scripts/fetch_api_docs.py

# 2. Build the OpenAPI spec.
./scripts/build_openapi.py
```

Run both from the repo root so the default relative paths resolve.

## Why overrides?

The generator infers schemas and response types from the docs, but the docs
are occasionally incomplete or wrong compared to the live API (missing
fields, wrong nullability, structurally incorrect wire formats).
`api-docs/schema-overrides.yaml` captures these corrections — see the
comments at the top of that file for the schema.
