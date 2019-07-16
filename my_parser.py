import requests
from bs4 import BeautifulSoup
from config import url

def get_utc(city, url = url):

    address = url + city
    resp = requests.get(address)

    html = resp.content
    soup = BeautifulSoup(html, 'lxml')
    try:
        utc = soup.find('span', {'class': 'utc-difference'}).contents[0]
        return utc
    except IndexError:
        get_utc(city)