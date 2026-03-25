import logging
import requests


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

SCOPES = []
EMPTY_ARRAY = []


class NotebookLM:
    """
    Google API documentation:
        - https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks  # noqa: E501
    """

    def __init__(self, credentials) -> None:
        self.credentials = credentials

    def create_notebook(self, notebook_name: str) -> None:
        print("="*100)
        print(f"Creating notebook {notebook_name}")
        response = requests.post(
            "https://global-discoveryengine.googleapis.com/v1alpha/projects/maks-asp--pro--72/locations/global/notebooks",
            headers={
                "Authorization": f"Bearer {self.credentials.token}",
            },
            json={
                "title": notebook_name,
            },
        )
        print(response)
        print(response.json())
        print("="*100)

        return notebook_name