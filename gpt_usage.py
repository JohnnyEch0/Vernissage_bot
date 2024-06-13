import openai
import os
import sys
from dotenv import load_dotenv, find_dotenv
import helpers

_ = load_dotenv(find_dotenv()) # read local .env file


client = openai.OpenAI()

assistant_id = "asst_ysTuidcswz1rSfhJZwgGIjzR"

try:
    assistant = client.beta.assistants.retrieve(assistant_id)
except Exception as e:
    print(f"An error occurred while retrieving the assistant: {e}", file=sys.stderr)

# a thread can hold multiple messages
thread = client.beta.threads.create()

@helpers.timer_decorator
def get_assistant_response(message):

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    timeout_count = 0
    while True:
        if run.status == 'completed': 
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            single_massage = client.beta.threads.messages.retrieve(
                thread_id=thread.id,
                message_id=messages.data[0].id
            )

            return single_massage.content[0].text.value
        
        elif timeout_count > 10:
            print("Timeout error")
            return "Timeout error"
            
        else:
            print(run.status)
            timeout_count += 1



def check_assistant_exists(assistant_id):
    try:
        response = client.beta.assistants.retrieve(assistant_id)
        print("assistant found", response)
        return True if response else False
    except Exception as e:
        print(f"An error occurred while checking the assistant: {e}", file=sys.stderr)
        return False
    

