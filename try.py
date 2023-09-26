import scrapy
from scrapy.crawler import CrawlerProcess

# Request the URL https://conjugador.reverso.net/conjugacion-espanol-verbo-tener.html and store the response in the variable response using scrapy
class SpanishVerbSpider(scrapy.Spider):
    name = "spanish_verb_spider"
    start_urls = ["https://conjugador.reverso.net/conjugacion-espanol-verbo-tener.html"]
    
    def parse(self, response):
        # Extract the list of conjugations from the response
        conjugations = response.css("div.wrap-verbs-tables > table > tbody > tr > td > a::text").getall()
        
        # Yield the conjugations
        yield conjugations
        
# Instantiate the CrawlerProcess object
process = CrawlerProcess()

# Tell the process which spider to use
process.crawl(SpanishVerbSpider)

