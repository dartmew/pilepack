# PilePack

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/pilepack)](https://pypi.org/project/pilepack/)
[![Tests](https://img.shields.io/badge/tests-43%20passed-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-87%25-yellowgreen)](#-тестирование)
[![CLI](https://img.shields.io/badge/CLI-ready-blue)](#-использование)

[English](README.md) | **Русский**

**Соберите свой проект в один файл для анализа ИИ**  
Объединяет все файлы проекта в один файл — идеально для отправки в LLM (ChatGPT, Claude, Copilot, Deepseek и др.).

---

## Зачем pilepack?

- 🪶 **Всего 1 зависимость** — работает везде, где есть Python 3.8+.
- ⚡ **Потоковый движок** — упаковывает огромные проекты, не съедая память.
- 🔐 **Маскировка секретов из коробки** — никаких утёкших токенов в чатах с LLM.
- 📂 **Полное дерево каталогов** + содержимое файлов в одном текстовом/Markdown-файле.
- 🧪 **Протестировано, типизировано, активно поддерживается.**

---

## ✨ Возможности

- 📁 **Рекурсивное сканирование** — обходит все файлы в каталоге.
- 💾 **Потоковый вывод** — минимальное потребление памяти даже на больших проектах.
- 🚫 **Учитывает .gitignore** — можно отключить через `--no-gitignore`.
- 🧹 **Дополнительные правила `.pilignor`** — свои исключения поверх `.gitignore`.
- 🪄 **`--init-ignore`** — создаёт стартовый `.pilignor` (safe или aggressive).
- 🔗 **Пропускает симлинки по умолчанию** — включается через `--follow-symlinks`.
- 🌳 **Дерево структуры** — показывает иерархию проекта.
- 📄 **Встроенное содержимое** — каждый файл идёт со своим заголовком-путём.
- 🔐 **Маскировка секретов** — скрывает пароли, токены, ключи (`--mask-secrets`).
- 🖨️ **Два формата вывода** — обычный текст (`txt`) или Markdown (`md`).
- 💾 **Сохранение в файл** — через `-o output.txt`.

---

## 📦 Установка

```bash
pip install pilepack
```

Из исходников:

```bash
git clone https://github.com/dartmew/pilepack.git
cd pilepack
pip install -e .
```

## 🚀 Использование

Базовая команда — укажите путь к проекту:

```bash
pilepack /path/to/your/project
```

Перенаправить вывод в файл:

```bash
pilepack . > report.txt
```

Пример вывода (txt)

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

Формат Markdown

```bash
pilepack . -f md -o report.md
```

Создаёт Markdown-файл с подсветкой синтаксиса.

Показать только структуру (без содержимого файлов)

```bash
pilepack . --no-content
```

Маскировать секреты

```bash
pilepack . --mask-secrets
```

Заменяет значения password=, api_key=, token= и длинные строки (base64/hex) на \*\*\*.

Отключить .gitignore

```bash
pilepack . --no-gitignore
```

Явно следовать симлинкам

```bash
pilepack . --follow-symlinks
```

## 🧹 Свои правила игнорирования через `.pilignor`

`.gitignore` хорош для Git, но при упаковке проекта для LLM часто нужны
дополнительные исключения (дампы, отчёты, ассеты), которые при этом должны
оставаться в репозитории. Положите файл `.pilignor` в корень — его правила
применяются **поверх** `.gitignore`, в этом же порядке, поэтому `.pilignor`
может и возвращать файлы обратно с помощью `!`.

```gitignore
# .pilignor
static/*
!static/js/
media/
*_dump.md
report.txt
```

Сгенерировать стартовый файл (как `git init` — он никогда не перезаписывает
существующий файл, если не указать `--force`):

```bash
pilepack --init-ignore                       # пресет safe
pilepack --init-ignore -m aggressive         # + ассеты, дампы, крупные файлы
pilepack --init-ignore --force               # перезаписать существующий .pilignor
```

Использовать `.pilignor` как самостоятельный файл игнора (полностью игнорируя `.gitignore`):

```bash
pilepack . --no-gitignore
```

Игнорировать оба файла (упаковать всё):

```bash
pilepack . --no-gitignore --no-pilignor
```

## 📋 Опции CLI

| Опция               | Описание                                                     |
| ------------------- | ------------------------------------------------------------ |
| `root`              | Каталог для сканирования (по умолчанию: текущий)             |
| `--no-content`      | Показать только структуру, без содержимого файлов            |
| `--mask-secrets`    | Маскировать пароли, токены, API-ключи                        |
| `-o, --output`      | Записать отчёт в файл вместо stdout                          |
| `--no-gitignore`    | Не учитывать правила `.gitignore`                            |
| `--no-pilignor`     | Не учитывать правила `.pilignor`                             |
| `-i, --init-ignore` | Создать стартовый файл `.pilignor` и выйти                   |
| `-m, --ignore-mode` | Пресет для `--init-ignore`: `safe` (по умолчанию) или `aggressive` |
| `--force`           | Перезаписать существующий `.pilignor` при `--init-ignore`    |
| `--follow-symlinks` | Следовать симлинкам при сканировании                         |
| `-f, --format`      | Формат вывода: `txt` (по умолчанию) или `md`                 |

## 🧪 Тестирование

Установите зависимости для тестов и запустите:

```bash
pip install -e .[test]
pytest
```

С покрытием:

```bash
pytest --cov=pilepack
```

Текущее покрытие: 87% (43 теста, все проходят).

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

## 📄 Лицензия

[MIT](LICENSE) © 2026 Vasili S. Pribylov

## 🤝 Участие в разработке

Issues и pull requests приветствуются! Для крупных изменений сначала откройте issue для обсуждения.

## 💬 Поддержка

Не стесняйтесь [открыть issue](https://github.com/dartmew/pilepack/issues) для багов, вопросов или предложений. Постараюсь ответить в течение нескольких дней.

Проект активно поддерживается (по состоянию на 2026).

## 🙏 Благодарности

Вдохновлён необходимостью легко передавать код в большие языковые модели.
