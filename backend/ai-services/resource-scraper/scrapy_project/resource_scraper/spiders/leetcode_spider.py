import scrapy
import json
from urllib.parse import urljoin

class LeetcodeSpider(scrapy.Spider):
    name = "leetcode"
    allowed_domains = ["leetcode.com"]
    start_urls = ["https://leetcode.com/api/problems/all/"]  # GraphQL endpoint would be better, but this API exists

    def parse(self, response):
        data = json.loads(response.text)
        for problem in data['stat_status_pairs']:
            stat = problem['stat']
            title_slug = stat['question__title_slug']
            problem_url = f"https://leetcode.com/problems/{title_slug}/"
            yield scrapy.Request(
                url=problem_url,
                callback=self.parse_problem,
                meta={
                    'platform': 'LeetCode',
                    'problem_id': stat['question_id'],
                    'title': stat['question__title'],
                    'difficulty': problem['difficulty']['level']
                }
            )

    def parse_problem(self, response):
        item = ProblemItem()
        item['platform'] = 'LeetCode'
        item['problem_id'] = response.meta['problem_id']
        item['url'] = response.url
        item['title'] = response.meta['title']
        # Difficulty mapping
        diff_map = {1: 'Easy', 2: 'Medium', 3: 'Hard'}
        item['difficulty'] = diff_map.get(response.meta['difficulty'], 'Unknown')
        # Tags are hidden in script; we can extract from page source
        script = response.xpath('//script[contains(text(), "pageData")]/text()').get()
        if script:
            # Very rough extraction; better to use GraphQL in production
            pass
        # Description
        description = response.css('.content__u3I1').get()
        item['description'] = description
        # Sample tests (not easily extracted without JS execution)
        # We'll leave these empty for now
        item['sample_inputs'] = []
        item['sample_outputs'] = []
        yield item