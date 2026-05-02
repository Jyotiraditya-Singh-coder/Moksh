import scrapy
from urllib.parse import urljoin
from ..items import ProblemItem
import re

class CodeforcesSpider(scrapy.Spider):
    name = "codeforces"
    allowed_domains = ["codeforces.com"]
    start_urls = ["https://codeforces.com/problemset"]

    def parse(self, response):
        # Extract problem links from the problemset page
        for row in response.css('tr[data-problemid]'):
            link = row.css('td:nth-child(2) a::attr(href)').get()
            if link:
                yield scrapy.Request(
                    url=urljoin(response.url, link),
                    callback=self.parse_problem,
                    meta={'platform': 'Codeforces'}
                )
        # Follow pagination
        next_page = response.css('.pagination .arrow a::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=urljoin(response.url, next_page), callback=self.parse)

    def parse_problem(self, response):
        item = ProblemItem()
        item['platform'] = 'Codeforces'
        # Extract problem ID (e.g., "1A")
        item['problem_id'] = response.url.split('/')[-2] + '/' + response.url.split('/')[-1]
        item['url'] = response.url
        item['title'] = response.css('.title::text').get().strip()
        # Difficulty (rating)
        rating = response.css('.tag-box[title*="difficulty"]::text').get()
        if rating:
            item['difficulty'] = rating.strip()
        # Tags
        tags = response.css('.tag-box:not([title*="difficulty"]) a::text').getall()
        item['tags'] = [t.strip() for t in tags]
        # Description (may contain multiple sections)
        description = response.css('.problem-statement').get()
        item['description'] = description
        # Input/Output format
        input_spec = response.xpath('//div[contains(@class,"input-specification")]/p/text()').getall()
        output_spec = response.xpath('//div[contains(@class,"output-specification")]/p/text()').getall()
        item['input_format'] = ' '.join(input_spec).strip()
        item['output_format'] = ' '.join(output_spec).strip()
        # Constraints (usually inside the problem statement, may need custom extraction)
        # Sample tests
        samples = response.css('.sample-test')
        sample_inputs = []
        sample_outputs = []
        for sample in samples:
            inp = sample.css('.input pre::text').get()
            out = sample.css('.output pre::text').get()
            if inp:
                sample_inputs.append(inp.strip())
            if out:
                sample_outputs.append(out.strip())
        item['sample_inputs'] = sample_inputs
        item['sample_outputs'] = sample_outputs
        # Time and memory limits
        time_limit = response.xpath('//div[contains(@class,"time-limit")]/text()').get()
        memory_limit = response.xpath('//div[contains(@class,"memory-limit")]/text()').get()
        if time_limit:
            item['time_limit'] = time_limit.strip()
        if memory_limit:
            item['memory_limit'] = memory_limit.strip()
        yield item