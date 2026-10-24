import shutil
import subprocess

from prompt import SYSTEM_PROMPT


def call_local_ai(prompt: str, model: str = "gemma3:1b") -> str:
    if shutil.which("ollama") is None:
        raise RuntimeError("Ollama is not installed. Install Ollama to use local mode.")

    result = subprocess.run(
        ["ollama", "run", model, prompt],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        error_text = (result.stderr or result.stdout or "Unknown Ollama error").strip()
        raise RuntimeError(f"Local model error: {error_text}")

    return result.stdout.strip() or "No response from local model."


def build_tutor_prompt(chapter_name: str, exercise_text: str, student_code: str) -> str:
    return f"""You are a patient, beginner-friendly Python tutor.

You are helping a student learning {chapter_name}.

Exercise: {exercise_text}

Student code so far:
{student_code or 'No code written yet'}

Give one tiny, encouraging hint. Do not give the full answer. Ask one short guiding question and explain one small concept. Keep it under 150 words.

Follow this style:
- warm and calm
- beginner-friendly
- focused on learning by doing
- never reveal the final solution immediately

{SYSTEM_PROMPT}
"""


def generate_hint(provider: str, model: str, chapter_name: str, exercise_text: str, student_code: str) -> str:
    if (provider or "local").lower() not in {"local", "auto", ""}:
        raise RuntimeError(f"This branch supports only local models. Received provider: {provider}")

    selected_model = model or "gemma3:1b"
    prompt = build_tutor_prompt(chapter_name, exercise_text, student_code)
    return call_local_ai(prompt, model=selected_model)
