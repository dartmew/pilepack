import sys
from io import StringIO

import pytest

from pilepack.cli import _stream_report, main


def test_stream_report_no_content(test_project):
    stream = StringIO()
    _stream_report(test_project, stream, include_content=False, fmt="txt")
    output = stream.getvalue()
    assert "--- FILE:" not in output
    assert "test_project" in output
    assert "main.py" in output


def test_cli_basic(test_project, capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["pilepack", str(test_project), "--no-content"])
    main()
    captured = capsys.readouterr()
    assert "test_project" in captured.out
    assert "main.py" in captured.out
    assert "--- FILE:" not in captured.out


def test_cli_output_file(test_project, tmp_path, monkeypatch):
    out_file = tmp_path / "report.txt"
    monkeypatch.setattr(
        sys, "argv", ["pilepack", str(test_project), "-o", str(out_file)]
    )
    main()
    assert out_file.exists()
    content = out_file.read_text()
    assert "main.py" in content


def test_cli_follow_symlinks_flag(test_project, tmp_path, monkeypatch, capsys):
    outside_file = tmp_path / "outside.txt"
    outside_file.write_text("outside")
    link = test_project / "linked-outside.txt"
    try:
        link.symlink_to(outside_file)
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"symlinks are not supported here: {exc}")

    monkeypatch.setattr(
        sys,
        "argv",
        ["pilepack", str(test_project), "--no-content", "--follow-symlinks"],
    )
    main()

    captured = capsys.readouterr()

    assert "linked-outside.txt" in captured.out


def test_cli_invalid_dir(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["pilepack", "/nonexistent"])
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "not a valid directory" in captured.err


def test_cli_init_ignore_creates_file(test_project, capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["pilepack", str(test_project), "--init-ignore"])
    main()
    pilignor = test_project / ".pilignor"
    assert pilignor.exists()
    assert "venv/" in pilignor.read_text()


def test_cli_init_ignore_does_not_overwrite_without_force(
    test_project, capsys, monkeypatch
):
    pilignor = test_project / ".pilignor"
    pilignor.write_text("custom/\n")
    monkeypatch.setattr(sys, "argv", ["pilepack", str(test_project), "--init-ignore"])
    main()
    captured = capsys.readouterr()
    assert pilignor.read_text() == "custom/\n"
    assert "already exists" in captured.err


def test_cli_init_ignore_overwrites_with_force(test_project, monkeypatch):
    pilignor = test_project / ".pilignor"
    pilignor.write_text("custom/\n")
    monkeypatch.setattr(
        sys, "argv", ["pilepack", str(test_project), "--init-ignore", "--force"]
    )
    main()
    assert "venv/" in pilignor.read_text()


def test_cli_init_ignore_aggressive_mode(test_project, monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        ["pilepack", str(test_project), "--init-ignore", "-m", "aggressive"],
    )
    main()
    content = (test_project / ".pilignor").read_text()
    assert "static/" in content


def test_cli_no_pilignor_flag(test_project, capsys, monkeypatch):
    (test_project / ".pilignor").write_text("main.py\n")
    monkeypatch.setattr(
        sys, "argv", ["pilepack", str(test_project), "--no-content", "--no-pilignor"]
    )
    main()
    captured = capsys.readouterr()
    assert "main.py" in captured.out
