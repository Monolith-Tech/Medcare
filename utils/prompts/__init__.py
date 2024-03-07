# Prompts

import json


# transcription prompt
def conversation_prompt(transcription_input: str) -> str:
    with open('utils/prompts/conversation.json', 'r') as file:
        prompt = json.load(file)

    # Insert the input transcription into the last user role content
    prompt[-1]['content'] = prompt[-1]['content'].format(transcription=transcription_input)
    return prompt


# soap prompt
def SOAP_prompt(conversation_input: str) -> str:
    with open('utils/prompts/SOAP.json', 'r') as file:
        prompt = json.load(file)

    # Insert the input SOAP into the last user role content
    prompt[-1]['content'] = prompt[-1]['content'].format(conversation=conversation_input)
    return prompt


# DD prompt
def DD_prompt(SOAP: str, test_results: str) -> str:
    with open('utils/prompts/DD.json', 'r') as file:
        prompt = json.load(file)

    # Insert the input DD into the last user role content
    prompt[-1]['content'] = prompt[-1]['content'].format(
        SOAP = SOAP,
        test_results = test_results
    )
    return prompt


# DD prompt
def summarize_prompt(test_results: str) -> str:
    with open('utils/prompts/summarize.json', 'r') as file:
        prompt = json.load(file)

    # Insert the input DD into the last user role content
    prompt[-1]['content'] = prompt[-1]['content'].format(
        test_results = test_results
    )
    return prompt
