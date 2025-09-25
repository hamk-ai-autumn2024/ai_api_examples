from google import genai
from google.genai import types
import os
import requests

# Assume GEMINI_API_KEY is set in environment variable

# Define a function that the model can call to load a URL
load_url_declaration = {
    "name": "load_url",
    "description": "Loads the content of a given URL and returns it as text, or null if it cannot be loaded.",
    "parameters": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The absolute URL to fetch.",
            }
        },
        "required": ["url"],
    },
}


def load_url(url: str) -> str | None:
    """Fetch a URL and return the response text or None on failure."""
    try:
        resp = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                " AppleWebKit/537.36 (KHTML, like Gecko)"
                " Chrome/125.0.0.0 Safari/537.36"
            },
        )
        if resp.ok:
            # Return full text on success
            return resp.text
        return None
    except Exception:
        return None


# Configure the client and tools
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
tools = types.Tool(function_declarations=[load_url_declaration])
config = types.GenerateContentConfig(tools=[tools])

# Define user prompt using the sample URL
sample_url = "https://developers.googleblog.com/en/introducing-gemini-2-5-flash-image/"
contents = [
    types.Content(
        role="user",
        parts=[
            types.Part(
                text=(
                    "Please load this URL and provide a brief summary: "
                    f"{sample_url}"
                )
            )
        ],
    )
]

# Send request with function declarations
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=contents,
    config=config,
)

# Try to find a function call in the first candidate's parts
function_call = None
if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
    for part in response.candidates[0].content.parts:
        if getattr(part, "function_call", None):
            function_call = part.function_call
            break

print(function_call)

if function_call and function_call.name == "load_url":
    # Execute the function
    result = load_url(**function_call.args)
    print("Function execution: fetched content" if result else "Function execution: None")

    # Create a function response part
    function_response_part = types.Part.from_function_response(
        name=function_call.name,
        response={"result": result},
    )

    # Append the model's tool call and our function response
    contents.append(response.candidates[0].content)
    contents.append(types.Content(role="user", parts=[function_response_part]))

    final_response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=config,
        contents=contents,
    )

    print(final_response.text)
else:
    print("No function call was made or function call was not 'load_url'")
    print(f"Response: {response.text}")