import subprocess
import json
import os
import time
from typing import List, Dict, Any

def run_spider(spider_name: str, output_file: str = None):
    """Run a single spider and save output to a file."""
    cmd = [
        "scrapy", "crawl", spider_name,
        "-s", "LOG_LEVEL=INFO"
    ]
    # Optionally specify output file (scrapy can do this via -o)
    if output_file:
        cmd.extend(["-o", output_file])
    result = subprocess.run(cmd, cwd="./scrapy_project", capture_output=True, text=True)
    return result.returncode == 0

def run_all_spiders():
    """Run all defined spiders."""
    spiders = ["codeforces", "leetcode", "geeksforgeeks"]
    results = {}
    for spider in spiders:
        print(f"Running {spider}...")
        output = f"/tmp/{spider}_output.json"
        success = run_spider(spider, output)
        results[spider] = {"success": success, "output": output if success else None}
    return results

if __name__ == "__main__":
    run_all_spiders()