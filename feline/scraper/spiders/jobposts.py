import scrapy
from urllib.parse import urlparse


class Extractor:
    job_attrs = [
        "application_url",
        "title",
        "description",
        "job_type",
        "category"
    ]
    company_attrs = [
        "logo",
        "name",
        "description"
    ]

    # PARSING DATA:
    # --------------------------------------------
    def get_attr(self, response, attr_name, *args, **kwargs):
        extract_method = getattr(self, f"get_{attr_name}", None)
        
        if callable(extract_method):
            return extract_method(response, *args, **kwargs)
        
        instance_attr = getattr(self, f"{attr_name}_path")
        attr_data = response.xpath(instance_attr)

        if not kwargs.get("raw"):
            attr_data = attr_data.get() if not kwargs.get("many") else attr_data.getall()

        return attr_data

    def is_valid_job(self, job_card):
        return job_card.xpath(self.valid_job_path).get()

    def parse_company(self, response, **kwargs):
        kwargs["country"] = self.get_attr(response, "country")
        kwargs["company"] = {
            attr_name: self.get_attr(response, f"company_{attr_name}")
            for attr_name in self.company_attrs
        }

        return kwargs

    def parse_job(self, response, **kwargs):
        kwargs["jobpost"] = {
            attr_name: self.get_attr(response, f"job_{attr_name.replace('job_', '')}")
            for attr_name in self.job_attrs
        }

        return response.follow(
            url = self.get_attr(response, "company_url"),
            callback = self.parse_company,
            cb_kwargs = kwargs
        )

    def parse_page(self, response, **kwargs):
        for job_card in self.get_attr(response, "job_cards", raw=True):
            if not self.is_valid_job(job_card):
                continue

            yield response.follow(
                url = self.get_attr(job_card, "job_url"),
                callback = self.parse_job,
                cb_kwargs = kwargs
            )

    def parse(self, response, source):
        for page_href in self.get_attr(response, "pages_url", many=True):
            yield response.follow(
                url = page_href,
                callback = self.parse_page,
                cb_kwargs=dict(source=source)
            )


class HimalayasExtractor(Extractor):
    root_url = "https://himalayas.app/jobs"
    pages_url_path = "//div[@role='navigation']/div[@id='page-nums']/a/text()"
    valid_job_path = "//*[@class='badge badge-gray no-hover']//span/@data-badge-value"
    country_path = "//label/..//label[contains(text(), 'Countries')]/..//span/text()"

    job_cards_path = "//ul//*[@name='card']"
    job_url_path = "@data-path"
    job_application_url_path = "//h3[contains(text(), 'Apply now')]/../..//a/@href"
    job_title_path = "//h1/text()"
    job_description_path = "//*[@class='trix-content']"
    job_type_path = "//label/..//label[contains(text(), 'Job type')]/..//p/text()"
    job_category_path = "//label/..//label[contains(text(), 'Job categories')]/..//span/text()"
    #job_tags_path = "//label/..//label[contains(text(), 'Skills')]/.."
    
    company_url_path = "//label[contains(text(), 'Primary industry')]/../../..//a/@href"
    company_logo_path = "//header//header//img/@src"
    company_name_path = "//h1//span/text()"
    company_description_path = "//*[@class='trix-content']"

    def get_pages_url(self, response, *args, **kwargs):
        pages_count = response.xpath(self.pages_url_path)[-1].get()
        return [
            f"{self.root_url}?page={page}"
            for page in range(1, int(pages_count) + 1)
        ]


class GetonbrdExtractor(Extractor):
    pages_url_path = "//a[@title]/@href"
    valid_job_path = ".//span[@class='location']"
    valid_job_re = "Remote|remote"
    
    country_path = "//span[@class='location-flag']/../span[@itemprop]/@text()"

    job_cards_path = "//ul//a[@data-turbo='false']"
    job_url_path = "@href"
    job_application_url_path = "//a[@id='apply_bottom']/@href"
    job_title_path = "//h1/span/text()"
    job_description_path = "//div[@itemprop='description']"
    job_type_path = "//h2[@class='size1 mb-3 w400 lh2']/text()"
    job_category_path = "//h2[@class='size1 mb-3 w400 lh2']/text()"
    
    company_url_path = "//a[@class='gb-company-logo__link']/@href"
    company_name_path = "//h2/text()"
    company_description_path = "//*[@id='about']"
    company_logo_path = "//span[@class='gb-header-brand__logo border-radius']/@style"
    company_logo_re = "url[(](.*)[)]"

    def is_valid_job(self, job_card):
        return job_card.xpath(self.valid_job_path).re(self.valid_job_re)
  
    def get_company_logo(self, response, *args, **kwargs):
        return response.xpath(self.company_logo_path).re(self.company_logo_re)[0]


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

   