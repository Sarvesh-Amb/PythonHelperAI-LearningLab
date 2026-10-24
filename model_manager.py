import os
import shutil
import subprocess

LOW_END_MODELS = ["gemma3:1b", "gemma3:2b", "qwen2.5-coder:3b"]
STANDARD_MODELS = ["gemma3:2b", "gemma3:4b", "qwen2.5-coder:3b", "qwen2.5-coder:7b"]


def detect_local_models():
    if shutil.which("ollama") is None:
        return []
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=False)
        if result.returncode != 0:
            return []
        lines = result.stdout.strip().splitlines()[1:]
        models = []
        for line in lines:
            if not line:
                continue
            name = line.split()[0]
            if name:
                models.append(name)
        return models
    except Exception:
        return []


def choose_model(provider: str, requested_model: str = ""):
    if provider == "local":
        models = detect_local_models()
        if not models:
            return requested_model or "gemma3:1b"
        if requested_model in models:
            return requested_model
        return models[0]

    if provider == "cloud":
        return requested_model or "gpt-4o-mini"

    models = detect_local_models()
    has_azure = bool(os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"))
    if has_azure:
        return requested_model or "gpt-4o-mini"
    if requested_model and requested_model in models:
        return requested_model
    if models:
        return models[0]
    return "gemma3:1b"


def get_provider_status():
    local = detect_local_models()
    azure_ok = bool(os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"))
    status_lines = []
    status_lines.append("System status:\n")
    status_lines.append(f"- Ollama installed: {'yes' if shutil.which('ollama') else 'no'}")
    status_lines.append(f"- Local models: {', '.join(local) if local else 'none'}")
    status_lines.append(f"- Azure config: {'ready' if azure_ok else 'not configured'}")
    return "\n".join(status_lines)


def recommend_model_for_system(ram_mb: int | None = None):
    if ram_mb is None:
        return "gemma3:1b"
    if ram_mb < 6000:
        return "gemma3:1b"
    if ram_mb < 12000:
        return "gemma3:2b"
    if ram_mb < 18000:
        return "qwen2.5-coder:3b"
    return "gemma3:4b"
