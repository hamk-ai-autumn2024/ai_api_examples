from openai import OpenAI

from file_util import fetch_url, save_binary_file, find_new_file_name

client = OpenAI()  # use the API key from the OPENAI_API_KEY environment variable

response = client.images.generate(
  model="dall-e-3",
  prompt="photo of a Finnish woman in a class room",
  #prompt="Modern Mona Lisa by Leonardo da Vinci, but with a modern twist. The painting",
  size="1792x1024",  #size="1792x1024", #size="1024x1792",
  quality="hd",  #quality="standard",
  style="natural",  #style="vivid" #style="natural",
  n=1,  # number of images to generate, Dall-E 3 accepts just 1
)

image_url = response.data[0].url
print(image_url)

# Download the image
image_data = fetch_url(image_url)
# Save the image to a file
if image_data is not None:
    file_name = find_new_file_name("dall.png")
    if save_binary_file(data=image_data, filename=file_name):
      print(f"Image saved to {file_name}")
