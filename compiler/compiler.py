"""Validate knowledge-base Markdown and emit deterministic JSON artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

SCHEMA_VERSION = "1.0.0"
OUTPUT_FORMAT_VERSION = "1.0.0"
IDENTIFIER = re.compile(r"^[a-z][a-z0-9-]*(?::[a-z][a-z0-9-]*)+$")
TOPIC_SLUG = re.compile(r"^[a-z][a-z0-9-]*$")
HEADING_ID = re.compile(r"^(.*?)\s+\{#([^{}]+)\}\s*$")

DOCUMENT_FIELDS = {
    "schema_version", "id", "type", "title", "description", "topics", "keywords", "status",
    "relationships", "sources", "authors", "parent", "reviewed", "valid_from", "valid_until",
}
REQUIRED_DOCUMENT_FIELDS = {
    "schema_version", "id", "type", "title", "description", "topics", "keywords", "status",
    "relationships", "sources",
}
SOURCE_FIELDS = {"id", "url", "citation", "title", "authors", "published", "accessed", "supports"}
RELATION_FIELDS = {"type", "target"}


class DuplicateKeyError(ValueError):
    pass


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    result: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in result
        except TypeError as exc:
            raise DuplicateKeyError("mapping keys must be scalar values") from exc
        if duplicate:
            raise DuplicateKeyError(f"duplicate key {key!r}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


@dataclass(frozen=True)
class Diagnostic:
    severity: str
    code: str
    message: str
    path: str
    line: int | None = None
    field: str | None = None

    def __str__(self) -> str:
        location = self.path
        if self.line is not None:
            location += f":{self.line}"
        if self.field:
            location += f" ({self.field})"
        return f"{location}: {self.severity} {self.code}: {self.message}"


@dataclass
class ParsedDocument:
    relative_path: str
    metadata: dict[str, Any]
    preamble: str
    sections: list[dict[str, Any]]
    source_records: list[dict[str, Any]]


def _plain(value: Any) -> Any:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_plain(item) for item in value]
    return value


def _front_matter(text: str) -> tuple[dict[str, Any] | None, str, int | None, str | None]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None, text, None, "missing YAML front matter starting with ---"
    closing = next((i for i in range(1, len(lines)) if lines[i].strip() in {"---", "..."}), None)
    if closing is None:
        return None, "", None, "unterminated YAML front matter"
    try:
        metadata = yaml.load("".join(lines[1:closing]), Loader=UniqueKeyLoader)
    except (yaml.YAMLError, DuplicateKeyError) as exc:
        mark = getattr(exc, "problem_mark", None)
        line = mark.line + 2 if mark else None
        return None, "".join(lines[closing + 1:]), line, f"invalid YAML front matter: {exc}"
    if not isinstance(metadata, dict):
        return None, "".join(lines[closing + 1:]), 2, "front matter must be a YAML mapping"
    return _plain(metadata), "".join(lines[closing + 1:]), None, None


def _scan_headings(body: str) -> tuple[str, list[dict[str, Any]], list[Diagnostic]]:
    lines = body.splitlines(keepends=True)
    offsets: list[int] = []
    offset = 0
    for line in lines:
        offsets.append(offset)
        offset += len(line)

    headings: list[dict[str, Any]] = []
    diagnostics: list[Diagnostic] = []
    fence_char: str | None = None
    fence_size = 0
    for line_number, line in enumerate(lines, 1):
        fence = re.match(r"^ {0,3}(`{3,}|~{3,})(.*?)(?:\r?\n)?$", line)
        if fence:
            token = fence.group(1)
            if fence_char is None:
                fence_char, fence_size = token[0], len(token)
            elif token[0] == fence_char and len(token) >= fence_size and not fence.group(2).strip():
                fence_char, fence_size = None, 0
            continue
        if fence_char is not None:
            continue
        match = re.match(r"^ {0,3}(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*(?:\r?\n)?$", line)
        if not match:
            continue
        title_with_id = match.group(2).strip()
        id_match = HEADING_ID.match(title_with_id)
        title = id_match.group(1).strip() if id_match else title_with_id
        headings.append({
            "line": line_number,
            "offset": offsets[line_number - 1],
            "level": len(match.group(1)),
            "title": title,
            "id": id_match.group(2) if id_match else None,
        })

    stack: list[dict[str, Any]] = []
    for index, heading in enumerate(headings):
        while stack and stack[-1]["level"] >= heading["level"]:
            stack.pop()
        heading["ancestors"] = [item["id"] for item in stack if item["id"]]
        if index and heading["level"] > headings[index - 1]["level"] + 1:
            diagnostics.append(Diagnostic(
                "error", "HEADING_LEVEL_SKIP",
                f"heading level {heading['level']} skips a level after heading at line {headings[index - 1]['line']}",
                "", heading["line"],
            ))
        if not heading["id"]:
            diagnostics.append(Diagnostic(
                "error", "HEADING_ID_MISSING", "heading must have an explicit stable ID using {#id}",
                "", heading["line"],
            ))
        if not heading["title"]:
            diagnostics.append(Diagnostic("error", "HEADING_TITLE_EMPTY", "heading title must not be empty", "", heading["line"]))
        stack.append(heading)

    preamble = body[:headings[0]["offset"]].strip() if headings else body.strip()
    sections: list[dict[str, Any]] = []
    for index, heading in enumerate(headings):
        end = len(body)
        for following in headings[index + 1:]:
            if following["level"] <= heading["level"]:
                end = following["offset"]
                break
        heading_end = body.find("\n", heading["offset"])
        if heading_end < 0:
            heading_end = len(body)
        sections.append({
            "id": heading["id"],
            "title": heading["title"],
            "level": heading["level"],
            "ancestors": heading["ancestors"],
            "order": index,
            "content": body[heading_end + 1:end].strip(),
            "line": heading["line"],
        })
    return preamble, sections, diagnostics


def _is_date(value: Any) -> bool:
    if isinstance(value, date) and not isinstance(value, datetime):
        return True
    if isinstance(value, str):
        try:
            return date.fromisoformat(value).isoformat() == value
        except ValueError:
            return False
    return False


def _validate_document(metadata: dict[str, Any], relative_path: str,
                       vocabularies: dict[str, set[str]]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    def error(code: str, message: str, field: str | None = None) -> None:
        diagnostics.append(Diagnostic("error", code, message, relative_path, field=field))

    if any(not isinstance(key, str) for key in metadata):
        error("FIELD_NAME_TYPE", "all document metadata keys must be strings")
        return diagnostics
    for field in sorted(REQUIRED_DOCUMENT_FIELDS - set(metadata)):
        error("FIELD_REQUIRED", "required field is missing", field)
    for field in sorted(set(metadata) - DOCUMENT_FIELDS):
        error("FIELD_UNKNOWN", "field is not defined by schema version 1.0.0", field)
    for field in ("schema_version", "id", "type", "title", "description", "status"):
        if field in metadata and not isinstance(metadata[field], str):
            error("FIELD_TYPE", "must be a string", field)
    if metadata.get("schema_version") != SCHEMA_VERSION:
        error("SCHEMA_VERSION", f"must be {SCHEMA_VERSION}", "schema_version")
    if isinstance(metadata.get("id"), str) and not IDENTIFIER.fullmatch(metadata["id"]):
        error("IDENTIFIER_FORMAT", "must match the documented stable identifier format", "id")
    for field in ("title", "description"):
        if field in metadata and (not isinstance(metadata[field], str) or not metadata[field].strip()):
            error("FIELD_EMPTY", "must be a non-empty string", field)

    for field, vocabulary in (("type", "document_types"), ("status", "statuses")):
        value = metadata.get(field)
        if isinstance(value, str) and value not in vocabularies.get(vocabulary, set()):
            error("VALUE_UNKNOWN", f"must be one of: {', '.join(sorted(vocabularies.get(vocabulary, set())))}", field)

    for field in ("topics", "keywords", "authors"):
        if field not in metadata:
            continue
        values = metadata[field]
        if not isinstance(values, list) or any(not isinstance(value, str) or not value.strip() for value in values):
            error("FIELD_TYPE", "must be a list of non-empty strings", field)
            continue
        if len(values) != len(set(values)):
            error("VALUE_DUPLICATE", "list values must be unique", field)
        if field == "topics":
            for topic in values:
                if not TOPIC_SLUG.fullmatch(topic):
                    error("TOPIC_FORMAT", "topic must be a lowercase slug", field)
                elif topic not in vocabularies.get("topics", set()):
                    error("TOPIC_UNKNOWN", f"unknown topic {topic!r}; add it to the controlled topic vocabulary", field)

    for field in ("relationships", "sources"):
        if field in metadata and not isinstance(metadata[field], list):
            error("FIELD_TYPE", "must be a list", field)
    relationships = metadata.get("relationships", [])
    if isinstance(relationships, list):
        for index, relation in enumerate(relationships):
            field = f"relationships[{index}]"
            if not isinstance(relation, dict):
                error("FIELD_TYPE", "relationship must be a mapping", field)
                continue
            if any(not isinstance(key, str) for key in relation):
                error("FIELD_NAME_TYPE", "relationship keys must be strings", field)
                continue
            for key in sorted(set(relation) - RELATION_FIELDS):
                error("FIELD_UNKNOWN", "relationship field is not defined", f"{field}.{key}")
            for key in sorted(RELATION_FIELDS - set(relation)):
                error("FIELD_REQUIRED", "relationship field is required", f"{field}.{key}")
            relation_type = relation.get("type")
            if not isinstance(relation_type, str) or relation_type not in vocabularies.get("relationship_types", set()):
                error("RELATIONSHIP_TYPE", "unknown relationship type", f"{field}.type")
            target = relation.get("target")
            if not isinstance(target, str) or not IDENTIFIER.fullmatch(target):
                error("IDENTIFIER_FORMAT", "target must be a canonical document or section ID", f"{field}.target")

    sources = metadata.get("sources", [])
    if isinstance(sources, list):
        for index, source in enumerate(sources):
            field = f"sources[{index}]"
            if not isinstance(source, dict):
                error("FIELD_TYPE", "source must be a mapping", field)
                continue
            if any(not isinstance(key, str) for key in source):
                error("FIELD_NAME_TYPE", "source keys must be strings", field)
                continue
            for key in sorted(set(source) - SOURCE_FIELDS):
                error("FIELD_UNKNOWN", "source field is not defined", f"{field}.{key}")
            source_id = source.get("id")
            if not isinstance(source_id, str) or not IDENTIFIER.fullmatch(source_id):
                error("IDENTIFIER_FORMAT", "source requires a valid stable ID", f"{field}.id")
            if not source.get("url") and not source.get("citation"):
                error("SOURCE_LOCATOR", "source requires url or citation", field)
            url = source.get("url")
            if url is not None and (not isinstance(url, str) or not re.match(r"^https?://\S+$", url)):
                error("SOURCE_URL", "url must be an absolute HTTP(S) URL", f"{field}.url")
            citation = source.get("citation")
            if citation is not None and (not isinstance(citation, str) or not citation.strip()):
                error("SOURCE_CITATION", "citation must be a non-empty string", f"{field}.citation")
            if "title" in source and (not isinstance(source["title"], str) or not source["title"].strip()):
                error("FIELD_TYPE", "must be a non-empty string", f"{field}.title")
            if "authors" in source and (
                not isinstance(source["authors"], list)
                or any(not isinstance(author, str) or not author.strip() for author in source["authors"])
            ):
                error("FIELD_TYPE", "must be a list of non-empty strings", f"{field}.authors")
            for date_field in ("published", "accessed"):
                if date_field in source and not _is_date(source[date_field]):
                    error("DATE_FORMAT", "must be an ISO 8601 calendar date", f"{field}.{date_field}")
            supports = source.get("supports", [])
            if not isinstance(supports, list) or any(
                not isinstance(item, str) or not IDENTIFIER.fullmatch(item) for item in supports
            ):
                error("REFERENCE_FORMAT", "supports must be a list of canonical IDs", f"{field}.supports")

    if "parent" in metadata and (
        not isinstance(metadata["parent"], str) or not IDENTIFIER.fullmatch(metadata["parent"])
    ):
        error("REFERENCE_FORMAT", "parent must be a canonical document ID", "parent")
    for field in ("reviewed", "valid_from", "valid_until"):
        if field in metadata and not _is_date(metadata[field]):
            error("DATE_FORMAT", "must be an ISO 8601 calendar date", field)
    valid_from, valid_until = metadata.get("valid_from"), metadata.get("valid_until")
    if _is_date(valid_from) and _is_date(valid_until) and valid_from > valid_until:
        error("DATE_RANGE", "valid_from must not be later than valid_until", "valid_from")
    return diagnostics


def _read_vocabulary(schema_path: Path) -> tuple[dict[str, set[str]], list[Diagnostic]]:
    try:
        raw = yaml.load(schema_path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except (OSError, yaml.YAMLError, DuplicateKeyError) as exc:
        return {}, [Diagnostic("error", "VOCABULARY_READ", str(exc), str(schema_path))]
    if not isinstance(raw, dict) or raw.get("schema_version") != SCHEMA_VERSION:
        return {}, [Diagnostic("error", "VOCABULARY_SCHEMA", "vocabulary schema_version must be 1.0.0", str(schema_path))]
    if any(not isinstance(key, str) for key in raw):
        return {}, [Diagnostic("error", "VOCABULARY_FIELD", "vocabulary keys must be strings", str(schema_path))]
    allowed_fields = {"schema_version", "document_types", "statuses", "relationship_types", "topics"}
    diagnostics: list[Diagnostic] = []
    for field in sorted(set(raw) - allowed_fields):
        diagnostics.append(Diagnostic("error", "VOCABULARY_FIELD", f"unknown vocabulary field {field!r}", str(schema_path)))
    vocabularies: dict[str, set[str]] = {}
    for field in ("document_types", "statuses", "relationship_types", "topics"):
        values = raw.get(field)
        if not isinstance(values, list) or any(not isinstance(value, str) or not value.strip() for value in values):
            diagnostics.append(Diagnostic("error", "VOCABULARY_VALUES", f"{field} must be a list of non-empty strings", str(schema_path), field=field))
            continue
        if len(values) != len(set(values)):
            diagnostics.append(Diagnostic("error", "VOCABULARY_DUPLICATE", f"{field} values must be unique", str(schema_path), field=field))
        if field == "topics" and any(not TOPIC_SLUG.fullmatch(value) for value in values):
            diagnostics.append(Diagnostic("error", "VOCABULARY_TOPIC_FORMAT", "topics must be lowercase slugs", str(schema_path), field=field))
        vocabularies[field] = set(values)
    return vocabularies, diagnostics


def compile_repository(root: Path, *, schema_path: Path | None = None,
                       mode: str = "strict", compiler_version: str = "0.1.0") -> tuple[list[Diagnostic], dict[str, Any] | None]:
    """Compile Markdown files below root. Report mode never writes artifacts."""
    if mode not in {"strict", "report"}:
        raise ValueError(f"unsupported compilation mode: {mode}")
    root = root.resolve()
    schema_path = (schema_path or Path(__file__).with_name("schema.yaml")).resolve()
    vocabularies, diagnostics = _read_vocabulary(schema_path)
    markdown_files = sorted(
        path for path in root.rglob("*.md")
        if path.is_file() and not path.is_symlink()
    )
    documents: list[ParsedDocument] = []
    seen_ids: dict[str, tuple[str, str]] = {}
    for path in markdown_files:
        relative = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            diagnostics.append(Diagnostic("error", "SOURCE_READ", str(exc), relative))
            continue
        metadata, body, line, front_error = _front_matter(text)
        if front_error:
            diagnostics.append(Diagnostic("error", "FRONT_MATTER", front_error, relative, line))
            _, sections, heading_diagnostics = _scan_headings(text)
            diagnostics.extend(
                Diagnostic(item.severity, item.code, item.message, relative, item.line, item.field)
                for item in heading_diagnostics
            )
            continue
        assert metadata is not None
        diagnostics.extend(_validate_document(metadata, relative, vocabularies))
        preamble, sections, heading_diagnostics = _scan_headings(body)
        diagnostics.extend(
            Diagnostic(item.severity, item.code, item.message, relative, item.line, item.field)
            for item in heading_diagnostics
        )
        document_id = metadata.get("id")
        if isinstance(document_id, str) and IDENTIFIER.fullmatch(document_id):
            if document_id in seen_ids:
                prior_path, prior_kind = seen_ids[document_id]
                diagnostics.append(Diagnostic("error", "IDENTIFIER_DUPLICATE",
                    f"ID {document_id!r} already used by {prior_kind} in {prior_path}", relative, field="id"))
            else:
                seen_ids[document_id] = (relative, "document")
        source_records = metadata.get("sources", []) if isinstance(metadata.get("sources", []), list) else []
        documents.append(ParsedDocument(relative, metadata, preamble, sections, source_records))

    for document in documents:
        for section in document.sections:
            identifier = section["id"]
            if not identifier:
                continue
            if not IDENTIFIER.fullmatch(identifier):
                diagnostics.append(Diagnostic("error", "IDENTIFIER_FORMAT", "section ID must match the documented format", document.relative_path, section["line"]))
            elif identifier in seen_ids:
                prior_path, prior_kind = seen_ids[identifier]
                diagnostics.append(Diagnostic("error", "IDENTIFIER_DUPLICATE",
                    f"ID {identifier!r} already used by {prior_kind} in {prior_path}", document.relative_path, section["line"]))
            else:
                seen_ids[identifier] = (document.relative_path, "section")

    source_definitions: dict[str, dict[str, Any]] = {}
    source_associations: dict[str, set[str]] = {}
    for document in documents:
        local_source_ids: set[str] = set()
        for source in document.source_records:
            if not isinstance(source, dict) or not isinstance(source.get("id"), str):
                continue
            source_id = source["id"]
            if source_id in local_source_ids:
                diagnostics.append(Diagnostic("error", "SOURCE_DUPLICATE",
                    f"source ID {source_id!r} appears more than once in this document",
                    document.relative_path, field="sources"))
                continue
            local_source_ids.add(source_id)
            normalized = _plain(source)
            if source_id in seen_ids and seen_ids[source_id][1] != "source":
                diagnostics.append(Diagnostic("error", "IDENTIFIER_DUPLICATE",
                    f"source ID {source_id!r} conflicts with {seen_ids[source_id][1]}", document.relative_path))
            elif source_id in source_definitions and source_definitions[source_id] != normalized:
                diagnostics.append(Diagnostic("error", "SOURCE_CONFLICT",
                    f"source ID {source_id!r} has conflicting definitions", document.relative_path))
            else:
                source_definitions[source_id] = normalized
                seen_ids[source_id] = (document.relative_path, "source")
                source_associations.setdefault(source_id, set()).add(
                    str(document.metadata.get("id", ""))
                )

    document_ids = {doc.metadata.get("id") for doc in documents if isinstance(doc.metadata.get("id"), str)}
    section_ids = {section["id"] for doc in documents for section in doc.sections if section["id"]}
    known_targets = document_ids | section_ids
    for document in documents:
        parent = document.metadata.get("parent")
        if parent and parent not in document_ids:
            diagnostics.append(Diagnostic("error", "REFERENCE_UNRESOLVED",
                f"parent ID {parent!r} does not resolve to a document", document.relative_path, field="parent"))
        relationships = document.metadata.get("relationships", [])
        if isinstance(relationships, list):
            for index, relation in enumerate(relationships):
                if isinstance(relation, dict) and relation.get("target") not in known_targets:
                    diagnostics.append(Diagnostic("error", "REFERENCE_UNRESOLVED",
                        f"target ID {relation.get('target')!r} does not resolve", document.relative_path,
                        field=f"relationships[{index}].target"))
        for index, source in enumerate(document.source_records):
            if isinstance(source, dict) and isinstance(source.get("supports", []), list):
                for target in source.get("supports", []):
                    if target not in known_targets:
                        diagnostics.append(Diagnostic("error", "REFERENCE_UNRESOLVED",
                            f"source target ID {target!r} does not resolve", document.relative_path,
                            field=f"sources[{index}].supports"))

    parent_by_id = {doc.metadata.get("id"): doc.metadata.get("parent") for doc in documents
                    if isinstance(doc.metadata.get("id"), str)}
    for document in documents:
        current = document.metadata.get("id")
        visited: set[str] = set()
        while current in parent_by_id and parent_by_id[current]:
            if current in visited:
                diagnostics.append(Diagnostic("error", "PARENT_CYCLE", "parent hierarchy contains a cycle",
                    document.relative_path, field="parent"))
                break
            visited.add(current)
            current = parent_by_id[current]

    diagnostics.sort(key=lambda item: (item.path, item.line or 0, item.code, item.field or ""))
    if any(item.severity == "error" for item in diagnostics) or mode == "report":
        return diagnostics, None

    document_records: list[dict[str, Any]] = []
    section_records: list[dict[str, Any]] = []
    relationship_records: list[dict[str, Any]] = []
    source_records_out: dict[str, dict[str, Any]] = {}
    for document in documents:
        metadata = _plain(document.metadata)
        document_records.append({
            "id": metadata["id"], "type": metadata["type"], "title": metadata["title"],
            "description": metadata["description"], "topics": metadata["topics"],
            "keywords": metadata["keywords"], "status": metadata["status"],
            "authors": metadata.get("authors", []), "parent": metadata.get("parent"),
            "reviewed": metadata.get("reviewed"), "valid_from": metadata.get("valid_from"),
            "valid_until": metadata.get("valid_until"), "path": document.relative_path,
            "preamble": document.preamble,
        })
        for section in document.sections:
            section_records.append({
                "id": section["id"], "document_id": metadata["id"], "title": section["title"],
                "level": section["level"], "ancestors": section["ancestors"],
                "order": section["order"], "content": section["content"],
            })
        for relation in metadata["relationships"]:
            relationship_records.append({
                "source": metadata["id"], "type": relation["type"], "target": relation["target"],
            })
        for source in document.source_records:
            normalized = _plain(source)
            source_records_out[normalized["id"]] = {
                **normalized,
                "documents": sorted(source_associations.get(normalized["id"], set())),
            }

    document_records.sort(key=lambda item: item["id"])
    section_records.sort(key=lambda item: item["id"])
    relationship_records.sort(key=lambda item: (item["source"], item["type"], item["target"]))
    sources_out = [source_records_out[key] for key in sorted(source_records_out)]

    artifact_data = {
        "documents.json": document_records,
        "sections.json": section_records,
        "relationships.json": relationship_records,
        "sources.json": sources_out,
    }
    serialized = {name: _json_bytes(value) for name, value in artifact_data.items()}
    digest_input = b"".join(name.encode() + b"\0" + serialized[name] for name in sorted(serialized))
    digest = hashlib.sha256(digest_input).hexdigest()
    manifest = {
        "output_format_version": OUTPUT_FORMAT_VERSION,
        "schema_versions": sorted({doc.metadata["schema_version"] for doc in documents}),
        "compiler_version": compiler_version,
        "digest": digest,
        "artifacts": sorted([*artifact_data, "manifest.json"]),
        "document_count": len(document_records),
        "section_count": len(section_records),
        "relationship_count": len(relationship_records),
        "source_count": len(sources_out),
    }
    artifact_set = {**serialized, "manifest.json": _json_bytes(manifest)}
    return diagnostics, {"manifest": manifest, "artifacts": artifact_set}


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def _write_artifact_set(output_dir: Path, artifact_set: dict[str, bytes], digest: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / OUTPUT_FORMAT_VERSION / digest
    if destination.exists():
        for name, content in artifact_set.items():
            if not (destination / name).is_file() or (destination / name).read_bytes() != content:
                raise OSError(f"existing artifact set is incomplete or has conflicting content: {destination}")
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = Path(tempfile.mkdtemp(prefix=".compiler-", dir=destination.parent))
        try:
            for name, content in artifact_set.items():
                (temporary / name).write_bytes(content)
            os.replace(temporary, destination)
        except Exception:
            shutil.rmtree(temporary, ignore_errors=True)
            raise
    current = {
        "output_format_version": OUTPUT_FORMAT_VERSION,
        "digest": digest,
        "path": f"{OUTPUT_FORMAT_VERSION}/{digest}",
    }
    fd, temp_name = tempfile.mkstemp(prefix=".current-", dir=output_dir)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(_json_bytes(current))
        os.replace(temp_name, output_dir / "current.json")
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise
    return destination


def publish_result(result: dict[str, Any], output_dir: Path) -> Path:
    """Publish a successful compilation result to an output directory."""
    return _write_artifact_set(output_dir, result["artifacts"], result["manifest"]["digest"])


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("docs"),
                        help="Markdown source root (default: docs/)")
    parser.add_argument("--schema", type=Path, help="schema/vocabulary YAML path")
    parser.add_argument("--output", type=Path, help="write artifacts to this output directory after validation")
    parser.add_argument("--mode", choices=("strict", "report"), default="strict")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = args.root.resolve()
    schema_path = args.schema.resolve() if args.schema else Path(__file__).with_name("schema.yaml")
    output_dir = args.output.resolve() if args.output else None
    diagnostics, result = compile_repository(root, schema_path=schema_path, mode=args.mode)
    for diagnostic in diagnostics:
        print(diagnostic, file=sys.stderr)
    errors = sum(item.severity == "error" for item in diagnostics)
    if args.mode == "report":
        print(f"Migration report: {errors} error(s) across {len(diagnostics)} diagnostic(s).", file=sys.stderr)
        return 0
    if errors:
        print(f"Compilation failed with {errors} error(s).", file=sys.stderr)
        return 1
    if result:
        if output_dir is not None:
            publish_result(result, output_dir)
        print(f"Compiled {result['manifest']['document_count']} documents and "
              f"{result['manifest']['section_count']} sections (sha256 {result['manifest']['digest']}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())