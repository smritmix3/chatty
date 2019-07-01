from bs4 import BeautifulSoup
import urllib.request
import csv


url_page ="https://www.easystepin.com/"
page = urllib.request.urlopen(url_page)
soup = BeautifulSoup(page, 'html.parser')
message = soup.find('div', attrs={'class': 'easy_step_left'})
results = message.find_all('p')
print('Number of results', len(results))
mess = []

for p in results:
    mess.append(p.text)

mess1 = ''.join(mess[0:len(results)-3])
print(str(mess1))
