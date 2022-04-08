import scrapy
from urllib.parse import urlparse


class HimalayasExtractor:
    source_name = "himalayas.app"
    url = "https://himalayas.app/jobs"

    def parse_company(self, response, **kwargs):
        meta = response.xpath("//label/..")
        country = meta.xpath("//label[contains(text(), 'Countries')]/..")
        
        kwargs["source"] = urlparse(response.url).netloc
        kwargs["country"] = country.css("span::text").get()

        kwargs["company"] = {
            "logo": response.xpath("//header//header//img/@src").get(),
            "name": response.css("h1 span::text").get(),
            "description": response.css(".trix-content").get()
        }

        return kwargs

    def parse_job(self, response):
        meta = response.xpath("//label/..")
        apply_now = response.xpath("//h3[contains(text(), 'Apply now')]/../..")

        # ABOUT THIS ROLE
        job_type = meta.xpath("//label[contains(text(), 'Job type')]/..")
        job_categories = meta.xpath("//label[contains(text(), 'Job categories')]/..")[0]
        job_tags = meta.xpath("//label[contains(text(), 'Skills')]/..")[0]
        
        # ABOUT THE COMPANY
        company_href = meta.xpath("//label[contains(text(), 'Primary industry')]/../../..//a/@href").get()

        jobpost = {
            "application_url": apply_now.css('a').xpath('@href').get(),
            "title": response.css("h1::text").get(),
            "description": response.css(".trix-content").get(),
            "job_type": job_type.css("p::text").get(),
            "category": job_categories.css("span::text").get()
        }

        return response.follow(
            url = company_href,
            callback = self.parse_company,
            cb_kwargs = dict(jobpost=jobpost)
        )

    def parse_job_list(self, response):
        job_cards = response.css("ul div.cursor-pointer")

        for job_card in job_cards:
            job_requirement = job_card.css(".badge.badge-gray.no-hover")

            if job_requirement.xpath("//span/@data-badge-value").get():
                continue

            job_href = job_card.xpath("@data-path").get()
            yield response.follow(job_href, callback=self.parse_job)

    def parse(self, response):
        pages_number = response.xpath("//div[@role='navigation']/div[@id='page-nums']/a/text()")[-1].get()

        for page in range(1, int(pages_number) + 1):
            page_href = f"{self.url}?page={page}"
            yield response.follow(page_href, callback=self.parse_job_list)
            

class JobPostSpider(scrapy.Spider):
    name = 'jobpost'
    allowed_domains = ['himalayas.app']
    start_urls = ['https://himalayas.app/jobs']
    extractors = {
        "himalayas.app": HimalayasExtractor()
    }

    def parse(self, response):
        domain = urlparse(response.url).netloc
        return self.extractors[domain].parse(response)

   