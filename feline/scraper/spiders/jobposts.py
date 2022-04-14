import scrapy
from urllib.parse import urlparse
from .utils.extractor import Extractor
from .utils.configurations import *

class HimalayasExtractor(Extractor):
    generic_config_class = HimalayasGenericConfig
    company_config_class = HimalayasCompanyConfig
    job_config_class = HimalayasJobConfig
    

class GetonbrdExtractor(Extractor):
    generic_config_class = GetonbrdGenericConfig
    company_config_class = GetonbrdCompanyConfig
    job_config_class = GetonbrdJobConfig

    def is_valid_job(self, job_card):
        self.generic.set_response(job_card)
        return self.generic._valid_job.re(self.generic.valid_job_re)


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

   