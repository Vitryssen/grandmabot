from urllib.request import urlopen, Request
import argparse
import json
from bs4 import BeautifulSoup
import itertools
import random

REQUEST_HEADER = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

def get_soup(url, header):
    response = urlopen(Request(url, headers=header))
    return BeautifulSoup(response, 'html.parser')

def get_query_url(query, pages, ext):
    query = query.replace(" ","+")
    print("searching for:",query)
    return "https://www.google.co.in/search?q={}&source=lnms&tbm=isch&tbs=itp:{}&ijn={}".format(query, ext, pages)

def extract_images_from_soup(soup):
    image_elements = soup.find_all("div", {"class": "rg_meta"})
    metadata_dicts = (json.loads(e.text) for e in image_elements)
    link_type_records = ((d["ou"], d["ity"]) for d in metadata_dicts)
    randomValue = random.randint(0, 99)
    index = 0
    for url, image_type in link_type_records:
        if(index == randomValue):
            values = [url, image_type]
            return values[0]
        else:
            index = index + 1

def extract_images(query, page, ext):
    url = get_query_url(query, page, ext)
    soup = get_soup(url, REQUEST_HEADER)
    link_type_records = extract_images_from_soup(soup)
    if link_type_records != None:
        return link_type_records
    else:
        return False