# Compiler Design

**Status:** Proposed

**Scope:** Allocate the [compiler requirements](requirements.md) to the compiler core, its
ProperDocs integration, and generated representations.

## 1. Purpose

The compiler is the boundary between canonical knowledge and machine-readable representations. It
provides one place to validate knowledge integrity and assemble document- and section-level records
before the repository is published.

Repository source remains authoritative. ProperDocs renders the human-facing site; compiler outputs
serve independent consumers. Neither the renderer nor a downstream search or AI protocol owns the
knowledge model.

## 2. Architecture

The compiler has three logical parts:

- **Source model:** Markdown documents plus their structured metadata and the maintained topic
  vocabulary.
- **Compiler core:** parses the source model, checks local and repository-wide integrity, and builds
  document, section, relationship, and provenance records.
- **ProperDocs adapter:** invokes the core during a site build, reports diagnostics through the build
  system, and places successful compiled artifacts in the published site output.

The core owns parsing-independent validation and record construction. The adapter owns build-lifecycle
integration and output placement. The knowledge schema and output contract are specified in
[Compiler Implementation](implementation.md).

### 2.1 Context and interactions

```text
Authors --> Canonical Markdown + metadata + topic vocabulary
                              |
                              v
                    ProperDocs build hook
                              |
                     Compiler core
                     /            \
          build diagnostics     JSON artifacts
                                     |
                       independent language-model tools
```

- Authors edit canonical Markdown and metadata in Git.
- The ProperDocs adapter invokes the compiler as part of the normal site build.
- ProperDocs renders the site and presents compiler diagnostics. A compiler error fails the build.
- The compiler emits versioned artifacts alongside the built site for static hosting and independent
  consumption.
- Independent language-model-based tools may read compiled artifacts. Their user interfaces and
  retrieval behavior are outside the compiler boundary.

The compiler owns the contract between canonical source and compiled records. The ProperDocs adapter
is the only compiler component coupled to ProperDocs. It enforces the integrity and diagnostic
requirements at the publication boundary while keeping the core reusable for local checks and other
consumers.

### 2.2 Build lifecycle

ProperDocs supports local Python hook scripts configured in `properdocs.yml`. The global `on_files`
hook provides the build-wide integration point for validation. It stages artifacts inside the site
build directory; a post-build hook publishes the completed artifact set by updating its publication
marker only after successful site generation. This avoids a separate validation command and prevents
partially built data from being published. CI uploads and deploys only after the build succeeds, so a
failed build cannot replace the currently deployed site with incomplete artifacts.
The compiler core reads the configured documentation root rather than relying only on ProperDocs'
file collection, so excluded Markdown files are also validated. Hook details and version-specific
behavior are specified in [Compiler Implementation](implementation.md).

The hook adapter shall be thin: it translates compiler diagnostics into ProperDocs build errors and
does not define schema rules. Hook configuration, lifecycle state, and output paths are detailed in
[Compiler Implementation](implementation.md).

### 2.3 Alternatives and rationale

- **Separate command run before ProperDocs:** provides a clear standalone entry point, but duplicates
  build orchestration and allows contributors to build the site without the integrity check. A
  separate command may be added later for editor feedback, but it is not the publication gate.
- **ProperDocs plugin package:** provides reusable distribution, but adds packaging and installation
  work for an integration used by this repository alone. A configured hook script is sufficient for
  the initial adapter.
- **Schema implemented inside the hook:** is simple initially, but couples the knowledge contract to
  one renderer and makes independent testing and consumption harder. The schema and compiler core
  remain independent; only the adapter uses ProperDocs APIs.

This choice follows the current build environment, which already runs ProperDocs. It also keeps the
schema independent of ProperDocs, MkDocs, StrictDoc, and any particular language model or AI
protocol. This supports independent consumers without making a consumer part of the compiler.

## 3. Boundaries and constraints

- The core may use Markdown and YAML libraries available to the implementation, but it shall not call
  ProperDocs APIs.
- The adapter may use ProperDocs hook APIs, but it shall not change canonical source or schema
  semantics.
- Generated files are build outputs, not source records. They shall be recreated from canonical
  inputs and shall not be edited by consumers.
- External URL availability is not an input to successful compilation; the build must not require
  network access to validate provenance.
- The knowledge base is not a requirements-management system. Its schema is for broad scientific and
  technical knowledge, not only formal engineering requirements.
