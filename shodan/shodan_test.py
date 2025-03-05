import shodan

SHODAN_API_KEY = "mPlhaagev2zQ4sbtZiCKcAN8Buy5al94"
api = shodan.Shodan(SHODAN_API_KEY)

try:
    info = api.info()
    print("API Plan:", info['plan'])
    print("Query Credits:", info['query_credits'])
except shodan.APIError as e:
    print('Error: {}'.format(e))