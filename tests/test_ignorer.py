import pytest
from pathlib import Path
from pilepack.ignorer import load_gitignore, is_ignored

def test_load_gitignore_missing(tmp_path):
    spec = load_gitignore(tmp_path)
    assert not spec.match_file("any.py")

def test_load_gitignore_existing(test_project):
    gitignore = test_project / ".gitignore"
    gitignore.write_text("*.log\ntemp/\n")
    spec = load_gitignore(test_project)
    assert spec.match_file("debug.log")
    assert spec.match_file("temp/file.txt")
    assert not spec.match_file("main.py")

def test_is_ignored_file(test_project):
    gitignore = test_project / ".gitignore"
    gitignore.write_text("*.log")
    spec = load_gitignore(test_project)
    log_file = test_project / "debug.log"
    assert is_ignored(log_file, test_project, spec) is True
    assert is_ignored(test_project / "main.py", test_project, spec) is False

def test_is_ignored_directory_contests(test_project):
    gitignore = test_project / ".gitignore"
    gitignore.write_text("temp/")
    spec = load_gitignore(test_project)
    inner_file = test_project / "temp" / "debug.log"
    assert is_ignored(inner_file, test_project, spec) is True