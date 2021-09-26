from bs4 import BeautifulSoup
import requests
import json
import re

def jakmall_product_detail_scrapper(endpoint):
	results = {'product': [], 'message': 'OK'}
	frame = requests.get('https://www.jakmall.com/' + endpoint).text
	soup = BeautifulSoup(frame, 'html.parser')

	scripts = soup.find('script', text=re.compile("var spdt"))
	script_cleaned = str(scripts)[str(scripts).find('var spdt = '):str(scripts).find('var wlsc = ')]
	script_cleaned = script_cleaned.replace('var spdt = ', '').replace('};','}')
	try:
		products = json.loads(script_cleaned)
		results['products'] = products
		results['products']['name'] = soup.find('div', 'crumb__link crumb__link--last').text
	except Exception as e:
		results['message'] = e
	return results


def jakmall_product_list_scrapper(endpoint):
	results = {'product': [], 'message': 'OK'}
	frame = requests.get('https://www.jakmall.com/' + endpoint).text
	soup = BeautifulSoup(frame, 'html.parser')

	scripts = soup.find('script', text=re.compile("var result"))
	script_cleaned = str(scripts)[str(scripts).find('var result = '):str(scripts).find('var config = ')]
	script_cleaned = script_cleaned.replace('var result = ', '').replace('};','}')
	try:
		products = json.loads(script_cleaned)
		results['products'] = products['products']
	except Exception as e:
		results['message'] = e
	return results