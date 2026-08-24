from app.ai.local_provider import LocalAIProvider
from app.config import AI_PROVIDER


def get_ai_provider():

    if AI_PROVIDER == "local":

        return LocalAIProvider()

    # ========================================================
    # AZURE OPENAI FUTURE
    # ========================================================
    #
    # When Azure OpenAI is available:
    #
    # from app.ai.azure_provider import AzureOpenAIProvider
    #
    # return AzureOpenAIProvider()
    #
    # Only this provider-selection layer needs updating.
    # ========================================================

    raise ValueError(
        f"Unsupported AI provider: {AI_PROVIDER}"
    )


def analyze_incident(
    evidence: dict,
) -> dict:

    provider = get_ai_provider()

    return provider.analyze_incident(
        evidence
    )


def review_deployment(
    deployment: str,
) -> dict:

    provider = get_ai_provider()

    return provider.review_deployment(
        deployment
    )


def review_iac(
    content: str,
    iac_type: str,
) -> dict:

    provider = get_ai_provider()

    return provider.review_iac(
        content,
        iac_type,
    )