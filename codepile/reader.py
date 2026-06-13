import re
from pathlib import Path
from typing import Optional


SECRET_PATTERNS = [
    (r'(password|passwd|pwd)\s*[=:]\s*["\']?([^"\'\s]+)["\']?', r'\1="***"'),
    (r'(api_key|apikey)\s*[=:]\s*["\']?([^"\'\s]+)["\']?', r'\1="***"'),
    (r'(token|access_token)\s*[=:]\s*["\']?([^"\'\s]+)["\']?', r'\1="***"'),
    (r'(secret|private_key)\s*[=:]\s*["\']?([^"\'\s]+)["\']?', r'\1="***"'),
    (r'(?:\\b[A-Za-z0-9+/]{40,}\\b)', '***'),
    (r'(?:\\b[0-9a-f]{32,}\\b)', '***')
]


def _is_binary_content(data: bytes) -> bool:
    if b'\x00' in data:
        return True
    non_ascii = sum(1 for b in data if b > 127)

    if len(data) > 0 and non_ascii / len(data) > 0.3:
        return True
    return False


def _mask_secrets_in_text(text: str) -> str:
    for pattern, replacement in SECRET_PATTERNS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def read_file(file_path: Path, mask_secrets: bool = False) -> Optional[str]:
    try:
        raw_data = file_path.read_bytes()
    except (OSError, IOError) as e:
        print(f"Failed to read {file_path}: {e}")
        return None

    if _is_binary_content(raw_data):
        return None
    encodings = ['utf-8', 'cp1251', 'latin1']

    for enc in encodings:
        try:
            text = raw_data.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        return None

    if text.startswith('\ufeff'):
        text = text[1:]

    if mask_secrets:
        text = _mask_secrets_in_text(text)

    return text
