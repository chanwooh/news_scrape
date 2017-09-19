import unicodecsv
import scrapy
import re
from scrapy.http.request import Request
from scrapy.selector import Selector

externalCounter = 0

class WorldJournalSpider(scrapy.Spider):
    name = "WorldJournalCSV"

    def start_requests(self):

        # Create CSV Writer for csv document
        # Comment out lines 20 and 21 if you want to append to file

        ffile = open('./csv/worldjournal.csv', "w+")
        ffile.close()

        # Most Read
        url = 'http://www.worldjournal.com/topic/%E8%B6%85%E4%BA%BA%E6%B0%A3%E6%96%B0%E8%81%9E-2/'
        request = Request(url=url, callback=self.parse)
        request.meta['type'] = 'Most Read'
        yield request

        # US Section
        url = 'http://www.worldjournal.com/topic/%E7%BE%8E%E5%9C%8B%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD/'
        request = Request(url=url, callback=self.parse)
        request.meta['type'] = 'United States'
        yield request

        # NY Section
        url = 'http://www.worldjournal.com/topic/%E7%B4%90%E7%B4%84%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD/'
        request = Request(url=url, callback=self.parse)
        request.meta['type'] = 'New York'
        yield request

        # LA Section
        url = 'http://www.worldjournal.com/topic/%E6%B4%9B%E6%9D%89%E7%A3%AF%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD/'
        request = Request(url=url, callback=self.parse)
        request.meta['type'] = 'Los Angeles'
        yield request

        # SF Section
        url = 'http://www.worldjournal.com/topic/%E8%88%8A%E9%87%91%E5%B1%B1%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD/'
        request = Request(url=url, callback=self.parse)
        request.meta['type'] = 'San Francisco'
        yield request

        # New Jersey Section
        url = 'http://www.worldjournal.com/topic/%E6%96%B0%E6%BE%A4%E8%A5%BF%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD/'
        request = Request(url=url, callback=self.parse)
        request.meta['type'] = 'New Jersey'
        yield request

        # Boston Section
        url = 'http://www.worldjournal.com/topic/%E6%B3%A2%E5%A3%AB%E9%A0%93%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD/'
        request = Request(url=url, callback=self.parse)
        request.meta['type'] = 'Boston'
        yield request

        # Chicago Section
        url = 'http://www.worldjournal.com/topic/%E8%8A%9D%E5%8A%A0%E5%93%A5%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD/'
        request = Request(url=url, callback=self.parse)
        request.meta['type'] = 'Chicago'
        yield request

        # D.C. Section
        url = 'http://www.worldjournal.com/topic/%E5%A4%A7%E8%8F%AF%E5%BA%9C%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD/'
        request = Request(url=url, callback=self.parse)
        request.meta['type'] = 'D.C.'
        yield request

        # Houston-Dallas Section
        url = 'http://www.worldjournal.com/topic/%E4%BC%91%E5%A3%AB%E9%A0%93%E9%81%94%E6%8B%89%E6%96%AF%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD/'
        request = Request(url=url, callback=self.parse)
        request.meta['type'] = 'Houston-Dallas'
        yield request

        # Atlanta Section
        url = 'http://www.worldjournal.com/topic/%E5%96%AC%E5%B7%9E%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD/'
        request = Request(url=url, callback=self.parse)
        request.meta['type'] = 'Atlanta'
        yield request

        # San Diego Section
        url = 'http://www.worldjournal.com/topic/%E8%81%96%E5%9C%B0%E7%89%99%E5%93%A5%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD/'
        request = Request(url=url, callback=self.parse)
        request.meta['type'] = 'San Diego'
        yield request

    def parse(self, response):
        sel = Selector(response)

        links = sel.xpath('//*[@id="sticky-content"]/div/article/div/h2/a/@href')
        string_links = links.extract()

        if response.meta['type'] == 'Most Read':
            for link in string_links:
                regex = re.compile('.com/(.*?)/article')
                link_id = regex.search(link)
                if link_id:
                    link_id = link_id.group(1)
                    request = Request("http://ctr2.worldjournal.com/wjcounter.php?aid="+link_id, callback=self.parse_get_views)
                    request.meta['link'] = link
                    request.meta['type'] = response.meta['type']
                    yield request
        else:
            for i in range(0, 14):
                regex = re.compile('.com/(.*?)/article')
                link_id = regex.search(string_links[i])
                if link_id:
                    link_id = link_id.group(1)
                    request = Request("http://ctr2.worldjournal.com/wjcounter.php?aid="+link_id, callback=self.parse_get_views)
                    request.meta['link'] = string_links[i]
                    request.meta['type'] = response.meta['type']
                    yield request

    def parse_get_views(self, response):

        script_body = response.body
        regex = re.compile('\{cnt:"(.*?)"}')
        views = regex.search(script_body)

        if views:
            views = views.group(1)
        else:
            views = ""

        request = Request(response.meta['link'], callback=self.parse_link)
        request.meta['views'] = views
        request.meta['type'] = response.meta['type']
        request.meta['link'] = response.meta['link']
        yield request

    def parse_link(self, response):
        global externalCounter
        sel = Selector(response)

        # Title
        title = sel.xpath('//*[@id="sticky-content"]/div[1]/div[1]/h1/text()')
        title = title.extract()
        title = title[0].encode('utf-8')

        # Name of News Site
        news_site = "World Journal"

        # Section Name
        section = response.meta['type']

        # Date
        date = sel.xpath('//*[@id="sticky-content"]/div[1]/div[1]/time/@datetime')
        date = date.extract()
        date = date[0].encode('utf-8')

        # Link
        link = response.meta['link']

        # View Count
        views = response.meta['views'].encode('utf-8')

        with open('./csv/worldjournal.csv', "ab") as ffile:
            writer = unicodecsv.writer(ffile, delimiter=',', quotechar='"', quoting=unicodecsv.QUOTE_ALL)
            writer.writerow(['WJ'+str(externalCounter), title, news_site, section, date, link, views])

        externalCounter += 1
