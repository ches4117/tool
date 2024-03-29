from bs4 import BeautifulSoup
from pathlib import Path
import re
import os
import urllib
import requests

root = './'

def setDictionary(title):
    if title != '':
        title = '\\' + title
    path = root + title
    return path

def createDictionary(path):
    if not os.path.isdir(path):
        os.mkdir(path)

my_file = Path("./href_list.json")
if my_file.is_file():
    file = open('./href_list.json', 'r',
                encoding='utf-8', errors='ignore')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.8'}
    for url in file:
        if url == '\n':
            continue
        code = int(url.split('/')[4])
        res = requests.post(
            url.rstrip(), headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        if soup.find('h1', id='gj'):
            title = soup.find('h1', id='gj').text
            title = title.replace('\ufffd', '')
            title = title.replace('/', '_')
            title = title.replace(':', '_')
            title = title.replace('\\', '_')
            title = title.replace('?', '_')
            title = title.replace('*', '_')
            path = setDictionary(title.encode('GBK', 'ignore').decode('GBK'))
            createDictionary(path)

            img_list = soup.find_all(
                'a', href=re.compile("https://e-hentai.org/s/"))
            for link in img_list:
                img_url = link.get('href')
                res = requests.post(
                    img_url, headers=headers)
                soup = BeautifulSoup(res.text, "html.parser")

                file_name = soup.find(id='i2').div.next_sibling.getText()
                file_name = file_name.split(' :: ')[0]
                full_file_name = os.path.join(path, file_name)
                
                src = soup.find('img', id='img').attrs['src']
                urllib.request.urlretrieve(src, full_file_name)
        else:
            pass

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
