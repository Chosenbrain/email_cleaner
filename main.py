import tkinter as tk
from components.ui_components import create_button
from components.navigation import create_back_button
from components.branding import create_navbar, add_footer
from features.remove_duplicates import RemoveDuplicatesPage
from features.email_cleaner import email_cleaner_page
from features.email_sorter import EmailSorterPage

class EmailCleanerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Email Cleaner & Extractor - Created by Chosenbrain")
        self.geometry("800x600")
        self.resizable(False, False)
        self.configure(bg="#1e1e2f")

        create_navbar(self)
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_screen()
        
        tk.Label(self, text="Welcome to Email Cleaner & Extractor", font=("Arial", 24, "bold"), bg="#1e1e2f", fg="white").pack(pady=20)
        create_button(self, "🌀 Remove Duplicates & Suspicious Emails", self.open_remove_duplicates).pack(pady=15)
        create_button(self, "🧹 Email Cleaner (Remove Bounced Emails)", self.open_email_cleaner).pack(pady=15)
        create_button(self, "📑 Email Sorter", self.open_email_sorter).pack(pady=15)

        add_footer(self)

    def clear_screen(self):
        for widget in self.winfo_children():
            if widget.winfo_class() != 'Frame':
                widget.destroy()

    def open_remove_duplicates(self):
        RemoveDuplicatesPage(self)

    def open_email_cleaner(self):
        email_cleaner_page(self)

    def open_email_sorter(self):
        EmailSorterPage(self)
        
    def clear_screen(self):
        """Properly clear all widgets before switching pages"""
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = EmailCleanerApp()
    app.mainloop()
