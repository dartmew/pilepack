from typing import Dict, List, Optional, Tuple
from pathlib import Path


def _format_tree(tree: Dict, prefix: str = '', is_last: bool = True) -> str:
    lines = []
    items = sorted(tree.items(), key=lambda x: (isinstance(x[1], dict), x[0].lower()), reverse=True)

    for i, (name, subtree) in enumerate(items):
        is_last_item = (i == len(items) - 1)
        connector = '└── ' if is_last_item else '├── '
        display_name = name + '/' if isinstance(subtree, dict) else name
        lines.append(prefix + connector + display_name)

        if isinstance(subtree, dict):
            new_prefix = prefix + ('    ' if is_last_item else '│   ')
            lines.append(_format_tree(subtree, new_prefix, is_last_item))
    return '\n'.join(lines)


def _render_txt(root_name: str, tree: Dict, files_content: List[Tuple[Path, Optional[str]]]) -> str:
    tree_str = _format_tree(tree)
    output = [f"{root_name}\n{tree_str}"]

    if files_content:
        output.append("\n" + "=" * 80 + "\n")

        for rel_path, content in files_content:

            if content is not None:
                output.append(f"--- FILE: {rel_path} ---")
                output.append(content)
                output.append("")
            else:
                output.append(f"--- FILE: {rel_path} [BINARY OR UNREADABLE] ---\n")
    return "\n".join(output)


def _render_md(root_name: str, tree: Dict, files_content: List[Tuple[Path, Optional[str]]]) -> str:
    tree_str = _format_tree(tree)
    output = [f"# {root_name}\n```\n{tree_str}\n```"]

    if files_content:
        output.append("\n---\n")

        for rel_path, content in files_content:
            
            if content is not None:
                ext = rel_path.suffix.lower()
                lang = {
                    '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
                    '.html': 'html', '.css': 'css', '.json': 'json',
                    '.md': 'markdown', '.yaml': 'yaml', '.yml': 'yaml',
                    '.sh': 'bash', '.txt': 'text'
                }.get(ext, 'text')
                output.append(f"## `{rel_path}`\n```{lang}\n{content}\n```\n")
            else:
                output.append(f"## `{rel_path}`\n*[BINARY OR UNREADABLE]*\n")
    return '\n'.join(output)


def render(root_name: str, tree: Dict, files_content: List[Tuple[Path, Optional[str]]], fmt: str = "txt") -> str:
    if fmt == "txt":
        return _render_txt(root_name, tree, files_content)
    elif fmt == "md":
        return _render_md(root_name, tree, files_content)
    else:
        raise ValueError(f"Unsupported format: {fmt}. Supported: 'txt', 'md'")