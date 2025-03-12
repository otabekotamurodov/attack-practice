import requests


def check_admin_pages():
    input_file = "results/shodan_results.txt"
    output_file = "results/open_admin_pages.txt"

    with open(input_file, "r") as file:
        ip_addresses = [line.strip() for line in file.readlines()]

    valid_admin_pages = []

    for ip in ip_addresses:
        for protocol in ["http", "https"]:
            url = f"{protocol}://{ip}/admin/"
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"Admin page found: {url}")
                    valid_admin_pages.append(url)
            except requests.RequestException as e:
                print(f"Error while checking {url}: {e}")

    with open(output_file, "w") as file:
        for page in valid_admin_pages:
            file.write(f"{page}\n")

    print(f"Open admin pages saved to {output_file}")


if __name__ == "__main__":
    check_admin_pages()
