# Compiler Requirements

## Purpose and scope

The compiler shall make knowledge-base content reliable for human readers and machine consumers. It
shall preserve the repository's human-readable knowledge while providing a trustworthy structured
representation. These requirements apply to the compiler and its outputs. The compiler produces
structured, language-model-friendly data. It does not provide a search service or an AI protocol
endpoint.

## Requirements

### Canonical knowledge

- The compiler shall treat human-readable repository content as the authoritative knowledge source.
- Compiler execution shall not alter canonical source content.
- The compiler shall keep generated representations distinguishable from canonical content and
  regenerable from source.

### Structured representation

- The compiler shall represent each knowledge document and its addressable sections as structured
  records.
- The structured representation shall preserve document and section identity, hierarchy, order,
  content, and relevant descriptive information.
- The structured representation shall preserve defined relationships among knowledge records and
  their provenance.
- The compiler shall provide stable identities that do not depend on mutable titles, heading text,
  or file paths.
- A consumer shall be able to retrieve a section independently and determine its containing
  document and place in the document hierarchy.

### Integrity and diagnostics

- The compiler shall detect malformed or incomplete structured records, identity conflicts, invalid
  hierarchy, and unresolved internal references.
- Diagnostics shall identify the affected source and record or field and provide enough information
  to correct the problem.
- Invalid knowledge data shall prevent a successful publication build. The compiler shall not
  silently discard or reinterpret invalid data.

### Interoperability and reproducibility

- The compiler shall produce a documented machine-readable representation that preserves context
  and is suitable for independent processing, including by language-model-based tools.
- Equivalent source and compiler versions shall produce equivalent, deterministic representations.
- The knowledge model shall not depend on a particular documentation renderer, language model, or
  AI protocol.
- The compiler shall support consistent validation in contributor and publication workflows.

## Exclusions

The compiler does not provide a search interface, search API, or MCP server. Search, retrieval,
question-answering, and language-model services are outside its scope. The compiler does not need to
generate summaries or FAQ content. If summaries are produced by a later consumer, they remain derived
data and shall not replace canonical content.

## Related documents

[Compiler Design](design.md) describes the architecture. [Compiler Implementation](implementation.md)
defines the source schema, output format, and verification plan.