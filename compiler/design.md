# Knowledge Base Compiler Design

**Status:** Proposed

**Scope:** Compile canonical knowledge-base Markdown into validated, structured representations.

## 1. Purpose

The compiler gives the knowledge base a consistent information model and detects broken structure
before publication. It reads Markdown and YAML metadata, validates them against the
[knowledge schema](knowledge-schema.md), resolves references across the repository, and emits
deterministic machine-readable artifacts.

Markdown in Git remains authoritative. The compiler does not own knowledge, render the website, run a
search service, or implement an AI protocol. ProperDocs currently builds the human-facing site.
Search, APIs, and MCP may consume compiler outputs independently.

## 2. Requirements

The compiler MUST:

- Validate front matter, identifiers, enumerated values, dates, heading IDs, heading hierarchy, and
  metadata field types against the versioned schema.
- Detect duplicate IDs, unresolved internal references, invalid parent hierarchies, and conflicting
  definitions of shared source IDs.
- Preserve document metadata, document preambles, section content, heading order and levels,
  ancestor relationships, provenance, and typed relationships.
- Produce deterministic, versioned JSON representations from the same inputs.
- Report actionable diagnostics that identify the file and relevant field, heading, or identifier.
- Fail the build when structured data is invalid; never silently drop invalid or unsupported data.
- Leave canonical Markdown unchanged.

The compiler SHOULD run locally and in CI using the same validation rules. Its core MUST NOT depend
on ProperDocs, MkDocs, StrictDoc, MCP, a search engine, or a language model.

## 3. Boundaries and interactions

```text
Canonical Markdown + schema + topic vocabulary
                    |
                    v
               Compiler
              /        \
             v          v
  ProperDocs build   JSON artifacts
                         |
                 search / API / MCP
```

- **Knowledge authors** edit Markdown and front matter in Git.
- **The compiler** parses source, validates the global model, and writes generated artifacts.
- **ProperDocs** renders human-facing documentation from Markdown. It does not define or amend the
  canonical metadata model.
- **Artifact consumers** read documented JSON outputs. Search, API, and MCP implementations are
  replaceable consumers and are outside this compiler's runtime boundary.
- **CI** runs the compiler before site publication and prevents publication when compilation fails.

The compiler owns the contract between source files and compiled representations. Interfaces among
ProperDocs, artifact consumers, and hosting services remain owned by their respective designs.

## 4. Inputs and outputs

### 4.1 Inputs

The compiler receives:

1. A root directory containing Markdown knowledge documents.
2. The source schema version declared in each document's front matter.
3. A maintained topic vocabulary supplied as repository data.
4. An output directory and an explicit validation mode.

The initial implementation uses the repository's `docs/` directory as the input set. It excludes
non-Markdown files and site-generated files. It MUST discover documents deterministically and MUST
not follow symlinks outside the configured root.

### 4.2 Outputs

The initial compiled format is versioned JSON. It MUST include logical representations for:

- **Documents:** IDs, metadata, source paths for diagnostics/navigation, and preamble content.
- **Sections:** IDs, owning document IDs, titles, heading levels, ordered ancestor IDs, source order,
  and section Markdown content.
- **Relationships:** typed source and target IDs, including parent hierarchy and provenance links.
- **Sources:** normalized provenance records and their source-document associations.
- **Manifest:** source schema version(s), output format version, compiler version, and inventory of
  generated artifacts.

One JSON file per logical collection is a suitable initial layout. Exact filenames are an output
format decision and MUST be recorded with the format version. Search indexes and summaries are
later derived artifacts; they MUST NOT become canonical or be prerequisites for validating source.

All JSON output MUST be UTF-8, stable-key ordered where applicable, and deterministic for identical
inputs and compiler versions. Output paths MUST be documented. Generated files MUST be written only
to the configured output directory.

## 5. Compilation flow

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
6. **Serialize:** if there are no errors, write the complete, deterministic JSON artifact set and
   manifest. Do not leave a partially updated artifact set on failure.

