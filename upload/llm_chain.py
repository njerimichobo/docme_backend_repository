import sys
import os
import django
import requests
from django.conf import settings

# Set the base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'willamabackend.settings')
django.setup()

# Constants
BASE_API_URL = settings.LANG_URL
LANGFLOW_ID = "1033f222-ac23-46c7-bfc3-bfa1d70eadfa"
FLOW_ID = "63039459-7c6b-44f5-8270-1978012b0f0b"
APPLICATION_TOKEN = settings.API_TOKEN
ENDPOINT = "ceaae400-92ca-4e1a-8b54-0159fc4dc064"


def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN,
               "Content-Type": "application/json", }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        text = (
            data.get("outputs", [{}])[0]
            .get("outputs", [{}])[0]
            .get("results", {})
            .get("message", {})
            .get("data", {})
            .get("text")
        )

        if not text:
            raise ValueError("Chat message text not found in response.")
        return text
    except requests.exceptions.RequestException as e:
        # Log detailed error
        print(f"Error communicating with Langflow API: {e}")
        raise
