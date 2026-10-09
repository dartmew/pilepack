from pilepack.ignorer import is_ignored, load_gitignore, load_spec


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


def test_load_spec_merges_pilignor(test_project):
    (test_project / ".gitignore").write_text("*.log\n")
    (test_project / ".pilignor").write_text("data/\n")
    spec = load_spec(test_project)
    assert spec.match_file("debug.log")
    assert spec.match_file("data/config.txt")
    assert not spec.match_file("main.py")


def test_load_spec_pilignor_can_negate_gitignore(test_project):
    (test_project / ".gitignore").write_text("static/*\n")
    (test_project / ".pilignor").write_text("!static/js/\n")
    spec = load_spec(test_project)
    assert spec.match_file("static/css/app.css")
    assert not spec.match_file("static/js/app.js")


def test_load_spec_can_disable_gitignore(test_project):
    (test_project / ".gitignore").write_text("*.log\n")
    (test_project / ".pilignor").write_text("data/\n")
    spec = load_spec(test_project, use_gitignore=False)
    assert not spec.match_file("debug.log")
    assert spec.match_file("data/config.txt")


def test_load_spec_can_disable_pilignor(test_project):
    (test_project / ".gitignore").write_text("*.log\n")
    (test_project / ".pilignor").write_text("data/\n")
    spec = load_spec(test_project, use_pilignor=False)
    assert spec.match_file("debug.log")
    assert not spec.match_file("data/config.txt")


def test_load_spec_missing_files(tmp_path):
    spec = load_spec(tmp_path)
    assert not spec.match_file("any.py")
