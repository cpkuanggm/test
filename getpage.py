import requests
import bs4

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

page = "https://manhua.fzdm.com/1/brc30/index_8.html"
res = requests.get(page, stream=True, verify=False, headers=headers)
res.raise_for_status()
with open('123.html', 'w+', encoding='UTF-8') as f:
    f.write(res.text)
soup = bs4.BeautifulSoup(res.text, 'lxml')
