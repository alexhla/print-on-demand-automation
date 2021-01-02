import requests
import json
import os

# local imports
import config

HEADER = {'Authorization': 'Bearer {}'.format(config.PRINTIFY_API_TOKEN)}
URL_BASE = 'https://api.printify.com'
URL_BLUEPRINTS = '/v1/catalog/blueprints.json'
URL_PRINT_PROVIDERS = '/v1/catalog/print_providers.json'

### GET list of printify blueprints
# endpoint = os.path.join(URL_BASE, URL_BLUEPRINTS)
# response = requests.get(endpoint, headers=HEADER)
# print(f'GET {endpoint}')
# print(f'response is {response}')

### Filter Out Poster and Canvas Blueprints
# for blueprint in response.json():
# 	if any(x in blueprint['title'] for x in ['Canvas', 'Poster']):
# 		print(f'\n{blueprint}\n')

### ID: 97 - Poster
### ID: 443 - Posters (EU)
### ID: 492 - Premium Framed Vertical Poster
### ID: 493 - Premium Framed Horizontal Poster
### ID: 50 - Canvas Gallery Wrap
### ID: 190 - Vertical Framed Premium Gallery Wrap Canvas
### ID: 193 - Horizontal Framed Premium Gallery Wrap Canvas
### ID: 196 - Square Framed Premium Gallery Wrap Canvas
### ID: 534 - Wood Canvas
poster_blueprint_ids = [97, 443, 492, 493]
canvas_blueprint_ids = [50, 190, 193, 196, 534]

### GET list of poster printify providers
for pid in poster_blueprint_ids:
	endpoint = os.path.join(URL_BASE, 'v1/catalog/blueprints/', str(pid), 'print_providers.json')
	response = requests.get(endpoint, headers=HEADER)
	print(f'\nGET {endpoint}')
	for provider in response.json():
		print(provider)

### GET list of poster printify providers
# for pid in poster_blueprint_ids:
# 	endpoint = os.path.join(URL_BASE, 'v1/catalog/blueprints/', str(pid), 'print_providers.json')
# 	response = requests.get(endpoint, headers=HEADER)
# 	print(f'GET {endpoint}')
# 	print(f'response is {response.content}')