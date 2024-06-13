import openai
import tiktoken
import os
import logging

import tkinter as tk
import tkinter.ttk as ttk
from ttkbootstrap import Style

import gpt_usage

# set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# handlers
file_handler = logging.FileHandler("gpt_usage.log")
file_handler.setLevel(logging.ERROR)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(c_format)
file_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


app = tk.Tk()
app.title("Vernissage Chatbot")
app.geometry("800x600")

# set ttkbootstrap theme cyborgq
style = Style("cyborg")
style.theme_use("cyborg")




app.columnconfigure((0, 1, 2), weight=1)
app.rowconfigure((0, 1, 2), weight=1)

# place output field
output = tk.Text(app, wrap="word", font=("Helvetica", 12))
output.grid(row=0, column=0, columnspan=3, rowspan=2, sticky="nsew")

# place input field

input_field_var = tk.StringVar()
input = tk.Entry(app, textvariable=input_field_var)
input.grid(row=2, column=0, columnspan=3, sticky="nsew")


def process_input_txt(input):
    input_txt = input.widget.get()
    input_field_var.set("")
    response = gpt_usage.get_assistant_response(input_txt)

    #logging
    logger.debug(f"User: {input_txt}, Bot: {response}")

    output.insert(tk.END, f"User: {input_txt}\n")
    output.insert(tk.END, f"Bot: {response}\n") 
    

    input_field_var.set("")


  
# Calling on_change when you press the return key
app.bind("<Return>", process_input_txt)



app.mainloop()


