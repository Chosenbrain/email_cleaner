import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog
import os
import re
import random
import string
import dns.resolver
import threading


class EmailSorterPage:
    def __init__(self, parent):
        self.parent = parent
        self.original_emails = []
        self.sorted = False
        self.sorted_emails = {}
        self.build_ui()

    def build_ui(self):
        """Build the user interface."""
        self.parent.clear_screen()

        # Page Title
        tk.Label(self.parent, text="📑 Advanced Email Sorter", font=("Arial", 24, "bold"), bg="#1e1e2f", fg="white").pack(pady=10)

        # Upload File Button
        self.create_button("📁 Upload Email File", self.upload_email_file, "#D3D3D3", "#A9A9A9", "#000000").pack(pady=10)

        # Paste Emails Section
        tk.Label(self.parent, text="Or Paste Email Leads Below:", font=("Arial", 14, "bold"), bg="#1e1e2f", fg="white").pack()
        self.email_input = scrolledtext.ScrolledText(self.parent, wrap="word", width=60, height=10, font=("Arial", 12))
        self.email_input.pack(pady=10, fill="both", expand=True)

        # Sort Emails Button
        self.sort_button = self.create_button("📋 Sort Emails", self.start_sorting_thread, "#D3D3D3", "#A9A9A9", "#000000")
        self.sort_button.pack(pady=10)

        # Real-Time Progress Feedback
        self.progress_label = tk.Label(self.parent, text="Awaiting action...", font=("Arial", 12, "bold"), bg="#1e1e2f", fg="#FFD700")
        self.progress_label.pack()

        # Download Button (Initially Disabled)
        self.download_button = self.create_button("🔽 Download Files", self.download_sorted_emails, "#D3D3D3", "#A9A9A9", "#000000")
        self.download_button.config(state="disabled")
        self.download_button.pack(pady=10)

        # Back Button
        self.create_button("🔙 Back", self.back_to_main_menu, "#D3D3D3", "#A9A9A9", "#000000").pack(pady=20)

    def create_button(self, text, command, bg_color, hover_color, text_color):
        """Helper function to create buttons with hover effects."""
        button = tk.Button(self.parent, text=text, command=command, font=("Arial", 12, "bold"), bg=bg_color, fg=text_color, 
                           width=25, height=2, bd=2, relief="raised", cursor="hand2")
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=bg_color))
        return button

    def upload_email_file(self):
        """Upload and display the contents of an email file."""
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    emails = file.read().splitlines()
                    self.original_emails = [email.strip() for email in emails if self.validate_email(email.strip())]
                    self.email_input.delete("1.0", tk.END)
                    self.email_input.insert(tk.END, "\n".join(self.original_emails))
                    messagebox.showinfo("Success", "Email file uploaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {e}")

    def validate_email(self, email):
        """Check if the email is valid."""
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email)

    def start_sorting_thread(self):
        """Start the sorting process in a separate thread."""
        threading.Thread(target=self.sort_and_save_emails).start()

    def sort_and_save_emails(self):
        """Sort emails by domain and save each domain's emails in a separate file."""
        self.progress_label.config(text="Starting email sorting...")
        emails = self.email_input.get("1.0", "end").splitlines()
        self.original_emails = [email.strip() for email in emails if self.validate_email(email.strip())]

        if not self.original_emails:
            messagebox.showwarning("Warning", "No valid emails to sort.")
            return

        domain_dict = {}
        for email in self.original_emails:
            domain = email.split("@")[1]
            main_provider = self.get_provider_from_mx(domain)
            self.progress_label.config(text=f"Sorting: {main_provider} (Processing {email})")
            self.parent.update_idletasks()

            if main_provider not in domain_dict:
                domain_dict[main_provider] = []
            domain_dict[main_provider].append(email)

        self.sorted_emails = domain_dict
        self.sorted = True
        self.download_button.config(state="normal")
        self.progress_label.config(text="Sorting complete. Ready to download files.")

    def get_provider_from_mx(self, domain):
        """Get the main provider for the domain using the MX record."""
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            if answers:
                mx_record = str(answers[0].exchange)
                if 'yahoo' in mx_record:
                    return 'yahoo'
                elif 'aol' in mx_record:
                    return 'aol'
                elif 'att' in mx_record or 'sbcglobal' in mx_record or 'currently' in mx_record:
                    return 'att'
                elif 'google' in mx_record or 'gmail' in mx_record:
                    return 'gmail'
                else:
                    return domain.replace('.', '_')
        except Exception:
            return domain.replace('.', '_')

    def download_sorted_emails(self):
        """Allow users to download sorted files."""
        folder_path = filedialog.askdirectory()
        if not folder_path:
            messagebox.showwarning("Warning", "No folder selected.")
            return

        for provider, emails in self.sorted_emails.items():
            if emails:
                file_name = os.path.join(folder_path, f"{provider}_emails.txt")
                with open(file_name, 'w') as file:
                    file.write("\n".join(emails))

        messagebox.showinfo("Success", "All files have been successfully downloaded!")

    def back_to_main_menu(self):
        """Go back to the main menu."""
        self.parent.create_main_menu()
