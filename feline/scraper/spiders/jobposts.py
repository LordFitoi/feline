import scrapy
from urllib.parse import urlparse


class Extractor:
    def get_pages_url(self):
        return response.xpath(self.pages_url_path).get()

    # COMPANY META:
    # --------------------------------------------
    def get_company_url(self):
        return response.xpath(self.company_url_path).get()
    
    def get_company_name(self):
        return response.xpath(self.company_name_path).get()
    
    def get_company_logo(self):
        return response.xpath(self.company_logo_path).get()
    
    def get_company_description(self):
        return response.xpath(self.company_description_path).get()
    
    def get_company_country(self):
        return response.xpath(self.company_country_path).get()

    # JOBPOST META:
    # --------------------------------------------
    def get_job_url(self, job_card):
        return response.xpath(self.job_url_path).get()

    def get_job_apply_url(self):
        return response.xpath(self.job_apply_url_path).get()

    def get_job_title(self):
        return response.xpath(self.job_title_path).get()

    def get_job_description(self):
        return response.xpath(self.job_description_path).get()

    def get_job_type(self):
        return response.xpath(self.job_type_path).get()

    def get_job_category(self):
        return response.xpath(self.job_category_path).get()

    # PARSING DATA:
    # --------------------------------------------
    def parse_company(self, response, **kwargs):
        kwargs["country"] = self.get_company_country()
        kwargs["company"] = {
            "logo": self.get_company_logo(),
            "name": self.get_company_name(),
            "description": self.get_company_description()
        }

        return kwargs

    def parse_job(self, response, **kwargs):
        kwargs["jobpost"] = {
            "application_url": self.get_job_apply_url(),
            "title": self.get_job_title(),
            "description": self.get_job_description(),
            "job_type": self.get_job_type(),
            "category": self.get_job_category()
        }

        return response.follow(
            url = self.get_company_url(),
            callback = self.parse_company,
            cb_kwargs = kwargs
        )

    def parse_page(self, response):
        for job_card in self.get_job_cards():
            if self.is_invalid_job(job_card):
                continue

            yield response.follow(
                url = self.get_job_url(job_card),
                callback = self.parse_job
            )

    def parse(self, response):
        source = urlparse(response.url).netloc

        for page_href in self.get_pages_url():
            yield response.follow(
                url = page_href,
                callback = self.parse_page,
                cb_kwargs=dict(source=source)
            )

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


class GetonbrdExtractor:
    def parse_company(self, response, **kwargs):
        kwargs["source"] = urlparse(response.url).netloc
        kwargs["country"] = response.xpath("//span[@class='location-flag']/../span[@itemprop]/@text()", re="(\w+)").get()
        kwargs["company"] = {
            "logo": response.xpath("//span[@class='gb-header-brand__logo border-radius']/@style").re("url[(](.*)[)]")[0],
            "name": response.css("h2::text").get(),
            "description": response.xpath("//*[@id='about']").get()
        }

        return kwargs

    def parse_job(self, response):
        meta = response.xpath("//h2[@class='size1 mb-3 w400 lh2']")
        
        # ABOUT ROLE
        job_application_url = response.xpath("//a[@id='apply_bottom']/@href").get()
        job_title = response.xpath("//h1/span/text()").get()
        job_description = response.xpath("//div[@itemprop='description']").get()
        
        job_experience, job_type, job_category = [
            text for value in meta.xpath('text()|*/text()').getall()
            if (text := value.replace("\n", "")) not in ("", "|")
        ]
        
        # ABOUT THE COMPANY
        company_href = response.xpath("//a[@class='gb-company-logo__link']/@href").get()

        jobpost = {
            "application_url": job_application_url,
            "title": job_title,
            "description": job_description,
            "job_type": job_type,
            "category": job_category
        }
        
        return response.follow(
            url = company_href,
            callback = self.parse_company,
            cb_kwargs = dict(jobpost=jobpost)
        )

    def parse_job_list(self, response):
        job_cards = response.xpath("//ul//a[@data-turbo='false']")
        
        for job_card in job_cards:
            job_requirement = job_card.xpath(".//span[@class='location']").re("Remote|remote")

            if not job_requirement: continue

            job_href = job_card.xpath("@href").get()
            yield response.follow(job_href, callback=self.parse_job)

    def parse(self, response):
        job_categories = response.xpath("//a[@title]")

        for job_category in job_categories:
            page_href = job_category.xpath("@href").get()
            yield response.follow(page_href, callback=self.parse_job_list)


class JobPostSpider(scrapy.Spider):
    name = 'jobpost'
    allowed_domains = [
        'himalayas.app',
        'getonbrd.com'
    ]
    start_urls = [
        # 'https://himalayas.app/jobs',
        'https://www.getonbrd.com/jobs'
    ]
    extractors = {
        "himalayas.app": HimalayasExtractor(),
        "www.getonbrd.com": GetonbrdExtractor()
    }

    def parse(self, response):
        domain = urlparse(response.url).netloc
        return self.extractors[domain].parse(response)

   