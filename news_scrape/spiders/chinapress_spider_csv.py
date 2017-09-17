import unicodecsv
import scrapy
import re
from scrapy.http.request import Request
from scrapy.selector import Selector

externalCounter = 0

class ChinaPressSpider(scrapy.Spider):
    name = "ChinaPressCSV"

    def start_requests(self):

        # Create CSV Writer for csv document

        # Comment lines 17 and 18 out if you want to append to end of file
        ffile = open('./csv/chinapress.csv', "w+")
        ffile.close()

        # Most Read
        url = 'http://www.uschinapress.com/'
        request = Request(url=url, callback=self.parse_most_read)
        request.meta['type'] = 'Most Read'
        yield request

        # Washington Section
        url = 'http://news.uschinapress.com/Washington/'
        request = Request(url=url, callback=self.parse_socal)
        request.meta['type'] = 'Washington'
        yield request

    def parse_most_read(self, response):
        sel = Selector(response)

        links = sel.xpath('//*[@id="index_rank_tab1"]/li/a/@href')
        string_links = links.extract()

        for link in string_links:
            request = Request(link, callback=self.parse_link)
            request.meta['type'] = response.meta['type']
            request.meta['link'] = link
            yield request

    def parse_socal(self, response):
        sel = Selector(response)

        links = sel.xpath('//*[@id="Con_rank_tab1"]/li/a/@href')
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
        title = sel.xpath('/html/body/section/div/header/h1/text()')
        title = title.extract()

        if (len(title) != 0):
            # Xpath selector matched
            title = title[0].encode('utf-8')

            # Date
            date = sel.xpath('/html/body/section[1]/div[2]/header/div[1]/span[1]/text()')
            date = date.extract()
            date = date[0].encode('utf-8')

        else:
            # Xpath selector didn't match; try another Xpath selector
            title = sel.xpath('/html/body/div[3]/div[1]/div[1]/div[1]/h2/text()')
            title = title.extract()
            title = title[0].encode('utf-8')

            # Date
            date = sel.xpath('/html/body/div[3]/div[1]/div[1]/div[1]/div/span[1]/text()')
            date = date.extract()
            date = date[0].encode('utf-8')

        # Name of News Site
        news_site = "China Press"

        # Section Name
        section = response.meta['type']

        # Link
        link = response.meta['link']

        with open('./csv/chinapress.csv', "ab") as ffile:
            writer = unicodecsv.writer(ffile, delimiter=',', quotechar='"', quoting=unicodecsv.QUOTE_ALL)
            writer.writerow(['CP'+str(externalCounter), title, news_site, link, section, date])

        externalCounter += 1
