import os
import requests


class APIClient:

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.access_token = os.getenv("SQUARE_ACCESS_TOKEN")

        if not self.access_token:
            raise ValueError("SQUARE_ACCESS_TOKEN environment variable is not set.")

    def post(self, payload):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        response = requests.post(
            self.endpoint,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        return response.json()