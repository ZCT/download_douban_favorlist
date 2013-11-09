# coding=utf-8
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
#from scrapy.contrib.spiders import InitSpider
import os
import re
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.spiders.init import InitSpider

from scrapy.http import Request, FormRequest
from scrapy.selector import HtmlXPathSelector
#import .items.YinlianItem
from ..items import YinlianItem


def get_path(s):
    return s.rpartition('/')[2]


class DATSgmlLinkExtractor(SgmlLinkExtractor):
    def _link_allowed(self, link):
        allowed = SgmlLinkExtractor._link_allowed(self, link)
        if not allowed:
            return allowed
        path = get_path(link.url)
        yinlian = "d:\yinlian"
        path_join = os.path.join(yinlian, path)
        if os.path.exists(path_join):
            return False
        return True


class YinLianSpider(InitSpider, CrawlSpider):
    name = 'yinlian'
    login_page = 'http://info.gnete.com/names.nsf?Login'
    allowed_domains = ['info.gnete.com']
    start_urls = ['http://info.gnete.com/Merdown.nsf/mer?OpenView']
    #start_urls = ['http://info.gnete.com/MerDown.nsf/$$ViewTemplate+for+Mer?OpenForm=&Start=3321']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).

        Rule(SgmlLinkExtractor(
            allow=[re.compile('/Merdown\.nsf/mer/[A-F0-9]*\?OpenDocument', re.IGNORECASE),
                   re.compile('/Merdown.nsf/mer?OpenView', re.IGNORECASE)]),
             callback='parse_item', follow=True),
        #

        Rule(SgmlLinkExtractor(allow=[
            re.compile(r'/MerDown\.nsf/\$\$ViewTemplate\+for\+Mer\?OpenForm\&Start=[0-3]?[0-9]?[0-9]?[0-9]$',
                       flags=re.IGNORECASE), ]),
             follow=True),
        Rule(DATSgmlLinkExtractor(
            allow=[re.compile(r"/Merdown\.nsf/Mer/[0-9A-F]*/\$FILE/M[_0-9]*\.DAT", flags=re.IGNORECASE), ]),
             follow=False,
             callback='parse_dat'),
    )
    #star "http://info.gnete.com/Merdown.nsf/mer?OpenView"

    def __init__(self, *args, **kwargs):
        #self.login_page = 'http://info.gnete.com/names.nsf?Login'
        #InitSpider.__init__(self, *args, **kwargs)
        self._postinit_reqs = []
        self._init_complete = False
        self._init_started = False
        CrawlSpider.__init__(self, *args, **kwargs)

    def init_request(self):
        """This function is called before crawling starts."""
        return FormRequest(url=self.login_page, formdata={
            "%%ModDate": "0000000000000000",
            "Username": "******",
            "Password": "*******",
            "RedirectTo": "/home.nsf?OpenDatabase",
        }, callback=self.initialized)



        #return Request(url=self.login_page, callback=self.login)

        #def login(self, response):
        #    """Generate a login request."""
        #return FormRequest.from_response(response,
        #                                 formdata={'name': 'herman', 'password': 'password'},
        #                                 callback=self.check_login_response)

        #def check_login_response(self, response):
        #    """Check the response returned by a login request to see if we are
        #    successfully logged in.
        #    """
        #    print response.body
        #    self.initialized()
        #    print 'self.initialized()!!!!!!!!!!!!!!!!'
        #if "Hi Herman" in response.body:
        #    self.log("Successfully logged in. Let's start crawling!")
        #    # Now the crawling can begin..
        #    self.initialized()
        #else:
        #    self.log("Bad times :(")
        # Something went wrong, we couldn't log in, so nothing happens.


    def parse_dat(self, response):
        #self.ensure_login(response, self.parse_dat)
        print 'writing >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        path = get_path(response.url)
        yinlian = "d:\yinlian"
        if not os.path.exists(yinlian):
            os.mkdir(yinlian)
        with open(os.path.join(yinlian, path), 'wb') as f:
            f.write(response.body)


    def parse_item(self, response):
        #ensure_login
        hxs = HtmlXPathSelector(response)
        print 'parse_item!!!!!!!!!!!!!!!!!'
        item = YinlianItem()
        item['date'] = ''.join(hxs.select('/html/body/form/div/font/div/center/table/tbody/tr[2]/td/font[1]').extract())
        match = re.search(re.compile(r"/Merdown\.nsf/Mer/[0-9A-F]*/\$FILE/M[_0-9]*\.DAT", re.IGNORECASE), response.body)
        #if match:
        _url = match and match.group(0)
        item['download_url'] = _url
        #if _url:
        #    yield Request(_url)
        return item

    def ensure_login(self, response, callback):
        if u'ÇëÊäÈëÓÃ»§ÃûºÍ¿ÚÁî' in response.body.decode('gbk'):
            return FormRequest(url=self.login_page, formdata={
                "%%ModDate": "0000000000000000",
                "Username": "xxxxxxxxxxxxx",
                "Password": "xxxxxxxxxxxxxxx",
                "RedirectTo": "/home.nsf?OpenDatabase",
            }, callback=callback)

