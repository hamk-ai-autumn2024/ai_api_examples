import os
import json
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field

# This example no longer works with latest crawl4ai version

class OpenAIModelFee(BaseModel):
    model_name: str = Field(..., description="Name of the OpenAI model.")
    input_fee: str = Field(..., description="Fee for input token for the OpenAI model.")
    output_fee: str = Field(..., description="Fee for output token for the OpenAI model.")

# Assuming that OPENAI_API_KEY is set in the environment variables
async def extract_openai_fees():
    # Use the main pricing page which may be more accessible
    url = 'https://openai.com/pricing'

    async with AsyncWebCrawler(
        verbose=True,
        # Enable JavaScript rendering
        enable_javascript=True,
        # Add a reasonable timeout
        javascript_timeout=30
    ) as crawler:
        result = await crawler.arun(
            url=url,
            word_count_threshold=1,
            extraction_strategy=LLMExtractionStrategy(
                llm_provider="openai",
                model="gpt-4o-mini",
                schema=OpenAIModelFee.model_json_schema(),
                extraction_type="schema",
                instruction="From the crawled content, extract all mentioned model names along with their "
                            "fees for input and output tokens. Make sure not to miss anything in the entire content. "
                            'One extracted model JSON format should look like this: '
                            '{ "model_name": "GPT-4", "input_fee": "US$10.00 / 1M tokens", "output_fee": "US$30.00 / 1M tokens" }'
            ),
            bypass_cache=True,
        )

    # Print the type and content to understand what we're getting
    #print(result)
    print(f"Type of result.extracted_content: {type(result.extracted_content)}")
    print(f"Content: {result.extracted_content}")
    
    # Handle different possible formats
    try:
        # If it's already a Python object
        if isinstance(result.extracted_content, (list, dict)):
            model_fees = result.extracted_content
        # If it's a JSON string
        else:
            model_fees = json.loads(result.extracted_content)
            
        print(f"Number of models extracted: {len(model_fees)}")
        
        with open("openai_fees.json", "w", encoding="utf-8") as f:
            json.dump(model_fees, f, indent=2)
    except Exception as e:
        print(f"Error processing extraction result: {e}")
        # Save the raw output for inspection
        with open("raw_output.txt", "w", encoding="utf-8") as f:
            f.write(str(result.extracted_content))
        print("Raw output saved to raw_output.txt for inspection")

asyncio.run(extract_openai_fees())