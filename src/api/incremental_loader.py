from datetime import datetime, timezone


class IncrementalLoader:

    def __init__(self, api_client, pagination_handler):
        self.api_client = api_client
        self.pagination_handler = pagination_handler

    def build_payload(self, location_ids, last_watermark):
        current_time = datetime.now(timezone.utc).isoformat()

        payload = {
            "location_ids": location_ids,
            "limit": 500,
            "return_entries": False,
            "query": {
                "filter": {
                    "date_time_filter": {
                        "updated_at": {
                            "start_at": last_watermark,
                            "end_at": current_time
                        }
                    }
                },
                "sort": {
                    "sort_field": "UPDATED_AT",
                    "sort_order": "ASC"
                }
            }
        }

        return payload

    def load(self, location_ids, last_watermark):
        payload = self.build_payload(
            location_ids,
            last_watermark
        )

        records = self.pagination_handler.fetch_all(payload)

        return records