# Molecular Programmer Knowledge Base Schema

**Schema version:** `1.0.0`

**Status:** Proposed

This document defines the canonical information model for knowledge-base Markdown. Markdown files
remain the authoritative source. YAML front matter carries document metadata, and explicit heading
IDs identify sections. Documentation generators, search services, and AI protocols consume compiled
representations; they do not define this schema.

The terms **MUST**, **MUST NOT**, **SHOULD**, and **MAY** express requirements at the strength stated.

## 1. Source document format

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
relationships:
  - type: references
    target: mpkb:topic:nucleic-acid-hybridization
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

The example URLs and source are illustrative, not project citations. Existing files without
front matter or explicit heading IDs are legacy content; the compiler design defines how to migrate
them. A compiler MUST NOT silently invent stable IDs from filenames or heading text.

## 2. Identifier model

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

## 3. Document metadata

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

### 3.1 Document type vocabulary

The initial values are `article`, `index`, `tutorial`, `reference`, `news`, `glossary`, and
`dataset`. A type describes the content, not its folder or rendering behavior. Adding or removing a
value requires a schema change.

### 3.2 Topic vocabulary

Topic values are lowercase slugs matching `^[a-z][a-z0-9-]*$`. The controlled topic vocabulary is
maintained by the knowledge-base maintainers. A compiler MUST reject unknown topics in strict mode;
the vocabulary itself is data supplied to the compiler, not a hard-coded list in this document.
Keywords are free text and MUST NOT be treated as equivalent to topics.

### 3.3 Lifecycle vocabulary

The initial status values are:

- `draft`: work in progress; not presented as reviewed knowledge.
- `in-review`: awaiting review.
- `published`: available as current knowledge.
- `deprecated`: retained for context but replaced or no longer recommended.
- `archived`: retained for historical reference and not maintained.

`reviewed`, `valid_from`, and `valid_until` are calendar dates, not timestamps. If both validity
dates are present, `valid_from` MUST be earlier than or equal to `valid_until`.

## 4. Section model

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

## 5. References and relationships

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

## 6. Provenance records

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

## 7. Validation and canonical source rules

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

## 8. Versioning and compatibility

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