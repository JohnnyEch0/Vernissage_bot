from openai import Client, OpenAI, audio
import time
import sys
from pathlib import Path

from random import choice
from helpers import setup_logging

from dotenv import load_dotenv
load_dotenv()


import assistants


logger = setup_logging()

STEVEN_ID = "asst_BvCViX4J5fbyhJLZfJLVtwVW"
MELINA_ID = "asst_cmK7Ou1cftZDqXZmj4lQmO4Y"
DIALOGUE_AMOUNT = 10
RESPONSE_DELIMITER = "####"
SPEAKER_DELIMITER = "----"


INTERVENING = False  # If True, get a user-intervention Input after each response.
DEBUG = False 
AUDIO_STREAMING = True # If True, stream the responses to audio files
SPEAKER_VOICES = ("echo", "nova")

# OpenAI Setup
client = OpenAI()
thread = client.beta.threads.create()

# Specification
talker_1_instructions = "You are a far-right proto-fascist person in a non-professional setting, talk like a redditor."
talker_2_instructions = "You are a far-left antifascist person in a bad spot in their live, but you try to cover it up with a layed-back attitude."
additional_instructions = "You are to have a conversation with depth, try to remember and talk upon the things the other person says."
conversation_name = "Last Weekend 1"
intro_message = "Start a conversation about how bad the tram system has become."
intro_speaker = None

talker_1 = assistants.create_assistant(client, talker_1_instructions + additional_instructions)
talker_2 = assistants.create_assistant(client, talker_2_instructions + additional_instructions)
talkers = [talker_1, talker_2]


 

def get_assistant_response(message, assistant, thread):
    # Chance for intervention via command line input
    if INTERVENING:
        response = get_prompt_intervention()
        if response != "":
            # add a system message
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

    print("starting the run with the last message")
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
    if not response:
        print("response/message is missing, using default instead")
        response = "Start an iteresting conversation."

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
        
        response = completion

        counter += 1

def stream_response_to_audio(response, speaker, counter):
    AUDIO_STREAMING_PATH = Path(__file__).parent / f"data/speech{counter}.mp3"
    print("creating audio from response")
    response_audio = audio.speech.create(
            model="tts-1",
            voice= SPEAKER_VOICES[0] if speaker == talkers[0] else SPEAKER_VOICES[1],
            input=f"{response}",
            )
    response_audio.stream_to_file(AUDIO_STREAMING_PATH)
    print("Audio succesfully created")

def get_prompt_intervention():
    message = f"Prompt - Intervention, would you like the system a specific way in which to react? \n"
    response = input(message)
    if response == "-q":
        sys.exit("User ended the program")
    return response

if __name__ == "__main__":
    if not AUDIO_STREAMING:
        with open("gpt_usage_last_conver.txt", "w") as file:
            file.write("")
        
    main(intro_message, thread, talkers, intro_speaker)
    from data import mp3_joiner, delete_files
    mp3_joiner.stitch_mp3_files("99audio" + conversation_name + ".mp3")
    delete_files.main()
    sys.exit(0)

