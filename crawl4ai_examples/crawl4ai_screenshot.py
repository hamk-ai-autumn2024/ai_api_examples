import os, asyncio
from base64 import b64decode
from crawl4ai import AsyncWebCrawler, CacheMode

# This example no longer works with latest crawl4ai version

async def main():
    # Explicitly enable JavaScript rendering and other browser features
    async with AsyncWebCrawler(
        verbose=True,  # Print debugging info
        enable_javascript=True,  # Ensure JavaScript is enabled
        javascript_timeout=30  # Give enough time for the page to render
    ) as crawler:
        result = await crawler.arun(
            url="https://www.yle.fi/uutiset",
            bypass_cache=True,  # More current API than cache_mode
            screenshot=True
        )

        # Debug what the result contains
        print(f"Result attributes: {dir(result)}")
        
        # Check if screenshot is available using hasattr first
        if hasattr(result, "screenshot") and result.screenshot:
            print(f"Screenshot length: {len(result.screenshot)}")
            with open("yle.png", "wb") as f:
                f.write(b64decode(result.screenshot))
            print("[OK] Screenshot captured.")
        else:
            print("[ERROR] No screenshot available in result")
            
            # If you have success attribute, check it
            if hasattr(result, "success"):
                print(f"Success status: {result.success}")
            
            # If you have error_message attribute, print it
            if hasattr(result, "error_message"):
                print(f"Error message: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(main())
