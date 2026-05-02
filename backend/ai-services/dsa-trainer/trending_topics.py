import os
import json
from typing import List, Dict, Any
from groq import Groq
import requests

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
RESOURCE_SCRAPER_URL = os.getenv("RESOURCE_SCRAPER_URL", "http://resource-scraper:8013")

# In-memory storage for custom trend data
custom_trends = {}

async def fetch_scraped_trends() -> Dict[str, int]:
    """Call resource-scraper to get raw topic mention counts."""
    try:
        response = requests.post(f"{RESOURCE_SCRAPER_URL}/scrape/dsa-trends", timeout=60)
        if response.status_code == 200:
            data = response.json()
            return data.get("trends", {})
    except Exception as e:
        print(f"Error fetching scraped trends: {e}")
    return {}

async def synthesize_trends_with_groq(scraped_counts: Dict[str, int]) -> List[Dict[str, Any]]:
    """Use Groq to convert raw counts into a curated list of trending topics."""
    # Format the scraped data as a string
    counts_str = "\n".join([f"- {topic}: {count} mentions" for topic, count in scraped_counts.items()])
    prompt = f"""
You are a DSA trend analyst. Below are raw mention counts for various DSA topics scraped from the web in the last few days.

{counts_str}

Based on this data and your knowledge of current interview trends, identify the top 15 hottest topics. For each topic, provide:
- topic_name (string)
- category (e.g., "Array", "Tree", "Dynamic Programming")
- importance_score (integer 1-100, with 100 being most important)
- reason_for_trend (string, why it's hot now)
- key_subtopics (list of strings)
- frequency_in_interviews (string like "Very High", "High", "Medium")

Return the data as a JSON object with a key "topics" containing the array.
"""
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You output only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        if isinstance(data, dict) and "topics" in data:
            return data["topics"]
        elif isinstance(data, list):
            return data
        else:
            return []
    except Exception as e:
        print(f"Groq synthesis error: {e}")
        return []

async def get_trending_topics(source: str = "hybrid") -> List[Dict[str, Any]]:
    """
    Main function to get trending topics.
    source can be:
    - "hybrid": scrape then synthesize with Groq (default)
    - "groq": only Groq (fallback)
    - "custom": use manually set custom trends
    - "fallback": use hardcoded fallback
    """
    if source == "custom":
        if custom_trends:
            return custom_trends.get("topics", [])
        else:
            source = "hybrid"  # fallback to hybrid if custom empty
    if source == "hybrid":
        scraped = await fetch_scraped_trends()
        if scraped:
            return await synthesize_trends_with_groq(scraped)
        else:
            # if scraping fails, fallback to groq only
            source = "groq"
    if source == "groq":
        return await fetch_trending_topics_from_groq()
    # fallback
    return get_fallback_trends()

async def fetch_trending_topics_from_groq() -> List[Dict[str, Any]]:
    """Original Groq‑only method (fallback)."""
    prompt = """
You are a DSA trend analyst. Based on your knowledge of the software engineering interview landscape in 2025-2026, identify the top 15 hottest Data Structures and Algorithms topics that candidates should focus on.

For each topic, provide:
- topic_name (string)
- category (e.g., "Array", "Tree", "Dynamic Programming")
- importance_score (integer 1-100, with 100 being most important)
- reason_for_trend (string, why it's hot now)
- key_subtopics (list of strings)
- frequency_in_interviews (string like "Very High", "High", "Medium")

Return the data as a JSON object with a key "topics" containing the array.
"""
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You output only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        if isinstance(data, dict) and "topics" in data:
            return data["topics"]
        elif isinstance(data, list):
            return data
        else:
            return get_fallback_trends()
    except Exception as e:
        return get_fallback_trends()

def get_fallback_trends() -> List[Dict[str, Any]]:
    """Hardcoded fallback topics."""
    return [
        {"topic_name": "Dynamic Programming", "category": "DP", "importance_score": 100,
         "reason_for_trend": "Core to FAANG interviews; tests state management",
         "key_subtopics": ["Knapsack", "LCS", "Edit Distance", "Matrix Chain"],
         "frequency_in_interviews": "Very High"},
        {"topic_name": "Graph Algorithms", "category": "Graph", "importance_score": 98,
         "reason_for_trend": "Real-world applications in networking, social media",
         "key_subtopics": ["BFS/DFS", "Dijkstra", "Topological Sort", "Union-Find"],
         "frequency_in_interviews": "Very High"},
        # ... (other topics as before)
    ]

def update_custom_trends(topics: List[Dict[str, Any]]):
    """Update the in-memory custom trends (fine-tuning)."""
    global custom_trends
    custom_trends["topics"] = topics
    custom_trends["last_updated"] = __import__('datetime').datetime.utcnow().isoformat()
    return {"message": "Custom trends updated", "count": len(topics)}