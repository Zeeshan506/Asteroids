from pathlib import Path
import pytest
from scripts.check_line_counts import audit_directory, count_file_lines


def test_repository_files_conform_to_line_limit():
    repo_root = Path(__file__).resolve().parent.parent
    violations, total_scanned, max_seen = audit_directory(repo_root, max_lines=300)

    assert total_scanned > 0, "Audit must scan at least one source or spec file"
    assert (
        len(violations) == 0
    ), f"The following files exceed 300 lines: {[str(p) for p, _ in violations]}"
    assert max_seen <= 300


def test_line_count_audit_detects_violations(tmp_path: Path):
    oversized_file = tmp_path / "oversized.py"
    with open(oversized_file, "w", encoding="utf-8") as f:
        for i in range(350):
            f.write(f"# line {i}\n")

    violations, total_scanned, max_seen = audit_directory(tmp_path, max_lines=300)
    assert total_scanned == 1
    assert len(violations) == 1
    assert violations[0][0] == oversized_file
    assert violations[0][1] == 350
    assert max_seen == 350


def test_line_count_audit_ignores_excluded_directories(tmp_path: Path):
    venv_dir = tmp_path / ".venv"
    venv_dir.mkdir()
    large_in_venv = venv_dir / "large.py"
    with open(large_in_venv, "w", encoding="utf-8") as f:
        for i in range(500):
            f.write(f"# venv line {i}\n")

    violations, total_scanned, max_seen = audit_directory(tmp_path, max_lines=300)
    assert total_scanned == 0
    assert len(violations) == 0
