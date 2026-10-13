#!/usr/bin/env python3
"""Lint changed RFC documents. Untouched legacy RFCs are migrated incrementally."""
from __future__ import annotations
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
RFC_DIR = ROOT / "rfcs"
REQUIRED_METADATA = ("Status:", "Category:", "Scope:", "Created:", "Requires:", "Updates:", "Obsoletes:", "Threats addressed:")
REQUIRED_SECTIONS = (
    "## Abstract", "## Motivation", "## Terminology", "## Specification",
    "## 2flow interaction", "## Security considerations",
    "## Privacy considerations", "## Backward compatibility",
    "## Conformance", "## References",
)

def changed_rfc_paths() -> list[pathlib.Path]:
    base = os.environ.get("RFC_LINT_BASE")
    if base:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base}...HEAD"],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        if result.returncode == 0:
            return [ROOT / p for p in result.stdout.splitlines()
                    if p.startswith("rfcs/") and p.endswith(".md") and (ROOT / p).is_file()]
    return sorted(RFC_DIR.glob("RFC-*.md"))

def lint(path: pathlib.Path) -> list[str]:
    content = path.read_text(encoding="utf-8")
    errors = []
    for item in REQUIRED_METADATA:
        if not re.search(r"(?m)^-?\s*" + re.escape(item), content):
            errors.append(f"{path.relative_to(ROOT)}: missing metadata {item}")
    for section in REQUIRED_SECTIONS:
        if section not in content:
            errors.append(f"{path.relative_to(ROOT)}: missing section {section}")
    return errors

def main() -> int:
    paths = changed_rfc_paths()
    errors = [error for path in paths for error in lint(path)]
    if errors:
        print("\n".join(errors))
        return 1
    print(f"RFC lint passed for {len(paths)} changed document(s).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
