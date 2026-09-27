import json
import os

from azure.storage.filedatalake import DataLakeServiceClient


class ADLSWriter:

    def __init__(self, landing_path):
        self.storage_account = os.getenv("AZURE_STORAGE_ACCOUNT")
        self.storage_key = os.getenv("AZURE_STORAGE_KEY")

        if not self.storage_account or not self.storage_key:
            raise ValueError(
                "AZURE_STORAGE_ACCOUNT or AZURE_STORAGE_KEY is not set."
            )

        self.service_client = DataLakeServiceClient(
            account_url=f"https://{self.storage_account}.dfs.core.windows.net",
            credential=self.storage_key
        )

    def write_json(self, records, entity_name):

        if not records:
            print("No records to write.")
            return None

        file_system, base_path = self._parse_adls_path()

        file_system_client = self.service_client.get_file_system_client(
            file_system
        )

        file_path = (
            f"{base_path}/{entity_name}/"
            f"{entity_name}_{self._timestamp()}.json"
        )

        file_client = file_system_client.get_file_client(file_path)

        data = json.dumps(records, indent=2)

        file_client.upload_data(
            data,
            overwrite=True
        )

        print(f"Successfully landed data to: {file_path}")

        return file_path

    def _parse_adls_path(self):
        path = self.landing_path.replace("abfss://", "")

        container, path = path.split("@", 1)
        path = path.split(".dfs.core.windows.net/", 1)[1]

        return container, path

    @staticmethod
    def _timestamp():
        from datetime import datetime, timezone

        return datetime.now(timezone.utc).strftime(
            "%Y%m%d%H%M%S"
        )