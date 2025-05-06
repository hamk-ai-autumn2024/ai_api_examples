import os, json, asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy

async def extract_tech_content():
    # 1. LLM provider/model pair goes in LLMConfig
    llm_cfg = LLMConfig(
        provider="openai/gpt-4o-mini",          # "provider/model"
        api_token=os.getenv("OPENAI_API_KEY")   # env‑var still works
    )

    # 2. Build the strategy *once*
    llm_strategy = LLMExtractionStrategy(
        llm_config=llm_cfg,
        instruction="Extract only content related to technology",
        extraction_type="block",         # default; returns plain JSON
        input_format="markdown",
        extra_args={"temperature": 0.0, "max_tokens": 1000},
        apply_chunking=True, chunk_token_threshold=1000
    )

    # 3. Wrap it in a run‑config; put all “per‑crawl” flags here
    run_cfg = CrawlerRunConfig(
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS
    )

    # 4. Run
    async with AsyncWebCrawler() as crawler:             # headless browser auto‑defaults :contentReference[oaicite:5]{index=5}
        result = await crawler.arun(
            url="https://www.nbcnews.com/business",
            config=run_cfg
        )

    # 5. Handle errors & consume extraction
    if not result.success:
        raise RuntimeError(result.error_message)

    tech_content = json.loads(result.extracted_content)
    print(f"{len(tech_content)} tech items extracted")

    with open("tech_content.json", "w", encoding="utf-8") as f:
        json.dump(tech_content, f, indent=2)

    # Optional: show token usage/cost
    llm_strategy.show_usage()            # prints a tiny report :contentReference[oaicite:6]{index=6}

asyncio.run(extract_tech_content())
