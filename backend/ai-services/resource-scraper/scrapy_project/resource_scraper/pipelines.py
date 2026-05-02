import json
import os
from datetime import datetime

class ProblemPipeline:
    """Pipeline to store scraped problems in a JSON file and optionally MongoDB."""

    def open_spider(self, spider):
        self.items = []
        self.filename = f"/tmp/problems_{spider.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    def close_spider(self, spider):
        with open(self.filename, 'w') as f:
            json.dump(self.items, f, indent=2)
        spider.logger.info(f"Saved {len(self.items)} items to {self.filename}")

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item