import helpers
import sys
import gpt_usage
import tkinter as tk
import with_customtk as w_ctk

assistant_id = "asst_RrFvu2tTZl5PxFb9gFOD0CmI"

def process_input_txt(input_txt, assistant, thread):
    
    if input_txt is None or input_txt == "":
        logger.error("No input text provided")
        return
    
    logger.debug(f"process_input_txt called with {input_txt}")
    
    app.input_widget.delete(0, "end")

    # validate input
    moderation = gpt_usage.check_user_input(input_txt)
    if moderation:
        app.output(f"Leider konnte ich deine Anfrage nicht verarbeiten, bitte stelle Fragen im Bezug zur Ausstellung. \n", "Assistant")
        return
    
    # protect against prompt injection
    prompt_injection = gpt_usage.detect_prompt_injection(input_txt)
    if prompt_injection:
        app.output(f"Leider konnte ich deine Anfrage nicht verarbeiten, bitte stelle Fragen im Bezug zur Ausstellung. \n", "Assistant")
        return
    
    app.output(input_txt, "user")

    # get response from assistant
    response = gpt_usage.get_assistant_response(input_txt, assistant, thread, debug=True)

    #logging
    logger.debug(f"User: {input_txt}, Bot: {response}")

    # output.insert(tk.END, f"User: {input_txt}\n")
    app.output(response, "Assistant") 



if __name__ == "__main__":
    # logging setup
    logger = helpers.setup_logging()

    # check if assistant exists
    try:
        assistant, thread = gpt_usage.check_assistant_exists(assistant_id=assistant_id)
    except TypeError:
        sys.exit(1)
    
    logger.debug(f"assistant: {assistant}, thread: {thread}")
    
    
    # app setup
    app = w_ctk.Application()

    logger.debug("App created")
    
    # Calling on_change when you press the return key
    """
    app, output, input_widget, input_field_var = helpers.setup_tkinter_app()
    app.bind("<Return>", lambda x: process_input_txt(input_field_var.get(), assistant, thread))
    """
    app.send_button.bind("<Button-1>", lambda x: process_input_txt(app.input_widget.get(), assistant, thread))
    app.bind("<Return>", lambda x: process_input_txt(app.input_widget.get(), assistant, thread))
    app.mainloop()



