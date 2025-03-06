import shodan
import json
from dotenv import load_dotenv, dotenv_values

config = dotenv_values(".env")

api = shodan.Shodan(config["API_KEY"])

try:
    query = "country:uz"
    results = api.search(query)

    structured_results = []

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

    # JSON faylga saqlash
    with open("shodan_results.json", "w", encoding="utf-8") as json_file:
        json.dump(structured_results, json_file, indent=4, ensure_ascii=False)

    # TXT faylga faqat IP-larni saqlash
    with open("shodan_results.txt", "w", encoding="utf-8") as txt_file:
        for entry in structured_results:
            txt_file.write(f"IP: {entry['IP']}\n")

    print("")

except shodan.APIError as e:
    print(f"Shodan API xatosi: {e}")
