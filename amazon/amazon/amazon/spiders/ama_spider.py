from gc import callbacks
import scrapy
from ..items import AmazonItem


class AmaSpiderSpider(scrapy.Spider):
    name = 'ama_spider'
    pg = 2
    start_urls = ['https://www.amazon.in/s?k=book&crid=2II9WNNPC7FO7&sprefix=book%2Caps%2C281&ref=nb_sb_noss_1']

    def product(self, response):
        items = AmazonItem()

        title = response.xpath("//h1[@id='title']/span[@id='productTitle']/text()").get()
        price = response.xpath("//span[@class='a-color-base']/span[@class='a-size-base a-color-price a-color-price']/text()").get()
        image = response.xpath("//div[@id='img-canvas']/img/@src").get()

        items['title'] = title
        items['price'] = price
        items['image'] = image
        yield items


    def parse(self, response):
        link = response.xpath("//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-2']/a/@href").getall()
        
        for l in link:
            links = 'https://www.amazon.in/'+l
            
            yield response.follow(links, callback=self.product)
        next_page = 'https://www.amazon.in/s?k=book&page='+str(AmaSpiderSpider.pg)+'&crid=2II9WNNPC7FO7&qid=1661064636&sprefix=book%2Caps%2C281&ref=sr_pg_'+str(AmaSpiderSpider.pg)
        if AmaSpiderSpider.pg <=20:
            AmaSpiderSpider.pg+=1
            
            yield response.follow(next_page, callback = self.parse)