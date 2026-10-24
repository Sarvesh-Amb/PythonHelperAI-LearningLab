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


def mark_chapter_complete(chapter_id, progress_data=None):
    if progress_data is None:
        progress_data = load_progress()
    try:
        chapter_id = int(chapter_id)
    except (TypeError, ValueError):
        return progress_data
    completed = set(progress_data.get("completed_chapters", []))
    completed.add(chapter_id)
    progress_data["completed_chapters"] = sorted(completed)
    save_progress(progress_data)
    return progress_data


def mark_checkpoint_passed(checkpoint_id, progress_data=None):
    if progress_data is None:
        progress_data = load_progress()
    try:
        checkpoint_id = int(checkpoint_id)
    except (TypeError, ValueError):
        return progress_data
    passed = set(progress_data.get("passed_checkpoints", []))
    passed.add(checkpoint_id)
    progress_data["passed_checkpoints"] = sorted(passed)
    save_progress(progress_data)
    return progress_data


def get_progress_summary(progress_data):
    completed = progress_data.get("completed_chapters", [])
    passed = progress_data.get("passed_checkpoints", [])
    return {
        "completed_chapters": sorted(set(int(item) for item in completed if str(item).strip())),
        "passed_checkpoints": sorted(set(int(item) for item in passed if str(item).strip())),
    }


def load_checkpoints():
    checkpoints_dir = Path(__file__).resolve().parent / "data" / "checkpoints"
    if not checkpoints_dir.exists():
        return []

    checkpoints = []
    for checkpoint_file in sorted(checkpoints_dir.glob("*.json")):
        try:
            with checkpoint_file.open("r", encoding="utf-8") as f:
                checkpoint = json.load(f)
            if isinstance(checkpoint, dict):
                checkpoints.append(checkpoint)
        except (json.JSONDecodeError, OSError):
            continue
    return checkpoints


def get_checkpoint_for_chapter(chapter_id):
    try:
        target_id = int(chapter_id)
    except (TypeError, ValueError):
        return None

    for checkpoint in load_checkpoints():
        try:
            if int(checkpoint.get("chapter_id")) == target_id:
                return checkpoint
        except (TypeError, ValueError):
            continue
    return None


def validate_checkpoint(checkpoint, answers):
    if checkpoint is None:
        return 0, 0

    correct = 0
    total = len(checkpoint.get("questions", []))
    for question in checkpoint.get("questions", []):
        qid = str(question.get("id"))
        expected = str(question.get("answer", "")).strip().lower()
        given = str(answers.get(qid, "")).strip().lower()
        if given == expected:
            correct += 1
    return correct, total
