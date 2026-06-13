import pytest
from pathlib import Path
from pilepack.cli import main, _generate_report
import sys

def test_generate_report_no_content(test_project):
    report = _generate_report(test_project, include_content=False, fmt="txt")
    assert "--- FILE:" not in report
    assert "test_project" in report
    assert "main.py" in report

def test_cli_basic(test_project, capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["pilepack", str(test_project), "--no-content"])
    main()
    captured = capsys.readouterr()
    assert "test_project" in captured.out
    assert "main.py" in captured.out
    assert "--- FILE:" not in captured.out

def test_cli_output_file(test_project, tmp_path, monkeypatch):
    out_file = tmp_path / "report.txt"
    monkeypatch.setattr(sys, "argv", ["pilepack", str(test_project), "-o", str(out_file)])
    main()
    assert out_file.exists()
    content = out_file.read_text()
    assert "main.py" in content

def test_cli_invalid_dir(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["pilepack", "/nonexistent"])
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "not a valid directory" in captured.err