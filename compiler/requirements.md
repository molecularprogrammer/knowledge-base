# Compiler Requirements

**UID:** `MPKB-COMP-REQ-001`

**Status:** Proposed

## 1. Purpose and scope

The compiler shall make knowledge-base content reliable for human readers and machine consumers. It
shall preserve the repository's human-readable knowledge while providing a trustworthy structured
representation. These requirements apply to the compiler and its outputs, not to search, API, or AI
services that may later consume those outputs.

The terms **shall**, **shall not**, **should**, and **may** express requirements at the strength
stated.

## 2. Requirements

### Canonical knowledge

- **MPKB-COMP-REQ-002:** The compiler shall treat reviewed, human-readable repository content as the
  authoritative knowledge source.
- **MPKB-COMP-REQ-003:** Compiler execution shall not alter canonical source content.
- **MPKB-COMP-REQ-004:** The compiler shall keep generated representations distinguishable from
  canonical content and regenerable from that content.

### Structured representation

- **MPKB-COMP-REQ-005:** The compiler shall represent each knowledge document and its addressable
  sections as structured records.
- **MPKB-COMP-REQ-006:** The structured representation shall preserve document and section identity,
  hierarchy, order, content, and relevant descriptive information.
- **MPKB-COMP-REQ-007:** The structured representation shall preserve defined relationships among
  knowledge records and the provenance associated with them.
- **MPKB-COMP-REQ-008:** The compiler shall provide stable identities that do not depend on mutable
  titles, heading text, or file paths.
- **MPKB-COMP-REQ-009:** A consumer shall be able to retrieve a section independently and determine
  its containing document and place in the document hierarchy.

### Integrity and diagnostics

- **MPKB-COMP-REQ-010:** The compiler shall detect malformed or incomplete structured records,
  identity conflicts, invalid hierarchy, and unresolved internal references.
- **MPKB-COMP-REQ-011:** Diagnostics shall identify the affected source and record or field and shall
  give enough information to correct the problem.
- **MPKB-COMP-REQ-012:** Invalid knowledge data shall prevent a successful publication build; the
  compiler shall not silently discard or reinterpret invalid data.

### Interoperability and reproducibility

- **MPKB-COMP-REQ-013:** The compiler shall produce a documented machine-readable representation
  suitable for independent consumers.
- **MPKB-COMP-REQ-014:** Equivalent source and compiler versions shall produce equivalent,
  deterministic representations.
- **MPKB-COMP-REQ-015:** The knowledge model shall not depend on a particular documentation renderer,
  search service, language model, or AI protocol.
- **MPKB-COMP-REQ-016:** The compiler shall support consistent validation in contributor and
  publication workflows.

## 3. Exclusions

These requirements do not require the compiler to provide a search interface, API, MCP server,
semantic index, generated summary, or FAQ. Such services may consume compiler outputs under their
own requirements. Generated summaries shall not replace or become authoritative over canonical
content.

## 4. Traceability

The architecture and allocation of these requirements are defined in
[Compiler Design](design.md). Concrete source rules, formats, and verification methods are defined
in [Compiler Implementation](implementation.md).