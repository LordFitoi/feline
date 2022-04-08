from django.core.management.base import BaseCommand
from scraper.spiders.jobposts import JobPostSpider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scraper import settings

class Command(BaseCommand):
    help = "Extract job posts info from different pages"

    def handle(self, *args, **options):
        process_settings = Settings()
        process_settings.setmodule(settings)
        process = CrawlerProcess(settings=process_settings)

        process.crawl(JobPostSpider)
        process.start()