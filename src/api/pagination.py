class PaginationHandler:

    def __init__(self, api_client):
        self.api_client = api_client

    def fetch_all(self, payload):
        all_records = []

        while True:
            response = self.api_client.post(payload)

            records = response.get("orders", [])
            all_records.extend(records)

            cursor = response.get("cursor")

            if not cursor:
                break

            payload["cursor"] = cursor

        return all_records