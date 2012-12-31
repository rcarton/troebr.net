
from bs4 import BeautifulSoup
import requests
import time


WISHLIST_ID = '3HTH6XSK2NIZ5'
WISHLIST_URL = 'http://www.amazon.com/registry/wishlist/%s' % WISHLIST_ID

CACHE_EXPIRATION = 5 * 60
CACHE_ITEMS = None
CACHE_TIME = None

IMG_SIZE = 100

def get_items():
    """Builds a list of items."""
    global CACHE_ITEMS, CACHE_TIME
    
    if CACHE_ITEMS and time.time() < CACHE_TIME + CACHE_EXPIRATION:
        return CACHE_ITEMS
    
    r = requests.get(WISHLIST_URL)
    soup = BeautifulSoup(r.text, 'lxml')
    item_wrapper = soup.find_all(class_='itemWrapper')
    items = []
    for item in item_wrapper:
        d = {}
        d['title'] = item.find(name='span', class_='productTitle').a.text
        d['author'] = item.find(name='span', class_='tiny').text
        d['url'] = item.find(name='td', class_='productImage').a['href']
        img_url = item.find(name='td', class_='productImage').a.img['src']
        d['img_url'] = img_url.split('_', 2)[0] + '_SL' + str(IMG_SIZE) + '_.jpg'
        items.append(d)
    
    CACHE_TIME = time.time()
    CACHE_ITEMS = items
    return items
