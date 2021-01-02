# from config import API_KEY
import requests
import json

API_KEY = 'mou49qpl-b265-asco:826d-ojy6nbmxzay2'
URL_BASE = 'https://api.printful.com'

def get_product_types():
	product_types = {}
	response = requests.get(URL_BASE + '/products')
	for product in response.json()['result']:
		if product["type"] in product_types:
			product_types[product["type"]] += 1
		else:
			product_types[product["type"]] = 1
	return(product_types)

def print_product_info(product_type):
	product_info = []
	response = requests.get(URL_BASE + '/products')
	for product in response.json()['result']:	
		if product["type"] == product_type:
			product_info.append(product)
	return(product_info)

print(f'Product Types: {get_product_types()}')

for item in print_product_info("MUG"):
	print(f'\nProduct Info: {item}')