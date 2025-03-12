import shodan
import json
from dotenv import load_dotenv, dotenv_values

config = dotenv_values(".env")

api = shodan.Shodan(config["API_KEY"])
print(api.info())

# try:
#     query = "country:uz"
#     results = api.search(query)
#     print(results)
#
#
#
# except shodan.APIError as e:
#     print(f"Shodan API xatosi: {e}")
