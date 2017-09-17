from docx import Document
from docx.shared import Inches
import scrapy
import re
from scrapy.http.request import Request
from scrapy.selector import Selector

# Create object for word document
document = Document()

class WorldJournalSpider(scrapy.Spider):
    name = "WorldJournalWord"

    def start_requests(self):
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
                request = Request(link, callback=self.parse_link)
                request.meta['link'] = link
                request.meta['type'] = response.meta['type']
                yield request
        else:
            for i in range(0, 14):
                request = Request(string_links[i], callback=self.parse_link)
                request.meta['link'] = string_links[i]
                request.meta['type'] = response.meta['type']
                yield request

    def parse_link(self, response):
        sel = Selector(response)

        # Content
        content = sel.xpath('//*[@id="sticky-content"]/div/div/p/text()')
        content = content.extract()

        full_content = ""
        for paragraph in content:
            full_content += paragraph

        full_content = full_content.encode('unicode-escape').decode('unicode-escape')
        document.add_paragraph("Article: " + full_content)
        document.save('./word/worldjournal.docx')
