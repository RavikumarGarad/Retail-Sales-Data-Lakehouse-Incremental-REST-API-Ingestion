import time
import requests


class RetryHandler:

    def __init__(self, max_retries=3, backoff_seconds=5, retry_status_codes=None):
        self.max_retries = max_retries
        self.backoff_seconds = backoff_seconds
        self.retry_status_codes = retry_status_codes or [
            429, 500, 502, 503, 504
        ]

    def post(self, endpoint, headers, payload):
        for attempt in range(self.max_retries + 1):

            try:
                response = requests.post(
                    endpoint,
                    headers=headers,
                    json=payload,
                    timeout=30
                )

                if response.status_code not in self.retry_status_codes:
                    response.raise_for_status()
                    return response.json()

                if attempt < self.max_retries:
                    time.sleep(self.backoff_seconds)

            except requests.RequestException:

                if attempt < self.max_retries:
                    time.sleep(self.backoff_seconds)
                else:
                    raise

        raise RuntimeError("API request failed after maximum retries.")