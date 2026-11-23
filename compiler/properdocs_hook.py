"""Optional ProperDocs hook for compiler migration reporting."""

from __future__ import annotations

import logging
from pathlib import Path

from compiler.compiler import compile_repository

log = logging.getLogger("properdocs.compiler")


def on_files(files, config, **kwargs):
    """Report schema migration diagnostics without blocking the existing site build."""
    config_path = getattr(config, "config_file_path", None)
    repository_root = Path(config_path).resolve().parent if config_path else Path.cwd()
    docs_root = Path(config.docs_dir)
    if not docs_root.is_absolute():
        docs_root = repository_root / docs_root
    schema_path = repository_root / "compiler" / "schema.yaml"
    diagnostics, _ = compile_repository(docs_root, schema_path=schema_path, mode="report")
    for diagnostic in diagnostics:
        log.warning("%s", diagnostic)
    if diagnostics:
        log.info("Compiler migration report: %d diagnostic(s); run `task compiler:check` for strict validation.", len(diagnostics))
    return files


def on_post_build(config, **kwargs):
    """No compiled artifacts are published until legacy content migration is complete."""
    return None