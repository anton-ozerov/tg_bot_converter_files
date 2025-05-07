import re

INVALID_FILENAME_CHARS = r'[\\/:\*\?"<>\|\n\r\t]'

def is_valid_filename(name: str) -> bool:
    # Проверка на запрещённые символы и пустоту
    if not name or not name.strip():
        return False
    if re.search(INVALID_FILENAME_CHARS, name):
        return False
    if len(name) > 100:
        return False
    return True
