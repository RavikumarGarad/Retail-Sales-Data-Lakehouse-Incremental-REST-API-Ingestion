import json
from pathlib import Path


class WatermarkManager:

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def _load(self):
        if not self.file_path.exists():
            return {}

        with open(self.file_path, "r") as file:
            return json.load(file)

    def get_watermark(self, key, default_value):
        watermarks = self._load()

        return watermarks.get(key, default_value)

    def update_watermark(self, key, watermark):
        watermarks = self._load()

        watermarks[key] = watermark

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(self.file_path, "w") as file:
            json.dump(watermarks, file, indent=4)