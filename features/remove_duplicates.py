import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
import re
import threading
import json
import matplotlib.pyplot as plt
from utils.email_utils import remove_duplicates, remove_suspicious_emails

class RemoveDuplicatesPage:
    def __init__(self, parent):
        self.parent = parent
        self.cleaned_emails = []
        self.suspicious_emails = []
        self.duplicate_emails = []
        self.all_emails = []  # Holds all emails (uploaded + pasted)
        self.build_ui()

    def build_ui(self):
        """Build the user interface."""
        self.parent.clear_screen()

        # Page Title
        tk.Label(self.parent, text="🌐 Remove Duplicates & Suspicious Emails", font=("Arial", 24, "bold"), bg="#1e1e2f", fg="white").pack(pady=10)

        # Upload file button
        self.create_button("📁 Upload Email File", self.upload_multiple_files, "#007BFF", "#0056b3", "#000000").pack(pady=10)

        tk.Label(self.parent, text="OR", font=("Arial", 14, "bold"), bg="#1e1e2f", fg="white").pack()

        # Paste or upload email text area
        tk.Label(self.parent, text="Paste or Upload Your Email List Below:", font=("Arial", 14, "bold"), bg="#1e1e2f", fg="white").pack()
        self.email_input = scrolledtext.ScrolledText(self.parent, wrap="word", width=60, height=15, font=("Arial", 12))
        self.email_input.pack(pady=10, fill="both", expand=True)

        # Process button
        self.create_button("🚀 Process Emails", self.process_emails, "#28a745", "#218838", "#000000").pack(pady=10)

        # Download button
        self.create_button("🔽 Download Cleaned File", self.download_file, "#17a2b8", "#117a8b", "#000000").pack(pady=10)

        # Back button
        self.create_button("🔙 Back", self.back_to_main_menu, "#FF6347", "#FF4500", "#000000").pack(pady=20)

    def create_button(self, text, command, bg_color, hover_color, text_color):
        """Helper function to create consistent button styles."""
        button = tk.Button(self.parent, text=text, command=command, font=("Arial", 12, "bold"), bg=bg_color, fg=text_color, 
                           width=20, height=1, bd=2, relief="raised", cursor="hand2")
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=bg_color))
        return button

    def upload_multiple_files(self):
        """Allow multiple email files to be uploaded at once and display them in the text area."""
        file_paths = filedialog.askopenfilenames(filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv")])
        all_emails = []
        for file_path in file_paths:
            try:
                with open(file_path, 'r') as file:
                    all_emails.extend(file.read().splitlines())
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file: {e}")
        self.all_emails.extend(all_emails)
        self.display_emails()
        messagebox.showinfo("Success", "Files uploaded successfully. Click 'Process Emails' to continue.")

    def display_emails(self):
        """Display the pasted and uploaded emails in the main text area and copy to clipboard."""
        self.email_input.delete("1.0", tk.END)
        for email in self.all_emails:
            self.email_input.insert(tk.END, f"{email}\n")
        self.copy_to_clipboard("\n".join(self.all_emails))

    def copy_to_clipboard(self, text):
        """Copy the provided text to the clipboard."""
        self.parent.clipboard_clear()
        self.parent.clipboard_append(text)
        self.parent.update()  # now it stays on the clipboard even after the app is closed

    def process_emails(self):
        """Process emails pasted in the text area and uploaded files."""
        emails = self.email_input.get("1.0", "end").splitlines()
        self.process_emails_list(emails)

    def process_emails_list(self, emails):
        if not emails:
            messagebox.showwarning("Warning", "No emails to process.")
            return

        emails = [email.strip() for email in emails if email.strip()]
        original_count = len(emails)
        unique_emails = list(set(emails))
        self.duplicate_emails = list(set(emails) - set(unique_emails))
        self.cleaned_emails, self.suspicious_emails = remove_suspicious_emails(unique_emails)
        self.show_summary_report(original_count, len(self.duplicate_emails), len(self.suspicious_emails), len(self.cleaned_emails))

    def show_summary_report(self, total, duplicates, suspicious, cleaned):
        report = f"""
        📋 **Summary Report**
        ----------------------------
        🖍 Total Emails: {total}
        ✂️ Duplicates Removed: {duplicates}
        🚫 Suspicious Emails Removed: {suspicious}
        ✅ Total Cleaned Emails: {cleaned}
        """
        messagebox.showinfo("Summary Report", report)

    def download_file(self):
        if not self.cleaned_emails:
            messagebox.showwarning("Warning", "No cleaned emails available for download.")
            return

        folder_path = filedialog.askdirectory()
        if folder_path:
            file_path = os.path.join(folder_path, 'cleaned_emails.txt')
            try:
                with open(file_path, 'w') as file:
                    file.write("\n".join(self.cleaned_emails))
                messagebox.showinfo("Success", f"File saved successfully to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

    def back_to_main_menu(self):
        """Clear all data and return to the main menu."""
        self.cleaned_emails.clear()
        self.suspicious_emails.clear()
        self.duplicate_emails.clear()
        self.all_emails.clear()
        self.email_input.delete("1.0", tk.END)
        self.parent.create_main_menu()
