import pytest

from pilepack.ignorer import load_spec
from pilepack.suggestions import find_large_files, generate_ignore_content


def test_generate_ignore_content_safe_mode(test_project):
    content = generate_ignore_content(test_project, mode="safe")
    assert "venv/" in content
    assert "__pycache__/" in content
    assert "*.log" in content
    # assets are present only as commented hints in safe mode
    assert "# static/" in content


def test_generate_ignore_content_includes_secrets(test_project):
    content = generate_ignore_content(test_project, mode="safe")
    assert ".env" in content
    assert "*.pem" in content
    assert "*.key" in content


def test_generate_ignore_content_aggressive_mode(test_project):
    content = generate_ignore_content(test_project, mode="aggressive")
    assert "\nstatic/" in content
    assert "\nmedia/" in content


def test_find_large_files(test_project):
    big = test_project / "big.bin"
    big.write_bytes(b"x" * (200 * 1024))
    found = find_large_files(test_project, threshold=100 * 1024)
    assert "big.bin" in found


def test_find_large_files_skips_small(test_project):
    small = test_project / "small.txt"
    small.write_text("hello")
    found = find_large_files(test_project, threshold=100 * 1024)
    assert "small.txt" not in found


def test_find_large_files_respects_spec(test_project):
    ignored_dir = test_project / "ignored"
    ignored_dir.mkdir()
    big = ignored_dir / "big.bin"
    big.write_bytes(b"x" * (200 * 1024))
    (test_project / ".gitignore").write_text("ignored/\n")

    found = find_large_files(
        test_project, threshold=100 * 1024, spec=load_spec(test_project)
    )

    assert "ignored/big.bin" not in found


def test_generate_ignore_content_aggressive_skips_ignored_large_files(test_project):
    venv = test_project / "venv"
    venv.mkdir()
    big = venv / "lib.bin"
    big.write_bytes(b"x" * (200 * 1024))
    (test_project / ".gitignore").write_text("venv/\n")

    content = generate_ignore_content(test_project, mode="aggressive")

    assert "venv/lib.bin" not in content


def test_find_large_files_skips_symlinks(test_project, tmp_path):
    outside = tmp_path / "outside.bin"
    outside.write_bytes(b"x" * (200 * 1024))
    link = test_project / "linked.bin"
    try:
        link.symlink_to(outside)
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"symlinks are not supported here: {exc}")

    found = find_large_files(test_project, threshold=100 * 1024)

    assert "linked.bin" not in found
