# Create transcriptions

import os 
from dotenv import load_dotenv
load_dotenv()

audio_file_name = "demo_session.mp3"
audio_file = open(audio_file_name, "rb")



# Create transcripts using OpenAI's Whisper

import openai

client = openai.OpenAI()
openai.api_key = os.environ["OPENAI_API_KEY"]

print(f"* Transcribing {audio_file_name}")

transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="text"
)

print(transcription)
with open('whisper.txt', 'w') as file:
    file.write(transcription)



# # Create transcripts using Assembly-AI

# import assemblyai as aai

# aai.settings.api_key = os.environ["ASSEMBLY_AI_API"]
# transcriber = aai.Transcriber()

# transcription = transcriber.transcribe(audio_file_name).text

# print(transcription)
# with open('assembly-ai.txt', 'w') as file:
#     file.write(transcription)




