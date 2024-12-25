import tkinter as tk

def create_back_button(parent, command):
    button = tk.Button(parent, text="Back", command=command, font=("Arial", 16, "bold"))
    button.pack(pady=20)
