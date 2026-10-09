from pathlib import Path
from typing import Dict, List

from .ignorer import (
    GITIGNORE_FILENAME,
    PILIGNOR_FILENAME,
    is_ignored,
    load_spec,
)


def collect_files(
    root_path: Path,
    follow_gitignore: bool = True,
    follow_symlinks: bool = False,
    follow_pilignor: bool = True,
) -> List[Path]:
    if not root_path.is_dir():
        raise NotADirectoryError(f"{root_path} does not exist or is not a directory")

    spec = load_spec(
        root_path,
        use_gitignore=follow_gitignore,
        use_pilignor=follow_pilignor,
    )
    collected = []

    for item in root_path.rglob("*"):
        if any(part == ".git" for part in item.parts):
            continue
        if item.name in (GITIGNORE_FILENAME, PILIGNOR_FILENAME):
            continue
        if item.is_symlink() and not follow_symlinks:
            continue
        if is_ignored(item, root_path, spec):
            continue
        if item.is_file():
            rel = item.relative_to(root_path)
            collected.append(rel)
    return collected


def build_tree(files: List[Path]) -> Dict:
    tree = {}
    for path in files:
        parts = path.parts
        current = tree
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = None
    return tree
