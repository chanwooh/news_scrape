from docx import Document
from docx.shared import Inches
import scrapy
import re
from scrapy.http.request import Request
from scrapy.selector import Selector

# Create object for word document
document = Document()

class ChinaPressSpider(scrapy.Spider):
    name = "ChinaPressWord"

    def start_requests(self):
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
            yield request

    def parse_socal(self, response):
        sel = Selector(response)

        links = sel.xpath('//*[@id="Con_rank_tab1"]/li/a/@href')
        string_links = links.extract()

        for link in string_links:
            request = Request(link, callback=self.parse_link)
            request.meta['type'] = response.meta['type']
            yield request

    def parse_link(self, response):
        sel = Selector(response)

        # Content
        content = sel.xpath('/html/body/section/div/header/div/p//text()')
        content = content.extract()

        if (len(content) == 0):
            # Xpath selector didn't match; try another Xpath selector
            content = sel.xpath('//*[@id="zoom"]/p/text()')
            content = content.extract()

        full_content = ""
        for paragraph in content:
            full_content += paragraph

        full_content = full_content.encode('unicode-escape').decode('unicode-escape')
        document.add_paragraph("Article: " + full_content)
        document.save('./word/chinapress.docx')
