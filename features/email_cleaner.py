import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import re
import os
import threading
import socket
import smtplib
from queue import Queue  # Thread-safe queue for email statuses
from utils.email_utils import remove_bounced_emails_from_list, validate_email

# Global Variables
main_emails = []
bounce_emails = []
validation_emails = []
email_statuses = Queue()

def email_cleaner_page(parent):
    """Page logic for Email Cleaner (Manual & Automatic Cleaning)"""
    parent.clear_screen()
    tk.Label(parent, text="🧹 Email Cleaner (Manual & Automatic Cleaning)", font=("Arial", 24, "bold"), bg="#1e1e2f", fg="white").pack(pady=10)
    create_button(parent, "📂 Manual Cleaning", lambda: manual_cleaning_page(parent)).pack(pady=10)
    create_button(parent, "⚙️ Automatic Cleaning", lambda: automatic_cleaning_page(parent)).pack(pady=10)
    create_button(parent, "🔙 Back", parent.create_main_menu).pack(pady=20)


# **Manual Cleaning**
def manual_cleaning_page(parent):
    """Page logic for Manual Email Cleaning"""
    parent.clear_screen()
    tk.Label(parent, text="📂 Manual Cleaning (Remove Bounced Emails)", font=("Arial", 24, "bold"), bg="#1e1e2f", fg="white").pack(pady=10)

    create_button(parent, "📁 Upload Main Email File", lambda: upload_main_file(parent)).pack(pady=10)
    parent.main_file_label = tk.Label(parent, text="No file uploaded", bg="#1e1e2f", fg="white")
    parent.main_file_label.pack()

    create_button(parent, "📁 Upload Bounced Email File", lambda: upload_bounce_file(parent)).pack(pady=10)
    parent.bounce_file_label = tk.Label(parent, text="No file uploaded", bg="#1e1e2f", fg="white")
    parent.bounce_file_label.pack()

    create_button(parent, "🧹 Process Cleaning", lambda: process_manual_cleaning(parent)).pack(pady=10)
    create_button(parent, "🔙 Back", parent.create_main_menu).pack(pady=20)


def upload_main_file(parent):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        global main_emails
        with open(file_path, 'r') as file:
            main_emails = file.read().splitlines()
        parent.main_file_label.config(text=f"Uploaded: {os.path.basename(file_path)}")


def upload_bounce_file(parent):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        global bounce_emails
        with open(file_path, 'r') as file:
            bounce_emails = file.read().splitlines()
        parent.bounce_file_label.config(text=f"Uploaded: {os.path.basename(file_path)}")


def process_manual_cleaning(parent):
    global main_emails, bounce_emails
    if main_emails and bounce_emails:
        cleaned_emails, removed_count = remove_bounced_emails_from_list(main_emails, bounce_emails)
        messagebox.showinfo("Cleaned", f"{removed_count} Bounced Emails Removed!")
        download_cleaned_file(cleaned_emails)
    else:
        messagebox.showwarning("Error", "Please upload both main email list and bounce list.")


def download_cleaned_file(cleaned_emails):
    folder_path = filedialog.askdirectory()
    if folder_path:
        file_path = os.path.join(folder_path, 'cleaned_emails.txt')
        with open(file_path, 'w') as file:
            file.write("\n".join(cleaned_emails))
        messagebox.showinfo("Success", f"File saved successfully to {file_path}")


def automatic_cleaning_page(parent):
    """Page logic for Automatic Email Cleaning"""
    parent.clear_screen()

    # Page Title
    tk.Label(parent, text="⚙️ Automatic Cleaning (SMTP & Spam Detection)", font=("Arial", 24, "bold"), bg="#1e1e2f", fg="white").pack(pady=10)

    # Upload Email File Button
    create_button(parent, "📁 Upload Email File", lambda: upload_emails_for_validation(parent)).pack(pady=10)

    # Status Output (Live Log)
    parent.status_output = scrolledtext.ScrolledText(parent, wrap="word", width=60, height=10, font=("Arial", 12))
    parent.status_output.pack(pady=10)

    # Awaiting Action / Progress Label
    parent.progress_label = tk.Label(parent, text="Awaiting action...", font=("Arial", 12, "bold"), bg="#1e1e2f", fg="#FFD700")
    parent.progress_label.pack(pady=5)

    # Start Validation Button
    create_button(parent, "🚀 Start Validation", lambda: validate_emails(parent)).pack(pady=10)

    # Download Button (Initially Disabled)
    parent.download_button = create_button(parent, "🔽 Download Valid Emails", lambda: download_cleaned_file(valid_emails), state="disabled")
    parent.download_button.pack(pady=10)

    # Back Button
    create_button(parent, "🔙 Back", parent.create_main_menu).pack(pady=20)


def create_button(parent, text, command, state="normal"):
    """Helper function to create consistent button styles."""
    button = tk.Button(parent, text=text, command=command, font=("Arial", 12, "bold"), bg="#D3D3D3", fg="#000000", 
                       width=25, height=2, bd=2, relief="raised", cursor="hand2", state=state)
    button.bind("<Enter>", lambda e: button.config(bg="#A9A9A9"))
    button.bind("<Leave>", lambda e: button.config(bg="#D3D3D3"))
    return button


def upload_emails_for_validation(parent):
    """Upload email list for validation"""
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        global validation_emails
        with open(file_path, 'r') as file:
            validation_emails = file.read().splitlines()
        parent.status_output.insert('end', f"✅ Uploaded {len(validation_emails)} emails from {os.path.basename(file_path)}\n")
        parent.status_output.see('end')


def validate_emails(parent):
    """Start email validation"""
    if not validation_emails:
        messagebox.showwarning("Warning", "Please upload an email file before starting validation.")
        return

    parent.progress_label.config(text="Processing Emails...")
    for i, email in enumerate(validation_emails):
        thread = threading.Thread(target=validate_single_email, args=(email, parent, i + 1, len(validation_emails)))
        thread.start()


def validate_single_email(email, parent, index, total):
    """Validate a single email"""
    global valid_emails
    try:
        parent.status_output.insert('end', f"🔍 Validating: {email} ({index} of {total})\n")
        parent.status_output.see('end')
        parent.progress_label.config(text=f"Processing email {index} of {total}...")

        status = check_smtp_email(email)
        email_statuses.put((email, status))
        
        if status == "Valid":
            valid_emails.append(email)
        
        parent.status_output.insert('end', f"✅ Email: {email} | Status: {status}\n")
        parent.status_output.see('end')

        # Enable the download button after the last email is processed
        if index == total:
            parent.download_button.config(state="normal")
            parent.progress_label.config(text="Email validation complete!")
    except Exception as e:
        parent.status_output.insert('end', f"❌ Error checking {email}: {e}\n")
        parent.status_output.see('end')


def check_smtp_email(email):
    """Check SMTP status"""
    domain = email.split('@')[-1]
    try:
        mx_record = socket.gethostbyname(domain)
        server = smtplib.SMTP(timeout=5)
        server.connect(mx_record, 587)
        server.starttls()
        server.mail('chosen@supportupgrade.site')
        code, _ = server.rcpt(email)
        server.quit()
        return "Valid" if code == 250 else "Invalid"
    except Exception:
        return "Invalid"


def download_cleaned_file(cleaned_emails):
    """Download the cleaned email list"""
    folder_path = filedialog.askdirectory()
    if folder_path:
        file_path = os.path.join(folder_path, 'valid_emails.txt')
        try:
            with open(file_path, 'w') as file:
                file.write("\n".join(cleaned_emails))
            messagebox.showinfo("Success", f"File saved successfully to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")