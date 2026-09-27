```python
import json
from datetime import datetime, timezone

from src.api.api_client import APIClient
from src.api.retry_handler import RetryHandler
from src.api.pagination import PaginationHandler
from src.api.incremental_loader import IncrementalLoader
from src.api.watermark_manager import WatermarkManager
from src.utils.adls_writer import ADLSWriter


def load_config():
    with open("config/config.json", "r") as file:
        return json.load(file)


def main():
    config = load_config()

    sales_config = config["apis"]["sales"]
    retry_config = config["retry"]

    retry_handler = RetryHandler(
        max_retries=retry_config["max_retries"],
        backoff_seconds=retry_config["backoff_seconds"],
        retry_status_codes=retry_config["retry_status_codes"]
    )

    api_client = APIClient(
        endpoint=sales_config["endpoint"],
        retry_handler=retry_handler
    )

    pagination_handler = PaginationHandler(api_client)

    watermark_manager = WatermarkManager(
        "data/watermarks.json"
    )

    incremental_loader = IncrementalLoader(
        pagination_handler=pagination_handler,
        watermark_manager=watermark_manager
    )

    adls_writer = ADLSWriter(
        config["storage"]["landing_path"]
    )

    default_watermark = config["incremental_load"]["initial_watermark"]

    records = incremental_loader.load(
        location_ids=["YOUR_SQUARE_LOCATION_ID"],
        default_watermark=default_watermark
    )

    if not records:
        print("No new records found.")
        return

    print(f"Records fetched: {len(records)}")

    output_path = adls_writer.write_json(
        records=records,
        entity_name=sales_config["landing_folder"]
    )

    if output_path:
        new_watermark = datetime.now(
            timezone.utc
        ).isoformat()

        watermark_manager.update_watermark(
            key=sales_config["watermark_key"],
            watermark=new_watermark
        )

        print("Watermark updated successfully.")
        print(f"Landing path: {output_path}")


if __name__ == "__main__":
    main()
```
