import pytest
from pathlib import Path
from pilepack.reader import read_file, _mask_secrets_in_text

def test_read_text_utf8(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("hello world", encoding="utf-8")
    content = read_file(f)
    assert content == "hello world"

def test_read_binary(tmp_path):
    f = tmp_path / "binary.bin"
    f.write_bytes(b'\x00\x01\x02\x03')
    assert read_file(f) is None

def test_read_with_bom(tmp_path):
    f = tmp_path / "bom.txt"
    f.write_bytes(b'\xef\xbb\xbfhello')
    content = read_file(f)
    assert content == "hello"
    assert not content.startswith('\ufeff')

def test_mask_secrets():
    text = "password=12345, API_KEY=abc123, token = \"xyz\""
    masked = _mask_secrets_in_text(text)
    assert "password=***" in masked
    assert "API_KEY=***" in masked
    assert 'token = "***"' in masked
    assert "12345" not in masked
    assert "abc123" not in masked
    assert "xyz" not in masked


def test_mask_secrets_preserves_delimiter():
    text = "pwd:secret, api_key=hello"
    masked = _mask_secrets_in_text(text)
    assert "pwd:***" in masked
    assert "api_key=***" in masked


def test_read_file_with_masking(tmp_path):
    f = tmp_path / "secret.env"
    f.write_text("TOKEN=super-secret")
    content = read_file(f, mask_secrets=True)
    assert "super-secret" not in content
    assert "TOKEN=***" in content


def test_read_file_with_quoted_masking(tmp_path):
    f = tmp_path / "quoted.env"
    f.write_text('PASSWORD="mysecret"')
    content = read_file(f, mask_secrets=True)
    assert 'PASSWORD="***"' in content
    assert "mysecret" not in content


def test_mask_long_base64(tmp_path):
    text = 'data="YW55IGNhcm5hbCBwbGVhc3VyZSBpcyBhIGxvbmcgc3RyaW5nIGZvciB0ZXN0aW5nYmFzZTY0"'
    masked = _mask_secrets_in_text(text)
    assert "YW55IGNhcm5hbCBwbGVhc3VyZSBpcyBhIGxvbmcgc3RyaW5nIGZvciB0ZXN0aW5nYmFzZTY0" not in masked
    assert "***" in masked