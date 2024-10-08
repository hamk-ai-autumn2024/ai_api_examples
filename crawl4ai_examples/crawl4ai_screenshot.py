from crawl4ai import WebCrawler
import base64

# Create the WebCrawler instance
crawler = WebCrawler()
crawler.warmup()
url = "https://www.yle.fi/uutiset"

print(f"Running the crawler on {url}...")
# Run the crawler with the screenshot parameter
result = crawler.run(url=url, screenshot=True)

# Save the screenshot to a file
with open("screenshot.jpg", "wb") as f:
    f.write(base64.b64decode(result.screenshot))

print(f"Screenshot of {url} saved to 'screenshot.jpg'.")
