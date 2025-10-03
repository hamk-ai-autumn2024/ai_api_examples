"""Crawl4AI 0.6.2+ example: extract tech content with an OpenAI LLM."""

import asyncio
import json
from pathlib import Path
from typing import Any, List, Union

from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy

TECH_URL = "https://www.nbcnews.com/business"
OUTPUT_PATH = Path("tech_content.json")


async def extract_tech_content() -> None:
    llm_config = LLMConfig(provider="openai/gpt-4o-mini")
    extraction_strategy = LLMExtractionStrategy(
        llm_config=llm_config,
        instruction="Extract only content related to technology.\nReturn an array of JSON objects with keys 'title' and 'url'.",
        force_json_response=True,
        verbose=True,
    )

    run_config = CrawlerRunConfig(
        extraction_strategy=extraction_strategy,
        cache_mode=CacheMode.BYPASS,
        verbose=True,
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=TECH_URL, config=run_config)

    if not result.success:
        raise RuntimeError(f"Crawl failed: {result.error_message}")

    raw_content: Union[str, List[Any], None] = result.extracted_content
    if isinstance(raw_content, str):
        tech_content = json.loads(raw_content)
    elif raw_content is None:
        tech_content = []
    else:
        tech_content = raw_content

    print(f"Number of tech-related items extracted: {len(tech_content)}")
    for item in tech_content:
        #print(item)
        if "content" in item:
            print(item["content"][0])
            
    OUTPUT_PATH.write_text(json.dumps(tech_content, indent=2), encoding="utf-8")


if __name__ == "__main__":
    asyncio.run(extract_tech_content())
