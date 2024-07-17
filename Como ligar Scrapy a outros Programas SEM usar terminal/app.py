import scrapy
from scrapy.crawler import CrawlerProcess


class QuotesToScrapeSpider(scrapy.Spider):
    # Identidade
    name = 'quotebot'
    # Request

    def start_requests(self):
        # Definir url(s) a varrer
        urls = ['https://www.goodreads.com/quotes']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    # Response

    def parse(self, response):
        # aqui é onde você deve processar o que é retornado da response
        for elemento in response.xpath("//div[@class='quote']"):
            yield {
                'frase': elemento.xpath(".//div[@class='quoteText']/text()").get(),
                'autor': elemento.xpath(".//span[@class='authorOrTitle']/text()").get(),
                'tags': elemento.xpath(".//div[@class='greyText smallText left']/a/text()").getall()
            }

bot = CrawlerProcess(
    settings={
        "FEEDS": {
            "itens.csv": {"format":"csv"}
        }
    }
)

bot.crawl(QuotesToScrapeSpider)
bot.start()