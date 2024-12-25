📧 Email Cleaner & Extractor
Created by Chosenbrain

The Email Cleaner & Extractor is a multi-functional tool designed to help users clean, organize, and validate large email lists. It offers both manual and automatic cleaning methods. The app supports Windows and macOS, allowing users to download and run it as a standalone EXE (for Windows) or DMG (for macOS) application.
🚀 Features

    Manual Email Cleaning:
        Upload your email list and remove bounced/invalid emails.
        Manually review and clean emails with detailed feedback.
        Download the cleaned email list as a text file.

    Automatic Email Cleaning:
        Upload email files and validate them automatically.
        Real-time progress bar and live status updates for each email.
        Validate email addresses using SMTP and MX record checks.
        Download the cleaned list of valid emails after validation.

    Cross-Platform Compatibility:
        Windows (.exe) and macOS (.dmg) versions are available.
        No installation required. Simply download and run the app.

📥 Download & Installation
For Windows Users (EXE)

    Download the Windows EXE from the link below:
        Download Email Cleaner for Windows
    Double-click on the email_cleaner/dist/Email Cleaner & Extractor.exe file to launch the application.
    No installation is required — it works right out of the box.

For macOS Users (DMG)

    Download the macOS DMG from the link below:
        Download Email Cleaner for macOS
    Open the email_cleaner/dist/Email Cleaner & Extractor.dmg file.
    Drag and drop the app into your Applications folder.
    Open the app from Launchpad or Applications.

📘 How to Use
Manual Email Cleaning

    Click on Manual Cleaning.
    Upload your main email file and bounced email file.
    Click on Process Cleaning.
    Download the cleaned list of valid emails.

Automatic Email Cleaning

    Click on Automatic Cleaning.
    Upload your email file.
    Click Start Validation.
    View the live status of email validation.
    Download the final list of valid emails.

🖥️ How to Build Locally

If you'd like to customize or contribute to the app, you can build it locally.
🔧 Prerequisites

    Python 3.8+
    pip (Python package installer)
    Tkinter (comes pre-installed with Python)
    Wine (only for building Windows EXE on macOS)
    pyinstaller (to package the app)

📦 Build Instructions
Build EXE for Windows (on macOS or Windows)

If you want to create the Windows EXE file on macOS, follow these steps:

    Install Wine:

brew install --cask wine-stable

Install PyInstaller:

pip3 install pyinstaller

Build the EXE:

pyinstaller --onefile --windowed main.py

Check the dist folder for the main.exe file. Rename it to EmailCleaner.exe if necessary:

mv dist/main.exe dist/EmailCleaner.exe

Test the EXE with Wine:

    wine dist/EmailCleaner.exe

Build DMG for macOS

To create the DMG file on macOS, follow these steps:

    Install py2app:

pip3 install py2app

Create a setup.py file:

from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter', 'os', 'threading', 'socket', 'smtplib', 're', 'queue'],
    'iconfile': 'icon.icns',  # Optional: Replace with your icon path
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

Build the DMG:

python3 setup.py py2app

Check the dist folder for the EmailCleaner.app file.

Create a DMG:

    hdiutil create -volname "Email Cleaner" -srcfolder dist/EmailCleaner.app -ov -format UDZO EmailCleaner.dmg

📚 Requirements

To run the source code, you'll need the following Python libraries:

pip install -r requirements.txt

requirements.txt:

tkinter
smtplib
socket
threading
re
os
pyinstaller
py2app

🚀 Running From Source

To run the source code directly without downloading the app:

    Clone the repository:

git clone https://github.com/Chosenbrain/email_cleaner.git
cd email_cleaner

Install dependencies:

pip3 install -r requirements.txt

Run the app:

    python3 main.py

📂 File Structure

email_cleaner/
├── components/
│   └── ui_components.py
├── features/
│   ├── manual_cleaning.py
│   ├── automatic_cleaning.py
├── utils/
│   └── email_utils.py
├── dist/
│   └── EmailCleaner.exe  # Windows EXE
├── dist/
│   └── EmailCleaner.dmg  # macOS DMG
├── requirements.txt
├── README.md
├── main.py
└── setup.py

🔑 Key Commands
Command	Description
git clone <url>	Clone the GitHub repo
python3 main.py	Run the app from source
pyinstaller main.py	Create EXE (Windows)
python3 setup.py py2app	Create DMG (macOS)
📷 Screenshots
Home Screen	Manual Cleaning	Automatic Cleaning
	
	
📖 License

This project is licensed under the MIT License. See the LICENSE file for details.
💡 Contributing

We welcome contributions from the community. If you'd like to submit a feature request, report a bug, or contribute code, please fork the repository and create a pull request.
📧 Contact

For support, questions, or feature requests, please reach out to Chosenbrain or create an issue on the GitHub Issues page.
✨ Credits

This application was created by Chosenbrain. Special thanks to the open-source community for tools like Tkinter, PyInstaller, and Py2App.