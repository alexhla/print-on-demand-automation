import os
import json
import requests
import argparse

# local imports
import config

HEADER = {
	'Authorization': 'Bearer {}'.format(config.SQUARESPACE_API_TOKEN),
	'User-Agent': '{}'.format(config.SQUARESPACE_USER_AGENT),
	}




URL_STORE_PAGES = 'https://api.squarespace.com/1.0/commerce/store_pages'
URL_PRODUCTS = 'https://api.squarespace.com/1.0/commerce/products'




# Instantiate the argument parser object
ap = argparse.ArgumentParser()

ap.add_argument('-sbox', '--sandbox', action='store_true',
	help='Sandbox is for running prototype code and tests')

ap.add_argument('-showproducts', '--show_products', action='store_true',
	help='Display all prodcuts in the terminal')

args = vars(ap.parse_args())
print(f'----- Arguments -----\n{args}\n')






if args['sandbox']:
	print('------- Sandbox --------')

if args['show_products']:
	endpoint = URL_PRODUCTS
	print(f'\nGET {endpoint}')
	response = requests.get(endpoint, headers=HEADER)
	response = response.json()

	print(f'response type ----- {type(response)}')
	print(f'response length --- {len(response)}')

	for key, value in response.items():
		# print(f'type of key is {type(key)}\ntype of value is {type(value)}')
		print(f'response key --- {key}')

		if key == 'products':
			for count, item in enumerate(value):
				print(f'count is {count}')
				print(type(item))
				for k, v in item.items():
					print(f'{k}-----{v}\n\n')