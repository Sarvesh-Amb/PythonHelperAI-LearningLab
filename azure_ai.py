import shutil
import subprocess


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
