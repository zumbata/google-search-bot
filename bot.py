import urllib.parse as urlparse
import time
from bs4 import BeautifulSoup
import requests
import tldextract
import sys

domain = sys.argv[1]
keywords = [sys.argv[2], sys.argv[3], sys.argv[4]]
keywords_pos = {}
urlparams = {
    'num' : '100',
    'gl' : 'US',
    'ie' : 'utf-8',
    'oe' : 'utf-8',
    'safe' : 'off',
    'pws' : '0',
    'nfpr' : '1',
    'gws_rd' : 'ssl'
}
session = requests.Session()
last_req = time.time()
for keyword in keywords :
    url = 'https://www.google.com/search?'
    urlparams['q'] = keyword
    url = url + urlparse.urlencode(urlparams)
    headers = {
        'Host': 'www.google.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'utf-8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers'
    }
    res = session.get(url, headers=headers)
    soup = BeautifulSoup(res.text, features='html.parser')
    children_list = soup.find_all(class_="g")
    indexx = 1
    f = open("demo_{}".format(keyword), "w")
    f.write(res.text)
    f.close()
    for child in children_list : 
        d = child.find(class_="iUh30").getText()
        index = d.find(u'›')
        if index != -1 :
            d = d[:index]
        ext = tldextract.extract(str(d))
        d = '{uri.domain}.{uri.suffix}'.format(uri=ext)
        if domain.find(d) != -1 or d.find(domain) != -1:
            print("The domain {} was found at position {} when searhing the word {} \n".format(domain, indexx, keyword))
            break
        indexx += 1
    now = time.time()
    delay = last_req + 0.8 - now
    last_req = now
    if delay >= 0:
        time.sleep(delay)