from docx import Document
from docx.shared import Inches
import scrapy
import re
import csv
from scrapy.http.request import Request
from scrapy.selector import Selector

# Create object for word document
document = Document()

class ChinaPressSpider(scrapy.Spider):
    name = "ChinaPressWord"

    def start_requests(self):
        with open('./csv/chinapress.csv') as ffile:
            reader = csv.reader(ffile, delimiter=',')
            for row in reader:
                request = Request(row[3], callback=self.parse_link)
                request.meta['type'] = row[4]
                request.meta['id'] = row[0]
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
        document.add_paragraph(response.meta['id'] + ": " + full_content)
        document.save('./word/chinapress.docx')
