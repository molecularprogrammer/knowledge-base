Having reviewed the actual issue, I think it is already quite well conceived. I would not replace its architecture or make StrictDoc a dependency. I would make several targeted additions that turn the existing proposal into a more precise technical specification.

The biggest omission is that the issue specifies document metadata and document/section representations, but doesn't yet define the actual information model that makes those representations reliable.

Here are the changes I recommend.

## 1. Add an explicit section-level information model

The issue already calls for stable document IDs and machine-readable document/section representations (lines 173–183). I would expand this to require stable section identifiers and hierarchy.

Add under Machine-readable knowledge:

Writing

### Document and section model

- Every document must have a stable, globally unique identifier.
- Every section must have a stable identifier within the knowledge base.
- Section identifiers should be independent of heading text so that renaming a heading does not break references.
- The generated representation must preserve document hierarchy, heading levels, section ordering, and parent-child relationships.
- Sections should be independently addressable and retrievable.
- Each section representation should include its document ID, section ID, title, heading hierarchy, content, and relevant metadata.
- References to documents and sections must resolve to canonical identifiers rather than relying exclusively on filenames or heading text.
- The build process must detect duplicate identifiers, broken references, and invalid hierarchy.

Why: Section-level retrieval is essential for both conventional search and LLM retrieval. A document-level index alone is insufficient.

## 2. Define the metadata schema more rigorously

Currently, the issue lists the metadata fields but doesn't specify their semantics, types, or validation rules.

Add:

Writing

### Metadata schema requirements

Define and document a versioned metadata schema.

The schema should specify:

- Required and optional fields.
- Field types and allowed values.
- Identifier format and uniqueness requirements.
- Controlled vocabularies where appropriate.
- Relationship types and their semantics.
- Rules for references to other documents and sections.
- Defaults and backward-compatibility rules.
- Schema versioning and migration procedures.

Metadata should distinguish between:

- Descriptive metadata (title, description, topics, keywords).
- Structural metadata (document type, parent, sections).
- Relational metadata (references, dependencies, related documents).
- Provenance metadata (sources, authorship, attribution).
- Lifecycle metadata (status, review date, validity).

I would also explicitly distinguish `topics` from `keywords`: topics represent conceptual classification; keywords provide additional search terms.

## 3. Add explicit relationships and traceability

This is where StrictDoc offers some particularly valuable ideas.

Your existing issue mentions relationships, but doesn't specify what they mean.

Add:

Writing

### Knowledge relationships

Support explicit, typed relationships between documents and sections.

Potential relationship types include:

- references: one document cites another.
- related: documents concern related subjects.
- parent/child: hierarchical relationships.
- depends\_on: one document depends on another.
- supersedes/superseded\_by: documents representing successive versions.
- supports: a source or document supports an assertion.
- contradicts: documents contain conflicting assertions.

Relationships should:

- Have explicitly defined semantics.
- Reference stable document or section identifiers.
- Be validated during the build.
- Be represented in machine-readable output.
- Be navigable through the generated documentation and search interface where appropriate.

The relationship model should be extensible without requiring changes to the underlying document format.

I would not necessarily implement every relationship type initially. Define the model first, implement the most useful subset, and expand as needed.

## 4. Make provenance and citations first-class

This is particularly important when an LLM consumes the knowledge base.

Add:

Writing

### Sources and provenance

Where appropriate, documents and individual assertions should identify their sources.

Support:

- External source URLs and bibliographic references.
- References to other knowledge-base documents and sections.
- Attribution and authorship.
- Source descriptions and publication dates where available.
- Distinguishing sourced information from interpretation, opinion, and inference.

Generated machine-readable representations must preserve source references so that consuming applications can provide citations and trace information back to the original material.

This will make it possible for an MCP client to return answers with traceable sources instead of simply returning plausible-looking passages.

## 5. Explicitly specify canonical Markdown and generated representations

This is where I would incorporate the most important lesson from comparing StrictDoc and ProperDocs.

Add:

Writing

### Canonical source and generated representations

- Markdown files in GitHub remain the canonical source of knowledge.
- YAML front matter provides structured document metadata.
- Markdown remains ordinary, human-readable Markdown without requiring contributors to learn a proprietary document format.
- The metadata schema and document conventions must be independent of MkDocs, Material for MkDocs, MCP, or any particular plugin.
- Machine-readable representations are generated artifacts, not alternative sources of truth.
- Generated representations should use a documented, versioned format.
- The generated format should support JSON serialization and preserve document and section structure, metadata, identifiers, and relationships.
- The build process must not silently discard information that cannot be represented in the human-facing documentation.

I would specifically mention that StrictDoc's structured document model is an architectural reference worth evaluating, not a required dependency.

## 6. Add validation and consistency requirements

The existing issue already requires metadata validation in CI. I would expand that substantially.

Writing

### Knowledge-base validation

The CI pipeline should validate:

- Metadata against the documented schema.
- Uniqueness and validity of document and section identifiers.
- Internal document and section references.
- Relationship targets and relationship semantics.
- Required metadata fields.
- Heading hierarchy and section structure.
- Broken external and internal links where practical.
- Duplicate or conflicting identifiers.
- Generated representation consistency.

Validation errors should identify the affected file and field or section and provide actionable diagnostics.

The build should fail on structural errors that could compromise machine-readable knowledge.

This prevents the knowledge base from gradually becoming inconsistent as contributions accumulate.

## 7. Specify the generated machine-readable artifacts

The issue currently says to generate indexes and representations, but doesn't define what consumers can actually expect.

I would add:

Writing

### Generated artifacts

The build should produce independently consumable artifacts, including:

