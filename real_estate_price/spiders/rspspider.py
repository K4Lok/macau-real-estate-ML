import scrapy
import time

class RealEstatePrice(scrapy.Spider):
    name='rspspider'
    areas = ['黑沙環新填海區', '新口岸區', '筷子基區', '高士德及雅廉訪區', '沙梨頭及大三巴區', '南西灣及主教山區', '林茂塘區', '青洲區', '台山區', '望廈及水塘區', '外港及南灣湖新填海區', '下環區', '黑沙環及祐漢區', '新橋區', '荷蘭園區', '東望洋區(松山區)', '中區','氹仔舊城及馬場區', '北安及大潭山區', '大學及北安灣區', '氹仔中心區', '海洋及小潭山區']
    start_urls=[f'https://mo.centanet.com/Project/Searchs/?areas={areas[0]}']
    base_urls = f'https://mo.centanet.com/'

    def start_requests(self):
        for index, area in enumerate(self.areas):
            urls = f'https://mo.centanet.com/Project/Searchs/?areas={area}'
            yield scrapy.Request(urls, callback=self.parse, priority=-(index + 1) * 10)

    def parse(self, response):
        for estate in response.css('div.c-build-item'):
            raw_specs = estate.css('div.c-build-size::text').extract()
            yield {      
                'name': estate.css('div.c-build-title::text').get().strip(),
                'area': estate.css('div.c-build-area::text').get().strip(),
                'rent_or_sold': estate.css('div.c-build-price div label::text').get(),
                'specs': list(filter(None, list(map(lambda x: x.strip(), raw_specs)))),
                'price_hkd': estate.css('span.total-price::text').extract()[0].replace('HK', "").strip(),
                'price_mop': estate.css('span.total-price::text').extract()[3].strip(),
                'link': response.urljoin(estate.css('div.c-build-item::attr(href)').get())
            }
        
        next_page = response.xpath('//a[contains(text(), "»")]/@href').get()
        
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        
    # products = response.css('div.c-build-list').get()
    # name = products.css('div.c-build-title::text').get().strip()
    # area = products.css('div.c-build-area::text').get().strip()
    # raw_specs = products.css('div.c-build-size::text').extract()
    # specs = list(map(lambda x: x.strip(), raw_specs))
    # prices = products.css('div.c-build-price').get()
    # price_hkd = products.css('span.total-price').extract()[0]
    #  price_mop = products.css('span.total-price').extract()[1]