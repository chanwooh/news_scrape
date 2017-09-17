from docx import Document
from docx.shared import Inches
import scrapy
import re
from scrapy.http.request import Request
from scrapy.selector import Selector

# Create object for word document
document = Document()

class WenxuecitySpider(scrapy.Spider):
    name = "WenxuecityWord"

    def start_requests(self):
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
            yield request

    def parse_link(self, response):
        sel = Selector(response)

        # Content
        content = sel.xpath('//*[@id="articleContent"]/p/text()')
        content = content.extract()

        if (len(content) == 0):
            # Xpath selector didn't match; try another Xpath selector
            content = sel.xpath('//*[@id="articleContent"]/text()')
            content = content.extract()

        full_content = ""
        for paragraph in content:
            full_content += paragraph

        full_content = full_content.encode('unicode-escape').decode('unicode-escape')
        document.add_paragraph("Article: " + full_content)
        document.save('./word/wenxuecity.docx')
