import re
from pathlib import Path
from typing import Optional

SECRET_PATTERNS = [
    (r'(password|passwd|pwd)(\s*[=:]\s*)(["\']?)([^"\'\s]+)(\3)', r'\1\2\3***\5'),
    (r'(api_key|apikey)(\s*[=:]\s*)(["\']?)([^"\'\s]+)(\3)', r'\1\2\3***\5'),
    (r'(token|access_token)(\s*[=:]\s*)(["\']?)([^"\'\s]+)(\3)', r'\1\2\3***\5'),
    (r'(secret|private_key)(\s*[=:]\s*)(["\']?)([^"\'\s]+)(\3)', r'\1\2\3***\5'),
    (r'\b[A-Za-z0-9+/]{40,}\b', '***'),
    (r'\b[0-9a-f]{32,}\b', '***'),
]


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

    if b'\x00' in raw_data:
        return None
    try:
        text = raw_data.decode('utf-8-sig')
    except UnicodeDecodeError:
        for enc in ('utf-8', 'cp1251', 'latin1'):
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