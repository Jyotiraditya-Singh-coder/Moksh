import scrapy
from urllib.parse import quote
from ..items import ResourceItem

class CourseraSpider(scrapy.Spider):
    name = "coursera"
    
    def __init__(self, topic=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.topic = topic
        
    def start_requests(self):
        if not self.topic:
            return
        search_url = f"https://www.coursera.org/search?query={quote(self.topic)}"
        yield scrapy.Request(url=search_url, callback=self.parse)
    
    def parse(self, response):
        # Extract course cards
        cards = response.css('li.cds-9, li.cds-8')  # Coursera cards
        for card in cards[:10]:  # limit to first 10
            item = ResourceItem()
            item['title'] = card.css('h3::text').get()
            item['url'] = response.urljoin(card.css('a::attr(href)').get())
            item['source'] = 'Coursera'
            item['content_type'] = 'course'
            item['topic'] = self.topic
            # Determine if paid (most Coursera courses are free to audit, but certificates paid)
            # For simplicity, mark as free with optional certificate
            item['paid'] = False
            item['price'] = 'Free (audit) or paid certificate'
            # Description snippet
            desc = card.css('p::text').get()
            item['description'] = desc.strip() if desc else ''
            yield item