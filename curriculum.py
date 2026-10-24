import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data" / "chapters"


def load_chapters():
    chapters = []
    if not DATA_DIR.exists():
        return chapters
    for chapter_file in sorted(DATA_DIR.glob("*.json")):
        try:
            with chapter_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                chapters.append(data)
        except json.JSONDecodeError:
            continue
    return chapters


def get_chapter_by_id(chapters, chapter_id):
    for chapter in chapters:
        if chapter.get("id") == chapter_id:
            return chapter
    return None


def get_chapter_index(chapters, chapter_id):
    for idx, chapter in enumerate(chapters):
        if chapter.get("id") == chapter_id:
            return idx
    return 0
