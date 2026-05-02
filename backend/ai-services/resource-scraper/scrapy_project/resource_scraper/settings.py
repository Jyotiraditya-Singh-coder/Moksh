BOT_NAME = "resource_scraper"

SPIDER_MODULES = ["resource_scraper.spiders"]
NEWSPIDER_MODULE = "resource_scraper.spiders"

# Obey robots.txt
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 8
DOWNLOAD_DELAY = 1.0
RANDOMIZE_DOWNLOAD_DELAY = True

# Disable cookies
COOKIES_ENABLED = False

# Enable and configure pipelines
ITEM_PIPELINES = {
    "resource_scraper.pipelines.ProblemPipeline": 300,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"