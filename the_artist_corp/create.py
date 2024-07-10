
import openai
import time
import logging
import sys

from cs50 import SQL
from PIL import Image
import requests
from get_assistant_response import get_response as get_r
import os

# db = SQL("sqlite:///generated.db")

logger = logging.getLogger("mylogger")
# Configure logging
logging.basicConfig(filename='/path/to/logfile.log', level=logging.INFO)

# Create a handler to write to the log file
current_path = os.getcwd()
file_handler = logging.FileHandler(f'{current_path}/the_artist_corp/generated/generators.log')
file_handler.setLevel(logging.INFO)

# Add the handler to the logger
logger.addHandler(file_handler)

logger.error("Starting the artist corp")

artist_id = "asst_gYOk4TIfYW7ghgrw6PhvMXWI"

client = openai.OpenAI()
# artist = client.beta.assistants.retrieve(artist_id)
thread = client.beta.threads.create()

artist = client.beta.assistants.create(
    instructions="You are an highly skilled artist, you will take the users input as inspiration and create a detailed description of an intricate and very clever visual artwork.\
        When doing this, you always combine the inspiration in creative ways with your own ideas and experiences.\
            You are anti-establishment and always try to push the boundaries of what is possible.\
                You have been raised christian and with a lot of computers and games. You love music.\
                    You love collages, streetart and the internet.\
                        You wont explain your art, you want the viewer to make up their own mind.\
                            you will use imagery and ideas from your past and present to create a unique piece of art.",
    name="The Artist",
    tools=[],
    model="gpt-4-turbo",
    temperature=0.9,
)

prompt_engineer = client.beta.assistants.create(
    instructions="You are a master of creating prompts for the artist. \
        You will take the artwork as an input and respond with a prompt to create this artwork with gaenerative Image generator that the user specifies. ",
    name="Prompt Engineer",
    tools=[],
    model="gpt-4-turbo",
    temperature=0.4,
)




# get a great idea for an artwork
inspiration = input("Get a great idea for an artwork...")


# create the artwork
prompt = f"Create an artwork based on the idea: {inspiration}"
response = get_r(prompt, client, thread, artist)
# SQL.execute("INSERT INTO ideas (idea) VALUES (?)", response)
logger.error(f"Artwork: {response}")


# make it a prompt

prompt = f"Create an prompt for Dall-E 3 based on this artwork: {response}"
response = get_r(prompt, client, thread, prompt_engineer)
# SQL.execute("INSERT INTO prompts (prompt) VALUES (?)", response)
logger.error(f"Prompt: {response}")


# get dall-E image and save it

image = client.images.generate(
  model="dall-e-3",
  prompt=response,
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = image.data[0].url
logger.error(f"Image URL: {image_url}")

image = Image.open(requests.get(image_url, stream=True).raw)
path = f"{current_path}/the_artist_corp/generated/{inspiration}.png"
image.save(path)


# append the prompt to a textfile


