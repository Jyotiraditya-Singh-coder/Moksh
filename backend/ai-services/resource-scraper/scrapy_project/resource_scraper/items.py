import scrapy

class ProblemItem(scrapy.Item):
    """Represents a DSA problem scraped from any platform."""
    platform = scrapy.Field()          # e.g., "Codeforces", "LeetCode", "GeeksforGeeks"
    problem_id = scrapy.Field()         # original ID on the platform
    title = scrapy.Field()
    url = scrapy.Field()
    difficulty = scrapy.Field()          # e.g., "Easy", "Medium", "Hard", rating
    tags = scrapy.Field()                # list of topic tags
    description = scrapy.Field()         # full problem statement (HTML or text)
    input_format = scrapy.Field()        # optional
    output_format = scrapy.Field()       # optional
    constraints = scrapy.Field()         # optional
    sample_inputs = scrapy.Field()       # list of strings
    sample_outputs = scrapy.Field()      # list of strings
    time_limit = scrapy.Field()          # e.g., "2 seconds"
    memory_limit = scrapy.Field()        # e.g., "256 MB"
    editorial_url = scrapy.Field()       # optional link to solution
    scraped_at = scrapy.Field()          # timestamp