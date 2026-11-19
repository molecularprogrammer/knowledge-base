# Compiler Implementation

**Status:** Proposed

**Allocates:** [Compiler Requirements](requirements.md)

**Implements:** [Compiler Design](design.md)

This document specifies the source schema, compiler behavior, ProperDocs hook contract, output
format, migration, and verification plan. These choices are proposed implementation details; they do
not change the architecture or the requirements.

## Source schema

**Schema version:** `1.0.0`

Markdown remains the authoritative knowledge source. YAML front matter carries document metadata.
generators and independent language-model-based tools consume compiled representations; they do not
define this schema.

The terms **MUST**, **MUST NOT**, **SHOULD**, and **MAY** express requirements at the strength
stated.

### Source document format

A knowledge document is a UTF-8 Markdown file with one YAML front matter block at the start of the
file, followed by its Markdown body:

```markdown
---
schema_version: "1.0.0"
id: mpkb:topic:dna-strand-displacement
type: article
title: DNA strand displacement
description: An overview of strand displacement reactions and their use in molecular programming.
topics:
  - nucleic-acids
keywords:
  - toehold
  - strand exchange
status: published
relationships: []
sources:
  - id: source:example-paper-2024
    url: https://example.org/paper
    title: Example paper
    published: 2024-01-15
    accessed: 2025-01-15
---

# DNA strand displacement {#mpkb:section:dna-strand-displacement}

Content with a [citation](https://example.org/paper).

## Toehold-mediated displacement {#mpkb:section:toehold-mediated-displacement}

Section content.
```

