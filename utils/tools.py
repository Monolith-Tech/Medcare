# Utilities

import openai

import os 
from dotenv import load_dotenv
load_dotenv()

# API_KEY setup
openai_client = openai.OpenAI()
openai.api_key = os.environ["OPENAI_API_KEY"]

# models
class Models:
    model_3 = "gpt-3.5-turbo"
    model_3_turbo = "gpt-3.5-turbo-16k"
    model_4 = "gpt-4"
    model_4_turbo = "gpt-4-turbo-preview"

# GPT chat completion
def get_openai_response(prompt, model=Models.model_3) -> str:
    response = openai_client.chat.completions.create(
        model = model,
        messages = prompt,
        temperature = 0.3,
    )

    output = response.choices[0].message.content
    return output

