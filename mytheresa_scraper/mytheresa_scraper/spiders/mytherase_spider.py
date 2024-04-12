import scrapy

class MytheresaSpider(scrapy.Spider):
    name = 'mytheresa_spider'
    allowed_domains = ['mytheresa.com']
    start_urls = ['https://www.mytheresa.com/int_en/men/shoes.html',
                  'https://www.mytheresa.com/int/en/men/bags',
                  'https://www.mytheresa.com/int/en/men/clothing/shirts/casual-shirts'
                  ''
                  ]

    def parse(self, response):
        # Extract product URLs and iterate over them
        for product in response.css('div.item__info a::attr(href)').extract():
            yield response.follow(product, self.parse_product)

        # Find and follow pagination links
       

    def parse_product(self, response):
        # Extract product details
        yield {
            'name': response.css('div.item__info__header__designer::text').get(),
            'price': response.css('span.pricing__prices__price::text').getall(),
            'link': response.css('a.item__link').attrib['href']        # Add other fields as needed
        }

        next_page_url = response.css('a.next-page::attr(href)').get()
        if next_page_url:
            # Create request for next page
            yield scrapy.Request(url=next_page_url, callback=self.parse_next_page)

    def parse_next_page(self, response):
        # Extract data from next page
        for product in response.css('div.item'):
            yield {
                'name': response.css('div.item__info__header__designer::text').get(),
                'price': response.css('span.pricing__prices__price::text').getall(),
                'link': response.css('a.item__link').attrib['href']
                
            }

        # Extract URL of next page (if exists) and repeat process
        next_page_url = response.css('a.next-page::attr(href)').get()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse_next_page)

