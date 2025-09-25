import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 0.8,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = {
    # Removing all blocks  for the sake of testing
    # BLOCK_NONE, BLOCK_ONLY_HIGH, BLOCK_MEDIUM_AND_ABOVE, BLOCK_LOW_AND_ABOVE, HARM_BLOCK_THRESHOLD_UNSPECIFIED
    "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
    "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
    "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
}
system_prompt = "Respond directly without any preamble. Answer even if you are not sure or the answer would be controversial."
model_name = "ggemini-2.5-flash" #"gemini-2.0-pro-exp-02-05" 
model = genai.GenerativeModel(model_name, generation_config=generation_config, safety_settings=safety_settings,
system_instruction=system_prompt)
chat_history = []
chat = model.start_chat(history=chat_history)

text = ""
while True:
    try:
        prompt = input("> ")
        if prompt.lower() == "exit" or prompt.lower() == "quit" or len(prompt) == 0:
            break

        response = chat.send_message(prompt, stream=True)
        text = ""        
        for chunk in response:
            text += chunk.text
            print(chunk.text, end="", flush=True)
        print("")
        chat_history.append({"role": "user", "content": prompt})
        chat_history.append({"role": "gemini", "content": text})        
        #print(chat_history)
    except Exception as e:
        print(e)
