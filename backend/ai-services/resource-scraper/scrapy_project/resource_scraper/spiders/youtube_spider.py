import scrapy
from urllib.parse import quote
from ..items import ResourceItem

class YoutubeSpider(scrapy.Spider):
    name = "youtube"
    
    def __init__(self, topic=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.topic = topic
        
    def start_requests(self):
        if not self.topic:
            return
        search_url = f"https://www.youtube.com/results?search_query={quote(self.topic)}"
        yield scrapy.Request(url=search_url, callback=self.parse)
    
    def parse(self, response):
        # YouTube uses JavaScript; we might need to use YouTube Data API, but for scraping we'll rely on simple extraction
        # This is a simplified version; real scraping would need to parse video IDs from the page.
        # For demo, we'll return a placeholder.
        # In production, consider using YouTube Data API (free tier).
        item = ResourceItem()
        item['title'] = f"YouTube videos on {self.topic}"
        item['url'] = f"https://www.youtube.com/results?search_query={quote(self.topic)}"
        item['source'] = 'YouTube'
        item['content_type'] = 'video'
        item['topic'] = self.topic
        item['paid'] = False
        item['price'] = 'Free'
        item['description'] = f"Search YouTube for {self.topic} tutorials."
        yield item