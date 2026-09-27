
# # APIClient
#    │
#    ├── Gets endpoint from config
#    │
#    ├── Gets Square token from environment variable
#    │
#    ├── Creates authentication headers
#    │
#    ├── Sends POST request
#    │
#    ├── Checks HTTP status
#    │
#    └── Returns JSON response

import os

class APIClient:

    def __init__(self, endpoint, retry_handler):
        self.endpoint = endpoint
        self.retry_handler = retry_handler
        self.access_token = os.getenv("SQUARE_ACCESS_TOKEN")

        if not self.access_token:
            raise ValueError(
                "SQUARE_ACCESS_TOKEN environment variable is not set."
            )

    def post(self, payload):

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        return self.retry_handler.post(
            endpoint=self.endpoint,
            headers=headers,
            payload=payload
        )