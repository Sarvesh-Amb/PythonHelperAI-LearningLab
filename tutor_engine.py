import os
import shutil
import subprocess

from model_manager import choose_model, detect_local_models
from prompt import SYSTEM_PROMPT


def azure_config_present() -> bool:
    return bool(
        os.getenv("AZURE_OPENAI_API_KEY")
        and os.getenv("AZURE_OPENAI_ENDPOINT")
        and os.getenv("AZURE_OPENAI_DEPLOYMENT")
    )


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


def call_azure_ai(prompt: str, deployment: str | None = None) -> str:
    if not azure_config_present():
        raise RuntimeError(
            "Azure OpenAI is not configured. Set AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, and AZURE_OPENAI_DEPLOYMENT."
        )

    from openai import AzureOpenAI

    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )

    model_name = deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT")
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=250,
    )

    return response.choices[0].message.content.strip() or "No response from Azure model."


def build_tutor_prompt(chapter_name: str, exercise_text: str, student_code: str) -> str:
    return f"""You are helping a student learning {chapter_name}.

Exercise: {exercise_text}

Student code so far:
{student_code or 'No code written yet'}

Give a tiny, encouraging hint. Do not give the full answer. Ask one short guiding question and explain just one small concept. Keep it under 150 words.
"""


def generate_hint(provider: str, model: str, chapter_name: str, exercise_text: str, student_code: str) -> str:
    prompt = build_tutor_prompt(chapter_name, exercise_text, student_code)

    selected_provider = provider
    selected_model = choose_model(provider, model)

    if provider in {"local", "auto"}:
        try:
            return call_local_ai(prompt, model=selected_model)
        except Exception as local_error:
            if provider == "local":
                raise RuntimeError(f"Local tutor failed: {local_error}") from local_error
            if azure_config_present():
                return call_azure_ai(prompt, deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"))
            raise RuntimeError(f"Local tutor failed and Azure is not configured: {local_error}") from local_error

    if provider == "cloud":
        if not azure_config_present():
            raise RuntimeError(
                "Cloud mode requires Azure configuration: AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, and AZURE_OPENAI_DEPLOYMENT."
            )
        return call_azure_ai(prompt, deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"))

    raise RuntimeError(f"Unsupported provider: {provider}")
