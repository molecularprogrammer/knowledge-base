from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from compiler.compiler import compile_repository, publish_result


VALID_FRONT_MATTER = """---
schema_version: "1.0.0"
id: mpkb:document:alpha
type: article
title: Alpha
description: Test document.
topics: [chemistry]
keywords: [test]
status: published
relationships: []
sources:
  - id: mpkb:source:paper
    citation: Example paper
---

Preamble.

# Alpha {#mpkb:section:alpha}

Alpha content.

## Child {#mpkb:section:child}

Child content.
"""


class CompilerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.docs_root = self.root / "docs"
        self.docs_root.mkdir()
        self.schema_path = self.root / "schema.yaml"
        self.schema_path.write_text(
            "schema_version: '1.0.0'\n"
            "document_types: [article]\n"
            "statuses: [published]\n"
            "relationship_types: [references, related]\n"
            "topics: [chemistry]\n",
            encoding="utf-8",
        )
        self.write_doc("alpha.md", VALID_FRONT_MATTER)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write_doc(self, relative_path: str, content: str) -> Path:
        path = self.docs_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def compile(self, *, mode: str = "strict", output: Path | None = None):
        diagnostics, result = compile_repository(self.docs_root, schema_path=self.schema_path, mode=mode)
        if output is not None and result is not None:
            publish_result(result, output)
        return diagnostics, result

    def test_compiles_documents_sections_and_provenance(self) -> None:
        diagnostics, result = self.compile()
        self.assertEqual([], diagnostics)
        assert result is not None
        artifacts = result["artifacts"]
        documents = json.loads(artifacts["documents.json"])
        sections = json.loads(artifacts["sections.json"])
        sources = json.loads(artifacts["sources.json"])
        self.assertEqual("Preamble.", documents[0]["preamble"])
        self.assertEqual(["mpkb:section:alpha"], sections[1]["ancestors"])
        self.assertEqual("Child content.", sections[1]["content"])
        self.assertEqual("mpkb:source:paper", sources[0]["id"])
        self.assertEqual(["mpkb:document:alpha"], sources[0]["documents"])

    def test_duplicate_yaml_keys_are_rejected(self) -> None:
        self.write_doc("alpha.md", VALID_FRONT_MATTER.replace("title: Alpha\n", "title: Alpha\ntitle: Duplicate\n"))
        diagnostics, _ = self.compile()
        self.assertIn("FRONT_MATTER", {item.code for item in diagnostics})

    def test_missing_front_matter_is_reported(self) -> None:
        self.write_doc("legacy.md", "# Legacy\n")
        diagnostics, _ = self.compile(mode="report")
        self.assertTrue(any(item.code == "FRONT_MATTER" and item.path == "legacy.md" for item in diagnostics))

    def test_missing_section_id_and_fenced_heading(self) -> None:
        content = VALID_FRONT_MATTER + "\n## Missing ID\n\n```md\n# Example {#mpkb:section:example}\n```\n"
        self.write_doc("alpha.md", content)
        diagnostics, _ = self.compile()
        missing = [item for item in diagnostics if item.code == "HEADING_ID_MISSING"]
        self.assertEqual(1, len(missing))
        self.assertNotIn("mpkb:section:example", {item.message for item in diagnostics})

    def test_headings_inside_indented_code_blocks_are_ignored(self) -> None:
        content = VALID_FRONT_MATTER + "\n    # Not a heading {#mpkb:section:fake}\n"
        self.write_doc("alpha.md", content)
        diagnostics, result = self.compile()
        self.assertEqual([], diagnostics)
        assert result is not None
        sections = json.loads(result["artifacts"]["sections.json"])
        self.assertNotIn("mpkb:section:fake", {section["id"] for section in sections})

    def test_empty_heading_id_is_not_accepted(self) -> None:
        self.write_doc("alpha.md", VALID_FRONT_MATTER.replace("{#mpkb:section:alpha}", "{#}"))
        diagnostics, _ = self.compile()
        self.assertIn("HEADING_ID_MISSING", {item.code for item in diagnostics})

    def test_relationship_must_resolve(self) -> None:
        content = VALID_FRONT_MATTER.replace("relationships: []", "relationships:\n  - type: references\n    target: mpkb:document:missing")
        self.write_doc("alpha.md", content)
        diagnostics, _ = self.compile()
        self.assertIn("REFERENCE_UNRESOLVED", {item.code for item in diagnostics})

    def test_parent_cycle_is_rejected(self) -> None:
        first = VALID_FRONT_MATTER.replace("id: mpkb:document:alpha", "id: mpkb:document:alpha\nparent: mpkb:document:beta")
        second = VALID_FRONT_MATTER.replace("mpkb:document:alpha", "mpkb:document:beta").replace("topics: [chemistry]", "topics: [chemistry]\nparent: mpkb:document:alpha")
        self.write_doc("alpha.md", first)
        self.write_doc("beta.md", second)
        diagnostics, _ = self.compile()
        self.assertIn("PARENT_CYCLE", {item.code for item in diagnostics})

    def test_unknown_topic_is_rejected(self) -> None:
        self.write_doc("alpha.md", VALID_FRONT_MATTER.replace("chemistry", "unknown-topic"))
        diagnostics, _ = self.compile()
        self.assertIn("TOPIC_UNKNOWN", {item.code for item in diagnostics})

    def test_missing_topic_vocabulary_does_not_accept_topics(self) -> None:
        self.schema_path.write_text(
            "schema_version: '1.0.0'\n"
            "document_types: [article]\n"
            "statuses: [published]\n"
            "relationship_types: [references]\n"
            "topics: []\n",
            encoding="utf-8",
        )
        diagnostics, _ = self.compile()
        self.assertIn("TOPIC_UNKNOWN", {item.code for item in diagnostics})

    def test_duplicate_document_id_is_rejected(self) -> None:
        self.write_doc("beta.md", VALID_FRONT_MATTER)
        diagnostics, _ = self.compile()
        self.assertIn("IDENTIFIER_DUPLICATE", {item.code for item in diagnostics})

    def test_duplicate_section_id_is_rejected(self) -> None:
        content = VALID_FRONT_MATTER + "\n## Duplicate {#mpkb:section:alpha}\n"
        self.write_doc("alpha.md", content)
        diagnostics, _ = self.compile()
        self.assertIn("IDENTIFIER_DUPLICATE", {item.code for item in diagnostics})

    def test_invalid_mode_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.compile(mode="unknown")

    def test_invalid_front_matter_does_not_hide_heading_errors(self) -> None:
        self.write_doc("legacy.md", "---\nnot: [valid\n---\n# Legacy\n")
        diagnostics, _ = self.compile(mode="report")
        codes = {item.code for item in diagnostics}
        self.assertIn("FRONT_MATTER", codes)
        self.assertIn("HEADING_ID_MISSING", codes)

    def test_report_mode_never_writes_artifacts(self) -> None:
        output = self.root / "site" / "knowledge-base"
        self.write_doc("legacy.md", "# Legacy\n")
        self.compile(mode="report")
        self.assertFalse(output.exists())

    def test_output_is_deterministic_and_published_atomically(self) -> None:
        output = self.root / "site" / "knowledge-base"
        first_diagnostics, first = self.compile(output=output)
        second_diagnostics, second = self.compile(output=output)
        self.assertEqual([], first_diagnostics)
        self.assertEqual([], second_diagnostics)
        assert first is not None and second is not None
        self.assertEqual(first["manifest"]["digest"], second["manifest"]["digest"])
        current = json.loads((output / "current.json").read_text(encoding="utf-8"))
        self.assertEqual(first["manifest"]["digest"], current["digest"])

    def test_strict_failure_does_not_replace_current_pointer(self) -> None:
        output = self.root / "site" / "knowledge-base"
        diagnostics, result = self.compile(output=output)
        self.assertEqual([], diagnostics)
        assert result is not None
        previous = (output / "current.json").read_bytes()
        self.write_doc("legacy.md", "# Legacy\n")
        diagnostics, result = self.compile()
        self.assertIsNone(result)
        self.assertTrue(diagnostics)
        self.assertEqual(previous, (output / "current.json").read_bytes())


if __name__ == "__main__":
    unittest.main()