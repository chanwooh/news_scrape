# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Inches
import scrapy
import re
import json
import docx
from scrapy.http.request import Request
from scrapy.selector import Selector

# Create object for word document
document = Document()

class AggregateSpider(scrapy.Spider):
    name = "AggregateWord"

    def start_requests(self):

        urls = ["LMO-MMOgw6c~",
                "LMO-NsOkw63Csg~~",
                "LMO_NMOiw60~",
                "LMO6MMOmw6bCsQ~~",
                "L8O_N8Otw6fCsA~~",
                "L8O9MMOmw6zCtg~~",
                "JMO6OcOt",
                "LMO_MMOhw64~",
                "KcO_McOiw6Y~",
                "KcO5M8Otw6nCtw~~",
                "KsO3MsOmw67Cug~~",
                "KcO4NcOnw6bCtA~~",
                "KMO6MsOtw6fCsA~~",
                "KcO4OcOhw6_Ctw~~",
                "L8O7McOgw6s~",
                "L8O9OcOtw6jCsw~~",
                "LsO7MsOnw6nCsA~~",
                "KsO3McOlw6vCsg~~",
                "L8O2OcOmw6fCtA~~",
                "L8O7M8Okw67CsA~~",
                "JMO5MsOtw6w~",
                "LMO_McOtw6_Cu8Ol",
                "LMO_McOtw6_Cu8Oh",
                "KcO4OMOjw6jCtA~~",
                "LMO2NsOjw6bCuw~~",
                "LsO3McOmw6g~",
                "LMO2NsOjw6bCtA~~",
                "LMO5NsOsw6w~"]

        names = [u"这才是美国",
                 u"华人生活网",
                 u"北美省钱快报",
                 u"纽约君",
                 u"洛杉矶华人资讯网",
                 u"美国168资讯网",
                 u"带你游遍美国",
                 u"美国留学那点事",
                 u"美国华人家园",
                 u"美国中文网",
                 u"北美华人之声",
                 u"大纽约华人资讯",
                 u"世界说",
                 u"西雅图雷尼尔",
                 u"政见",
                 u"纽约人",
                 u"湾区那些事儿",
                 u"美国华人之声",
                 u"休斯顿在线",
                 u"美帝正能量",
                 u"亚特兰大华人生活网",
                 u"亚特兰大华人圈",
                 u"美国华人",
                 u"选美",
                 u"美国生活在线",
                 u"北美留学生日报",
                 u"这里是美国",
                 u"假装在纽约"]

        paragraph = document.add_paragraph(names[0].encode('unicode-escape').decode('unicode-escape'))
        document.add_section()

        # Make requests
        for i in range(0, 28):
            request = Request(url='http://top.aiweibang.com/article/getarticles/',
                              callback=self.parse,
                              method='POST',
                              headers={'Host':'top.aiweibang.com',
                                       'Connection':'keep-alive',
                                       'Pragma':'no-cache',
                                       'Cache-Control':'no-cache',
                                       'Accept':'application/json, text/plain, */*',
                                       'X-Requested-With':'XMLHttpRequest',
                                       'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                                       'Content-Type':'application/json;charset=UTF-8',
                                       'Referer':"http://top.aiweibang.com/article/" + urls[i],
                                       'Accept-Encoding':'gzip, deflate',
                                       'Accept-Language':'en-US,en;q=0.8',
                                       'Cookie':'Hm_lvt_45cdb9a58c4dd401ed07126f3c04d3c4=1501449933; Hm_lpvt_45cdb9a58c4dd401ed07126f3c04d3c4=1503615904'},
                              body='{"PageIndex":1,"PageSize":20,"Type":0,"Wechat":"'+urls[i]+'"}')

            if(i != 27):
                paragraph = document.add_paragraph('\n' + '\n' + names[i+1].encode('unicode-escape').decode('unicode-escape'))
                document.add_section()
                request.meta['before_para'] = paragraph
            else:
                request.meta['before_para'] = "EOD"

            yield request

    def parse(self, response):
        global externalCounter
        data = json.loads(response.text)

        size = data['data']['size']

        for i in range(0, size):
            title = data['data']['data'][i]['Title'].encode('unicode-escape').decode('unicode-escape')
            link_id = data['data']['data'][i]['Id'].encode('utf8')

            request = Request(url="http://top.aiweibang.com/article/url?aid=" + link_id, callback=self.parse_link)
            request.meta['title'] = title
            request.meta['before_para'] = response.meta['before_para']
            yield request

    def parse_link(self, response):
        sel = Selector(response)

        # Content
        content = sel.xpath('//*[@id="js_content"]/p/span/text()')
        content = content.extract()

        if (len(content) == 0):
            # Xpath selector didn't match; try another Xpath selector
            content = sel.xpath('//*[@id="js_content"]/p/text()')
            content = content.extract()

        full_content = ""
        for paragraph in content:
            full_content += paragraph

        full_content = full_content.encode('unicode-escape').decode('unicode-escape')
        p = document.add_paragraph('\n')
        p.add_run(response.meta['title'] + ": ").bold = True

        if (full_content != ""):
            if (response.meta['before_para'] == "EOD"):
                document.add_paragraph(full_content)
            else:
                response.meta['before_para'].insert_paragraph_before(full_content)
        else:
            document.add_paragraph("Content is unavailable. It has been deleted, moved, or requires a QR scan.")

        document.save('./word/aggregate.docx')
