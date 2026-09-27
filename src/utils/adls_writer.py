import json
from datetime import datetime


class ADLSWriter:

    def __init__(self, landing_path):
        self.landing_path = landing_path

    def write_json(self, records, entity_name):
        current_date = datetime.utcnow()

        output_path = (
            f"{self.landing_path}/"
            f"{entity_name}/"
            f"year={current_date.year}/"
            f"month={current_date.month:02d}/"
            f"day={current_date.day:02d}/"
            f"{entity_name}_{current_date.strftime('%Y%m%d%H%M%S')}.json"
        )

        print(f"Writing {len(records)} records to:")
        print(output_path)

        # ADLS write implementation will be added here.

        return output_path