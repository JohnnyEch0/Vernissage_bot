import helpers
import sys
import gpt_usage
import tkinter as tk

assistant_id = "asst_ysTuidcswz1rSfhJZwgGIjzR"

def process_input_txt(input_txt, assistant, thread):
    
    if input_txt is None or input_txt == "":
        logger.error("No input text provided")
        return
    
    logger.debug(f"process_input_txt called with {input_txt}")
    
    input_field_var.set("")
    # validate input
    moderation = gpt_usage.check_user_input(input_txt)
    if moderation:
        output.insert(tk.END, f"Leider konnte ich deine Anfrage nicht verarbeiten, bitte stelle Fragen im Bezug zur Ausstellung. \n")
        return
    
    # protect against prompt injection
    prompt_injection = gpt_usage.detect_prompt_injection(input_txt)
    if prompt_injection:
        output.insert(tk.END, f"Leider konnte ich deine Anfrage nicht verarbeiten, bitte stelle Fragen im Bezug zur Ausstellung. \n")
        return

    # get response from assistant
    response = gpt_usage.get_assistant_response(input_txt, assistant, thread, debug=True)

    #logging
    logger.debug(f"User: {input_txt}, Bot: {response}")

    # output.insert(tk.END, f"User: {input_txt}\n")
    output.insert(tk.END, f"Bot: {response}\n") 

    input_field_var.set("")


if __name__ == "__main__":
    # check if assistant exists
    try:
        assistant, thread = gpt_usage.check_assistant_exists(assistant_id=assistant_id)
    except TypeError:
        sys.exit(1)
    
    
    # logging setup
    logger = helpers.setup_logging()

    # app setup
    app, output, input_widget, input_field_var = helpers.setup_app()
    
    # Calling on_change when you press the return key
    app.bind("<Return>", lambda x: process_input_txt(input_field_var.get(), assistant, thread))

    app.mainloop()



