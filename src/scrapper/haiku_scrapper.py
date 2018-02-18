from bs4 import BeautifulSoup
import urllib.request
import time
import json

URL = "http://www.tempslibres.org/tl/tlphp/{}"


links = list()
with urllib.request.urlopen(URL.format("dbmots.php?lg=e")) as response:
    html = response.read()
    soup = BeautifulSoup(html)
    for link in soup.findAll('a'):
        href = link.get('href')
        if href is not None and 'dbhk' in href and 'mot=' in href:
            links.append(href)

haikus = list()
processed = list()
for link in links:
    try:
        with urllib.request.urlopen(URL.format(link)) as response:
            html = response.read()
            soup = BeautifulSoup(html)
            print(link)
            for haiku in soup.findAll("p", {"class": "haiku"}):
                raw = haiku.getText()
                haikus.append(raw)
    except Exception:
        print('Bar url {}'.format(URL.format(link)))
        pass
    json.dump(haikus, fp=open('./haikus.json', 'w'))
    processed.append(link)
    json.dump(processed, fp=open('./processed.json', 'w'))
    print('Got {} haikus, sleeping for 1 seconds'.format(len(haikus)))
    time.sleep(0.5)

json.dump(haikus, fp=open('./haikus.json', 'w'))

