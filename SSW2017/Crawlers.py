import urllib2
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re
from urlparse import urljoin
from Pages import Page

ignorewords = set(['the','of','to','and','a','in','is','it'])

class Crawler:
    """Basic crawler"""
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.conpancol
        self.collection = self.db.wordsSsc2017
        self.collection.delete_many({})

    def crawl(self, pages, depth=2):

        for i in range(depth):

            newpages = set()

            for page in pages:
                print page
                try:
                    c = urllib2.urlopen(page)
                except:
                    print "Could not open %s" % page
                    continue
                soup = BeautifulSoup(c.read(), 'html.parser')

                # ... set content of current page
                self.addtoindex(page, soup)

                # ... add new linked pages
                links = soup('a')

                for link in links:
                    if 'href' in dict(link.attrs):
                        url = urljoin(page, link['href'])
                        if url.find("'") != -1:
                            continue
                        url = url.split('#')[0]
                        if url[0:4] == 'http' and not self.isindexed(url):
                            newpages.add(url)
                        linktext = self.gettextonly(link)

            pages = newpages


    def addtoindex(self, page, soup):

        if self.isindexed(page):
            return

        text = self.gettextonly(soup)
        words = self.separatewords(text.encode('utf-8').strip())

        pg0 = Page()
        pg0.setUrl(page)
        pg0.setContent(words)

        # ... extract domain from url
        pos = page.find('//')+2
        domain = page[pos:].split('/')[0]
        pg0.setDomain(domain)
        # ... write to DB
        self.dbcommit(pg0)
        #print pg0

    def gettextonly(self,soup):
        v = soup.string
        if v==None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()

    def separatewords(self,text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s!= '']

    def isindexed(self,url):
        return False

    def dbcommit(self,page):
        obj_id = self.collection.insert_one(page.__dict__)
        print obj_id

