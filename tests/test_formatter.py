import pytest
from pathlib import Path
from io import StringIO
from pilepack.formatter import write_report, _format_tree
from pilepack.collector import collect_files, build_tree

def test_format_tree_simple():
    tree = {"a.py": None, "b": {"c.py": None}}
    result = _format_tree(tree)
    assert "b/" in result
    assert "a.py" in result

def test_write_report_txt(test_project):
    files = collect_files(test_project, follow_gitignore=False)
    tree = build_tree(files)

    main_file = None
    for f in files:
        if f.name == "main.py":
            main_file = f
            break
    assert main_file is not None, "main.py not found in test project"

    def content_gen():
        yield main_file, (test_project / main_file).read_text()

    stream = StringIO()
    write_report(stream, "test_project", tree, content_gen(), fmt="txt")
    output = stream.getvalue()
    assert "--- FILE: main.py ---" in output
    assert "def main():" in output

def test_write_report_md(test_project):
    files = collect_files(test_project, follow_gitignore=False)
    tree = build_tree(files[:2])

    main_file = next((f for f in files if f.name == "main.py"), None)
    assert main_file is not None, "main.py not found"

    def content_gen():
        yield main_file, (test_project / main_file).read_text()

    stream = StringIO()
    write_report(stream, "test_project", tree, content_gen(), fmt="md")
    output = stream.getvalue()
    assert "## `main.py`" in output
    assert "```python" in output