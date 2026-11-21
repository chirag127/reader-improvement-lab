"""Validate the public research corpus offline; never execute reader applications."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import date, datetime, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LOCAL_DIRECTORIES = {".git", ".local", ".venv", "node_modules", "__pycache__", ".superpowers", "private", "raw", "build", "dist", ".gradle", "vendor"}
FORBIDDEN_SUFFIXES = {".apk", ".apks", ".aab", ".dex", ".jar", ".so", ".class", ".smali", ".keystore", ".jks", ".pem", ".key"}
FORBIDDEN_DIRECTORIES = {"decompiled", "decompilation", "smali"}
TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".txt", ".xml", ".py", ".mjs", ".js", ".sh", ".yml", ".yaml", ".toml"}
FEATURE_EVIDENCE_TYPES = {"documented", "static-observation", "upstream-report", "proposal", "unknown", "blocked", "runtime-observation"}
HOST_EVIDENCE_TYPES = {
    "contribution-record-validation", "fixture-tooling-verification", "git-publication-verification",
    "host-build", "host-tooling-verification", "host-unit-test", "independent-evidence-review",
    "reference-engine-check", "repository-validation", "runtime-delivery-verification",
    "runtime-resource-cleanup", "scenario-fixture-verification", "synthetic-scenario-inputs",
}
EVIDENCE_TYPES = FEATURE_EVIDENCE_TYPES | HOST_EVIDENCE_TYPES
RUNTIME_STATUSES = {"pass", "partial", "fail", "blocked", "not-run"}
PUBLIC_REFERENCE_KEYS = {
    "report_path", "draft_path", "evidence_path", "identity_record", "test_plan",
    "evidence_manifest", "build_record", "reproduction_script", "test_plan_path",
    "artifact_record", "permission_record", "public_record", "identity_disambiguation_path",
}
COMMIT_KEYS = {"commit", "upstream_revision", "original_research_revision", "verified_commit", "baseline_commit", "fixed_commit", "contribution_commit", "source_revision", "production_revision", "source_base_gitlink"}
REFERENCE = re.compile(r"^ {0,3}\[([^\]\n]+)\]:\s*(?:<([^>]+)>|(\S+)).*$", re.MULTILINE)
INLINE_LINK = re.compile(r"!?\[([^\]\n]*)\]\((<[^>\n]+>|(?:[^()\s]|\([^()]*\))+)(?:\s+\"[^\"]*\")?\)")
PAIRED_REFERENCE = re.compile(r"!?\[([^\[\]\n]+)\]\[([^\]\n]*)\]")


def unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"Duplicate JSON member: {key}")
        value[key] = item
    return value


def reject_constant(value):
    raise ValueError(f"Non-JSON numeric constant: {value}")


def normalized(value):
    return " ".join(str(value).split()).casefold()


def is_reparse(path):
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def linked_ancestor(path, boundary=None):
    """Check before resolving: resolution would erase a junction or symlink alias."""
    for item in (path, *path.parents):
        if item == boundary:
            break
        try:
            if is_reparse(item):
                return True
        except FileNotFoundError:
            continue
    return False


def prose_only(text):
    """Ignore YAML metadata and fenced code when resolving rendered prose links."""
    lines = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL).splitlines()
    if lines and lines[0] == "---":
        end = next((i for i in range(1, len(lines)) if lines[i] == "---"), None)
        if end is not None:
            lines = lines[end + 1:]
    result, fence = [], None
    for line in lines:
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            run = marker[1]
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence):
                fence = None
            result.append("")
        else:
            result.append(line if fence is None else "")
    return "\n".join(result)


def markdown_anchors(text):
    prose = prose_only(text)
    anchors = {html.unescape(value) for value in re.findall(r"\b(?:id|name)=[\"']([^\"']+)[\"']", prose)}
    used = set()
    lines = prose.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"^ {0,3}#{1,6}\s+(.+?)(?:\s+#+)?\s*$", line)
        if match:
            title = match[1]
        elif line.strip() and index + 1 < len(lines) and re.fullmatch(r" {0,3}(?:=+|-+)\s*", lines[index + 1]):
            title = line.strip()
        else:
            continue
        title = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", title)
        title = re.sub(r"\[([^\]]+)\]\[[^\]]*\]", r"\1", title)
        title = html.unescape(re.sub(r"<[^>]*>", "", title))
        pieces = re.split(r"(`+[^`]*`+)", title)
        title = "".join(piece.strip("`") if piece.startswith("`") else re.sub(r"(?<!\w)_{1,3}(.+?)_{1,3}(?!\w)", r"\1", piece) for piece in pieces)
        title = re.sub(r"[*~`]", "", title).lower()
        slug = re.sub(r"[^\w\- ]", "", title).replace(" ", "-")
        candidate, index = slug, 0
        while candidate in used:
            index += 1
            candidate = f"{slug}-{index}"
        used.add(candidate)
        anchors.add(candidate)
    return anchors


class Validator:
    def __init__(self, root):
        self.root = root.resolve()
        self.errors = []
        self.documents = {}
        self.texts = {}
        self.files = []
        self.link_count = 0
        self.hash_count = 0
        self.counts = Counter()
        self.pending = []
        self.public_file_ids = set()
        self.output = None
        self.applications = set()
        self.finding_ids = set()
        self.fixture_records = {}
        self.observed_at = datetime.now(timezone.utc).isoformat()
        self.candidates = None
        self.inventory_mode = "standalone-filesystem"

    def error(self, code, path, message):
        item = {"code": code, "path": str(path), "message": message}
        if item not in self.errors:
            self.errors.append(item)

    def required_text(self, value, keys, path):
        if not isinstance(value, dict):
            self.error("record-shape", path, "Expected an object")
            return False
        valid = True
        for key in keys:
            if not isinstance(value.get(key), str) or not value[key].strip():
                self.error("required-field", path, f"Missing nonempty string: {key}")
                valid = False
        return valid

    def items(self, value, key, path, nonempty=True):
        rows = value.get(key) if isinstance(value, dict) else None
        if not isinstance(rows, list) or (nonempty and not rows):
            self.error("record-shape", path, f"Expected {'nonempty ' if nonempty else ''}array: {key}")
            return []
        return rows

    def document(self, path):
        value = self.documents.get(path)
        if not isinstance(value, dict):
            self.error("required-document", path, "Required JSON object is missing or invalid")
            return {}
        return value

    def dated(self, value, path):
        try:
            if not isinstance(value, str):
                raise ValueError("Missing date")
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                date.fromisoformat(value)
            elif re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})", value):
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            else:
                raise ValueError("Invalid date")
        except ValueError:
            self.error("observation-date", path, "Expected an ISO observation date")

    def strings(self, value, key, path, nonempty=True):
        rows = self.items(value, key, path, nonempty)
        if any(not isinstance(item, str) or not item.strip() for item in rows):
            self.error("required-field", path, f"Expected nonempty strings in {key}")
        return [item for item in rows if isinstance(item, str) and item.strip()]

    def digest(self, value, path):
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            self.error("hash-format", path, "Expected a complete lowercase SHA-256")
            return False
        return True

    def revision(self, value, path):
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{40}", value):
            self.error("source-revision", path, "Expected a full source commit")
            return False
        return True

    def publication_candidates(self):
        """Use the real index and unignored additions; never stage or invoke hooks."""
        if not (self.root / ".git").exists():
            return None
        self.inventory_mode = "git-tracked-and-unignored"
        environment = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}
        for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR"):
            environment.pop(key, None)
        try:
            result = subprocess.run(
                ["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", str(self.root),
                 "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
                stdin=subprocess.DEVNULL, capture_output=True, timeout=30, env=environment,
            )
            if result.returncode:
                raise ValueError("Git could not enumerate publication candidates")
            paths = set(result.stdout.decode("utf-8").split("\0")) - {""}
        except (OSError, ValueError, subprocess.TimeoutExpired) as error:
            self.error("publication-inventory", ".", type(error).__name__)
            return set()
        for path in sorted(paths):
            parts = Path(path).parts
            if path.startswith("/") or ".." in parts or "\\" in path or ":" in path:
                self.error("publication-inventory", ".", "Git returned a nonrelative path")
            elif any(part.casefold() in LOCAL_DIRECTORIES for part in parts):
                self.error("forbidden-file", path, "Local, private, build or dependency material is a publication candidate")
        return paths

    def scan(self):
        if not self.root.is_dir():
            self.error("repository-root", ".", "Repository root does not exist")
            return
        def walk_error(error):
            self.error("unreadable-directory", ".", type(error).__name__)

        self.candidates = self.publication_candidates()
        candidate_directories = None if self.candidates is None else {
            parent.as_posix() for path in self.candidates for parent in Path(path).parents
        }
        for directory, folders, filenames in os.walk(self.root, followlinks=False, onerror=walk_error):
            folders[:] = sorted(name for name in folders if name.casefold() not in LOCAL_DIRECTORIES
                                and (candidate_directories is None or (Path(directory) / name).relative_to(self.root).as_posix() in candidate_directories))
            for name in folders[:]:
                child = Path(directory) / name
                relative = child.relative_to(self.root).as_posix()
                if name.casefold() in FORBIDDEN_DIRECTORIES:
                    self.error("forbidden-file", relative, "Bulk extracted source does not belong in the public corpus")
                    folders.remove(name)
                    continue
                try:
                    if is_reparse(child) or not child.resolve().is_relative_to(self.root):
                        self.error("public-symlink", relative, "Public symlinks, junctions and reparse directories are not followed")
                        folders.remove(name)
                except (OSError, RuntimeError) as error:
                    self.error("unreadable-directory", relative, type(error).__name__)
                    folders.remove(name)
            for name in sorted(filenames):
                path = Path(directory) / name
                relative = path.relative_to(self.root).as_posix()
                if relative == ".git":
                    continue
                if self.candidates is not None and relative not in self.candidates:
                    continue
                self.files.append(relative)
                try:
                    if linked_ancestor(path, self.root) or not path.resolve().is_relative_to(self.root):
                        self.error("public-symlink", relative, "Public file links require materialized reviewed contents")
                        continue
                    info = path.stat()
                    if not stat.S_ISREG(info.st_mode):
                        self.error("forbidden-file", relative, "Expected a regular public file")
                        continue
                    self.public_file_ids.add((info.st_dev, info.st_ino))
                except (OSError, RuntimeError) as error:
                    self.error("unreadable-file", relative, type(error).__name__)
                    continue
                lower_name = name.casefold()
                if path.suffix.lower() in FORBIDDEN_SUFFIXES or lower_name in {".env", "local.properties", ".npmrc", ".netrc", "credentials.json", "secrets.json", "adbkey"} or lower_name.startswith(".env.") and lower_name != ".env.example":
                    self.error("forbidden-file", relative, "Private binary, key or environment artifact in public corpus")
                if path.suffix.lower() not in TEXT_SUFFIXES:
                    continue
                try:
                    text = path.read_text(encoding="utf-8")
                except (OSError, UnicodeError) as error:
                    self.error("unreadable-text", relative, type(error).__name__)
                    continue
                self.texts[relative] = text
                markers = [
                    r"-----BEGIN (?:[A-Z]+ )*PRIVATE KEY-----",
                    r"\bgh[pousr]_[A-Za-z0-9]{30,}\b",
                    r"\bgithub_pat_[A-Za-z0-9_]{40,}\b",
                    r"\b[A-Za-z]:[\\/]Users[\\/][^\s<>\"']+",
                ]
                if any(re.search(pattern, text) for pattern in markers):
                    self.error("sensitive-content", relative, "Credential or machine-local user-path marker; inspect locally")
                if path.suffix.lower() == ".json":
                    try:
                        self.documents[relative] = json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)
                    except (ValueError, RecursionError) as error:
                        self.error("invalid-json", relative, str(error))
                elif path.suffix.lower() == ".jsonl":
                    for number, line in enumerate(text.splitlines(), 1):
                        if line.strip():
                            try:
                                json.loads(line, object_pairs_hook=unique_object, parse_constant=reject_constant)
                            except (ValueError, RecursionError) as error:
                                self.error("invalid-json", relative, f"Line {number}: {error}")

    def local_path(self, reference, base, origin, code="link-path"):
        if not isinstance(reference, str):
            self.error(code, origin, "Expected a repository-relative POSIX path")
            return None
        decoded = unquote(reference)
        if not decoded or "\x00" in decoded or "\\" in decoded or ":" in decoded or decoded.startswith("/"):
            self.error(code, origin, "Expected a repository-relative POSIX path")
            return None
        lexical = base / decoded
        try:
            if linked_ancestor(lexical, self.root):
                self.error(code, origin, "Reference traverses a symlink, junction or reparse point")
                return None
            candidate = lexical.resolve()
        except (OSError, RuntimeError, ValueError):
            self.error(code, origin, "Cannot resolve local reference")
            return None
        if not candidate.is_relative_to(self.root):
            if origin in {"AGENTS.md", "CLAUDE.md"} and code == "link-path" and re.fullmatch(r"(?:\.\./)+(?:AGENTS\.md|docs/okf/agent-policies/public-project\.md)", decoded):
                return None
            self.error(code, origin, "Reference escapes the public repository")
            return None
        relative = candidate.relative_to(self.root)
        if any(part.casefold() in LOCAL_DIRECTORIES | FORBIDDEN_DIRECTORIES for part in relative.parts):
            self.error(code, origin, "Reference points into excluded local/private material")
            return None
        return candidate

    def link(self, target, origin, base=None):
        if not isinstance(target, str) or not target.strip():
            self.error("missing-source", origin, "Source/link must be a nonempty string")
            return
        target = target.strip().strip("<>")
        try:
            parts = urlsplit(target)
        except ValueError:
            self.error("invalid-link", origin, "Cannot parse URL")
            return
        if parts.scheme in {"http", "https", "mailto"}:
            if parts.scheme != "mailto" and (not parts.hostname or parts.username or parts.password):
                self.error("invalid-link", origin, "HTTP sources need a host and must not contain credentials")
            return
        if parts.scheme or parts.netloc:
            self.error("invalid-link", origin, "Unsupported source/link scheme")
            return
        candidate = self.local_path(parts.path, base or self.root, origin) if parts.path else self.local_path(origin, self.root, origin)
        if candidate is None:
            return
        self.link_count += 1
        if not candidate.exists():
            self.error("missing-link", origin, f"Unresolved local target: {target}")
            return
        relative = candidate.relative_to(self.root).as_posix()
        if self.candidates is not None and relative not in self.candidates and not (
            candidate.is_dir() and any(path.startswith(relative.rstrip("/") + "/") for path in self.candidates)
        ):
            self.error("unpublished-link", origin, f"Target is not a publication candidate: {target}")
            return
        if not parts.fragment:
            return
        fragment = unquote(parts.fragment)
        relative = candidate.relative_to(self.root).as_posix()
        text = self.texts.get(relative)
        if text is None and candidate.is_file():
            try:
                text = candidate.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                pass
        line = re.fullmatch(r"L(\d+)(?:-L?(\d+))?", fragment)
        if line:
            first, last = int(line[1]), int(line[2] or line[1])
            if text is None or not 1 <= first <= last <= len(text.splitlines()):
                self.error("invalid-line-anchor", origin, f"Line range outside target: {target}")
        elif candidate.suffix == ".md" and text is not None:
            if fragment not in markdown_anchors(text):
                self.error("missing-anchor", origin, f"Unresolved Markdown anchor: {target}")
        else:
            self.error("missing-anchor", origin, f"Unsupported local fragment: {target}")

    def markdown(self):
        for path, text in self.texts.items():
            if not path.endswith(".md"):
                continue
            if path.startswith("knowledge/"):
                front = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.DOTALL)
                if not front or any(not re.search(rf"^{key}:\s*\S", front[1], re.MULTILINE) for key in ("type", "title", "description", "tags", "timestamp")):
                    self.error("frontmatter", path, "Knowledge note needs type/title/description/tags/timestamp metadata")
                if front:
                    keys = re.findall(r"^([A-Za-z][\w-]*):", front[1], re.MULTILINE)
                    if any(count > 1 for count in Counter(keys).values()):
                        self.error("frontmatter", path, "Repeated frontmatter key")
                    stamp = re.search(r"^timestamp:[ \t]*(.+)$", front[1], re.MULTILINE)
                    if stamp:
                        self.dated(stamp[1].strip().strip("\"'"), path)
            prose = prose_only(text)
            rendered_prose = re.sub(r"(`+)([^`]*?)\1", "", prose)
            explicit_ids = [html.unescape(value) for value in re.findall(r"\bid=[\"']([^\"']+)[\"']", rendered_prose)]
            if any(count > 1 for count in Counter(explicit_ids).values()):
                self.error("duplicate-anchor", path, "Repeated explicit HTML id")
            definitions = {}
            for match in REFERENCE.finditer(prose):
                key = normalized(match[1])
                if key in definitions:
                    self.error("duplicate-reference", path, f"Repeated reference definition: {match[1]}")
                definitions[key] = match[2] or match[3]
            prose = REFERENCE.sub("", prose)
            prose = re.sub(r"(`+)([^`]*?)\1", "", prose)
            base = (self.root / path).parent
            for target in definitions.values():
                self.link(target, path, base)
            for match in INLINE_LINK.finditer(prose):
                self.link(match[2], path, base)
            remaining = INLINE_LINK.sub("", prose)
            for match in PAIRED_REFERENCE.finditer(remaining):
                key = normalized(match[2] or match[1])
                if key not in definitions:
                    self.error("unresolved-reference", path, f"Undefined reference: {match[2] or match[1]}")
            remaining = PAIRED_REFERENCE.sub("", remaining)
            for match in re.finditer(r"\[([A-Z][A-Z0-9-]*\d[A-Z0-9-]*)\](?![\[(])", remaining):
                if normalized(match[1]) not in definitions:
                    self.error("unresolved-reference", path, f"Undefined source reference: {match[1]}")
            for target in re.findall(r"\b(?:href|src)=[\"']([^\"']+)[\"']", prose):
                self.link(html.unescape(target), path, base)

    def sources(self, value, path):
        if not isinstance(value, list) or not value:
            self.error("missing-source", path, "At least one source is required")
            return
        for source in value:
            self.link(source.get("url") if isinstance(source, dict) else source, path)
            if isinstance(source, dict):
                self.required_text(source, ("url", "evidence_type"), path)
                self.dated(source.get("observed_at"), path)

    def identities(self, records, path):
        found = set()
        for row in records:
            if not self.required_text(row, ("id",), path):
                continue
            identifier = row.get("id")
            if not isinstance(identifier, str):
                continue
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", identifier):
                self.error("invalid-id", path, f"Invalid record ID: {identifier}")
            if identifier in found:
                self.error("duplicate-id", path, f"Repeated ID: {identifier}")
            found.add(identifier)
        return found

    def records(self):
        artifact = self.document("data/artifact.json")
        self.required_text(artifact, ("id", "sha256", "provenance", "evidence_type"), "data/artifact.json")
        self.dated(artifact.get("observed_at"), "data/artifact.json")
        self.strings(artifact, "limitations", "data/artifact.json")
        if artifact.get("evidence_type") != "static-observation":
            self.error("evidence-boundary", "data/artifact.json", "Artifact identity is a static observation")
        if not re.fullmatch(r"[0-9a-f]{64}", str(artifact.get("sha256", ""))):
            self.error("artifact-identity", "data/artifact.json", "Expected a complete SHA-256")
        for path, value in self.documents.items():
            if isinstance(value, dict) and "artifact_sha256" in value:
                if value.get("artifact_sha256") != artifact.get("sha256") or value.get("artifact_id", artifact.get("id")) != artifact.get("id"):
                    self.error("artifact-identity", path, "Supplied-artifact identity does not match data/artifact.json")
        baseline_path = "data/moon-baseline.json"
        baseline = self.document(baseline_path)
        self.dated(baseline.get("observed_at"), baseline_path)
        features = self.items(baseline, "features", baseline_path)
        baseline_ids = self.identities(features, baseline_path)
        for feature in features:
            if not self.required_text(feature, ("id", "title", "evidence_type"), baseline_path):
                continue
            if feature["evidence_type"] not in FEATURE_EVIDENCE_TYPES:
                self.error("evidence-type", baseline_path, "Unknown feature evidence classification")
            self.sources(feature.get("sources"), baseline_path)
            self.strings(feature, "limitations", baseline_path)
        static_path = "evidence/static/observations.json"
        static = self.document(static_path)
        self.dated(static.get("observed_at"), static_path)
        if static.get("evidence_type") != "static-observation":
            self.error("evidence-boundary", static_path, "Static findings must retain their evidence class")
        self.finding_ids = self.identities(self.items(static, "findings", static_path), static_path)
        for finding in self.items(static, "findings", static_path):
            if self.required_text(finding, ("id", "title"), static_path):
                self.strings(finding, "observed", static_path)
                self.strings(finding, "unknown", static_path)
                self.items(finding, "evidence", static_path)
        baseline_ids |= self.finding_ids
        self.document("data/apk-structure.json")
        applications = {"moonreader"}
        for filename in ("alternatives-android", "alternatives-desktop-web", "commercial-alternatives"):
            path = f"data/{filename}.json"
            value = self.document(path)
            self.dated(value.get("observed_at"), path)
            entries = self.items(value, "alternatives", path)
            ids = self.identities(entries, path)
            if applications.intersection(ids):
                self.error("duplicate-id", path, "Application ID is already declared in another inventory")
            applications |= ids
            self.counts["alternatives"] += len(entries)
            for entry in entries:
                if not self.required_text(entry, ("id", "name", "license", "evidence_type"), path):
                    continue
                self.strings(entry, "platforms", path)
                self.strings(entry, "formats", path)
                if filename != "commercial-alternatives":
                    if not re.fullmatch(r"[0-9a-f]{40}", str(entry.get("commit", ""))):
                        self.error("source-revision", path, f"{entry.get('id')}: expected a full source commit")
                    self.link(entry.get("repository"), path)
                self.sources(entry.get("sources"), path)
                self.strings(entry, "limitations", path)
                for feature in self.items(entry, "features", path):
                    if self.required_text(feature, ("name", "evidence_type", "source_url"), path):
                        if feature["evidence_type"] not in FEATURE_EVIDENCE_TYPES:
                            self.error("evidence-type", path, "Unknown feature evidence classification")
                        self.link(feature.get("source_url"), path)
                if isinstance(entry.get("report_path"), str):
                    self.link(entry["report_path"], path)
        self.applications = applications
        all_proposal_ids = set()
        for filename in ("moon-improvements", "alternative-proposals-android", "alternative-proposals-desktop-web"):
            path = f"data/{filename}.json"
            value = self.document(path)
            self.dated(value.get("observed_at"), path)
            entries = self.items(value, "proposals", path)
            identifiers = self.identities(entries, path)
            if identifiers & all_proposal_ids:
                self.error("duplicate-id", path, "Proposal ID is already declared in another backlog")
            all_proposal_ids |= identifiers
            is_moon = filename == "moon-improvements"
            self.counts["moon_proposals" if is_moon else "alternative_proposals"] += len(entries)
            if is_moon and len(entries) < 50:
                self.error("proposal-count", path, "At least fifty Moon proposals are required")
            outcomes, titles = set(), set()
            for entry in entries:
                fields = ("id", "title", "application_id", "priority", "evidence_type", "status")
                if not self.required_text(entry, fields, path):
                    continue
                pattern = r"MOON-(?!000)[0-9]{3}" if is_moon else r"ALT-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*"
                if not re.fullmatch(pattern, entry["id"]):
                    self.error("invalid-id", path, f"Invalid proposal ID: {entry['id']}")
                if entry.get("application_id") not in applications or is_moon and entry.get("application_id") != "moonreader":
                    self.error("unknown-application", path, f"Invalid target for {entry.get('id')}")
                if entry.get("evidence_type") != "proposal" or entry.get("status") != "draft":
                    self.error("proposal-status", path, "Backlogs contain draft proposals, not test results or delivered fixes")
                if entry.get("priority") not in {"high", "medium", "low"}:
                    self.error("proposal-priority", path, "Expected high, medium or low priority")
                self.sources(entry.get("sources"), path)
                for field in ("acceptance_criteria", "limitations"):
                    for item in self.items(entry, field, path):
                        if not isinstance(item, str) or not item.strip():
                            self.error("required-field", path, f"Empty {field} item in {entry.get('id')}")
                if is_moon:
                    if not self.required_text(entry, ("category", "relationship_to_baseline", "existing_capability", "rationale", "requested_change"), path):
                        continue
                    if entry.get("relationship_to_baseline") not in {"extension", "reliability-candidate", "new-capability-candidate"}:
                        self.error("baseline-relationship", path, "Unknown relationship to the existing baseline")
                    for reference in self.items(entry, "baseline_refs", path):
                        if not isinstance(reference, str) or reference not in baseline_ids:
                            self.error("unknown-baseline", path, f"Unresolved baseline for {entry.get('id')}")
                    outcome = normalized(entry.get("requested_change", ""))
                    if outcome in outcomes:
                        self.error("duplicate-outcome", path, "Repeated requested outcome after whitespace/case normalization")
                    outcomes.add(outcome)
                else:
                    self.required_text(entry, ("basis",), path)
                title = normalized(entry.get("title", ""))
                if title in titles:
                    self.error("duplicate-title", path, "Repeated proposal title")
                titles.add(title)

    def metadata(self):
        """Validate declared metadata without dereferencing intentionally withheld paths."""
        artifact = self.document("data/artifact.json")
        for path, document in self.documents.items():
            stack = [(document, None)]
            while stack:
                value, inherited_type = stack.pop()
                if isinstance(value, list):
                    stack.extend((item, inherited_type) for item in value)
                    continue
                if not isinstance(value, dict):
                    continue
                evidence_type = value.get("evidence_type", inherited_type)
                if "evidence_type" in value and (not isinstance(evidence_type, str) or evidence_type not in EVIDENCE_TYPES):
                    self.error("evidence-type", path, "Unknown evidence classification")
                non_application = isinstance(evidence_type, str) and evidence_type in HOST_EVIDENCE_TYPES | {"static-observation", "documented", "proposal", "unknown", "blocked", "upstream-report"}
                for key, item in value.items():
                    if key in PUBLIC_REFERENCE_KEYS or key.endswith("_evidence_path"):
                        self.link(item, path)
                    elif key == "source_url" and item is not None:
                        self.link(item, path)
                    elif key in {"observed_at", "observed_on", "observed_at_utc", "retrieved_at"}:
                        self.dated(item, path)
                    elif key == "sha256" or key.endswith("_sha256") or key in {"test_source_sha256_lf", "test_plan_sha256_at_curation"}:
                        if item is not None:
                            self.digest(item, path)
                    elif key in COMMIT_KEYS and item is not None:
                        self.revision(item, path)
                    elif key in {"finding_ids", "updated_finding_ids"}:
                        for identifier in self.strings(value, key, path):
                            if identifier not in self.finding_ids:
                                self.error("unknown-reference", path, f"Undeclared finding: {identifier}")
                    elif key in {"application_executed", "application_tests_executed", "moon_reader_tested", "application_runtime_executed"}:
                        if not isinstance(item, bool):
                            self.error("record-shape", path, f"Expected boolean: {key}")
                        elif item and non_application:
                            self.error("evidence-boundary", path, "Non-application evidence cannot claim application execution")
                    elif key in {"source", "record", "observations", "provenance", "evidence"} and isinstance(item, str) and re.match(r"^(?:data|knowledge|evidence|fixtures|scripts|tests)/", item):
                        self.link(item, path)
                    elif key in {"sources", "source_urls", "evidence"} and isinstance(item, list):
                        for reference in item:
                            if isinstance(reference, str):
                                self.link(reference, path)
                if "artifact_id" in value and value["artifact_id"] != artifact.get("id"):
                    self.error("artifact-identity", path, "Supplied-artifact ID does not match data/artifact.json")
                if "artifact_sha256" in value and value["artifact_sha256"] != artifact.get("sha256"):
                    self.error("artifact-identity", path, "Supplied-artifact digest does not match data/artifact.json")
                stack.extend((item, evidence_type) for item in value.values() if isinstance(item, (dict, list)))

    def contributions(self):
        found = set()
        self.counts["contributions"] = 0
        for path in self.files:
            if not path.startswith("data/contributions/") or not path.endswith(".json"):
                continue
            value = self.document(path)
            identifiers = self.identities([value], path)
            if identifiers & found:
                self.error("duplicate-id", path, "Contribution ID is already declared")
            found |= identifiers
            self.counts["contributions"] += 1
            fields = ("id", "app_id", "observed_at", "evidence_type", "evidence_scope", "upstream_url", "upstream_revision", "summary", "status")
            if not self.required_text(value, fields, path):
                continue
            if value["app_id"] not in self.applications:
                self.error("unknown-application", path, "Contribution target is not in the application inventory")
            self.revision(value["upstream_revision"], path)
            self.link(value["upstream_url"], path)
            self.sources(value.get("source_urls"), path)
            self.strings(value, "limitations", path)
            if value["status"] not in {"proposed", "implemented", "implemented-tested", "submitted", "merged"}:
                self.error("contribution-status", path, "Unknown contribution state")
            if value["status"] != "proposed":
                self.revision(value.get("commit"), path)
            if value["status"] in {"implemented-tested", "submitted", "merged"}:
                for check in self.items(value, "verification", path):
                    if self.required_text(check, ("name", "evidence_path"), path):
                        self.link(check["evidence_path"], path)
            if "publication" in value:
                publication = value["publication"]
                if not self.required_text(publication, ("status",), path):
                    continue
                if publication["status"] not in {"not-published", "pushed-to-fork", "submitted", "merged"}:
                    self.error("contribution-status", path, "Unknown publication state")
                if publication["status"] == "pushed-to-fork":
                    self.revision(publication.get("verified_commit"), path)
                    if publication.get("verified_commit") != value.get("commit"):
                        self.error("source-revision", path, "Published commit differs from the contribution commit")

    def hash_file(self, reference, expected, origin, base=None, code="evidence-hash", size=None):
        candidate = self.local_path(reference, base or self.root, origin, "fixture-path" if code == "fixture-hash" else "evidence-path")
        if candidate is None:
            return
        if self.candidates is not None and candidate.relative_to(self.root).as_posix() not in self.candidates:
            self.error("unpublished-link", origin, f"Hashed input is not a publication candidate: {reference}")
            return
        if not self.digest(expected, origin):
            return
        if size is not None and (type(size) is not int or size < 0):
            self.error("record-shape", origin, "Expected a nonnegative integer byte size")
            return
        try:
            if not stat.S_ISREG(candidate.stat().st_mode):
                raise OSError("Not a regular file")
            content = candidate.read_bytes()
        except OSError:
            self.error(code, origin, f"Hashed input unavailable: {reference}")
            return
        self.hash_count += 1
        if hashlib.sha256(content).hexdigest() != expected or size is not None and len(content) != size:
            self.error(code, origin, f"Hash or size mismatch: {reference}")
            return None
        return candidate

    def hash_rows(self, value, key, path, nonempty=True):
        checked = []
        for item in self.items(value, key, path, nonempty):
            if not self.required_text(item, ("sha256",), path):
                continue
            reference = item.get("path", item.get("file"))
            if not isinstance(reference, str) or not reference.strip():
                self.error("required-field", path, f"Each {key} item needs a path or file")
                continue
            candidate = self.hash_file(reference, item["sha256"], path, size=item.get("size_bytes"))
            if candidate is not None:
                checked.append(candidate)
        return checked

    def fixtures_and_receipts(self):
        fixture_ids = set()
        for path, base in (("fixtures/manifest.json", self.root / "fixtures"), ("data/scenario-fixtures.json", self.root)):
            value = self.document(path)
            entries = self.items(value, "fixtures", path, nonempty=path.startswith("fixtures/"))
            identifiers = self.identities(entries, path)
            if identifiers & fixture_ids:
                self.error("duplicate-id", path, "Fixture ID is already declared in another manifest")
            fixture_ids |= identifiers
            for entry in entries:
                if self.required_text(entry, ("id", "path", "sha256"), path):
                    self.hash_file(entry["path"], entry["sha256"], path, base, "fixture-hash", entry.get("size_bytes"))
                    self.counts["fixtures"] += 1
                    candidate = self.local_path(entry["path"], base, path, "fixture-path")
                    if candidate is not None:
                        self.fixture_records[entry["id"]] = (candidate.relative_to(self.root).as_posix(), entry["sha256"])
            if "generator_sha256" in value:
                origin = value.get("origin")
                if self.required_text(origin, ("source",), path):
                    self.hash_file(origin["source"], value["generator_sha256"], path)
            font = value.get("unicode_font")
            if isinstance(font, dict) and "license_sha256" in font:
                self.hash_file(font.get("license_path"), font["license_sha256"], path, base)
        for path, value in self.documents.items():
            if path.startswith("evidence/reviews/") or path == "evidence/runtime/verification.json":
                self.hash_rows(value, "inputs", path)
            if path == "evidence/fixture-verification.json":
                artifacts = value.get("artifacts") if isinstance(value, dict) else None
                if not isinstance(artifacts, dict) or not artifacts:
                    self.error("record-shape", path, "Expected nonempty artifacts object")
                    continue
                for key, item in artifacts.items():
                    if isinstance(item, dict):
                        if self.required_text(item, ("path", "sha256"), path):
                            self.hash_file(item["path"], item["sha256"], path)
                    elif key.endswith("_sha256"):
                        self.digest(item, path)
                    elif isinstance(item, str) and key + "_sha256" in artifacts:
                        self.hash_file(item, artifacts[key + "_sha256"], path)
                    elif isinstance(item, str):
                        self.link(item, path)
                    else:
                        self.error("record-shape", path, "Invalid fixture artifact reference")
            if path == "evidence/scenario-fixture-verification.json":
                hashes = value.get("artifact_hashes") if isinstance(value, dict) else None
                if not isinstance(hashes, dict) or not hashes:
                    self.error("record-shape", path, "Expected nonempty artifact_hashes object")
                    continue
                for reference, expected in hashes.items():
                    self.hash_file(reference, expected, path)
                self.hash_rows(value, "input_hashes", path)
        latest_static = "evidence/static/bounded-followup-verification.json" if "evidence/static/bounded-followup-verification.json" in self.documents else "evidence/static/verification.json"
        if latest_static in self.files:
            self.hash_rows(self.document(latest_static), "checked_public_files", latest_static)

    def runtime(self):
        path = "data/runtime-results.json"
        if path not in self.files:
            self.pending.append({"path": path, "message": "Application-result integration is absent; no runtime coverage inferred"})
            return
        value = self.document(path)
        self.required_text(value, ("id", "observed_at", "evidence_type", "artifact_id", "artifact_sha256", "test_plan", "test_plan_sha256_at_curation", "evidence_manifest", "report_path"), path)
        if value.get("evidence_type") != "runtime-observation":
            self.error("evidence-boundary", path, "Runtime records must identify their evidence class")
        self.hash_file(value.get("test_plan"), value.get("test_plan_sha256_at_curation"), path)
        self.strings(value, "limitations", path)
        environment = value.get("environment")
        environment_id = environment.get("id") if isinstance(environment, dict) else None
        if not isinstance(environment_id, str) or not environment_id:
            self.error("record-shape", path, "Runtime environment needs an ID")
        cases = self.items(value, "cases", path)
        identifiers = self.identities(cases, path)
        if identifiers != {f"RT-{i:02}" for i in range(1, 37)} or len(cases) != 36:
            self.error("runtime-coverage", path, "Expected one record for each RT-01 through RT-36")
        counts = Counter()
        for case in cases:
            fields = ("id", "title", "status", "evidence_type", "artifact_sha256", "environment_id", "observed_at", "source_url", "expected", "actual")
            if not self.required_text(case, fields, path):
                continue
            status = case["status"]
            if status not in RUNTIME_STATUSES:
                self.error("runtime-status", path, "Unknown runtime case state")
                continue
            counts[status] += 1
            executed = status in {"pass", "partial", "fail"}
            expected_type = "runtime-observation" if executed else "blocked" if status == "blocked" else "unknown"
            if case["evidence_type"] != expected_type:
                self.error("evidence-boundary", path, f"{case['id']}: classification disagrees with execution state")
            if case["environment_id"] != environment_id:
                self.error("unknown-reference", path, f"{case['id']}: undeclared environment")
            self.strings(case, "limitations", path)
            for evidence in self.strings(case, "evidence", path, nonempty=executed):
                self.link(evidence, path)
            steps = self.items(case, "steps", path, nonempty=executed)
            for number, step in enumerate(steps, 1):
                if self.required_text(step, ("action",), path) and (type(step.get("number")) is not int or step["number"] != number):
                    self.error("record-shape", path, f"{case['id']}: steps must be numbered consecutively")
            for item in self.items(case, "inputs", path, nonempty=False):
                if self.required_text(item, ("id", "path", "sha256"), path):
                    if self.fixture_records.get(item["id"]) != (item["path"], item["sha256"]):
                        self.error("fixture-identity", path, f"{case['id']}: input differs from the canonical fixture identity")
                    self.hash_file(item["path"], item["sha256"], path)
            subchecks = self.items(case, "subchecks", path, nonempty=executed)
            self.identities(subchecks, path)
            sub_statuses = set()
            for subcheck in subchecks:
                if not self.required_text(subcheck, ("id", "status", "actual"), path):
                    continue
                sub_statuses.add(subcheck["status"])
                if subcheck["status"] not in RUNTIME_STATUSES:
                    self.error("runtime-status", path, "Unknown subcheck state")
                if status == "pass" and subcheck["status"] != "pass":
                    self.error("runtime-status", path, "Passing case contains incomplete or failed subchecks")
                for evidence in self.strings(subcheck, "evidence", path, nonempty=False):
                    self.link(evidence, path)
            if status == "fail" and "fail" not in sub_statuses:
                self.error("runtime-status", path, "Failed case needs a failed subcheck")
            if status == "partial" and ("pass" not in sub_statuses or not sub_statuses.intersection({"not-run", "blocked", "partial"}) or "fail" in sub_statuses):
                self.error("runtime-status", path, "Partial case needs successful and incomplete subchecks, without a hidden failure")
            if not executed and sub_statuses.intersection({"pass", "partial", "fail"}):
                self.error("runtime-status", path, "Unexecuted case contains executed subchecks")
        summary = value.get("summary")
        if not isinstance(summary, dict):
            self.error("record-shape", path, "Expected a runtime summary object")
        else:
            expected = {**{status: counts[status] for status in RUNTIME_STATUSES}, "total": len(cases), "executed_at_least_in_part": sum(counts[status] for status in ("pass", "partial", "fail"))}
            for key, count in expected.items():
                if type(summary.get(key)) is not int or summary[key] != count:
                    self.error("runtime-count", path, f"Summary disagrees with case records: {key}")
        self.counts["runtime_cases"] = len(cases)
        for status in sorted(RUNTIME_STATUSES):
            self.counts[f"runtime_{status}"] = counts[status]
        manifest_path = value.get("evidence_manifest")
        bound_evidence = set()
        if isinstance(manifest_path, str):
            manifest = self.document(manifest_path)
            checked = self.hash_rows(manifest, "files", manifest_path)
            bound_evidence.update(checked)
            files = self.items(manifest, "files", manifest_path)
            references = [item["path"] for item in files if isinstance(item, dict) and isinstance(item.get("path"), str)]
            if len(set(references)) != len(references) or len(bound_evidence) != len(checked):
                self.error("duplicate-reference", manifest_path, "Repeated runtime evidence file")
            if type(manifest.get("file_count")) is not int or manifest["file_count"] != len(files):
                self.error("runtime-count", manifest_path, "Manifest file count disagrees with its entries")
        stack = [value]
        while stack:
            item = stack.pop()
            if isinstance(item, list):
                stack.extend(item)
            elif isinstance(item, dict):
                if "path" in item and "sha256" in item:
                    self.hash_file(item["path"], item["sha256"], path)
                if "evidence" in item:
                    for reference in self.strings(item, "evidence", path, nonempty=False):
                        self.link(reference, path)
                        try:
                            parts = urlsplit(reference.strip().strip("<>"))
                        except ValueError:
                            continue
                        if parts.scheme or parts.netloc:
                            self.error("unbound-evidence", path, "Retained runtime evidence must be a local manifest file; external citations belong in source_url")
                            continue
                        candidate = self.local_path(parts.path or path, self.root, path, "evidence-path")
                        if candidate is not None and candidate not in bound_evidence:
                            self.error("unbound-evidence", path, f"Runtime evidence has no checked manifest digest: {reference}")
                stack.extend(child for child in item.values() if isinstance(child, (dict, list)))
        cleanup = value.get("cleanup")
        if self.required_text(cleanup, ("status", "receipt"), path):
            self.link(cleanup["receipt"], path)
            receipt = self.document(cleanup["receipt"])
            if cleanup["status"] != receipt.get("status"):
                self.error("runtime-status", path, "Cleanup summary disagrees with its receipt")

    def prepare_output(self, destination):
        self.output = None
        if destination is None:
            return
        try:
            lexical = destination.absolute()
            if linked_ancestor(lexical):
                raise ValueError("Output traverses a symlink, junction or reparse point")
            candidate = lexical.resolve()
            if candidate.is_relative_to(self.root) and candidate.relative_to(self.root).parts[:1] != (".local",):
                raise ValueError("In-repository receipts must be written under .local, never into the public corpus")
            if candidate.exists():
                info = candidate.stat()
                if not stat.S_ISREG(info.st_mode):
                    raise ValueError("Output must be a regular file")
                if (info.st_dev, info.st_ino) in self.public_file_ids:
                    raise ValueError("Output aliases an examined public input")
            self.output = candidate
        except (OSError, RuntimeError, ValueError) as error:
            self.error("output-path", "--output", str(error) if isinstance(error, ValueError) else type(error).__name__)

    def write_report(self, rendered):
        destination = self.output
        self.prepare_output(destination)
        if self.output is None:
            return
        temporary = None
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=destination.parent, prefix=".reader-validation-", suffix=".tmp", delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(rendered)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, destination)
        except OSError as error:
            self.error("output-write", "--output", type(error).__name__)
        finally:
            if temporary is not None:
                try:
                    temporary.unlink(missing_ok=True)
                except OSError as error:
                    self.error("output-write", "--output", type(error).__name__)

    def run(self, output=None):
        self.scan()
        for path in ("README.md", "LICENSE", "AGENTS.md", "CLAUDE.md", "knowledge/index.md", "knowledge/bundle.md", "knowledge/design.md", "knowledge/methodology.md", "knowledge/coverage.md", "knowledge/reporting.md", "knowledge/feature-matrix.md", "knowledge/moon-improvements.md", "knowledge/testing-plan.md"):
            if path not in self.files:
                self.error("required-document", path, "Required public document is missing")
        if "CLAUDE.md" in self.texts and self.texts["CLAUDE.md"] != "@AGENTS.md\n":
            self.error("instruction-adapter", "CLAUDE.md", "Expected the one-line AGENTS.md import")
        self.records()
        self.metadata()
        self.contributions()
        self.markdown()
        self.fixtures_and_receipts()
        self.runtime()
        self.prepare_output(output)
        return self.report()

    def report(self):
        return {
            "schema_version": 1,
            "evidence_type": "repository-validation",
            "observed_at": self.observed_at,
            "status": "fail" if self.errors else "pending" if self.pending else "pass",
            "application_tests_executed": False,
            "publication_inventory": self.inventory_mode,
            "summary": {**self.counts, "public_files": len(self.files), "json_files": len(self.documents), "local_links_checked": self.link_count, "file_hashes_checked": self.hash_count, "errors": len(self.errors)},
            "errors": self.errors,
            "pending": self.pending,
            "limitations": [
                "Offline validation of public files, record contracts, references and selected evidence hashes; not a reader application test.",
                "External URLs are checked syntactically, not fetched. Markdown parsing covers the corpus's inline/reference links, ATX/setext headings and explicit anchors, not all CommonMark extensions.",
                "Normalized outcome uniqueness detects exact duplicates, not semantic padding; independent content review supplies that judgment.",
                "Private raw evidence is excluded. Initial static verification is historical when the bounded-follow-up verification is present; current checks bind the latter's selected public inputs.",
                "Credential/path checks are bounded markers, not a comprehensive secret scan or legal determination.",
                "Runtime validation checks record completeness, identities, references and arithmetic, not the truth of screenshots or application behavior. Missing runtime integration is reported as pending.",
                "Filesystem checks reject existing symlink/junction and output/input aliases; concurrent malicious filesystem mutation is outside this offline check's scope.",
            ],
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", help="Emit JSON (also the default)")
    args = parser.parse_args()
    validator = Validator(args.root)
    report = validator.run(args.output)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if validator.output is not None:
        validator.write_report(rendered)
        report = validator.report()
        rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    print(rendered, end="")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
