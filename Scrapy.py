import scrapy
from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
import datetime
import csv

class MySpider(Spider):
    domain_name = 'www.barnesjewish.org'
    name = domain_name.split('.')[1]  # splits the www and org from the domain name
    allowed_domains = [domain_name]
    start_urls = [f'http://{domain_name}/sitemaps', f'https://{domain_name}']
    run_number = 2  # You need to manually increase this each time you run the spider on the same day
    urls = set()  # change list to set to inherently remove duplicates

    def parse(self, response):
        link_extractor = LinkExtractor(allow_domains=self.allowed_domains, deny=[r'login?', r'Register?'])
        for link in link_extractor.extract_links(response):
            self.urls.add(link.url)  # store the url
            yield scrapy.Request(link.url, callback=self.parse)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=scrapy.signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        # spider finished crawling, time to write the data
        filename = f"./Output/{self.name}_{datetime.datetime.now().strftime('%Y%m%d')}_{self.run_number}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            for url in self.urls:  # urls set contains unique urls
                writer.writerow([url])

        spider.logger.info('Spider closed: %s', spider.name)