Parsing and validation do not modify source files. Consumers MUST treat outputs from a failed
compilation as invalid; the compiler SHOULD stage files and replace the previous output set only
after successful compilation.

## 6. Diagnostics and exit behavior

Each diagnostic includes a severity, stable code, message, source file, and—when available—line,
field path, heading, or affected ID. Messages SHOULD state the corrective action. Diagnostics are
deterministically ordered by file, source position, and code.

- **Error:** compilation cannot produce a valid model; exit non-zero and do not publish new outputs.
- **Warning:** content may be valid but needs attention; exit success unless strict warning policy is
  enabled.
- **Informational:** migration or summary information; does not affect exit status.

Malformed front matter, missing required fields, duplicate IDs, unknown required vocabulary values,
unresolved references, and invalid heading hierarchy are errors. Link checks to external URLs are
optional warnings only; network access is not required for a successful compilation.

## 7. Legacy content migration

The current repository contains Markdown files without schema front matter or explicit heading IDs.
Migration is therefore a prerequisite to enforcing strict compilation over all `docs/` content.

The compiler MAY provide a **migration report** mode that lists missing metadata and proposed IDs,
but proposed IDs are suggestions only. A maintainer assigns and commits stable IDs explicitly.
Generated IDs MUST NOT be written into source automatically because path- or heading-derived IDs can
change when content moves or is renamed.

Rollout proceeds in stages:

1. Define and review the schema and compiler contract.
2. Add schema-compliant metadata and stable heading IDs to existing documents, preserving current
   content and links.
3. Run validation in reporting mode during migration and resolve every error.
4. Enable strict validation in local build tasks and CI.
5. Generate and publish machine-readable artifacts with the site or as separately consumable static
   files.

There is no permanent silent fallback for legacy documents. Once strict mode is enabled, every
knowledge document in the configured root must conform.

## 8. Testing and acceptance

The compiler is acceptable for strict CI use when tests demonstrate that:

- Valid source compiles to the documented JSON format, and repeated runs produce byte-identical
  artifacts.
- Missing or malformed front matter, wrong types, unknown fields/values, invalid dates, and
  unsupported schema versions fail with source-specific diagnostics.
- Duplicate document, section, and source IDs are detected across files.
- Heading IDs remain unchanged when heading titles change; missing IDs and skipped heading levels
  fail validation.
- Document, section, parent, relationship, and provenance targets resolve correctly; missing
  targets and parent cycles fail validation.
- Section records preserve document ID, heading hierarchy, order, title, content, and source data.
- A failure does not replace a previously valid artifact set with partial outputs.
- Compiled JSON can be consumed without loading ProperDocs or an MCP implementation.
- The site and compiler builds both fail in CI when their required validation fails.

Tests SHOULD use small fixture repositories that cover one invariant at a time, plus an integration
fixture with nested sections, relationships, and provenance.

## 9. Delivery phases

1. **Schema and model:** finalize the source contract and topic vocabulary; record open vocabulary
   ownership decisions.
2. **Minimum compiler:** implement parsing, schema validation, stable section extraction, global
   reference checks, diagnostics, and deterministic JSON generation.
3. **Repository migration:** add explicit metadata and IDs to existing knowledge documents and
   enable strict CI validation.
4. **Consumer integration:** publish generated artifacts and connect static search or other
   consumers as separate components.
5. **Optional extensions:** evaluate summaries, semantic search, API, and MCP independently. These
   must consume the canonical compiled model and must not change its ownership.

## 10. Open decisions

- Where and how the controlled topic vocabulary is maintained and reviewed.
- The compiler implementation language and Markdown/YAML parser, chosen to fit the repository's
  build environment and parser behavior.
- Exact artifact filenames and output location for the first output-format version.
- Whether document type and lifecycle vocabularies need additional values before migration.
- How compiler and artifact-format versions are exposed in the repository's build tooling.

Resolve these decisions before declaring the output format stable. Do not make a documentation
generator, StrictDoc, or MCP a canonical dependency while doing so.