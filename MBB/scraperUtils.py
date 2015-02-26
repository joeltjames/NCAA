import requests
from bs4 import BeautifulSoup

def getSoup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    return soup