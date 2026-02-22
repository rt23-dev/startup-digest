import anthropic
import os
import json
from db import is_seen, mark_seen

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """
You are a startup intelligence agent. Your job is to find the latest startup news including:
- New startups that have been founded recently
- Funding rounds (Seed, Series A, B, C etc.)
- General interesting startup news
- Job opportunities at startups

Search the web for the latest news. For each item found, return a JSON array like this:
[
  {
    "title": "...",
    "summary": "...",
    "url": "...",
    "category": "Funding | New Startup | News | Jobs"
  }
]
Return ONLY the JSON array, no extra text.
"""

def run_agent() -> list[dict]:
    queries = [
        "startup funding rounds today 2025",
        "new startups founded this week",
        "startup news today",
        "startup job opportunities this week"
    ]

    all_results = []

    for query in queries:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=[{"role": "user", "content": f"Search for: {query}"}]
        )

        # Extract text from response
        for block in response.content:
            if block.type == "text":
                try:
                    items = json.loads(block.text)
                    for item in items:
                        url = item.get("url", "")
                        if url and not is_seen(url):
                            all_results.append(item)
                            mark_seen(url)
                except json.JSONDecodeError:
                    pass

    return all_results