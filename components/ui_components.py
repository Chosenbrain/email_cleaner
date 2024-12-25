import tkinter as tk

def create_button(parent, text, command):
    """Reusable button design."""
    button = tk.Button(
        parent, 
        text=text, 
        font=("Arial", 16, "bold"), 
        bg="#FBBF24", 
        fg="#1e1e2f", 
        width=40, 
        height=2, 
        command=command
    )
    return button
