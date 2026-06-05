import os
from dotenv import load_dotenv

load_dotenv()

DOC_ENDPOINT = os.getenv(
    "AZURE_DOC_INTELLIGENCE_ENDPOINT"
)

DOC_KEY = os.getenv(
    "AZURE_DOC_INTELLIGENCE_KEY"
)

AZURE_OPENAI_ENDPOINT = os.getenv(
    "AZURE_OPENAI_ENDPOINT"
)

AZURE_OPENAI_KEY = os.getenv(
    "AZURE_OPENAI_KEY"
)

AZURE_OPENAI_DEPLOYMENT = os.getenv(
    "AZURE_OPENAI_DEPLOYMENT"
)