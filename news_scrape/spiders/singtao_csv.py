import unicodecsv
import scrapy
import re
import json
import time
import sys
from scrapy.http.request import Request

externalCounter = 0

class SingtaoSpider(scrapy.Spider):
    name = "SingtaoCSV"

    def start_requests(self):

        # Make sure we have necessary data before continuining
        if (len(sys.argv) != 6):
            print "Need more information! Need 6 arguments; given " + str(len(sys.argv))
            print "Format as: scrapy crawl SingtaoCSV -a year=<year> -a month=<month>"
            print "<year> should be formatted as ####"
            print "<month> should be formatted as ##"
            return

        # Create CSV Writer for csv document

        # Comment lines 17 and 18 out if you want to append to file
        ffile = open('./csv/singtao.csv', "w+")
        ffile.close()

        # Make Calendar Requests
        headers = {
            'pragma': 'no-cache',
            'origin': 'https://www.singtaousa.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'x-chrome-uma-enabled': '1',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'cache-control': 'no-cache',
            'authority': 'www.googleapis.com',
            'referer': 'https://www.singtaousa.com/la/search/',
            'x-client-data': 'CJC2yQEIprbJAQjBtskBCPqcygEIqZ3KAQjSncoBCKijygE=',
        }

        for i in range (0, 10):

            dataCounter = 1

            # All months have at least 28 days
            while dataCounter <= 28:

                # Get First Date
                leftDate = str(dataCounter)
                if dataCounter <= 9:
                    leftDate = '0' + leftDate

                # Get Second Date
                dataCounter += 1
                rightDate = str(dataCounter)
                if dataCounter <= 9:
                    rightDate = '0' + rightDate

                dataCounter += 1

                url = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyC2n479BCncR6aW15ogLEz6BPa78eA_XgM&' + 'cx=000349818001918521514:ygfnnyqz8kc&' +'q=%22%E7%9A%84%E2%80%9C&' + 'sort=date%3Ar%3A' + self.year + self.month + leftDate + '%3A' + self.year + self.month + rightDate + '%2Cdate&' +'exactTerms=%E7%9A%84&' + 'c2off=1&' + 'start=' + str(i*10+1)
                request = Request(url=url,
                                  callback=self.parse,
                                  method='GET',
                                  headers=headers,
                                  )
                yield request
                #time.sleep(3)

            # If not February, get the 29th and 30th
            if self.month != 2:
                url = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyC2n479BCncR6aW15ogLEz6BPa78eA_XgM&' + 'cx=000349818001918521514:ygfnnyqz8kc&' +'q=%22%E7%9A%84%E2%80%9C&' + 'sort=date%3Ar%3A' + self.year + self.month + '29%3A' + self.year + self.month + '30%2Cdate&' +'exactTerms=%E7%9A%84&' + 'c2off=1&' + 'start=' + str(i*10+1)
                request = Request(url=url,
                                  callback=self.parse,
                                  method='GET',
                                  headers=headers,
                                  )
                yield request
                #time.sleep(3)

            # All these months have 31 days
            if self.month is 1 or self.month is 3 or self.month is 5 or self.month is 7 or self.month is 8 or self.month is 10 or self.month is 12:
                url = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyC2n479BCncR6aW15ogLEz6BPa78eA_XgM&' + 'cx=000349818001918521514:ygfnnyqz8kc&' +'q=%22%E7%9A%84%E2%80%9C&' + 'sort=date%3Ar%3A' + self.year + self.month + '31%3A' + self.year + self.month + '31%2Cdate&' +'exactTerms=%E7%9A%84&' + 'c2off=1&' + 'start=' + str(i*10+1)
                request = Request(url=url,
                                  callback=self.parse,
                                  method='GET',
                                  headers=headers,
                                  )
                yield request
                #time.sleep(3)

    def parse(self, response):
        global externalCounter

        # Get JSON of response
        data = json.loads(response.text)
        print data
        totalResults = data['queries']['request'][0]['count']

        # Only attempt to get information if there is information to retrieve
        if totalResults is not 0:
            for i in range (0, int(totalResults)):
                title = data['items'][i]['title']
                news_site = "Singtao Daily"
                date = data['items'][i]['pagemap']['document'][0]['pubdate']
                link = data['items'][i]['link']
                section = data['items'][i]['pagemap']['document'][0]['newscat']
                with open('./csv/singtao.csv', "ab") as ffile:
                    writer = unicodecsv.writer(ffile, delimiter=',', quotechar='"', quoting=unicodecsv.QUOTE_ALL)
                    writer.writerow(['ST'+str(externalCounter), title, news_site, link, section, date])

                externalCounter += 1
