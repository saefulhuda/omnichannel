from bs4 import BeautifulSoup
import requests

LOGIN_URL = "https://www.jakmall.com/login"

def get_authenticity_token(html):
    soup = BeautifulSoup(html, "html.parser")
    token = soup.find('input', attrs={'name': '_token'})
    if not token:
        print('could not find `authenticity_token` on login form')
    return token.get('value').strip()


def get_action(html):
    soup = BeautifulSoup(html, "html.parser")
    n = soup.find('form')
    if not n:
        print('Form not found')
    return n.get('action').strip()    


email = "gada54ra@gmail.com"  # login email
password = "lostsaga01"  # login password

payload = {
    'email': email,
    'password': password,
}

session = requests.Session()
session.headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36')}
response = session.get(LOGIN_URL)

token = get_authenticity_token(response.text)
ACTION_URL = get_action(response.text)
payload.update({
    '_token': token
})
print('Payload:', payload)

print(f"attempting to log in as {email}")
print(ACTION_URL, payload)
p = session.post(ACTION_URL, data=payload)  # perform login
account = session.get('https://www.jakmall.com/affiliate/inventory?tab=inventory-list')
soup = BeautifulSoup(p.text, 'html.parser')