from gc import callbacks
import scrapy

class SoldEstatePrice(scrapy.Spider):
    name = 'soldspider'
    start_urls = ['https://mo.centanet.com/Transaction']
    stop_on_year = '2009'

    def parse(self, response):
        for estate in response.css('tr.data-tr'):
            region = estate.css('td:nth-child(1) div::text').get()
            area = estate.css('td:nth-child(2) div::text').get()
            usage = estate.css('td:nth-child(3) div::text').get()
            building_name = estate.css('td:nth-child(4) div::text').get()
            unit = estate.css('td:nth-child(5) div::text').get()
            scaleable_area = estate.css('td:nth-child(6) div::text').get()
            rent_or_sell = estate.css('td:nth-child(7) div::text').get()
            price = estate.css('td:nth-child(8) div::text').get()
            price_per_inch = estate.css('td:nth-child(9) div::text').get()
            transaction_year_month = estate.css('td:nth-child(11) div::text').get()
            
            if self.stop_on_year in transaction_year_month:
                return

            yield {
                'region': region,
                'area': area,
                'usage': usage,
                'building_name': building_name,
                'unit': unit,
                'scaleable_area': scaleable_area,
                'rent_or_sell': rent_or_sell,
                'price': price.strip(),
                'price_per_inch': price_per_inch,
                'transaction_year_month': transaction_year_month.strip()
            }
        
        # next_page = response.css('ul.pagination li:nth-child(8) a::attr(href)').get()
        next_page = response.xpath('//a[contains(text(), "»")]/@href').get()

        if next_page is not None:
            yield response.follow(response.urljoin(next_page), callback=self.parse)
            # yield scrapy.Request(response.urljoin(next_page), callbacks=self.parse)