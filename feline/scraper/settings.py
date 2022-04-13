# Scrapy settings for scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from django.conf import settings

BOT_NAME = 'scraper'

SPIDER_MODULES = ['feline.scraper.spiders']
NEWSPIDER_MODULE = 'feline.scraper.spiders'

IMAGES_STORE = settings.MEDIA_ROOT

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scraper (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
   'feline.scraper.pipelines.JobPostPipeline': 300,
}
