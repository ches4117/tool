from bs4 import BeautifulSoup
from pathlib import Path
import re
import urllib

my_file = Path("./href_list.json")
if my_file.is_file():
    print("!!!")
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
        file.write(href + '\n')
