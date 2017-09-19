import unicodecsv
import scrapy
import re
from scrapy.http.request import Request
from scrapy.selector import Selector
from urllib2 import unquote

externalCounter = 0

class WenxuecitySpider(scrapy.Spider):
    name = "WenxuecityCSV"

    def start_requests(self):

        # Create CSV Writer for csv document

        # Comment out lines 18 and 19 if you want to append to file
        ffile = open('./csv/wenxuecity.csv', "w+")
        ffile.close()

        # Most Commented
        url = 'http://www.wenxuecity.com/news/'
        request = Request(url=url, callback=self.parse_most_commented)
        request.meta['type'] = 'Most Commented'
        yield request

    def parse_most_commented(self, response):
        sel = Selector(response)

        links = sel.xpath('/html/body/div[4]/div[4]/div/div[2]/a/@href')
        string_links = links.extract()

        for link in string_links:
            request = Request("http://www.wenxuecity.com" + link, callback=self.parse_link)
            request.meta['type'] = response.meta['type']
            request.meta['link'] = "http://www.wenxuecity.com" + link
            yield request

    def parse_link(self, response):
        global externalCounter
        sel = Selector(response)

        # Title
        title = sel.xpath('/html/body/div[3]/div[1]/h3/text()')
        if not title:
            title = sel.xpath('//*[@id="preview"]/div[1]/h1')
        title = title.extract()
        title = title[0].encode('utf-8')

        # Date
        date = sel.xpath('//*[@id="postmeta"]/time/@datetime')
        date = date.extract()
        date = date[0].encode('utf-8')

        # Name of News Site
        news_site = "Wenxuecity"

        # Section Name
        section = response.meta['type']

        # Link
        link = response.meta['link']

        with open('./csv/wenxuecity.csv', "ab") as ffile:
            writer = unicodecsv.writer(ffile, delimiter=',', quotechar='"', quoting=unicodecsv.QUOTE_ALL)
            writer.writerow(['WXC'+str(externalCounter), title, news_site, link, section, date])

        externalCounter += 1
