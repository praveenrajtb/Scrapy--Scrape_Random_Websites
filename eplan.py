# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request, FormRequest

class EplanSpider(Spider):
    name = 'eplan'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://eplanning.ie/']

    # page 1 http://eplanning.ie/
    def parse(self, response):

        # Scrape all the urls , if the url is '#' pass, else produce request
        urls = response.xpath('//a/@href').extract()
        for url in urls:
            if '#' == url:
                pass
            else:
                yield Request(url, callback=self.parse_application)

    # page 2 http://www.eplanning.ie/CarlowCC/searchtypes            
    def parse_application(self, response):

        # url for 'Received Applications' and complete the url with urljoin, request with url
        app_url = response.urljoin(response.xpath('//*[contains(@class, "glyphicon glyphicon-inbox btn-lg")]/following-sibling::a/@href').extract_first())
        yield Request(app_url, callback=self.parse_form)

    # page 3 http://www.eplanning.ie/CarlowCC/SearchListing/RECEIVED
    # Click Radio button corresponds to 42 and pass that info along with the next url request
    def parse_form(self, response):
        yield FormRequest.from_response(response,
                                        formdata={'RdoTimeLimit': '42'},
                                        dont_filter = True,
                                        formxpath='(//form)[2]',
                                        callback=self.parse_pages)

    #  page 4 'http://www.eplanning.ie/CarlowCC/searchresults'     
    def parse_pages(self, response):

        # Extract all the url in Page Number : 1, Request with each url
        application_urls = response.xpath('//td/a/@href').extract()
        for url in application_urls:
            url = response.urljoin(url)
            yield Request(url, callback=self.parse_items)

        # Find the url for pages from 2 to last page. Request back to parse_pages with each page request    
        next_page_url = response.xpath('//*[@rel="next"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(absolute_next_page_url, callback=self.parse_pages)

    # page 5 http://www.eplanning.ie/CarlowCC/AppFileRefDetails/1910/0
    def parse_items(self,response):

        # FInd the agent button , if the agent button is visible extract the datas else log message Agent button ot found
        agent_btn = response.xpath('//*[@value="Agents"]/@style').extract_first()
        if 'display: inline;  visibility: visible;' in agent_btn:
            name = response.xpath('//tr[th="Name :"]/td/text()').extract_first()
            address_first = response.xpath('//tr[th="Address :"]/td/text()').extract()
            address_second = response.xpath('//tr[th="Address :"]/following::td/text()').extract()[0:3]
            address = address_first + address_second
            phone = response.xpath('//tr[th="Phone :"]/td/text()').extract_first()
            fax = response.xpath('//tr[th="Fax :"]/td/text()').extract_first()
            email = response.xpath('//tr[th="e-mail :"]/td/a/text()').extract()
            url = response.url
            yield {'name' : name,
                    'address' : address,
                    'address' : address,
                    'phone' : phone,
                    'fax' : fax,
                    'email' : email,
                    'url' : url
            }

        else:
            self.logger.info('Agent button not found in the page, passing invalid url')
