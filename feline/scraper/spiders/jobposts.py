import scrapy
from urllib.parse import urlparse
from .utils.extractor import Extractor
from .utils.configurations import HimalayasConfig, GetonbrdConfig

class HimalayasExtractor(Extractor):
    config_class = HimalayasConfig
    

class GetonbrdExtractor(Extractor):
    config_class = GetonbrdConfig


class JobPostSpider(scrapy.Spider):
    name = 'jobpost'
    allowed_domains = [
        'himalayas.app',
        'getonbrd.com'
    ]
    start_urls = [
        'https://himalayas.app/jobs',
        'https://www.getonbrd.com/jobs'
    ]
    extractors = {
        "himalayas.app": HimalayasExtractor(),
        "getonbrd.com": GetonbrdExtractor()
    }

    def parse(self, response):
        source = urlparse(response.url).netloc.replace("www.", "")
        return self.extractors[source].parse(response, source)

   