import customtkinter as ctk


colors = {
    "p_d_grey" : "#2f2e30",
    "p_m1_grey" : "#3f3e40",
    "p_m2_grey" : "#57525c",
    "p_m3_grey" : "#675f6e",
    "p_l_grey" : "#998aa8",
    "d_purple" : "#392c47",
}

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Vernissage Bot")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")

        self.rowconfigure(0, weight=1)

        self.rowconfigure(1, weight=5)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=6)
        self.columnconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(self, text="Vernissage Assistant", font=("Helvetica", 40, "bold"))
        self.title_label.grid(row=0, column=0, pady=30, columnspan=2, sticky="nsew")

        self.frame = ctk.CTkScrollableFrame(self, fg_color=colors["p_d_grey"], corner_radius=10, border_width=1, border_color="darkgrey") # fg"#323232"
        self.frame.grid(row=1, column=0, sticky="nsew", ipadx=50, ipady=10, padx=50, pady=10, columnspan=2)

        self.frame.rowconfigure((0,1,2,3,4), weight=1)
        self.frame.columnconfigure((0,1), weight=1)

        self.send_button = ctk.CTkButton(self, text="Send", font=("Helvetica", 12), fg_color=colors["d_purple"])
        self.send_button.grid(row=2, column=1, pady=10, sticky="ew", padx=50)
        # self.send_button.bind("<Button-1>", lambda x: self.create_message(self.input_field.get()))

        self.input_widget = ctk.CTkEntry(self, width=100, font=("Helvetica", 12))
        self.input_widget.grid(row=2, column=0, pady=10, sticky="ew", padx=50)

        self.message_frames = []

        self.output = self.create_message
        

    def create_message(self, message, sender="user"):
        # message = self.input_widget.get()
        message_widget = Message_Widget(self.frame, message, sender, color= colors["p_m1_grey"] if sender == "user" else colors["p_m2_grey"])
        self.message_frames.append(message_widget)
        
        if len(self.message_frames) > 10:
            self.message_frames.pop(0)

        for i, widget in enumerate(self.message_frames):
            widget.grid_forget()
            widget.grid(row=i, column=1 if widget.sender == "user" else 0, sticky="ew", pady=10, padx=10, ipadx=5, ipady=5)

class Message_Widget(ctk.CTkFrame):
    def __init__(self, parent, message, sender, color="darkgrey"):
        super().__init__(parent, fg_color=color)
        self.message = message
        self.sender = sender
        self.message_label = ctk.CTkLabel(self, text=f"{sender}: {message}", font=("Helvetica", 12), wraplength=300, justify="left", fg_color=color)
        self.message_label.pack(side="left", padx=10, pady=5)

    def get_message(self):
        return self.message

    def get_sender(self):
        return self.sender

    def get_widget(self):
        return self.message_label

    def set_message(self, message):
        self.message = message
        self.message_label.config(text=f"{self.sender}: {self.message}")

    def set_sender(self, sender):
        self.sender = sender
        self.message_label.config(text=f"{self.sender}: {self.message}")

    def set_widget(self, widget):
        self.message_label = widget

"""
window = ctk.CTk()
window.title("Vernissage Bot")
window.geometry("800x600")
ctk.set_appearance_mode("dark")

window.rowconfigure(0, weight=1)

window.rowconfigure(1, weight=5)
window.rowconfigure(2, weight=1)
window.columnconfigure(0, weight=6)
window.columnconfigure(1, weight=1)


title_label = ctk.CTkLabel(window, text="Vernissage Assistant", font=("Helvetica", 40, "bold"))
# title_label.pack(pady=30)
title_label.grid(row=0, column=0, pady=30, columnspan=2, sticky="nsew")

frame = ctk.CTkFrame(window, fg_color=("#323232"), corner_radius=10, border_width=1, border_color="#0e0f16")
frame.grid(row=1, column=0, sticky="nsew", ipadx=50, ipady=10, padx=50, pady=10, columnspan=2)
# frame.pack(fill="both", padx=100, pady=100, expand=True)

frame.rowconfigure((0,1,2,3,4), weight=1)
frame.columnconfigure((0,1), weight=1)

send_button = ctk.CTkButton(window, text="Send", font=("Helvetica", 12))
send_button.grid(row=2, column=1, pady=10, sticky="ew", padx=50)
send_button.bind("<Button-1>", lambda x: create_message(input_field.get()))
# send_button.pack(pady=5, side="right", anchor="w", padx=100, )

input_field = ctk.CTkEntry(window, width=100, font=("Helvetica", 12))
input_field.grid(row=2, column=0, pady=10, sticky="ew", padx=50)
# input_field.pack(fill="x", padx=100, side="bottom", pady=30)

message_frames = []
def create_message(message, sender="user"):

    message = input_field.get()
    input_field.delete(0, "end")
    message_widget = Message_Widget(frame, message, sender)
    message_frames.append(message_widget)
    if len(message_frames) > 5:
        message_frames.pop(0)

    for i, widget in enumerate(message_frames):
        widget.grid_forget()
        widget.grid(row=i, column=1 if widget.sender == "user" else 0, sticky="ew", pady=10, padx=10, ipadx=5, ipady=5)
"""




# window.mainloop()