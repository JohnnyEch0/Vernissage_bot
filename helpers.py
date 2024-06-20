import time

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time:.4f} seconds to execute.")
        return result
    return wrapper


def setup_logging():
    import logging
    logger = logging.getLogger("mylogger")
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

    # add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def setup_tkinter_app():
    import tkinter as tk
    from ttkbootstrap import Style

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
    return app, output, input, input_field_var