import os
import json
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field

class OpenAIModelFee(BaseModel):
    model_name: str = Field(..., description="Name of the OpenAI model.")
    input_fee: str = Field(..., description="Fee for input token for the OpenAI model.")
    output_fee: str = Field(..., description="Fee for output token for the OpenAI model.")

async def extract_openai_fees():
    url = 'https://openai.com/api/pricing/'

    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url=url,
            word_count_threshold=1,
            extraction_strategy=LLMExtractionStrategy(
                provider="openai/gpt-4o-mini",
                api_token=os.getenv('OPENAI_API_KEY'),
                schema=OpenAIModelFee.model_json_schema(),
                extraction_type="schema",
                instruction="From the crawled content, extract all mentioned model names along with their "
                            "fees for input and output tokens. Make sure not to miss anything in the entire content. "
                            'One extracted model JSON format should look like this: '
                            '{ "model_name": "GPT-4", "input_fee": "US$10.00 / 1M tokens", "output_fee": "US$30.00 / 1M tokens" }'
            ),
            bypass_cache=True,
        )

    model_fees = json.loads(result.extracted_content)
    print(f"Number of models extracted: {len(model_fees)}")

    with open("openai_fees.json", "w", encoding="utf-8") as f:
        json.dump(model_fees, f, indent=2)

asyncio.run(extract_openai_fees())