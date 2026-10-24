import json
from pathlib import Path


def load_chapters(chapter_dir: Path):
    if not chapter_dir.exists():
        return []
    chapters = []
    for item in sorted(chapter_dir.glob("*.json")):
        try:
            data = json.loads(item.read_text())
            if isinstance(data, dict):
                chapters.append(data)
            elif isinstance(data, list):
                chapters.extend(data)
        except json.JSONDecodeError:
            continue
    return chapters


def get_current_chapter(chapters, index):
    if not chapters:
        return None
    if index < 0:
        index = 0
    if index >= len(chapters):
        index = len(chapters) - 1
    return chapters[index]
