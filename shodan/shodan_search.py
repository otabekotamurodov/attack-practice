import shodan

SHODAN_API_KEY = "mPlhaagev2zQ4sbtZiCKcAN8Buy5al94"

api = shodan.Shodan(SHODAN_API_KEY)

# Wrap the request in a try/ except block to catch errors
try:
    # Search Shodan
    results = api.search('country:uz')

    # Show the results
    print('Results found: {}'.format(results['total']))
    for result in results['matches']:
        print('IP: {}'.format(result['ip_str']))
        print(result['data'])
        print('')
except shodan.APIError as e:
    print('Error: {}'.format(e))
