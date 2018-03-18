from Crawlers import Crawler
import csv

# pages = ["http://srinox.com/"]
pages = []

with open('href-exlist.txt', 'rb') as f:
    reader = csv.reader(f, dialect="excel-tab")
    for row in reader:
        pages.append(row[-1])

crawler = Crawler()
crawler.crawl(pages)



