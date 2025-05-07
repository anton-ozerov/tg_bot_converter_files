import asyncio
from pathlib import Path
from typing import List


async def async_clear_folder(folder_path: str, filenames: List[str]):
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        return

    for name in filenames:
        file_path = folder / name
        if file_path.is_file():
            await asyncio.to_thread(file_path.unlink)
