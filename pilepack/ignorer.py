from pathlib import Path
from typing import List

from pathspec import GitIgnoreSpec, PathSpec

GITIGNORE_FILENAME = ".gitignore"
PILIGNOR_FILENAME = ".pilignor"


def _read_patterns(path: Path) -> List[str]:
    """Read an ignore file and return its lines (empty list if unreadable)."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read().splitlines()
    except OSError:
        return []


def load_spec(
    root_path: Path,
    use_gitignore: bool = True,
    use_pilignor: bool = True,
) -> PathSpec:
    """Combine .gitignore and .pilignor rules into a single spec.

    Rules are loaded in order: .gitignore first, then .pilignor, so the
    latter can override earlier rules (including negation with `!`).
    """
    lines: List[str] = []
    if use_gitignore:
        lines.extend(_read_patterns(root_path / GITIGNORE_FILENAME))
    if use_pilignor:
        lines.extend(_read_patterns(root_path / PILIGNOR_FILENAME))
    return GitIgnoreSpec.from_lines(lines)


def load_gitignore(root_path: Path) -> PathSpec:
    """Backward-compatible helper: load .gitignore rules only."""
    return load_spec(root_path, use_gitignore=True, use_pilignor=False)


def is_ignored(path, root: Path, spec: PathSpec) -> bool:
    original = str(path)
    path_obj = Path(original)

    if not path_obj.is_absolute():
        path_obj = root / path_obj

    try:
        rel_path = path_obj.relative_to(root)
    except ValueError:
        return False
    rel_str = rel_path.as_posix()

    return spec.match_file(rel_str)
