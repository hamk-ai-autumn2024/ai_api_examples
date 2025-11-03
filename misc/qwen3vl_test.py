from openai import OpenAI
import base64
import requests

client = OpenAI(api_key="123", base_url="http://154.54.100.195:8000/v1")

model = "Qwen/Qwen3-VL-2B-Instruct"

def get_image_base64_from_url(image_url):
    response = requests.get(image_url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return base64.b64encode(response.content).decode("utf-8")

def ocr_page_with_nanonets_s(img_base64):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{img_base64}"},
                    },
                    {
                        "type": "text",
                        "text": "explain the photo in detail please!",
                    },
                ],
            }
        ],
        temperature=0.0,
        max_tokens=15000 # max 16192
    )
    return response.choices[0].message.content

#test_img_url = "https://m.media-amazon.com/images/I/81BsQ0JPvbL._UF894,1000_QL80_.jpg"
test_img_url = "https://images.cdn.yle.fi/image/upload/ar_1.4256983240223464,c_fill,g_faces,h_841,w_1200/dpr_1.0/q_auto:eco/f_auto/fl_lossy/v1641302788/39-89861461d44ab40631a"
img_base64 = get_image_base64_from_url(test_img_url)
print(ocr_page_with_nanonets_s(img_base64))