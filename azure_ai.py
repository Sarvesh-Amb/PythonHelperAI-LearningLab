import os

from openai import AzureOpenAI


def call_azure_ai(prompt: str, model: str = "gemma3:1b") -> str:
    """Call an Azure-hosted Gemma deployment using the Azure OpenAI-compatible API."""
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT") or model.replace(":", "-")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")

    if not api_key or not endpoint:
        raise RuntimeError(
            "Azure configuration is incomplete. Set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT."
        )

    client = AzureOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version=api_version,
    )

    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=500,
    )

    try:
        content = response.choices[0].message.content
    except Exception:
        content = str(response)

    if not content:
        raise RuntimeError("Azure Gemma returned an empty response.")

    return str(content).strip()


def call_azure_gemma(prompt: str, model: str = "gemma3:1b") -> str:
    return call_azure_ai(prompt, model=model)
