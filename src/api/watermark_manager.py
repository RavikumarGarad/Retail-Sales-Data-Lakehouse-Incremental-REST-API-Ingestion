from datetime import datetime, timezone


class IncrementalLoader:

    def __init__(self, pagination_handler, watermark_manager):
        self.pagination_handler = pagination_handler
        self.watermark_manager = watermark_manager

    def build_payload(self, location_ids, last_watermark):
        current_time = datetime.now(timezone.utc).isoformat()

        return {
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

    def load(self, location_ids, default_watermark):
        last_watermark = self.watermark_manager.get_watermark(
            "sales",
            default_watermark
        )

        payload = self.build_payload(
            location_ids,
            last_watermark
        )

        records = self.pagination_handler.fetch_all(payload)

        return records