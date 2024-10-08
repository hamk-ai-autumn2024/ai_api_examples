import asyncio
from crawl4ai import AsyncWebCrawler

# first install pip crawl4ai
# then run "playwright install" as normal user (not admin)
async def main():
    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler(verbose=True) as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url="https://www.nbcnews.com/business")

        # Print the extracted content
        print(result.markdown)

# Run the async main function
asyncio.run(main())
