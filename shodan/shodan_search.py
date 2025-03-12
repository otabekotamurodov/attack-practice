import shodan
import json
from dotenv import dotenv_values
import time

config = dotenv_values(".env")

api = shodan.Shodan(config["API_KEY"])
print(api.info())

query = "country:uz"
max_pages = 10
natija_soni = 0
structured_results = []

try:
    for page in range(1, max_pages + 1):
        try:
            results = api.search(query, page=page)

            if not results['matches']:
                break

            for result in results['matches']:
                structured_results.append({
                    "IP": result.get("ip_str", "N/A"),
                    "Port": result.get("port", "N/A"),
                    "Organization": result.get("org", "N/A"),
                    "ISP": result.get("isp", "N/A"),
                    "Hostnames": result.get("hostnames", []),
                    "Location": result.get("location", {}),
                    "Data": result.get("data", "N/A")
                })
                natija_soni += 1

            print(f"Sahifa {page}: {len(results['matches'])} ta natija olindi, jami: {natija_soni}")
            time.sleep(1)
        except shodan.APIError as e:
            print(f"API xatosi sahifa {page}: {e}")
            break

    with open("results/shodan_results.json", "w", encoding="utf-8") as json_file:
        json.dump(structured_results, json_file, indent=4, ensure_ascii=False)

    with open("results/shodan_results.txt", "w", encoding="utf-8") as txt_file:
        for entry in structured_results:
            txt_file.write(f"{entry['IP']}\n")

    print(f"Natijalar saqlandi! Jami IP: {natija_soni}")

except shodan.APIError as e:
    print(f"Shodan API xatosi: {e}")
