import unicodecsv
import scrapy
import re
import json
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

        # # Washington Section
        # url = 'http://news.uschinapress.com/Washington/'
        # request = Request(url=url, callback=self.parse_washington)
        # request.meta['type'] = 'Washington'
        # yield request

        # New York Section
        for i in range(0, 10):
            url = 'http://207.254.179.87/search/searchNyqbZw.jsp?channelname=yaowen&channel=yes&start=' + str(i) + '0'
            request = Request(url=url, callback=self.parse_ny)
            request.meta['type'] = 'New York'
            yield request

        # San Francisco Section
        for i in range(1, 51):
            url = 'http://sf.uschinapress.com/san/news_san/' + str(i) + '.shtml'
            request = Request(url=url, callback=self.parse_sf_sea_tex)
            request.meta['type'] = 'San Francisco'
            yield request

        # Seattle Section
        for i in range(1, 51):
            url = 'http://sea.uschinapress.com/seattle/xicheng/' + str(i) + '.shtml'
            request = Request(url=url, callback=self.parse_sf_sea_tex)
            request.meta['type'] = 'Seattle'
            yield request

        # Texas Section
        for i in range(1, 11):
            url = 'http://texas.uschinapress.com/texas/News/' + str(i) + '.shtml'
            request = Request(url=url, callback=self.parse_sf_sea_tex)
            request.meta['type'] = 'Texas'
            yield request

    def parse_most_read(self, response):
        sel = Selector(response)

        links = sel.xpath('//div[@class="ranking"]/div[@class="ranking_bottom"]/div/ul[1]/li/a/@href')
        string_links = links.extract()

        for link in string_links:
            request = Request(link, callback=self.parse_link)
            request.meta['type'] = response.meta['type']
            request.meta['link'] = link
            yield request

    def parse_washington(self, response):
        sel = Selector(response)

        links = sel.xpath('//*[@id="Con_rank_tab1"]/li/a/@href')
        string_links = links.extract()

        for link in string_links:
            request = Request(link, callback=self.parse_link)
            request.meta['type'] = response.meta['type']
            request.meta['link'] = link
            yield request

    def parse_ny(self, response):
        str_as_json = response.text[14:]
        str_as_json = str_as_json[13:]
        data = json.loads(str_as_json)

        for i in range(0, 10):
            link = data['docList'][i]['url']
            request = Request(link, callback=self.parse_link)
            request.meta['type'] = response.meta['type']
            request.meta['link'] = link
            yield request

    def parse_sf_sea_tex(self, response):
        sel = Selector(response)

        links = sel.xpath('//*[@id="content"]/dl/dt/a/@href')
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
        title = sel.xpath('//*[@id="content"]/div/h1/text()')
        title = title.extract()

        if (len(title) != 0):
            # Xpath selector matched
            try:
                title = title[0].encode('utf-8')
            except:
                title = "Unable to Parse Title"

            # Date
            date = sel.xpath('//*[@id="content"]/div[1]/div[1]/span/text()')
            date = date.extract()
            date = date[0].encode('utf-8')

        else:
            # Xpath selector didn't match; try another Xpath selector
            title = sel.xpath('//div[@class="title_news"]//text()')
            title = title.extract()

            if (len(title) != 0):
                title = title[0].encode('utf-8')

                # Date
                date = sel.xpath('//div[@class="forn_l"]/span//text()')
                date = date.extract()
                date = date[0].encode('utf-8')
            else:
                # Xpath selector didn't match; try another Xpath selector
                title = sel.xpath('//div[2]/header/h1/text()')
                title = title.extract()
                title = title[0].encode('utf-8')

                # Date
                date = sel.xpath('//header/div/span[1]/text()')
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
