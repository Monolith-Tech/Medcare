# Create transcriptions

from utils.tools import (
    openai_client,
    get_openai_response,
    Models
)

from utils.prompts import conversation_prompt


def transcribe_audio(audio_file_input: str) -> str:
    """
    Transcribe audio to text using the Whisper model.
    """
    
    with open(audio_file_input, 'rb') as audio_file:
        response = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        
    return response


def generate_conversation_transcript(transcription: str) -> str:
    """
    Generate structured conversation transcript from JSON file.
    """
    
    conversation = get_openai_response(
        prompt := conversation_prompt(transcription_input=transcription),
        model = Models.model_3_turbo
    )
    
    return conversation


def read_conversation(audio_file_input: str, verbose=True, save_to_file=None) -> str:
    """
    Process audio file to generate and optionally save a structured conversation.
    """

    print(f"* Transcribing {audio_file_input}")
    transcription = transcribe_audio(audio_file_input)
    if verbose:
        print('* Raw transcription:\n\n' + transcription)
    
    print(f"* Formatting transcription...")
    conversation = generate_conversation_transcript(transcription)
    if verbose:
        print('* Conversation:\n\n' + conversation)
    
    if save_to_file:
        with open(save_to_file, 'w') as file:
            file.write(conversation)
    
    return conversation


# main
if __name__ == "__main__":
    audio_filename = 'Demo/demo_session.mp3'
    output_filename = 'demo_session.test'
    
    read_conversation(
        audio_file_input=audio_filename,
        verbose=True,
        save_to_file=output_filename
    )
