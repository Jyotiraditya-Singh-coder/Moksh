import scrapy
from urllib.parse import quote
from ..items import ResourceItem

class UdemySpider(scrapy.Spider):
    name = "udemy"
    
    def __init__(self, topic=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.topic = topic
        
    def start_requests(self):
        if not self.topic:
            return
        search_url = f"https://www.udemy.com/courses/search/?q={quote(self.topic)}"
        yield scrapy.Request(url=search_url, callback=self.parse)
    
    def parse(self, response):
        cards = response.css('div[data-purpose="course-card"]')
        for card in cards[:10]:
            item = ResourceItem()
            item['title'] = card.css('h3::text').get()
            item['url'] = response.urljoin(card.css('a::attr(href)').get())
            item['source'] = 'Udemy'
            item['content_type'] = 'course'
            item['topic'] = self.topic
            # Check for price element
            price_elem = card.css('span[data-purpose="price"]::text').get()
            if price_elem and 'Free' in price_elem:
                item['paid'] = False
                item['price'] = 'Free'
            else:
                item['paid'] = True
                item['price'] = price_elem if price_elem else 'Paid'
            # Description
            desc = card.css('p::text').get()
            item['description'] = desc.strip() if desc else ''
            yield item