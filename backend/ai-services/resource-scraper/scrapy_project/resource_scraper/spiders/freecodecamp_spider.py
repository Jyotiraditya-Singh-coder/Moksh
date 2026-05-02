import scrapy
from urllib.parse import quote
from ..items import ResourceItem

class FreeCodeCampSpider(scrapy.Spider):
    name = "freecodecamp"
    
    def __init__(self, topic=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.topic = topic
        
    def start_requests(self):
        if not self.topic:
            return
        search_url = f"https://www.freecodecamp.org/news/search/?query={quote(self.topic)}"
        yield scrapy.Request(url=search_url, callback=self.parse)
    
    def parse(self, response):
        articles = response.css('.post-card')
        for article in articles[:10]:
            item = ResourceItem()
            item['title'] = article.css('h2::text').get()
            item['url'] = response.urljoin(article.css('a::attr(href)').get())
            item['source'] = 'freeCodeCamp'
            item['content_type'] = 'article'
            item['topic'] = self.topic
            item['paid'] = False
            item['price'] = 'Free'
            desc = article.css('p::text').get()
            item['description'] = desc.strip() if desc else ''
            yield item