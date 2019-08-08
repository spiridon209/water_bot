import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('URL')

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
    except AttributeError:
        return None
