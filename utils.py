# Utilities

import openai

import os 
from dotenv import load_dotenv
load_dotenv()

# API_KEY setup
client = openai.OpenAI()
openai.api_key = os.environ["OPENAI_API_KEY"]

# models
model = "gpt-3.5-turbo"
model_16k = "gpt-3.5-turbo-16k"
model_4 = "gpt-4"

# GPT chat completion
def get_openai_response(prompt_content: str, model=model):
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {
                "role": "system",
                "content": prompt_content
            }
        ],
        temperature = 0.3,
    )

    output = response.choices[0].message.content
    return output