The example source is illustrative, not a project citation. The example topic must be present in the
configured topic vocabulary. Existing files without front matter or explicit heading IDs are legacy
content. Migration procedures are in [Section 6](#6-legacy-content-migration). A compiler MUST NOT
silently invent stable IDs from filenames or heading text.

### Identifier model

All identifiers are case-sensitive, stable across edits, and globally unique across document,
section, and source records. An identifier MUST match:

```text
^[a-z][a-z0-9-]*(:[a-z][a-z0-9-]*)+$
```

Identifiers SHOULD use a readable namespace and MUST NOT encode mutable titles, file paths, or
heading text. Once published, an identifier MUST NOT be reassigned to a different entity. If an
entity is removed, its identifier MUST NOT be reused.

- A document ID identifies the document independent of its path.
- A section ID identifies one heading and its section body independent of heading text and path.
- A source ID identifies one provenance record within the knowledge base.

### Document metadata

The top-level YAML value MUST be a mapping. The following fields are defined:

| Field | Required | Type and constraints | Meaning |
| --- | --- | --- | --- |
| `schema_version` | Yes | String; supported semantic version | Version of this source metadata contract. |
| `id` | Yes | Identifier | Stable, globally unique document ID. |
| `type` | Yes | One value from the document type vocabulary | Broad content kind. |
| `title` | Yes | Non-empty string | Human-readable document title. |
| `description` | Yes | Non-empty string | Concise description for discovery and indexing. |
| `topics` | Yes | List of topic slugs; may be empty | Controlled conceptual classifications. |
| `keywords` | Yes | List of non-empty strings; may be empty | Additional search terms, not classifications. |
| `status` | Yes | One value from the lifecycle vocabulary | Current publication/review state. |
| `relationships` | Yes | List of relationship records; may be empty | Typed links to other documents or sections. |
| `sources` | Yes | List of source records; may be empty | Provenance for the document. |
| `authors` | No | List of non-empty strings | Contributor names or stable contributor identifiers. |
| `parent` | No | Target reference | Parent document for navigational hierarchy. |
| `reviewed` | No | ISO 8601 date (`YYYY-MM-DD`) | Date of the most recent substantive review. |
| `valid_from` | No | ISO 8601 date | Start of the period in which the content is intended to be valid. |
| `valid_until` | No | ISO 8601 date | End of the period in which the content is intended to be valid. |

Unknown fields MUST produce a validation error in schema version `1.0.0`; extensions require a
schema revision. Duplicate list values MUST be rejected where the field represents a set (`topics`,
`keywords`, `authors`).

#### Document type vocabulary

The initial values are `article`, `index`, `tutorial`, `reference`, `news`, `glossary`, and
`dataset`. A type describes the content, not its folder or rendering behavior. Adding or removing a
value requires a schema change.

#### Topic vocabulary

Topic values are lowercase slugs matching `^[a-z][a-z0-9-]*$`. The controlled topic vocabulary is
maintained by the knowledge-base maintainers. A compiler MUST reject unknown topics in strict mode;
the vocabulary itself is data supplied to the compiler, not a hard-coded list in this document.
Keywords are free text and MUST NOT be treated as equivalent to topics.

#### Lifecycle vocabulary

The initial status values are:

- `draft`: work in progress; not presented as reviewed knowledge.
- `in-review`: awaiting review.
- `published`: available as current knowledge.
- `deprecated`: retained for context but replaced or no longer recommended.
- `archived`: retained for historical reference and not maintained.

`reviewed`, `valid_from`, and `valid_until` are calendar dates, not timestamps. If both validity
dates are present, `valid_from` MUST be earlier than or equal to `valid_until`.

### Section model

Every Markdown heading in a conforming document MUST have an explicit stable ID using the
attribute-list syntax `{#<identifier>}` on the same line as the heading. Heading IDs share the
global identifier namespace with document and source IDs. A heading ID MUST be unique in the
knowledge base.

For each heading, the compiler MUST preserve its ID, displayed title, heading level, document ID,
ordered ancestor heading IDs, source order, and associated Markdown body. Heading levels MUST NOT
skip a level within a document (for example, `#` followed directly by `###`). The document title in
front matter is distinct from a body heading; a body heading ID identifies a section, not the
document.

Content before the first heading is the document preamble. It belongs to the document and MUST be
preserved; it is not assigned a section ID unless a later schema revision explicitly defines one.
Sections are addressable by their stable IDs and MUST be retrievable independently. Heading text
changes MUST NOT change section identity.

### References and relationships

A target reference is either a document ID or a section ID. References MUST use canonical IDs,
never only filenames, relative paths, or heading text. Every internal target MUST resolve to exactly
one document or section.

Each `relationships` item MUST be a mapping with exactly these fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `type` | Relationship vocabulary value | Directed semantic relation from the containing document to its target. |
| `target` | Target reference | Stable document or section ID. |

The initial relationship vocabulary is:

| Type | Semantics |
| --- | --- |
| `references` | The source cites or points to the target. |
| `related` | The source and target concern related subjects; no dependency is implied. |
| `depends_on` | The source relies on the target for context or operation. |
| `supersedes` | The source replaces the target as the current resource. |
| `supports` | The source provides evidence or rationale for the target. |
| `contradicts` | The source presents a claim or information that conflicts with the target. |

Relationships are directed. A compiler MUST NOT infer a reverse relationship unless its semantics
explicitly require one. Parent-child document hierarchy is represented by the optional `parent`
field, not duplicated as a relationship. A parent MUST resolve to a document ID; cycles in parent
hierarchy are invalid. New relationship types require a schema revision that defines their
direction and semantics.

### Provenance records

Each `sources` item MUST be a mapping with a unique `id` and at least one locator (`url` or
`citation`). Supported fields are:

| Field | Required | Type and constraints | Meaning |
| --- | --- | --- | --- |
| `id` | Yes | Identifier, globally unique | Stable source-record ID. |
| `url` | Conditional | Absolute HTTP(S) URL | Online location of the source. |
| `citation` | Conditional | Non-empty string | Bibliographic citation or other locator. |
| `title` | No | Non-empty string | Source title. |
| `authors` | No | List of non-empty strings | Source authors. |
| `published` | No | ISO 8601 date | Publication date, when known. |
| `accessed` | No | ISO 8601 date | Date the online source was accessed. |
| `supports` | No | List of target references | Documents or sections this source supports. |

If a source ID appears in more than one document, its fields MUST be identical; otherwise the
compiler reports a conflicting definition. Source records identify provenance, but do not by
themselves assert that every statement in a document is supported by that source. Assertion-level
annotations are outside this initial schema version.

### Validation and canonical source rules

A conforming source MUST:

1. Parse as UTF-8 Markdown with one valid YAML front matter mapping.
2. Satisfy all required-field, type, vocabulary, date, and identifier rules in this schema.
3. Have unique document, section, and source IDs across the knowledge base.
4. Have explicit IDs on all headings and a valid heading hierarchy.
5. Resolve every internal target, parent, and source `supports` reference.
6. Have no parent cycles or conflicting source definitions.

Markdown is canonical. Rendered HTML, indexes, JSON representations, and generated summaries are
derived artifacts. A build MUST fail on errors that make the structured model invalid and MUST
identify the source file and field, ID, or heading involved. It MUST preserve the metadata and
structure defined here in its outputs.

### Schema versioning and compatibility

`schema_version` uses `MAJOR.MINOR.PATCH` semantic version syntax:

- A **major** change may remove or redefine fields, values, or validation behavior and requires an
  explicit migration.
- A **minor** change may add backward-compatible optional fields or vocabulary values.
- A **patch** change clarifies the specification without changing valid source documents or output
  meaning.

The compiler MUST reject an unsupported major version. It MAY accept a newer minor version only
when it can preserve unknown optional fields without loss; otherwise it MUST fail with an actionable
diagnostic. The compiler MUST NOT rewrite canonical source files. Schema migrations are explicit
source changes reviewed and committed with the content; they MUST preserve stable IDs and
relationships. Generated output formats have their own version, independent of this source schema
version.

## Compilation behavior

### Inputs and dependencies

The initial implementation targets the repository's verified ProperDocs environment: Python 3.12,
ProperDocs 1.6.7, PyYAML 6.0.3 for front matter parsing, and Python-Markdown 3.11.1 for Markdown
structure parsing. These are the versions observed in the current container; the build image is
tagged `latest`, so CI must verify the versions rather than assume that tag is immutable.

The compiler receives:

1. Markdown files under the configured `docs_dir`.
2. The source schema version declared in each document's front matter.
3. A maintained topic vocabulary supplied as repository data.
4. An output staging directory and an explicit validation mode.

The compiler walks the configured documentation root, including Markdown files that ProperDocs may
exclude from rendering. It discovers files deterministically, does not follow symlinks outside the
root, and does not read generated site files.

### Compilation stages

The compiler runs these stages in order:

1. **Discover:** collect Markdown files under the configured root in stable path order.
2. **Parse:** read UTF-8 source, separate front matter from body, parse YAML, and extract headings,
   explicit IDs, and Markdown ranges for the document preamble and sections.
3. **Validate local records:** check metadata shape, schema version, field types, identifiers,
   allowed values, dates, duplicate fields/keys, and per-document heading order and hierarchy.
4. **Build the model:** create document, section, source, and relationship records while retaining
   source locations for diagnostics.
5. **Validate global invariants:** check ID uniqueness, target resolution, parent cycles, and shared
   source consistency.
6. **Serialize:** if there are no errors, write the complete, deterministic JSON artifact set to a
   staging directory. Do not publish partial outputs on failure.

Parsing and validation do not modify source files. Consumers MUST treat outputs from a failed
compilation as invalid.

### Diagnostics

Each diagnostic includes a severity, stable code, message, source file, and—when available—line,
field path, heading, or affected ID. Messages SHOULD state the corrective action. Diagnostics are
deterministically ordered by file, source position, and code.

- **Error:** compilation cannot produce a valid model; fail the ProperDocs build and do not publish
  staged outputs.
- **Warning:** content may be valid but needs attention; exit success unless strict warning policy is
  enabled.
- **Informational:** migration or summary information; does not affect build status.

Malformed front matter, missing required fields, duplicate IDs, unknown required vocabulary values,
unresolved references, and invalid heading hierarchy are errors. Compilation performs no network
requests to validate external URLs.

## ProperDocs hook integration

ProperDocs hook scripts are Python files listed in `properdocs.yml`; paths are relative to that
configuration file. A hook script defines event-handler functions without `self`. The initial
configuration is:

```yaml
hooks:
  - compiler/properdocs_hook.py
```

The hook module shall implement the global `on_files` and `on_post_build` events. The abbreviated
example below omits error diagnostics and deterministic staging setup:

```python
def on_files(files, config, **kwargs):
    stage = compile_and_stage(files, config)
    _staged_paths[id(config)] = stage
    return files

def on_post_build(config, **kwargs):
    publish_staged_artifacts(_staged_paths.pop(id(config)))
```

`on_files` runs once per build after ProperDocs collects the documentation files. The hook validates
the entire configured Markdown root, including files omitted from the rendered file collection. It
returns the unchanged `files` collection because it does not modify it. The compiler writes the
artifact set to a unique staging directory under `site_dir` only after validation succeeds.

In ProperDocs 1.6.7, `on_post_build` runs after the site files are written, but before ProperDocs
performs its final strict-warning check. It publishes the complete staged artifact set and updates the
publication marker atomically. A later build failure prevents CI from uploading or deploying the
site, even though the local `site_dir` may contain the newly generated files. If validation or site
generation fails before `on_post_build`, the staged files are not published. ProperDocs may clean
`site_dir` at the start of the next build; preservation of a prior local build directory is not
guaranteed. The output layout and publication procedure are defined in
[Section 4](#4-compiled-output-format).

The hook uses ProperDocs' plugin/build error mechanism for failures and ProperDocs logging for
warnings. It does not duplicate compiler validation rules. ProperDocs hook modules are not reloaded
for each `properdocs serve` rebuild; the hook must therefore avoid stale module-level per-build state.
Each build uses a unique staging directory. The next `on_files` invocation removes abandoned staging
directories from prior failed builds before compiling. These behaviors must be tested in the
repository's ProperDocs environment.

ProperDocs hooks use the same event-handler names and return contracts as plugins, but are local
scripts rather than installed plugin packages. See the [ProperDocs hook configuration](https://properdocs.org/user-guide/configuration/#hooks)
and [plugin event documentation](https://properdocs.org/dev-guide/plugins/#events).

## Compiled output format

Output format version `1.0.0` uses this layout:

```text
knowledge-base/
  current.json
  1.0.0/<sha256-of-artifact-set>/
    documents.json
    sections.json
    relationships.json
    sources.json
    manifest.json
```

The JSON files are UTF-8 with stable-key ordering and deterministic record ordering. The artifact
set digest is calculated from the serialized `documents.json`, `sections.json`, `relationships.json`,
and `sources.json` files, excluding `manifest.json` and `current.json`. The manifest records the
format version, source schema versions, compiler version, artifact filenames, and digest.
`current.json` records the format version, digest, and path to the immutable artifact-set directory.

ProperDocs cleans `site_dir` before it invokes `on_files`. The compiler then writes artifacts to a
unique staging directory under `site_dir`; the clean does not run again during that build. In
`on_post_build`, the hook moves the complete artifact set to its digest-named directory and atomically
replaces `current.json`. If that directory already exists, the hook verifies its manifest and
discards the duplicate staging directory. A failed compilation or site generation does not reach
`on_post_build`. A strict-warning failure occurs after `on_post_build`, so CI must upload and deploy
only when `properdocs build` exits successfully. Consumers first read `current.json`, then read only
files from its referenced immutable artifact set.

compiler. The compiler produces structured data, not a search index or service, generated summary,
API, or AI protocol endpoint.
Generated artifacts are never committed as canonical source.

## Implementation decisions to resolve

Resolve these before declaring the output format stable:

- Where and how the controlled topic vocabulary is maintained and reviewed.
- Exact artifact filenames, publication directory, and output-format version if they change from
  Section 4.
- Whether document type and lifecycle vocabularies need additional values before migration.
- How compiler and artifact-format versions are exposed in repository build tooling.
- Whether the ProperDocs version in CI matches the documented hook API and behavior under both
  `build` and `serve`.

## Legacy content migration

The current knowledge documents do not all have schema front matter or explicit heading IDs.
Migration is a prerequisite to strict compilation of the complete configured source root.

The compiler may provide a **migration report** mode that lists missing metadata and proposed IDs,
but proposed IDs are suggestions only. A maintainer assigns and commits stable IDs explicitly.
Generated IDs MUST NOT be written into source automatically because path- or heading-derived IDs can
change when content moves or is renamed.

Rollout proceeds in stages:

1. Review and approve the schema, compiler contract, and topic vocabulary.
2. Add schema-compliant metadata and stable heading IDs to existing documents, preserving current
   content and links.
3. Run validation in reporting mode during migration and resolve every error.
4. Enable strict validation in local build tasks and CI.
5. Publish machine-readable artifacts with the site for independent consumers.

There is no permanent silent fallback for legacy documents. Once strict mode is enabled, every
knowledge document in the configured source root must conform.

## Test plan

### Unit tests

Use focused fixture documents to verify:

- Valid front matter and Markdown parse into the expected document and section records.
- Missing or malformed front matter, duplicate YAML keys, wrong field types, unknown fields and
  values, invalid dates, and unsupported schema versions produce source-specific errors.
- Invalid identifiers, duplicate document/section/source IDs, missing heading IDs, duplicate heading
  IDs, and skipped heading levels are rejected.
- Section records preserve IDs after heading renames and retain title, content, level, ordering, and
  ancestor hierarchy.
- Internal document/section targets, parent references, source references, and topic values resolve
  correctly; missing targets, conflicting source definitions, and parent cycles fail.
- Compilation performs no network requests to validate external URLs.

### Compiler integration tests

Use small fixture roots to verify:

- Compilation discovers files deterministically and does not follow symlinks outside the configured
  root.
- A valid fixture produces the documented JSON records and manifest.
- Repeated runs with identical inputs and compiler versions produce byte-identical artifacts.
- A failed compilation leaves a previously valid published artifact set unchanged and publishes no
  partial output.
- The generated JSON can be read without importing ProperDocs or a language-model framework.

### ProperDocs hook tests

Run the hook in the same ProperDocs environment used by local development and CI to verify:

- Hook configuration loads and `on_files` receives the complete configured source collection.
- A valid build publishes all artifacts to the documented `site_dir` location.
- Invalid metadata produces a source-specific build failure and does not publish new artifacts.
- A later ProperDocs failure does not publish staged artifacts.
- A strict-mode abort after `on_post_build` does not upload or deploy the generated artifacts.
- `properdocs serve` rebuilds do not reuse stale compiler model or diagnostics from a previous build.
- Strict-mode warning behavior matches the project policy.

### Repository acceptance checks

Before strict CI enforcement:

- Every Markdown knowledge document in the configured source root conforms to schema version `1.0.0`.
- All IDs are unique and all internal references resolve.
- The ProperDocs site and compiled artifacts build successfully in CI from a clean checkout.
- The output directory contains only generated artifacts expected by the output manifest.
- Requirements, design, and implementation documents agree on scope, allocation, and status.

Tests SHOULD include an integration fixture with nested sections, relationships, provenance, and a
parent-child document hierarchy.