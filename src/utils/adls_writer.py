"""
ADLS Gen2 Writer

Responsible for writing raw API data to
Azure Data Lake Storage Gen2 landing zone.
"""

import json
from datetime import datetime

from azure.storage.filedatalake import DataLakeServiceClient


class ADLSWriter:

    def __init__(self, config):
        """
        Initialize ADLS connection using configuration.
        """

        self.config = config

        storage_account = config["adls"]["storage_account"]
        container = config["adls"]["container"]
        account_key = config["adls"]["account_key"]

        self.container_client = (
            DataLakeServiceClient(
                account_url=f"https://{storage_account}.dfs.core.windows.net",
                credential=account_key
            )
            .get_file_system_client(container)
        )

    def write_json(self, records, target_path):
        """
        Write JSON records to ADLS Gen2.

        Parameters:
            records      : List of API records
            target_path  : Destination path in ADLS
        """

        if not records:
            print("No records to write.")
            return

        try:

            # Convert records to JSON
            json_data = json.dumps(
                records,
                indent=2,
                default=str
            )

            # Create file client
            file_client = self.container_client.get_file_client(
                target_path
            )

            # Upload data
            file_client.upload_data(
                json_data,
                overwrite=True
            )

            print(
                f"Successfully written "
                f"{len(records)} records to ADLS: "
                f"{target_path}"
            )

        except Exception as error:

            print(
                f"Failed to write data to ADLS: {error}"
            )

            raise


if __name__ == "__main__":

    import json

    # Load project configuration
    with open(
        "config/config.json",
        "r",
        encoding="utf-8"
    ) as file:

        config = json.load(file)

    writer = ADLSWriter(config)

    print("ADLS Writer initialized successfully.")