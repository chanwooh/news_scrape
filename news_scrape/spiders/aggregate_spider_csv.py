# -*- coding: utf-8 -*-
import unicodecsv
import scrapy
import re
import json
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector

externalCounter = 0

class AggregateSpider(scrapy.Spider):
    name = "AggregateCSV"

    def start_requests(self):

        # Create CSV Writer for csv document

        # Comment lines 18 and 19 out if you want to append to file
        ffile = open('./csv/aggregate.csv', "w+")
        ffile.close()

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

        # Make requests
        for i in range(0, 28):
            for j in range(1, 11):
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
                                  body='{"PageIndex":'+str(j)+',"PageSize":20,"Type":0,"Wechat":"'+urls[i]+'"}')
                request.meta['name'] = names[i]
                yield request

    def parse(self, response):
        global externalCounter
        data = json.loads(response.text)
        size = data['data']['size']

        name = response.meta['name']

        for i in range(0, size):
            try:
                title = data['data']['data'][i]['Title'].encode('utf-8')
                date = data['data']['data'][i]['PostTime'].encode('utf-8')
                link_id = data['data']['data'][i]['Id'].encode('utf8')
                link = "http://top.aiweibang.com/article/url?aid=" + link_id
                like = data['data']['data'][i]['LikeNum']
                read = data['data']['data'][i]['ReadNum']

                with open('./csv/aggregate.csv', "ab") as ffile:
                    writer = unicodecsv.writer(ffile, delimiter=',', quotechar='"', quoting=unicodecsv.QUOTE_ALL)
                    writer.writerow(['AG'+str(externalCounter), name, title, date, link, read, like])

                externalCounter += 1
            except:
                pass