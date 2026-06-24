# BruteCreds - Threaded Login Testing Tool

A lightweight, multithreaded Python tool for testing login endpoints using a password wordlist. Designed for **authorized penetration testing, CTF challenges, and cybersecurity learning environments**.

---

## Disclaimer

This tool is intended **strictly for educational purposes and authorized security testing only**.

Do NOT use this tool against:
- Systems you do not own
- Production environments
- Any service without explicit permission

Unauthorized use may violate laws and regulations.

---

## Features

- Multithreaded password testing for faster execution
- Smart response detection (JSON + text-based analysis)
- Session reuse for improved performance
- Early stopping when valid credentials are found
- Thread-safe execution using locks and events
- Simple CLI-based usage

---

## Requirements

- Python 3.8+
- requests library

Install dependency:

```bash
pip install requests
```

---

## Usage

```bash
python brutecreds.py <url> <username> <wordlist> <threads>
```

---

## Example

```bash
python brutecreds.py http://127.0.0.1:5000/login admin rockyou.txt 10
```

---

## Parameters

| Argument   | Description |
|------------|-------------|
| url      | Target login endpoint (POST request URL) |
| username | Username to test |
| wordlist | File containing password list |
| threads  | Number of concurrent threads |

---

## How It Works

1. Loads passwords from the provided wordlist
2. Sends concurrent POST requests using threads
3. Submits username and password combinations
4. Analyzes server response to detect success
5. Stops immediately when valid credentials are found

---

## Success Detection Logic

A login attempt is considered successful if:

- The response contains a JSON field like token, OR
- HTTP status is 200 AND the response does NOT contain keywords like "invalid"

---

## Limitations

- No CAPTCHA bypass
- No proxy support
- No rate-limit handling
- Assumes standard form fields (username, password)
- Detection logic may require adjustment for custom applications

---

## Possible Improvements

- Proxy rotation support
- CAPTCHA handling modules
- Logging and result export (JSON/CSV)
- Configurable form field mapping
- Async version for higher performance
- Integration with pentesting tools (e.g., Burp Suite)

---

## Example Wordlist Format

```
123456
password
admin123
letmein
qwerty
```

---

## Author

Created as part of a cybersecurity learning journey focusing on:
- Authentication testing
- Python automation
- Penetration testing fundamentals
