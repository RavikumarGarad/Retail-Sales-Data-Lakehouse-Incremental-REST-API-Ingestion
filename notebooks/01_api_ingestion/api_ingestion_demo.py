import json

from src.api.api_client import APIClient
from src.api.retry_handler import RetryHandler
from src.api.pagination import PaginationHandler
from src.api.incremental_loader import IncrementalLoader
from src.api.watermark_manager import WatermarkManager


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

    records = incremental_loader.load(
        location_ids=["YOUR_SQUARE_LOCATION_ID"],
        default_watermark=config["incremental_load"]["initial_watermark"]
    )

    print(f"Total records fetched: {len(records)}")


if __name__ == "__main__":
    main()