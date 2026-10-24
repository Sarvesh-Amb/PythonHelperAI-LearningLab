import json
from pathlib import Path


def default_progress():
    return {
        "completed_chapters": [],
        "passed_checkpoints": [],
    }


def progress_path():
    root = Path(__file__).resolve().parent
    return root / "data" / "progress.json"


def load_progress(path=None):
    file_path = Path(path) if path else progress_path()
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        data = default_progress()
        save_progress(data, file_path)
        return data

    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        data = default_progress()
        save_progress(data, file_path)
        return data

    result = default_progress()
    result["completed_chapters"] = list(data.get("completed_chapters", []))
    result["passed_checkpoints"] = list(data.get("passed_checkpoints", []))
    return result


def save_progress(progress_data, path=None):
    file_path = Path(path) if path else progress_path()
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(progress_data, f, indent=2)


def mark_chapter_complete(progress_data, chapter_id):
    chapter_id = int(chapter_id)
    completed = set(progress_data.get("completed_chapters", []))
    completed.add(chapter_id)
    progress_data["completed_chapters"] = sorted(completed)
    return progress_data


def mark_checkpoint_passed(progress_data, checkpoint_id):
    checkpoint_id = int(checkpoint_id)
    passed = set(progress_data.get("passed_checkpoints", []))
    passed.add(checkpoint_id)
    progress_data["passed_checkpoints"] = sorted(passed)
    return progress_data


def get_progress_summary(progress_data):
    completed = progress_data.get("completed_chapters", [])
    passed = progress_data.get("passed_checkpoints", [])
    return {
        "completed_chapters": sorted(set(int(item) for item in completed)),
        "passed_checkpoints": sorted(set(int(item) for item in passed)),
    }
