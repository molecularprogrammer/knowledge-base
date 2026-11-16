Problem:
-
Language models could enable users to more effectively discover, navigate, and use the knowledge base.

Providing a dedicated technical chat expert as a feature of the knowledge base would be expensive and would limit users to a particular model or interface. Instead, make the knowledge base easily consumable by language models, allowing users to bring a model of their choice.

Solution:
-
Keep Markdown in GitHub as the canonical source of the knowledge base, with explicitly defined machine-readable metadata for each document.

The build process should generate machine-readable representations of the knowledge base in addition to the human-facing static documentation. This may include document metadata, relationships, search indexes, and precomputed summaries.

Model Context Protocol (MCP) can then provide an optional standardized interface for language models to search, navigate, and retrieve information from the knowledge base. The MCP server acts as a "librarian" interface to the knowledge base, rather than being the underlying knowledge representation itself.

This keeps the knowledge base independent of any particular language model or AI protocol and allows other machine-readable or AI interfaces to be added in the future.

Proposed architecture:
-
GitHub repository
→ Markdown + structured metadata
→ MkDocs build
→ GitHub Pages (human-facing documentation)
→ machine-readable indexes and representations
→ Cloudflare-hosted search API and MCP endpoint
→ locally-hosted search API and MCP endpoint (more powerful than hosted opens for content developers)

Technology:
-
- MkDocs
- Material for MkDocs
- GitHub
- GitHub Pages
- GitHub Actions
- Cloudflare Workers for API/MCP hosting, if needed

MCP / AI integration:
-
MkDocs/MkDocs Material may provide some MCP/LLM functionality directly or through plugins. Potential options:
- Material theme native MCP/AI support
- douinc/mkdocs-mcp-plugin
- ejsinfuego/mkdocs-mcp
- mkdocs-mcp
- mkdocs-ask-ai

These should be evaluated based on whether they generate useful, stable machine-readable representations and whether they can consume the project's own metadata schema, rather than making the project's knowledge representation dependent on a particular plugin.

Machine-readable knowledge:
-
- Define an explicit YAML front matter schema
- Assign stable IDs to documents
- Include document type, title, description, topics, keywords, and relationships
- Include structured references and provenance
- Include review/status information where appropriate
- Validate metadata automatically in CI
- Generate a machine-readable document index
- Generate static/full-text search indexes
- Generate machine-readable representations of documents and sections
- Generate precomputed summaries where useful
- Preserve links and relationships between documents

Acceptance criteria:
-
- Static documentation
- GitHub-based contribution workflow
- Explicit and documented metadata schema
- Automated metadata validation
- Stable document IDs
- Machine-readable document index
- Machine-readable document/section representations
- Static search
- Search API
- MCP endpoint
- Instructions for connecting common MCP-compatible clients
- Rate limiting for public search/MCP access
- Precomputed summaries
- FAQ/question-oriented content where useful
- No dependency on a particular language model
- No dependency on MCP for the underlying knowledge representation
- All core knowledge remains available as open, human-readable Markdown
