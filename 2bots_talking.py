from openai import Client, OpenAI, audio
import time
import sys
from pathlib import Path

from random import choice
from helpers import setup_logging

from dotenv import OPEN_AI_KEY


logger = setup_logging()

STEVEN_ID = "asst_BvCViX4J5fbyhJLZfJLVtwVW"
MELINA_ID = "asst_cmK7Ou1cftZDqXZmj4lQmO4Y"
DIALOGUE_AMOUNT = 8
RESPONSE_DELIMITER = "####"
SPEAKER_DELIMITER = "----"


INTERVENING = True  # If True, get a user-intervention Input after each response.
DEBUG = False 
AUDIO_STREAMING = False # If True, stream the responses to audio files
SPEAKER_VOICES = ("echo", "nova")

# OpenAI Setup
client = OpenAI()
steven = client.beta.assistants.retrieve(STEVEN_ID)
melina = client.beta.assistants.retrieve(MELINA_ID)
thread = client.beta.threads.create()

agents = [steven, melina]

def get_assistant_response(message, assistant, thread):
    if INTERVENING:
        response = get_prompt_intervention()
        if response != "":
            message_sys = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="assistant",
                content=response
                )


    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
        )

    run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
            max_completion_tokens=800
            )
    
    messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
    
    timeout_count = 0
    while True:
        
        if run.status == 'completed': 
            single_massage = client.beta.threads.messages.retrieve(
                thread_id=thread.id,
                message_id=messages.data[0].id
            )

            return single_massage.content[0].text.value
        
        elif timeout_count > 15:
            print("Timeout error")
            return "Timeout error"
            
        else:
            print(run.status)
            timeout_count += 1
            time.sleep(0.5)

def main(response, thread, agents, speaker):
    counter = 0
    while True:
        if counter == DIALOGUE_AMOUNT:
            break
        if speaker == agents[0]:
            completion = get_assistant_response(response, agents[1], thread)
            speaker = agents[1]
        else:
            completion = get_assistant_response(response, agents[0], thread )
            speaker = agents[0]

        print(f"----Message Nr: {counter}/{DIALOGUE_AMOUNT-1}----")
        logger.debug(f"{speaker.name}: {completion}")
        

        if AUDIO_STREAMING:
            stream_response_to_audio(completion, speaker, counter)
            
        else:
            with open("gpt_usage_last_conver.txt", "a") as file:
                file.write(f"{speaker.name}:{SPEAKER_DELIMITER} {completion}{RESPONSE_DELIMITER} \n")
        

        counter += 1

def stream_response_to_audio(response, speaker, counter):
    AUDIO_STREAMING_PATH = Path(__file__).parent / f"data/speech{counter}.mp3"
    response_audio = audio.speech.create(
            model="tts-1",
            voice= SPEAKER_VOICES[0] if speaker == agents[0] else SPEAKER_VOICES[1],
            input=f"{response}",
            )
    response_audio.stream_to_file(AUDIO_STREAMING_PATH)

def get_prompt_intervention():
    message = f"Prompt - Intervention, would you like the system a specific way in which to react? \n"
    response = input(message)
    if response == "-q":
        sys.exit("User ended the program")
    return response

if __name__ == "__main__":
    message = "And with that, im gonna hand the conversation over to Steven and Melina, thank you so much!"

    if not AUDIO_STREAMING:
        with open("gpt_usage_last_conver.txt", "w") as file:
            file.write("")
        
    main(message, thread, agents, "Moderator")
    sys.exit(0)

