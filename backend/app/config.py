import os


# ============================================================
# LOCAL CONFIGURATION
# ============================================================

AI_PROVIDER = os.getenv("AI_PROVIDER", "local")

API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))


# ============================================================
# AZURE OPENAI - FUTURE
# ============================================================
#
# These values are intentionally prepared now.
#
# When Azure OpenAI is available, add:
#
# AZURE_OPENAI_ENDPOINT
# AZURE_OPENAI_API_KEY
# AZURE_OPENAI_DEPLOYMENT
# AZURE_OPENAI_API_VERSION
#
# No Azure credentials are required for the current demo.
# ============================================================

AZURE_OPENAI_ENDPOINT = os.getenv(
    "AZURE_OPENAI_ENDPOINT",
    "",
)

AZURE_OPENAI_API_KEY = os.getenv(
    "AZURE_OPENAI_API_KEY",
    "",
)

AZURE_OPENAI_DEPLOYMENT = os.getenv(
    "AZURE_OPENAI_DEPLOYMENT",
    "",
)

AZURE_OPENAI_API_VERSION = os.getenv(
    "AZURE_OPENAI_API_VERSION",
    "2024-10-21",
)