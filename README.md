import os

from azure_ai import azure_config_present, call_azure_ai
from local_ai import call_local_ai
from model_manager import choose_model


def build_student_prompt(chapter_name: str, exercise_text: str, student_code: str = "") -> str:
    code_block = student_code.strip() if student_code.strip() else "(No code submitted yet)"
    return (
        f"Chapter: {chapter_name}\n"
        f"Exercise: {exercise_text}\n\n"
        f"Student code:\n{code_block}\n\n"
        "Give a small hint, ask one guiding question, and never give the full final solution. "
        "Keep the response beginner-friendly and short."
    )


def generate_hint(provider: str, model: str, chapter_name: str, exercise_text: str, student_code: str = "") -> str:
    provider_name = provider or "auto"
    selected_model = choose_model(provider_name, model)

    prompt = build_student_prompt(chapter_name, exercise_text, student_code)

    if provider_name == "cloud" or (provider_name == "auto" and azure_config_present()):
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        return call_azure_ai(prompt, deployment=deployment)

    return call_local_ai(prompt, model=selected_model)
