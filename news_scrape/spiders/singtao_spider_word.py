from docx import Document
from docx.shared import Inches
import scrapy
import re
from scrapy.http.request import Request
from scrapy.selector import Selector

# Create object for word document
document = Document()

class SingtaoSpider(scrapy.Spider):
    name = "SingtaoWord"

    def start_requests(self):
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
            yield request

    def parse_socal(self, response):
        sel = Selector(response)

        links = sel.xpath('//*[@id="mobTouchSwipeWrap"]/div/div/div/div/div/div/a/@href')
        string_links = links.extract()

        for link in string_links:
            request = Request(link, callback=self.parse_link)
            request.meta['type'] = response.meta['type']
            yield request

    def parse_link(self, response):
        sel = Selector(response)

        # Content
        content = sel.xpath('//*[@id="mobTouchSwipeWrap"]/div[1]/div/div[1]/div[2]/div[4]/p/text()')
        content = content.extract()

        full_content = ""
        for paragraph in content:
            full_content += paragraph

        full_content = full_content.encode('unicode-escape').decode('unicode-escape')
        document.add_paragraph("Article: " + full_content)
        document.save('./word/singtao.docx')
