#!/usr/bin/env python3
"""Modularity audit script enforcing <= 300 lines limit per source/spec file."""

import argparse
from pathlib import Path
import sys

DEFAULT_MAX_LINES = 300
DEFAULT_EXTENSIONS = {".py", ".md"}
EXCLUDED_DIRS = {
    ".git",
    ".venv",
    ".agents",
    "__pycache__",
    "build",
    "dist",
    ".pytest_cache",
}


def count_file_lines(file_path: Path) -> int:
    """Counts non-empty lines or total lines in a file."""
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        return sum(1 for _ in f)


def audit_directory(
    root_path: Path,
    max_lines: int = DEFAULT_MAX_LINES,
    extensions: set[str] | None = None,
) -> tuple[list[tuple[Path, int]], int, int]:
    """Audits files in root_path.

    Returns:
        (violations, total_files_scanned, max_line_count_seen)
    """
    if extensions is None:
        extensions = DEFAULT_EXTENSIONS

    violations: list[tuple[Path, int]] = []
    total_files = 0
    max_seen = 0

    for path in root_path.rglob("*"):
        if not path.is_file():
            continue
        # Skip if any parent part is in EXCLUDED_DIRS
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.suffix not in extensions:
            continue

        total_files += 1
        line_count = count_file_lines(path)
        if line_count > max_seen:
            max_seen = line_count
        if line_count > max_lines:
            violations.append((path, line_count))

    return violations, total_files, max_seen


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit source files against maximum line count constraint."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Root path to audit (default: current directory).",
    )
    parser.add_argument(
        "--max-lines",
        type=int,
        default=DEFAULT_MAX_LINES,
        help=f"Maximum allowed lines per file (default: {DEFAULT_MAX_LINES}).",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    violations, total_files, max_seen = audit_directory(root, args.max_lines)

    print(f"Auditing repository modularity at: {root}")
    print(f"Total files audited: {total_files}")
    print(f"Maximum line count found: {max_seen} (limit: {args.max_lines})")

    if violations:
        print("\n[FAILURE] The following files exceed the modularity limit:")
        for path, count in violations:
            rel = path.relative_to(root) if path.is_relative_to(root) else path
            print(f"  - {rel}: {count} lines (exceeds {args.max_lines})")
        return 1

    print("\n[SUCCESS] All files strictly conform to the modularity constraints.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
