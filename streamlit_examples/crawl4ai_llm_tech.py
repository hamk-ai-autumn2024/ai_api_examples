import os
import json
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy

async def extract_tech_content():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url="https://www.nbcnews.com/business",
            extraction_strategy=LLMExtractionStrategy(
                provider="openai/gpt-4o-mini",
                api_token=os.getenv('OPENAI_API_KEY'),
                instruction="Extract only content related to technology"
            ),
            bypass_cache=True,
        )

    tech_content = json.loads(result.extracted_content)
    print(f"Number of tech-related items extracted: {len(tech_content)}")

    with open("tech_content.json", "w", encoding="utf-8") as f:
        json.dump(tech_content, f, indent=2)

asyncio.run(extract_tech_content())