# -*- coding: utf-8 -*-
import unicodecsv
import scrapy
import re
import json
from lxml import html
from docx2html import convert
from scrapy.http import FormRequest, Request

keywordList = [u'Article ID',
               u'细分',
               u'細分',
               u'平权法案',
               u'平權法案',
               u'非法移民',
               u'庇护城市',
               u'庇護城市',
               u'跨性别',
               u'和平教恐惧',
               u'种族主义',
               u'種族主義',
               u'种族歧视',
               u'種族歧視',
               u'政治正确',
               u'政治正確',
               u'假新闻',
               u'假新聞',
               u'禁穆令',
               u'穆斯林禁令',
               u'白左',
               u'华左',
               u'极左',
               u'極左',
               u'极右',
               u'極右',
               u'另类右翼',
               u'另類右翼',
               u'民主党',
               u'民主黨',
               u'共和党',
               u'共和黨',
               u'左媒',
               u'左翼媒體',
               u'白人至上',
               u'黑命贵',
               u'也是命',
               u'白人',
               u'欧裔',
               u'歐裔',
               u'亚裔',
               u'亞裔',
               u'华人',
               u'华裔',
               u'華裔',
               u'非裔',
               u'黑人',
               u'拉丁裔',
               u'西裔',
               u'老墨',
               u'穆斯林',
               u'伊斯兰',
               u'伊斯蘭',
               u'和平教',
               u'绿教',
               u'绿左',
               u'自由',
               u'宽容',
               u'寬容',
               u'平等',
               u'正义',
               u'正義',
               u'权利',
               u'權利',
               u'多元化',
               u'AA',
               u'affirmative action',
               u'Alt right',
               u'BLM',
               u'Black Lives Matter']

def search(filename):

    # Create a dictionary with the keywordList; initialize all values to 0
    keywordDict = dict((keyword,0) for keyword in keywordList)

    # Open the file
    with open(filename, "r") as file:
        page = file.read()

    # Get file contents
    tree = html.fromstring(page)
    totalParagraphs = tree.xpath("/html/body/p/text()")

    # Loop through all the content by article and search for the keywords in the content
    # Write to csv file when complete
    for i in xrange(1, len(totalParagraphs)):
        articleId = tree.xpath("/html/body/h2["+str(i)+"]/text()")
        articleContent = tree.xpath("/html/body/p["+str(i)+"]/text()")
        try:
            articleContent = unicode(articleContent[0])

            # Search for each keyword in article content
            for keyword in keywordList:
                if keyword in articleContent:
                    keywordDict[keyword] += 1

            values = keywordDict.values()
            values[0] = articleId[0]

            # Open file and set parameters accordingly
            with open("./csv/keyword.csv", "ab") as ffile:
                writer = unicodecsv.writer(ffile, delimiter=',', quotechar='"', quoting=unicodecsv.QUOTE_ALL)
                writer.writerow(values)

            # Clear dictionary
            keywordDict = dict.fromkeys(keywordDict, 0)
        except:
            pass

def search_nonaggregate(filename):

    # Create a dictionary with the keywordList; initialize all values to 0
    keywordDict = dict((keyword,0) for keyword in keywordList)

    # Open the file
    with open(filename, "r") as file:
        page = file.read()

    # Get file contents
    tree = html.fromstring(page)
    totalParagraphs = tree.xpath("/html/body/p/text()")

    # Loop through all the content by article and search for the keywords in the content
    # Write to csv file when complete
    for i in xrange(1, len(totalParagraphs), 2):
        articleId = tree.xpath("/html/body/p["+str(i)+"]/text()")
        articleContent = tree.xpath("/html/body/p["+str(i+1)+"]/text()")
        try:
            articleContent = unicode(articleContent[0])

            # Search for each keyword in article content
            for keyword in keywordList:
                if keyword in articleContent:
                    keywordDict[keyword] += 1

            values = keywordDict.values()
            values[0] = articleId[0]

            # Open file and set parameters accordingly
            with open("./csv/keyword.csv", "ab") as ffile:
                writer = unicodecsv.writer(ffile, delimiter=',', quotechar='"', quoting=unicodecsv.QUOTE_ALL)
                writer.writerow(values)

            # Clear dictionary
            keywordDict = dict.fromkeys(keywordDict, 0)
        except:
            pass

# Script starts here
if __name__ == "__main__":

  # Write the first row to the csv file
  with open("./csv/keyword.csv", "w") as ffile:
      writer = unicodecsv.writer(ffile, delimiter=',', quotechar='"', quoting=unicodecsv.QUOTE_ALL)
      writer.writerow(keywordList)

   # Save Aggregate Word Document as Html File
  html_aggregate = convert('./word/aggregate.docx')
  with open('./html/aggregate.html', 'r+') as ffile:
      ffile.write(html_aggregate)
      search('./html/aggregate.html')
      ffile.close()

   # Save China Press Word Document as Html File
  html_chinapress = convert('./word/chinapress.docx')
  with open('./html/chinapress.html', 'w') as ffile:
      ffile.write(html_chinapress)
      search_nonaggregate('./html/chinapress.html')
      ffile.close()

   # Save Singtao Word Document as Html File
  html_singtao = convert('./word/singtao.docx')
  with open('./html/singtao.html', 'w') as ffile:
      ffile.write(html_singtao)
      search_nonaggregate('./html/singtao.html')
      ffile.close()

  # Save Wenxuecity Word Document as Html File
  html_wenxuecity = convert('./word/wenxuecity.docx')
  with open('./html/wenxuecity.html', 'w') as ffile:
      ffile.write(html_wenxuecity)
      search_nonaggregate('./html/wenxuecity.html')
      ffile.close()

  # Save World Journal Word Document as Html File
  html_worldjournal = convert('./word/worldjournal.docx')
  with open('./html/worldjournal.html', 'w') as ffile:
      ffile.write(html_worldjournal)
      search_nonaggregate('./html/worldjournal.html')
      ffile.close()
