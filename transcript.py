# Create transcriptions

from utils import (
    openai_client,
    get_openai_response,
    Models
)

# Processing
def read_conversation(audio_file_input: str, verbose=True, save_to_file=None) -> str:
    """_summary_

    Args:
        audio_file_input (str): Audio file name. Eg. Demo_session.mp3
        verbose (bool, optional): Print transcription. Defaults to True.
        save_to_file (str, optional): Save transcription to file. Defaults to None.
    """

    with open(audio_file_input, 'rb') as audio_file:
        print(f"* Transcribing {audio_file_input}")
        transcription = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )

    if verbose:
        print('* Raw transcription:\n\n' + transcription)

    system_instruction = "Please correct any errors or inaccuracies in the transcript I will provide, ensuring that the conversation remains structured with the format JSON format with 'doctor' and 'patient' as keys and their scripts as values. Ensure that the conversation is accurately reflected in this format. Make changes only where necessary to both clean the transcript and fit this structured format, and output only the JSON structure without additional text."
    
    example_input = """Transcript:\n
Hi there, how can I help you today?
I've been having headaches and feeling dizzy.
When did these symptoms start?
About three days ago.
    """
    
    example_output = """
{
    "doctor": "Hi there, how can I help you today?",
    "patient": "I've been having headaches and feeling dizzy.",
    "doctor": "When did these symptoms start?",
    "patient": "About three days ago."
}
    """
    
    prompt = [
        {
            'role': 'system',
            'content': system_instruction
        },
        {
            'role': 'assistant',
            'content': 'Okay, I understood the task.'
        },
        {
            'role': 'user',
            'content': example_input
        },
        {
            'role': 'assistant',
            'content': example_output
        },
        {
            'role': 'user',
            'content': f"Transcript:\n\n {transcription}"
        }
    ]
    
    # /utils.py
    conversation = get_openai_response(
        prompt = prompt,
        model = Models.model_3_turbo
    )

    if verbose:
        print('* Conversation:\n\n' + conversation)

    if save_to_file:
        with open(save_to_file, 'w') as file:
            file.write(conversation)
    
    return conversation


# main
if __name__ == "__main__":
    audio_filename = 'Demo/demo_session.mp3'
    output_filename = 'Demo/demo_session.txt'
    
    read_conversation(
        audio_file_input = audio_filename,
        verbose = True,
        save_to_file = output_filename
    )
