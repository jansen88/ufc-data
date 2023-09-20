import requests
from bs4 import BeautifulSoup
import numpy as np
import time

def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup

def sleep_randomly():
    """Sleep for some random time between requests"""
    sleep_time = np.random.uniform(2,4)
    time.sleep(sleep_time)
