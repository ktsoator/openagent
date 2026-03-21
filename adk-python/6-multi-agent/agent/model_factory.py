import os

from google.adk.models.lite_llm import LiteLlm


def get_provider(model_name: str) -> str:
    if "/" not in model_name:
        raise ValueError(
            "model_name must use the 'provider/model' format, "
            "for example 'openai/gpt-5.4' or "
            "'anthropic/claude-opus-4-6'."
        )
    return model_name.split("/", 1)[0].lower()


def normalize_openai_api_base(api_base: str) -> str:
    api_base = api_base.rstrip("/")
    return api_base if api_base.endswith("/v1") else f"{api_base}/v1"


def normalize_anthropic_api_base(api_base: str) -> str:
    api_base = api_base.rstrip("/")
    return api_base[:-3] if api_base.endswith("/v1") else api_base


def create_model(model_name: str | None = None) -> LiteLlm:
    model_name = model_name or os.getenv("MODEL_NAME", "openai/gpt-5.4")
    provider = get_provider(model_name)

    if provider == "openai":
        return LiteLlm(
            model=model_name,
            api_base=normalize_openai_api_base(
                os.getenv("OPENAI_API_BASE", "https://vip.aipro.love/v1")
            ),
            api_key=os.getenv("OPENAI_API_KEY", ""),
        )

    if provider == "anthropic":
        return LiteLlm(
            model=model_name,
            api_base=normalize_anthropic_api_base(
                os.getenv("ANTHROPIC_API_BASE", "https://vip.aipro.love")
            ),
            api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        )

    raise ValueError(
        f"Unsupported provider '{provider}'. "
        "Supported providers are 'openai' and 'anthropic'."
    )
