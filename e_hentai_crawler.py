from bs4 import BeautifulSoup
from pathlib import Path
import re
import urllib
import requests

my_file = Path("./href_list.json")
if my_file.is_file():
    file = open('./href_list.json', 'r',
                encoding='utf-8', errors='ignore')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.8'}
    for url in file:
        code = int(url.split('/')[4])
        res = requests.post(
            url.rstrip(), headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        img_list = soup.find_all(
            'a', href=re.compile("https://e-hentai.org/s/"))
        for link in img_list:
            img_url = link.get('href')
            print(img_url)
        break
    file.close()
else:
    file = open('./bookmarks_2019_7_28.html', 'r',
                encoding='utf-8', errors='ignore')
    href_list = []
    soup = BeautifulSoup(file, "html.parser")
    total = 0
    for entry in soup.find_all('a'):
        try:
            if re.search('exhentai.org/g', entry['href']):
                new_href = re.sub('exhentai', 'e-hentai', entry['href'])
                href_list.append(new_href)
        except:
            continue
    file.close()

    file = open('./href_list.json', 'w', encoding='utf-8', errors='ignore')
    for href in href_list:
        file.write(href + '\r\n')
