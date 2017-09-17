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

        names = ["\u8fd9\u624d\u662f\u7f8e\u56fd",
                 "\u534e\u4eba\u751f\u6d3b\u7f51",
                 "\u5317\u7f8e\u7701\u94b1\u5feb\u62a5",
                 "\u7ebd\u7ea6\u541b",
                 "\u6d1b\u6749\u77f6\u534e\u4eba\u8d44\u8baf\u7f51",
                 "\u7f8e\u56fd\u0031\u0036\u0038\u8d44\u8baf\u7f51",
                 "\u5e26\u4f60\u6e38\u904d\u7f8e\u56fd",
                 "\u7f8e\u56fd\u7559\u5b66\u90a3\u70b9\u4e8b",
                 "\u7f8e\u56fd\u534e\u4eba\u5bb6\u56ed",
                 "\u7f8e\u56fd\u4e2d\u6587\u7f51",
                 "\u5317\u7f8e\u534e\u4eba\u4e4b\u58f0",
                 "\u5927\u7ebd\u7ea6\u534e\u4eba\u8d44\u8baf",
                 "\u4e16\u754c\u8bf4",
                 "\u897f\u96c5\u56fe\u96f7\u5c3c\u5c14",
                 "\u653f\u89c1",
                 "\u7ebd\u7ea6\u4eba",
                 "\u6e7e\u533a\u90a3\u4e9b\u4e8b\u513f",
                 "\u7f8e\u56fd\u534e\u4eba\u4e4b\u58f0",
                 "\u4f11\u65af\u987f\u5728\u7ebf",
                 "\u7f8e\u5e1d\u6b63\u80fd\u91cf",
                 "\u4e9a\u7279\u5170\u5927\u534e\u4eba\u751f\u6d3b\u7f51",
                 "\u4e9a\u7279\u5170\u5927\u534e\u4eba\u5708",
                 "\u7f8e\u56fd\u534e\u4eba",
                 "\u9009\u7f8e",
                 "\u7f8e\u56fd\u751f\u6d3b\u5728\u7ebf",
                 "\u5317\u7f8e\u7559\u5b66\u751f\u65e5\u62a5",
                 "\u8fd9\u91cc\u662f\u7f8e\u56fd",
                 "\u5047\u88c5\u5728\u7ebd\u7ea6"]

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
            request.meta['name'] = names[i]
            yield request

    def parse(self, response):
        global externalCounter
        data = json.loads(response.text)
        size = data['data']['size']

        name = response.meta['name'].decode('unicode-escape').encode('utf-8')

        for i in range(0, size):
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
