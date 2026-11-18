# Knowledge Base Roadmap

**Status:** Exploratory; not a compiler requirement

The compiler establishes a canonical, machine-readable representation of the knowledge base. This
roadmap records possible downstream capabilities. It does not commit the project to a specific
search engine, hosting provider, language model, or AI protocol.

## Current foundation

- Keep open, human-readable Markdown in Git as the canonical knowledge source.
- Build the human-facing documentation site with ProperDocs and publish it through the existing
  GitHub Pages workflow.
- Validate structured metadata and generate versioned document and section representations as
  described in [Compiler Requirements](requirements.md), [Compiler Design](design.md), and
  [Compiler Implementation](implementation.md).
- Preserve the GitHub contribution and review workflow.

## Possible downstream capabilities

These capabilities may consume compiler artifacts. They are separate from the compiler and require
their own requirements and design before implementation:

- Static full-text search over documents and sections.
- A hosted or locally run search API.
- An optional Model Context Protocol (MCP) endpoint for search, navigation, and retrieval.
- Instructions for connecting common MCP-compatible clients.
- Rate limiting and other controls for public search or MCP access.
- Precomputed summaries and FAQ-style content where they improve discovery.
- Semantic or vector search and a richer knowledge graph.

An MCP server, if adopted, is one possible librarian interface. It does not define the knowledge
model. Users must remain free to use different language models and interfaces. Summaries and indexes
are derived data and must not replace canonical Markdown.

## Evaluation principles

Evaluate downstream tools independently from the knowledge model. Consider:

- Compatibility with ordinary Markdown and generated schema-versioned artifacts.
- Preservation of stable document and section identities and relationships.
- Interoperability with independent clients and services.
- Extensibility, accessibility, security, and maintenance requirements.
- Contributor experience and operational cost.

StrictDoc may inform structured traceability design, but the knowledge base is not a
requirements-management system and does not require StrictDoc's native format. Documentation
generators and integration plugins may render or consume the canonical model, but must not own it.

## Suggested delivery order

1. Complete the compiler schema, validation, and generated document/section artifacts.
2. Establish static search from compiled artifacts.
3. Evaluate search APIs and MCP as optional consumers of the same artifacts.
4. Add summaries, question-oriented content, or semantic retrieval only when user needs justify
   them.
