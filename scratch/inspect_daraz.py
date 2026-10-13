import requests, re, sys, json
url = 'https://www.daraz.com.bd/catalog/tea/'
headers = {'User-Agent': 'Mozilla/5.0'}
try:
    r = requests.get(url, headers=headers, timeout=20)
    print('status', r.status_code)
    txt = r.text
    # Find product cards – inspect common pattern
    # Looking for <a ... data-qa="product-name"
    snippets = re.findall(r'<a[^>]*data-qa="product-name"[^>]*>.*?</a>', txt)
    print('found name snippets', len(snippets))
    for s in snippets[:5]:
        print(s[:200])
except Exception as e:
    print('error', e)
