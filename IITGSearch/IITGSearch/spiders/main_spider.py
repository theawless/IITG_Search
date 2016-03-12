import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
import re
import urlparse
from IITGSearch.items import IITGSearchItem
import IITGSearch.setlog

logger = IITGSearch.setlog.logger


class IITGSpider(scrapy.Spider):
    name = "IITG"
    allowed_domains = ["iitg.ernet.in"]
    start_urls = [
        "http://intranet.iitg.ernet.in",
        "http://local.iitg.ernet.in"
    ]
    crawledLinks = set()

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        links = hxs.select("//a/@href").extract()

        # We stored already crawled links in this list
        # crawledLinks = []
        # Pattern to check proper link
        # linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")

        for link in links:
            _link = self.abs_url(link, response)
            # If it is a proper link and is not checked yet, yield it to the Spider
            if _link not in IITGSpider.crawledLinks:
                IITGSpider.crawledLinks.add(_link)
                logger.debug('  ' + _link)
                yield Request(_link, self.parse)

    def abs_url(self, url, response):
        base = response.xpath('//head/base/@href').extract()
        if base:
            base = base[0]
        else:
            base = response.url
        return urlparse.urljoin(base, url)


'''
        titles = hxs.select('//h1[@class="post_title"]/a/text()').extract()
        for title in titles:
            item = IITGSearchItem()
            item["title"] = title
            yield item
'''

'''
    def parse(self, response):
        for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        for sel in response.xpath('//ul/li'):
            item = IITGSearchItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item
'''
