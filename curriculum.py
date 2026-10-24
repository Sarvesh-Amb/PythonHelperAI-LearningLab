import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_chapters():
    chapters_dir = BASE_DIR / "data" / "chapters"
    if not chapters_dir.exists():
        return []

    chapters = []
    for chapter_file in sorted(chapters_dir.glob("chapter_*.json")):
        try:
            chapter = load_json(chapter_file)
            chapters.append(chapter)
        except json.JSONDecodeError:
            continue
    return chapters


def get_chapter_by_id(chapters, chapter_id):
    for chapter in chapters:
        if int(chapter.get("id")) == int(chapter_id):
            return chapter
    return None


def get_chapter_index(chapters, chapter_id):
    for idx, chapter in enumerate(chapters):
        if int(chapter.get("id")) == int(chapter_id):
            return idx
    return 0


def load_progress():
    progress_file = BASE_DIR / "data" / "progress.json"
    if not progress_file.exists():
        return {"completed_chapters": [], "passed_checkpoints": []}

    try:
        return load_json(progress_file)
    except json.JSONDecodeError:
        return {"completed_chapters": [], "passed_checkpoints": []}


def save_progress(progress):
    progress_file = BASE_DIR / "data" / "progress.json"
    progress_file.parent.mkdir(parents=True, exist_ok=True)
    with open(progress_file, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2)


def mark_chapter_complete(chapter_id):
    progress = load_progress()
    completed = set(progress.get("completed_chapters", []))
    completed.add(int(chapter_id))
    progress["completed_chapters"] = sorted(completed)
    save_progress(progress)
    return progress


def mark_checkpoint_passed(checkpoint_id):
    progress = load_progress()
    passed = set(progress.get("passed_checkpoints", []))
    passed.add(int(checkpoint_id))
    progress["passed_checkpoints"] = sorted(passed)
    save_progress(progress)
    return progress


def load_checkpoints():
    checkpoints_dir = BASE_DIR / "data" / "checkpoints"
    if not checkpoints_dir.exists():
        return []

    checkpoints = []
    for checkpoint_file in sorted(checkpoints_dir.glob("*.json")):
        try:
            checkpoint = load_json(checkpoint_file)
            checkpoints.append(checkpoint)
        except json.JSONDecodeError:
            continue
    return checkpoints


def get_checkpoint_for_chapter(chapter_id):
    for checkpoint in load_checkpoints():
        if int(checkpoint.get("chapter_id")) == int(chapter_id):
            return checkpoint
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
