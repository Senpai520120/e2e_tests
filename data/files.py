"""Files used in upload tests."""

from pathlib import Path

FILES_DIR = Path(__file__).parent / "files"

SAMPLE_TXT = FILES_DIR / "sample.txt"
SECOND_TXT = FILES_DIR / "second.txt"
CYRILLIC_TXT = FILES_DIR / "отчёт.txt"
HTML_FILE = FILES_DIR / "page.html"