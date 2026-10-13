import requests, sys
url = 'https://www.daraz.com.bd/catalog/tea/'
headers = {'User-Agent': 'Mozilla/5.0'}
try:
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    with open('C:/Users/Programmer Arjuna/Downloads/Liton Tea Stall/scratch/daraz_page.html', 'w', encoding='utf-8') as f:
        f.write(r.text)
    print('saved', len(r.text), 'bytes')
except Exception as e:
    print('error', e)
