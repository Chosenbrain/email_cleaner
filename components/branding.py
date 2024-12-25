import tkinter as tk

def create_navbar(parent):
    navbar = tk.Frame(parent, bg="#4caf50", height=50)
    navbar.pack(side="top", fill="x")
    title_label = tk.Label(navbar, text="Email Cleaner & Extractor", font=("Arial", 20, "bold"), bg="#4caf50", fg="white")
    title_label.pack(pady=5)

def add_footer(parent):
    footer = tk.Label(parent, text="Created by Chosenbrain", font=("Arial", 12, "italic"), bg="#1e1e2f", fg="#b0b0b0")
    footer.pack(side="bottom", pady=5)
