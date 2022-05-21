import scrapy

class CarsSpider(scrapy.Spider):
    name = 'cars'
    allowed_domains = ['carzz.ro']
    combustionTypes = ['GPL', 'Diesel', "Benzin\u0103", 'Hibrid']
    def start_requests(self):

        url = 'https://carzz.ro/autoturisme.html'
        yield scrapy.Request(url, callback = self.parse)

        for page in range(2, 610):
            url = 'https://carzz.ro/autoturisme_{}.html'.format(page)
            yield scrapy.Request(url, callback = self.parse)

    def parse(self, response):
        for link in response.css('.main_items'):
            yield response.follow(link, self.parse_cars)

    def parse_cars(self, response):
        price = response.xpath('//span[@id="price"]/text()').get()
        manufacturingYear = response.css('div.info_extra_details > span:nth-child(1)::text').get()
        kmOnBoard = response.css('div.info_extra_details > span:nth-child(3)::text').get()
        combustion = response.css('div.info_extra_details > span:nth-child(5)::text').get()
        brand = response.css('#extra-fields > div:nth-child(1) > h2 > a::text').get()

        kmOnBoardInt = int(kmOnBoard.replace(' ', '').replace('km', '').replace(',',''))
        formattedPrice = int(price.replace('.','').replace(' ',''))

        if ((formattedPrice > 1500) and (combustion in self.combustionTypes) and ('Mai' not in manufacturingYear)) :
            yield {
                'price': formattedPrice,
                'manufacturingYear': manufacturingYear,
                'kmOnBoard': kmOnBoardInt,
                'combustion': combustion,
                'url': response.url,
                'brand': brand
            }
        else:
            return