- `documents.json`: document metadata and identifiers.
- `sections.json`: section metadata, content, hierarchy, and identifiers.
- `relationships.json`: typed relationships between documents and sections.
- `sources.json`: source and provenance information, where applicable.
- `search-index.json`: searchable document and section content.
- `summaries.json`: precomputed summaries, where useful.
- `manifest.json`: artifact schema version, build information, and document inventory.

Artifacts should be available independently of the MCP server and search API.

The generated format should be documented and usable by external tools without requiring MkDocs or MCP.

The filenames are suggestions, not necessarily mandatory. The important thing is to define the logical outputs and their schemas.

## 8. Clarify the search architecture

The issue currently mentions static search and a search API without defining what search should support.

Add:

Writing

### Search and retrieval

The search system should support:

- Full-text search across documents and sections.
- Retrieval of individual sections.
- Filtering by document type, topic, keyword, and status.
- Lookup by stable document and section identifiers.
- Navigation through explicit relationships.
- Retrieval of surrounding context, including parent sections and related documents.
- Returning source identifiers and canonical URLs with search results.

Search results should provide enough structural and provenance information for a language model to cite and contextualize retrieved information.

The search implementation should remain replaceable and independent of the canonical knowledge representation.

I would also consider hybrid retrieval (keyword plus semantic/vector search), but avoid making a particular vector database a requirement.

## 9. Improve the MCP specification

MCP should expose the underlying knowledge model rather than become the model itself.

Add:

Writing

### MCP interface requirements

The MCP server should expose capabilities for:

- Searching documents and sections.
- Retrieving complete documents.
- Retrieving individual sections.
- Looking up documents and sections by stable identifiers.
- Discovering document metadata.
- Exploring document relationships.
- Retrieving source and provenance information.

The MCP interface should expose structured results rather than returning only rendered Markdown or unstructured text.

MCP resources, tools, and their schemas should be documented and should map to the underlying knowledge model.

The knowledge base must remain fully usable without MCP.

This is an important distinction: an MCP server that only wraps a text search endpoint would leave much of the potential value unused.

## 10. Add tests and quality criteria

I would add an explicit acceptance criterion for end-to-end verification.

Writing

### Machine-readability acceptance criteria

- A document can be uniquely identified and retrieved by ID.
- A section can be uniquely identified and retrieved by ID.
- Renaming a heading does not invalidate its stable section identifier.
- Document and section hierarchy is preserved in generated representations.
- Relationships can be traversed in both directions where appropriate.
- Provenance and source references survive the build process.
- All generated representations conform to documented schemas.
- An external program can consume the generated artifacts without depending on MkDocs.
- Search results identify their source documents and sections.
- MCP clients can search, navigate, and retrieve structured knowledge.
- A change to a Markdown source automatically updates the generated artifacts.
- CI detects malformed metadata, duplicate IDs, and broken internal references.

## 11. Add a technology evaluation decision

I would add one small section to prevent the project from prematurely committing to a documentation tool.

Writing

### Documentation tooling evaluation

Evaluate documentation tooling independently from the canonical knowledge representation.

Candidate tools may include MkDocs/Material for MkDocs, ProperDocs, and StrictDoc.

Evaluation criteria should include:

- Compatibility with ordinary Markdown.
- Support for YAML front matter and custom metadata.
- Preservation of stable document and section identifiers.
- Ability to generate structured document and section representations.
- Extensibility of the build pipeline.
- Search capabilities.
- Contribution experience through GitHub.
- Long-term maintenance and ecosystem maturity.

StrictDoc's structured document model and traceability capabilities should be considered as architectural references. Adoption of its native document format is not required.

The selected documentation tool must not become the owner of the canonical knowledge model.

## What I would prioritize

I wouldn't implement all of this at once. Here's my suggested priority:

| Priority | Changes | Importance |
| --- | --- | --- |
| P0 | Canonical source and schema | Foundational |
| P0 | Stable section IDs | Essential for retrieval |
| P0 | Structured document/section model | Essential for machine readability |
| P0 | Validation and references | Data integrity |
| P1 | Typed relationships | Knowledge navigation |
| P1 | Provenance and citations | Trustworthiness |
| P1 | Generated artifacts | Interoperability |
| P1 | Structured search and MCP | Consumption |
| P2 | Semantic/vector search | Advanced retrieval |
| P2 | Precomputed summaries | Retrieval optimization |
| P2 | Richer knowledge graph | Advanced reasoning |

## Two things I would explicitly avoid

1. Don't turn the knowledge base into a requirements-management system.

StrictDoc is a useful source of architectural ideas, but your knowledge base is broader than engineering specifications. Don't require every article to conform to a requirements-oriented document model.

2. Don't make machine-generated summaries canonical.

Summaries should be derived artifacts. The original Markdown remains authoritative. Summaries should be regenerable and clearly distinguished from source content.

## My overall assessment

Your existing issue is already strong in its architectural direction. It correctly separates:

- Canonical knowledge.
- Documentation presentation.
- Machine-readable representations.
- Search and retrieval.
- MCP as an optional interface.

What it needs most is a formal knowledge model between Markdown and the generated interfaces.

That is the central improvement I would make.

The architectural principle I'd add to the issue

> The knowledge base should be a structured, interconnected, provenance-aware collection of human-readable documents. Machine-readable representations and interfaces must be generated from this canonical source without making the source dependent on any particular documentation generator, search engine, language model, or AI protocol.

I would make that principle explicit near the top of the issue's Solution section. It captures the long-term objective much better than simply describing the addition of an MCP server.

The recommendations above build on the existing issue rather than requiring a redesign.
