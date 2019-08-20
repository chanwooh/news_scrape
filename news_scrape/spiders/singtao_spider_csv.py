import unicodecsv
import scrapy
import re
from scrapy.http.request import Request
from scrapy.selector import Selector

externalCounter = 0

class SingtaoSpider(scrapy.Spider):
    name = "SingtaoCSVDeprecated"

    def start_requests(self):

        # Create CSV Writer for csv document

        # Comment lines 17 and 18 out if you want to append to file
        ffile = open('./csv/singtao.csv', "w+")
        ffile.close()

        # Most Read
        url = 'https://www.singtaousa.com/la/'
        request = Request(url=url, callback=self.parse_most_read)
        request.meta['type'] = 'Most Read'
        yield request

        # SoCal Section
        url = 'https://www.singtaousa.com/la/453-%E5%8D%97%E5%8A%A0%E6%96%B0%E8%81%9E/'
        request = Request(url=url, callback=self.parse_socal)
        request.meta['type'] = 'Southern California'
        yield request

    def parse_most_read(self, response):
        sel = Selector(response)

        links = sel.xpath('//*[@id="daily"]/li/div/div/a/@href')
        string_links = links.extract()

        for link in string_links:
            request = Request(link, callback=self.parse_link)
            request.meta['type'] = response.meta['type']
            request.meta['link'] = link
            yield request

    def parse_socal(self, response):
        sel = Selector(response)

        links = sel.xpath('//*[@id="mobTouchSwipeWrap"]/div/div/div/div/div/div/a/@href')
        string_links = links.extract()

        for link in string_links:
            request = Request(link, callback=self.parse_link)
            request.meta['type'] = response.meta['type']
            request.meta['link'] = link
            yield request

    def parse_link(self, response):
        global externalCounter
        sel = Selector(response)

        # Title
        title = sel.xpath('//*[@id="mobTouchSwipeWrap"]/div/div/div/div/div/div/h1/text()')
        title = title.extract()
        title = title[0].encode('utf-8')
        title = title.lstrip()
        title = title.rstrip()

        # Name of News Site
        news_site = "Singtao Daily"

        # Section Name
        section = response.meta['type']

        # Date
        date = sel.xpath('//*[@id="mobTouchSwipeWrap"]/div[1]/div/div[1]/div[2]/div[2]/div/div[1]/text()')
        date = date.extract()
        date = date[1].encode('utf-8')

        # Link
        link = response.meta['link']

        with open('./csv/singtao.csv', "ab") as ffile:
            writer = unicodecsv.writer(ffile, delimiter=',', quotechar='"', quoting=unicodecsv.QUOTE_ALL)
            writer.writerow(['ST'+str(externalCounter), title, news_site, link, section, date])

        externalCounter += 1
