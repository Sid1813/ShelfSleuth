# Load and validate business knowledge from the ShelfSleuth OKF bundle

from pathlib import Path

import yaml


# Locate the OKF bundle containing this file

OKF_DIR = Path(__file__).resolve().parent


# Reserved OKF documents that are not treated as concept documents

RESERVED_FILES = {
    "index.md",
    "log.md",
}


def _parse_document(path):
    """
    Parse one OKF Markdown concept document.

    A concept document must contain YAML frontmatter
    followed by a non-empty Markdown body.
    """

    text = path.read_text(encoding="utf-8")

    # Concept documents must begin with YAML frontmatter.

    if not text.startswith("---"):
        raise ValueError(
            f"OKF document '{path}' is missing YAML frontmatter."
        )

    # Split only on the YAML frontmatter delimiters.

    parts = text.split("---", 2)

    if len(parts) != 3:
        raise ValueError(
            f"OKF document '{path}' has invalid frontmatter."
        )

    frontmatter = yaml.safe_load(parts[1])

    # Frontmatter must be a YAML mapping.

    if not isinstance(frontmatter, dict):
        raise ValueError(
            f"OKF document '{path}' must contain YAML metadata."
        )

    # 'type' is the required concept metadata field.

    if not frontmatter.get("type"):
        raise ValueError(
            f"OKF document '{path}' is missing required 'type' metadata."
        )

    # The remaining content is the Markdown concept body.

    body = parts[2].strip()

    if not body:
        raise ValueError(
            f"OKF document '{path}' has an empty Markdown body."
        )

    return {
        "metadata": frontmatter,
        "content": body,
    }


def load_okf_knowledge():
    """
    Load all OKF concept documents from the bundle.

    Markdown files are discovered recursively so the loader
    can support a hierarchical OKF bundle.

    Reserved documents such as index.md and log.md are
    excluded from the returned concept collection.
    """

    knowledge = {}

    # Recursively discover Markdown documents in the OKF bundle.

    markdown_files = sorted(OKF_DIR.rglob("*.md"))

    for path in markdown_files:

        # Skip reserved OKF documents regardless of directory depth.

        if path.name in RESERVED_FILES:
            continue

        # Parse and validate the concept document.

        concept = _parse_document(path)

        # Use the path relative to the OKF bundle as the concept key.

        relative_path = path.relative_to(OKF_DIR)

        concept_key = relative_path.with_suffix("").as_posix()

        # Preserve the existing simple keys for root-level concepts.

        if "/" not in concept_key:
            concept_key = concept_key.replace("-", "_")

        knowledge[concept_key] = concept

    return knowledge