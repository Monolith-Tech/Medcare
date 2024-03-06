# Prompts

import json


# transcription prompt
def transcription_prompt(transcription_input: str) -> str:
    with open('prompts/transcription.json', 'r') as file:
        prompt = json.load(file)
        
    # Insert the input transcription into the last user role content
    prompt[-1]['content'] = f"Transcript:\n\n{transcription_input}"
    return prompt
