# Prompts

import json


# transcription prompt
def conversation_prompt(transcription_input: str) -> str:
    with open('utils/prompts/conversation.json', 'r') as file:
        prompt = json.load(file)
        
    # Insert the input transcription into the last user role content
    prompt[-1]['content'].format(transcription=transcription_input)
    return prompt


# soap prompt
def SOAP_prompt(conversation_input: str) -> str:
    with open('utils/prompts/SOAP.json', 'r') as file:
        prompt = json.load(file)
        
    # Insert the input SOAP into the last user role content
    prompt[-1]['content'].format(conversation=conversation_input)
    return prompt

