import scrapy
from urllib.parse import quote
from ..items import ResourceItem

class EdxSpider(scrapy.Spider):
    name = "edx"
    
    def __init__(self, topic=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.topic = topic
        
    def start_requests(self):
        if not self.topic:
            return
        search_url = f"https://www.edx.org/search?q={quote(self.topic)}"
        yield scrapy.Request(url=search_url, callback=self.parse)
    
    def parse(self, response):
        cards = response.css('div.card')
        for card in cards[:10]:
            item = ResourceItem()
            item['title'] = card.css('h3::text').get()
            item['url'] = response.urljoin(card.css('a::attr(href)').get())
            item['source'] = 'edX'
            item['content_type'] = 'course'
            item['topic'] = self.topic
            # edX courses are free to audit
            item['paid'] = False
            item['price'] = 'Free (audit) or paid certificate'
            desc = card.css('p::text').get()
            item['description'] = desc.strip() if desc else ''
            yield item