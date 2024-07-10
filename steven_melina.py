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
INTERVENING = True  # If True, get a user-intervention Input after each response.
DEBUG = False

# OpenAI Setup
client = OpenAI()
steven = client.beta.assistants.retrieve(STEVEN_ID)
melina = client.beta.assistants.retrieve(MELINA_ID)
thread = client.beta.threads.create()

agents = [steven, melina]

def get_assistant_response(message, assistant, thread, debug=False, prompt_intervention=False):
    if prompt_intervention:
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
        if counter > DIALOGUE_AMOUNT:
            break
        if speaker == agents[0]:
            completion = get_assistant_response(response, agents[1], thread, DEBUG, INTERVENING)
            speaker = agents[1]
        else:
            completion = get_assistant_response(response, agents[0], thread, DEBUG, INTERVENING )
            speaker = agents[0]

        logger.debug(f"{speaker.name}: {completion}")
        response = completion

        speech_file_path = Path(__file__).parent / f"speech{counter}.mp3"
        response_audio = audio.speech.create(
            model="tts-1",
            voice="echo" if speaker == agents[0] else "nova",
            input=f"{response}",
            )
        response_audio.stream_to_file(speech_file_path)


        counter += 1
        # time.sleep(1)

def get_prompt_intervention():
    message = f"Prompt - Intervention, would you like the system a specific way in which to react? \n"
    response = input(message)
    if response == "-q":
        sys.exit("User ended the program")
    return response


if __name__ == "__main__":
    message = "And with that, im gonna hand the conversation over to Steven and Melina, thank you so much!"
    # message = "Und damit übergebe ich das Gespräch an Steven und Melina, vielen Dank euch!"
    main(message, thread, agents, "Moderator")
    sys.exit(0)

