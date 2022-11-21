import requests
from bs4 import BeautifulSoup

url = 'https://quasarzone.com/bbs/qb_saleinfo?device=mobile&'
hdr = {'User-Agent':'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}
res = requests.get(url, headers=hdr)

soap = BeautifulSoup(res.text, 'lxml')
list = soap.find_all('span', class_='ellipsis-with-reply-cnt')
for i in range(len(list)):
    #print(list[i].text)
    if " " in list[i].text:
        print(list[i].text)

pass