# Create transcriptions

import openai

from utils import get_openai_response

import os 
from dotenv import load_dotenv
load_dotenv()

# OpenAI client
client = openai.OpenAI()
openai.api_key = os.environ["OPENAI_API_KEY"]

# Processing
def read_conversation(audio_file_input: str, verbose=True, save_to_file=None) -> str:
    """_summary_

    Args:
        audio_file_input (str): Audio file name. Eg. Demo_sessoin.mp3
        verbose (bool, optional): Print transcription. Defaults to True.
        save_to_file (str, optional): Save transcription to file. Defaults to None.
    """

    with open(audio_file_input, 'rb') as audio_file:
        print(f"* Transcribing {audio_file_input}")
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )

    if verbose:
        print('='*30 + '\n' + 'Raw transcription:' + '\n' + '-'*30 + '\n' + transcription)

    prompt = f"""Please correct any errors or inaccuracies in this transcript, ensuring that the conversation remains structured with the format 'Doctor: Patient:' to clearly distinguish between the two speakers. Only make changes where absolutely necessary.\n\n Transcript:\n\n {transcription}"""
    
    # /utils.py
    conversation = get_openai_response(
        prompt_content = prompt
    )

    if verbose:
        print('='*30 + '\n' + 'Conversation:' + '\n' + '-'*30 + '\n' + conversation)

    if save_to_file:
        with open(save_to_file, 'w') as file:
            file.write(conversation)
    
    return conversation


# main
if __name__ == "__main__":
    audio_file_name = 'Demo/demo_session.mp3'
    read_conversation(
        audio_file_input = 'demo_session.mp3',
        verbose = True,
        save_to_file = 'Demo/demo_session.txt'
    )
