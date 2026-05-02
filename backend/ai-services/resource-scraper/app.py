import os
import time
import glob
import logging
import subprocess
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from scraper_runner import run_spider, run_all_spiders

app = FastAPI(title="Resource Scraper Service")

# -----------------------------------------------------------------------------
# Pydantic models
# -----------------------------------------------------------------------------
class ScrapeRequest(BaseModel):
    spider: str  # e.g., "codeforces", "leetcode", "geeksforgeeks", or "all"
    output_file: Optional[str] = None

class ScrapeResponse(BaseModel):
    spider: str
    success: bool
    message: str
    output_file: Optional[str] = None

class ProblemFileInfo(BaseModel):
    filename: str
    size: int
    modified: float

class ProblemListResponse(BaseModel):
    platform: str
    files: List[ProblemFileInfo]

# -----------------------------------------------------------------------------
# Background task helper
# -----------------------------------------------------------------------------
def run_spider_task(spider: str, output: str):
    """
    Task to run a spider in the background.
    Logs the result (in a real app, you could update a database).
    """
    success = run_spider(spider, output)
    logging.info(f"Spider {spider} finished with success={success}, output={output}")

# -----------------------------------------------------------------------------
# API Endpoints
# -----------------------------------------------------------------------------
@app.post("/scrape", response_model=ScrapeResponse)
async def scrape(req: ScrapeRequest, background_tasks: BackgroundTasks):
    """
    Trigger a spider to run.
    - spider: "codeforces", "leetcode", "geeksforgeeks", or "all"
    - output_file: optional custom output path (default: /tmp/<spider>_<timestamp>.json)
    """
    if req.spider == "all":
        background_tasks.add_task(run_all_spiders)
        return ScrapeResponse(
            spider="all",
            success=True,
            message="All spiders started in background",
            output_file=None
        )
    
    # Validate spider name
    valid_spiders = ["codeforces", "leetcode", "geeksforgeeks"]
    if req.spider not in valid_spiders:
        raise HTTPException(status_code=400, detail=f"Invalid spider. Choose from {valid_spiders} or 'all'")
    
    # Generate default output filename if not provided
    output = req.output_file or f"/tmp/{req.spider}_output_{int(time.time())}.json"
    
    # Run in background
    background_tasks.add_task(run_spider_task, req.spider, output)
    
    return ScrapeResponse(
        spider=req.spider,
        success=True,
        message=f"Spider {req.spider} started in background",
        output_file=output
    )

@app.get("/problems/{platform}", response_model=ProblemListResponse)
async def list_problems(platform: str):
    """
    List all scraped problem files for a given platform.
    Files are stored in /tmp/problems_<platform>_*.json (as defined in the pipeline).
    """
    pattern = f"/tmp/problems_{platform}_*.json"
    files = glob.glob(pattern)
    
    file_list = []
    for f in files:
        stat = os.stat(f)
        file_list.append(ProblemFileInfo(
            filename=os.path.basename(f),
            size=stat.st_size,
            modified=stat.st_mtime
        ))
    
    # Sort by modification time (newest first)
    file_list.sort(key=lambda x: x.modified, reverse=True)
    
    return ProblemListResponse(platform=platform, files=file_list)

@app.get("/health")
async def health():
    return {"status": "ok"}