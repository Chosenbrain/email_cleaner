import smtplib
import socket
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os


def remove_duplicates(emails):
    """Remove duplicate email addresses."""
    return list(set(emails))

def remove_suspicious_emails(emails):
    """Remove invalid or suspicious email addresses."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    clean_emails = [email for email in emails if re.match(pattern, email)]
    suspicious_emails = [email for email in emails if not re.match(pattern, email)]
    return clean_emails, suspicious_emails

def remove_bounced_emails_from_list(main_emails, bounced_emails):
    """Remove bounced emails from the main email list."""
    main_emails = list(set(main_emails))  
    bounced_emails = list(set(bounced_emails))  
    cleaned_emails = [email for email in main_emails if email not in bounced_emails]
    return cleaned_emails, len(main_emails) - len(cleaned_emails)

def smtp_email_verification(email):
    """Check if an email exists using SMTP verification."""
    try:
        domain = email.split('@')[-1]
        mx_record = socket.gethostbyname(domain)
        server = smtplib.SMTP(mx_record, 25, timeout=10)
        server.helo()
        server.mail('check@example.com')  
        code, message = server.rcpt(email)  
        server.quit()
        if code == 250:  
            return True  
        else:
            return False  
    except Exception as e:
        print(f"Error checking {email}: {e}")
        return False

def detect_spam_trap(email):
    """Check if the email is a known spam trap."""
    spam_trap_list = [
        "spamtrap@example.com",
        "abuse@example.com",
        "complaints@example.com",
        "postmaster@example.com",
        "noreply@example.com",
        "donotreply@example.com"
    ]
    if email.lower() in spam_trap_list:
        return True
    return False

def validate_email(email):
    """Full validation to check if email exists and is not a spam trap."""
    if detect_spam_trap(email):
        return "Spam Trap"
    
    if smtp_email_verification(email):
        return "Valid"
    else:
        return "Invalid"

# === Manual Cleaning Functions ===
main_emails = []
bounce_emails = []

def manual_cleaning_page(parent):
    """Page logic for Manual Email Cleaning"""
    parent.clear_screen()

    # Title
    tk.Label(parent, text="📂 Manual Cleaning (Remove Bounced Emails)", font=("Arial", 24, "bold"), bg="#1e1e2f", fg="white").pack(pady=10)

    # File upload status labels
    parent.main_file_status = tk.Label(parent, text="Main File: Not uploaded", font=("Arial", 12), bg="#1e1e2f", fg="white")
    parent.main_file_status.pack(pady=5)

    parent.bounce_file_status = tk.Label(parent, text="Bounced File: Not uploaded", font=("Arial", 12), bg="#1e1e2f", fg="white")
    parent.bounce_file_status.pack(pady=5)

    # Upload Main Email List
    tk.Button(parent, text="📁 Upload Main Email File", 
              command=lambda: upload_main_file(parent), 
              font=("Arial", 14, "bold"), bg="#4caf50", fg="white").pack(pady=10)

    # Upload Bounced Email List
    tk.Button(parent, text="📁 Upload Bounced Email File", 
              command=lambda: upload_bounce_file(parent), 
              font=("Arial", 14, "bold"), bg="#4caf50", fg="white").pack(pady=10)

    # Process Button (Initially Disabled)
    parent.process_button = tk.Button(parent, text="🧹 Remove Bounced Emails", 
                                      command=lambda: process_manual_cleaning(parent), 
                                      font=("Arial", 14, "bold"), bg="#FBBF24", fg="#1e1e2f", state="disabled")
    parent.process_button.pack(pady=10)

    # Back Button
    tk.Button(parent, text="🔙 Back", command=parent.create_main_menu, font=("Arial", 14, "bold")).pack(pady=20)

    global main_emails, bounce_emails
    main_emails, bounce_emails = [], []

def upload_main_file(parent):
    """Upload main email list"""
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            global main_emails
            main_emails = file.read().splitlines()
        parent.main_file_status.config(text=f"Main File: {file_path} ({len(main_emails)} emails) ✅")
        check_if_both_files_uploaded(parent)

def upload_bounce_file(parent):
    """Upload bounced email list"""
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            global bounce_emails
            bounce_emails = file.read().splitlines()
        parent.bounce_file_status.config(text=f"Bounced File: {file_path} ({len(bounce_emails)} emails) ✅")
        check_if_both_files_uploaded(parent)

def check_if_both_files_uploaded(parent):
    """Enable the Process button if both files are uploaded"""
    if main_emails and bounce_emails:
        parent.process_button.config(state="normal")

def process_manual_cleaning(parent):
    """Process cleaning for manual method"""
    if main_emails and bounce_emails:
        cleaned_emails, removed_count = remove_bounced_emails_from_list(main_emails, bounce_emails)
        messagebox.showinfo("Cleaned", f"{removed_count} Bounced Emails Removed!")
        download_cleaned_file(cleaned_emails)
    else:
        messagebox.showwarning("Error", "Please upload both main email list and bounce list.")

def download_cleaned_file(cleaned_emails):
    """Download the cleaned email list"""
    folder_path = filedialog.askdirectory()
    if folder_path:
        file_path = os.path.join(folder_path, 'cleaned_emails.txt')
        with open(file_path, 'w') as file:
            file.write("\n".join(cleaned_emails))
        messagebox.showinfo("Success", f"File saved successfully to {file_path}")

# === Automatic Cleaning Functions ===
def automatic_cleaning_page(parent):
    """Page logic for Automatic Email Cleaning"""
    parent.clear_screen()

    # Title
    tk.Label(parent, text="⚙️ Automatic Cleaning (SMTP & Spam Detection)", font=("Arial", 24, "bold"), bg="#1e1e2f", fg="white").pack(pady=10)

    # Upload Email List Button
    tk.Button(parent, text="📁 Upload Email File", command=lambda: upload_emails_for_validation(parent), font=("Arial", 14, "bold")).pack(pady=10)

    parent.file_status = tk.Label(parent, text="File Status: No file uploaded", font=("Arial", 12), bg="#1e1e2f", fg="white")
    parent.file_status.pack(pady=5)

    # Paste Email List
    email_input = scrolledtext.ScrolledText(parent, wrap="word", width=60, height=10, font=("Arial", 12))
    email_input.pack(pady=10)

    # Progress Bar
    parent.progress_bar = ttk.Progressbar(parent, orient="horizontal", length=300, mode="determinate")
    parent.progress_bar.pack(pady=10)

    # Validate Button
    tk.Button(parent, text="🚀 Start Validation", 
              command=lambda: validate_emails(parent, email_input), 
              font=("Arial", 14, "bold")).pack(pady=10)

    # Back Button
    tk.Button(parent, text="🔙 Back", command=parent.create_main_menu, font=("Arial", 14, "bold")).pack(pady=20)

    global validation_emails
    validation_emails = []

def upload_emails_for_validation(parent):
    """Upload file for validation"""
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            global validation_emails
            validation_emails = file.read().splitlines()
        parent.file_status.config(text=f"File uploaded: {len(validation_emails)} emails ✅")

def validate_emails(parent, email_input):
    """Validate emails in the file"""
    emails = email_input.get("1.0", "end").splitlines()
    if validation_emails:
        emails += validation_emails

    total_emails = len(emails)
    parent.progress_bar['maximum'] = total_emails

    valid_emails = []

    for i, email in enumerate(emails):
        status = validate_email(email)
        if status == "Valid":
            valid_emails.append(email)
        
        parent.progress_bar['value'] = i + 1
        parent.update_idletasks()

    save_cleaned_emails(valid_emails)

def save_cleaned_emails(emails):
    """Save the cleaned emails to a file"""
    folder_path = filedialog.askdirectory()
    if folder_path:
        file_path = os.path.join(folder_path, 'cleaned_emails.txt')
        with open(file_path, 'w') as file:
            file.write("\n".join(emails))
        messagebox.showinfo("Success", f"File saved successfully to {file_path}")