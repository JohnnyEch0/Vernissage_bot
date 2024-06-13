import helpers
import sys
import gpt_usage
import tkinter as tk

assistant_id = "asst_ysTuidcswz1rSfhJZwgGIjzR"


def process_input_txt(input):
    input_txt = input.widget.get()
    input_field_var.set("")
    response = gpt_usage.get_assistant_response(input_txt)

    #logging
    logger.debug(f"User: {input_txt}, Bot: {response}")

    output.insert(tk.END, f"User: {input_txt}\n")
    output.insert(tk.END, f"Bot: {response}\n") 

    input_field_var.set("")


if __name__ == "__main__":
    # check if assistant exists
    if not gpt_usage.check_assistant_exists(assistant_id=assistant_id):
        sys.exit(1)
    
    # logging setup
    logger = helpers.setup_logging()

    # app setup
    app, output, input, input_field_var = helpers.setup_app()
    
    # Calling on_change when you press the return key
    app.bind("<Return>", process_input_txt)

    app.mainloop()



