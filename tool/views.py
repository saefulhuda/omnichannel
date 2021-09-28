from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from bs4 import BeautifulSoup
import requests
import json
import threading
import time
from tool.models import JakmallScrapper, JakmallImagesScrapper
from django.contrib.auth.decorators import login_required

# Create your views here.

def _jakmall_login():
	results = {'message':'OK', 'session':''}
	""" Define login attribute """
	login_URL = 'https://www.jakmall.com/login'
	email = "gada54ra@gmail.com"
	password = "lostsaga01"
	payload = {'email': email, 'password': password}

	""" Start session """
	session = requests.Session()
	session.headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
		'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36')}
	try:
		response = session.get(login_URL)
	except Exception as e:
		results['message'] += str(e)
		return results
	soup = BeautifulSoup(response.text, "html.parser")

	action_URL = soup.find('form').get('action') + '121asa'
	if action_URL is not None:
		action_URL = action_URL.strip()
	token = soup.find('input', attrs={'name': '_token'})
	if token is not None:
		token = token.get('value').strip()
	if action_URL is not None and token is not None:
		print(f"Attempting log in jakmall.com as {email} to {action_URL} ...")
		payload.update({'_token': token})
		try:
			response = session.post(action_URL, data=payload)
			results['session'] = session
		except Exception as e:
			results['message'] += str(e)
			return results
	else:
		results['message'] = 'Token or action_URL not found'
	return results


def _jakmall_sync(session, endpoint, i):
	results = {'message':'OK', 'results':[], 'paging':0}
	inventory = session.get(endpoint)
	try:
		inventory = json.loads(inventory.text)
	except Exception as e:
		results['message'] = str(e)
		return results

	if len(inventory['data']) < 1:
		results['message'] = 'Data not found'
		return results

	for product in inventory['data']:
		product_existing = JakmallScrapper.objects.filter(pid=product['code'])
		saving = {
			'name':product['name'],
			'sku':product['sku'],
			'final_price':product['final_price'],
			'stock':product['stock'],
			'weight':int(product['weight_information'].replace('.','').replace('gr','').replace('kg','000'))}
		if product_existing.exists():
			save_product = product_existing.update(**saving)
		else:
			saving['pid'] = product['code']
			save_product = JakmallScrapper.objects.create(**saving)
			JakmallImagesScrapper.objects.create(
				jakmall_scrap=save_product,
				url=product['image'],
				image_type=2
				).save()
			save_product.save()
	results['paging'] = len(inventory['paging']['links']['first'])
	return results



@login_required
def cron_jakmall_sync(request):
	response = {'code':1, 'message':'', 'results':[]}
	login = _jakmall_login()
	if login['message'] == 'OK':
		session = login['session']
	else:
		response['code'] = 99
		response['message'] = login['message']
		return JsonResponse(response, safe=False)

	headers = {
	'accept': 'application/json, text/plain, */*',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
	'referer': 'https://www.jakmall.com/affiliate/inventory?tab=inventory-list',
	'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-platform': '"Windows"',
	'sec-fetch-dest': 'empty',
	'sec-fetch-mode': 'cors',
	'sec-fetch-site': 'same-origin',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
	'x-csrf-token': 'D7PL3sKR52xdiwzZ4w83zjW36XscbqI59hYBULs6',
	'x-requested-with': 'XMLHttpRequest'
	}
	page_counter = 1
	session.headers.update(headers)
	start_process = time.perf_counter()
	sync = _jakmall_sync(session, f"https://www.jakmall.com/affiliate/inventory?tab=inventory-list&page={page_counter}&json",page_counter)
	page_counter = sync['paging'] - page_counter
	threads = []
	while page_counter > 0:
		t = threading.Thread(target=_jakmall_sync, args=(session, f"https://www.jakmall.com/affiliate/inventory?tab=inventory-list&page={page_counter}&json",page_counter,))
		t.start()
		threads.append(t)
		page_counter -= 1

	for t in threads:
		t.join()

	end_process = time.perf_counter()
	response['message'] = f"Sync OK -- Execution Time: {str(end_process - start_process)[:4]} sec."
	return JsonResponse(response, safe=False)