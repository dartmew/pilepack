import pytest
from pathlib import Path
from pilepack.formatter import render, _format_tree

def test_format_tree_simple():
    tree = {"a.py": None, "b": {"c.py": None}}
    result = _format_tree(tree)
    assert "b/" in result
    assert "a.py" in result

def test_render_txt(test_project, tmp_path):
    from pilepack.collector import collect_files, build_tree
    files = collect_files(test_project, follow_gitignore=False)
    tree = build_tree(files)
    content_list = []
    for rel in files:
        if rel.name == "main.py":
            content = (test_project / rel).read_text()
            content_list.append((rel, content))
    output = render("test_project", tree, content_list, fmt="txt")
    assert "--- FILE: main.py ---" in output
    assert "def main():" in output

def test_render_md(test_project):
    from pilepack.collector import collect_files, build_tree
    files = collect_files(test_project, follow_gitignore=False)
    tree = build_tree(files[:2])
    content_list = [(files[0], (test_project / files[0]).read_text())]
    output = render("test_project", tree, content_list, fmt="md")
    assert "## `main.py`" in output
    assert "```python" in output