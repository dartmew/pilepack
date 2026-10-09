# PilePack

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/pilepack)](https://pypi.org/project/pilepack/)
[![Tests](https://img.shields.io/badge/tests-43%20passed-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-87%25-yellowgreen)](#-testing)
[![CLI](https://img.shields.io/badge/CLI-ready-blue)](#-usage)

**English** | [Русский](README.ru.md)

**Pack your codebase into a single file for AI analysis**  
Combine all your project files into one file — perfect for sending to LLMs (ChatGPT, Claude, Copilot, Deepseek, etc.).

---

## Why pilepack?

- 🪶 **Only 1 dependency** – runs anywhere Python 3.8+ is available.
- ⚡ **Streaming engine** – packs huge codebases without eating RAM.
- 🔐 **Secrets masking built-in** – no more leaked tokens in LLM chats.
- 📂 **Full directory tree** + file contents in one clean text/markdown.
- 🧪 **Tested, typed, actively maintained.**

---

## ✨ Features

- 📁 **Recursive scanning** – walks through all files in a directory.
- 💾 **Streaming output** – minimal memory usage even on huge codebases.
- 🚫 **Respects .gitignore** – optionally disable with `--no-gitignore`.
- 🧹 **Extra `.pilignor` rules** – layer project-specific exclusions on top of `.gitignore`.
- 🪄 **`--init-ignore`** – generate a starter `.pilignor` (safe or aggressive).
- 🔗 **Skips symlinks by default** – opt in with `--follow-symlinks`.
- 🌳 **Tree structure** – displays project hierarchy.
- 📄 **Embedded content** – each file is shown with its path header.
- 🔐 **Secrets masking** – hides passwords, tokens, keys (`--mask-secrets`).
- 🖨️ **Two output formats** – plain text (`txt`) or Markdown (`md`).
- 💾 **Save to file** – use `-o output.txt`.

---

## 📦 Installation

```bash
pip install pilepack
```

From source:

```bash
git clone https://github.com/dartmew/pilepack.git
cd pilepack
pip install -e .
```

## 🚀 Usage

Basic command – pass a path to your project:

```bash
pilepack /path/to/your/project
```

Redirect output to a file:

```bash
pilepack . > report.txt
```

Example output (txt)

```text
myproject
├── main.py
├── utils/
│   ├── helpers.py
│   └── __init__.py
└── README.md

================================================================================

--- FILE: main.py ---
import utils.helpers

def main():
    print("Hello")

--- FILE: utils/helpers.py ---
def greet(name):
    return f"Hi {name}"
```

Markdown format

```bash
pilepack . -f md -o report.md
```

Produces a Markdown file with syntax highlighting.

Show only structure (no file contents)

```bash
pilepack . --no-content
```

Mask secrets

```bash
pilepack . --mask-secrets
```

Replaces values of password=, api_key=, token=, and long strings (base64/hex) with \*\*\*.

Disable .gitignore

```bash
pilepack . --no-gitignore
```

Follow symbolic links explicitly

```bash
pilepack . --follow-symlinks
```

## 🧹 Custom ignore rules with `.pilignor`

`.gitignore` is great for Git, but packing a project for an LLM often needs
extra exclusions (dumps, reports, assets) that should still live in the repo.
Drop a `.pilignor` file in the root — its rules are applied **on top of**
`.gitignore`, in that order, so `.pilignor` can also re-include files with `!`.

```gitignore
# .pilignor
static/*
!static/js/
media/
*_dump.md
report.txt
```

Generate a starter file (like `git init`, it never overwrites an existing file
unless you pass `--force`):

```bash
pilepack --init-ignore                       # safe preset
pilepack --init-ignore -m aggressive         # + assets, dumps, large files
pilepack --init-ignore --force               # overwrite existing .pilignor
```

Use `.pilignor` as a standalone ignore file (ignore `.gitignore` completely):

```bash
pilepack . --no-gitignore
```

Ignore both files (pack everything):

```bash
pilepack . --no-gitignore --no-pilignor
```

## 📋 CLI Options

| Option              | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| `root`              | Directory to scan (default: current directory)               |
| `--no-content`      | Show tree structure only, skip file contents                 |
| `--mask-secrets`    | Mask passwords, tokens, API keys                             |
| `-o, --output`      | Write report to a file instead of stdout                     |
| `--no-gitignore`    | Do not respect `.gitignore` rules                            |
| `--no-pilignor`     | Do not respect `.pilignor` rules                             |
| `-i, --init-ignore` | Create a starter `.pilignor` file and exit                   |
| `-m, --ignore-mode` | Preset for `--init-ignore`: `safe` (default) or `aggressive` |
| `--force`           | Overwrite existing `.pilignor` with `--init-ignore`          |
| `--follow-symlinks` | Follow symbolic links during scanning                        |
| `-f, --format`      | Output format: `txt` (default) or `md`                       |

## 🧪 Testing

Install test dependencies and run:

```bash
pip install -e .[test]
pytest
```

With coverage:

```bash
pytest --cov=pilepack
```

Current coverage: 87% (43 tests, all passing).

```bash
Name                      Stmts   Miss  Cover
---------------------------------------------
pilepack\__init__.py          1      0   100%
pilepack\__main__.py          3      3     0%
pilepack\cli.py              71      5    93%
pilepack\collector.py        30      1    97%
pilepack\formatter.py        39      3    92%
pilepack\ignorer.py          31      3    90%
pilepack\reader.py           31     12    61%
pilepack\suggestions.py      40      6    85%
---------------------------------------------
TOTAL                       246     33    87%
```

## 📄 License

[MIT](LICENSE) © 2026 Vasili S. Pribylov

## 🤝 Contributing

Issues and pull requests are welcome! For major changes, please open an issue first to discuss.

## 💬 Support

Feel free to [open an issue](https://github.com/dartmew/pilepack/issues) for bugs, questions, or suggestions. I'll try to respond within a few days.

This project is actively maintained (as of 2026).

## 🙏 Acknowledgements

Inspired by the need to easily feed code into large language models.
