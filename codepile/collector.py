from ignorer import load_gitignore, is_ignored
from pathlib import Path


def collect_files(root_path: Path, follow_gitignore = True) -> list[Path]:
    if not root_path.is_dir():
        raise NotADirectoryError(f"{root_path} не существует или не папка")

    if follow_gitignore:
        spec = load_gitignore(root_path)
    else:
        spec = None
    collected = []

    for item in root_path.rglob('*'):
        if item.name == '.gitignore':
            continue
        if '.git' in item.parts:
            continue
        if spec and is_ignored(item, root_path, spec):
            continue
        if item.is_file():
            rel = item.relative_to(root_path)
            collected.append(rel)
    return collected



#root = Path(r'C:\Projects\Pets\codepile\tests\fixtures\test_project')
