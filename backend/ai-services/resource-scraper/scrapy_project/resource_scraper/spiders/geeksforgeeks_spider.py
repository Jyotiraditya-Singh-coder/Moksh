import scrapy
from urllib.parse import urljoin

class GeeksforGeeksSpider(scrapy.Spider):
    name = "geeksforgeeks"
    allowed_domains = ["geeksforgeeks.org"]
    start_urls = ["https://www.geeksforgeeks.org/data-structures/"]

    def parse(self, response):
        # Extract links to individual articles
        for link in response.css('h2 a::attr(href), h3 a::attr(href)').getall():
            yield scrapy.Request(
                url=urljoin(response.url, link),
                callback=self.parse_article,
                meta={'platform': 'GeeksforGeeks'}
            )
        # Follow pagination (if any)
        next_page = response.css('.next a::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=urljoin(response.url, next_page), callback=self.parse)

    def parse_article(self, response):
        item = ProblemItem()
        item['platform'] = 'GeeksforGeeks'
        item['problem_id'] = response.url.split('/')[-2] if response.url.endswith('/') else response.url.split('/')[-1]
        item['url'] = response.url
        item['title'] = response.css('h1::text').get().strip()
        # Difficulty (often in meta tags or content)
        difficulty = response.css('.difficulty-level::text').get()
        if difficulty:
            item['difficulty'] = difficulty.strip()
        # Tags (categories)
        tags = response.css('.tags a::text').getall()
        item['tags'] = [t.strip() for t in tags]
        # Description
        description = response.css('.entry-content').get()
        item['description'] = description
        # Sample tests (may be inside <pre> tags)
        sample_inputs = []
        sample_outputs = []
        # This is very site-specific; implement if needed
        item['sample_inputs'] = sample_inputs
        item['sample_outputs'] = sample_outputs
        yield item