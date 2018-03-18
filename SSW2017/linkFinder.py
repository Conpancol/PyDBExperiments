from bs4 import BeautifulSoup
from Exhibitors import Exhibitor
from pymongo import MongoClient

infile = open('href-exlist.html','r')

soup = BeautifulSoup(infile,'html.parser')
client = MongoClient('localhost', 27017)
db = client.conpancol
collection = db.ssc2017
result = collection.delete_many({})

output = open('href-exlist.txt', 'w')
csv_lines = []

for a in soup.find_all('a', href=True):
    link = a['href']
    if not link.startswith("#"):
        text = a.text
        pos = text.find("Stand")
        if pos > 0:
            info_text = text[:pos].encode('utf-8').strip()
            info = info_text.split('-')
            mx = len(info)
            name = ''.join(info[0:mx-1]).rstrip()
            country = info[mx-1].lstrip()
            url = link.encode('utf-8').strip()

            exhibitor = Exhibitor()
            exhibitor.setName(name)
            exhibitor.setCountry(country)
            exhibitor.setUrl(url)

            print name, country, link
            obj_id = collection.insert_one(exhibitor.__dict__)
            csv = name + "\t" + country + "\t" + url + "\n"
            csv_lines.append(str(csv))

output.writelines(csv_lines)
output.close()
