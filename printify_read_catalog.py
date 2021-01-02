import requests
import json
import os

# local imports
import config

HEADER = {'Authorization': 'Bearer {}'.format(config.PRINTIFY_API_TOKEN)}
URL_BASE = 'https://api.printify.com/v1/catalog/'
URL_BLUEPRINTS = 'blueprints.json'
URL_PRINT_PROVIDERS = 'print_providers.json'


#### GET list of printify providers
# endpoint = os.path.join(URL_BASE, URL_PRINT_PROVIDERS)
# response = requests.get(endpoint, headers=HEADER)
# for provider in response.json():
# 	if provider['location']['country'] == 'US':
# 		print(provider)



#### GET list of printify blueprints
endpoint = os.path.join(URL_BASE, URL_BLUEPRINTS)
print(f'GET {endpoint}')
response = requests.get(endpoint, headers=HEADER)
print(f'response is {response}')

for blueprint in response.json():
	if 'Poster' in blueprint['title']:
		print(f'\n{blueprint}\n')

