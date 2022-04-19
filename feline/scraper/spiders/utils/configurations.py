

class Configuration:
    def default_method(self, xpath):
        return self.response.xpath(xpath)

    def set_response(self, response):
        self.response = response

    def __getattr__(self, attr_name):
        if attr_name.startswith("_"):
            attr = getattr(self.__class__, attr_name[1:])
            attr_getter = self.__class__.__dict__.get(f"get{attr_name}")

            if not attr_getter:
                attr_getter = getattr(self.__class__, "default_method")

            return attr_getter(self, attr)


# HIMALAYAS CONFIGURATION
# --------------------------------------------------
class HimalayasConfig(Configuration):
    root_url = "https://himalayas.app/jobs"
    country = "//label/..//label[contains(text(), 'Countries')]/..//span/text()"
    pages_url = "//div[@role='navigation']/div[@id='page-nums']/a/text()"
    valid_job = "//*[@class='badge badge-gray no-hover']//span/@data-badge-value"
    
    job_application_url = "//h3[contains(text(), 'Apply now')]/../..//a/@href"
    job_category = "//label/..//label[contains(text(), 'Job categories')]/..//span/text()"
    job_tags = "//label/..//label[contains(text(), 'Skills')]/.."
    job_cards = "//ul//*[@name='card']"
    job_description = "//*[@class='trix-content']"
    job_title = "//h1/text()"
    job_type = "//label/..//label[contains(text(), 'Job type')]/..//p/text()"
    job_url = "@data-path"

    company_description = "//*[@class='trix-content']"
    company_logo = "//header//header//img/@src"
    company_name = "//h1//span/text()"
    company_url = "//label[contains(text(), 'Primary industry')]/../../..//a/@href"

    def get_company_logo(self, xpath):
        return self.response.xpath(xpath).get()

    def get_pages_url(self, xpath):
        pages_count = self.response.xpath(xpath)[-1].get()

        return [
            f"{self.root_url}?page={page}"
            for page in range(1, int(pages_count) + 1)
        ]


# GETONBRD CONFIGURATION
# --------------------------------------------------
class GetonbrdConfig(Configuration):
    pages_url = "//a[@title]/@href"
    country = "//span[@class='location-flag']/../span[@itemprop]/@text()"
    valid_job = ".//span[@class='location']"
    valid_job_re = "Remote|remote"
        
    job_application_url = "//a[@id='apply_bottom']/@href"
    job_cards = "//ul//a[@data-turbo='false']"
    job_category = "//h2[@class='size1 mb-3 w400 lh2']/text()"
    job_description = "//div[@itemprop='description']"
    job_job_type = "//h2[@class='size1 mb-3 w400 lh2']/text()"
    job_title = "//h1/span/text()"
    job_type = "//h2[@class='size1 mb-3 w400 lh2']/text()"
    job_url = "@href"

    company_description = "//*[@id='about']"
    company_logo = "//span[@class='gb-header-brand__logo border-radius']/@style"
    company_name = "//h2/text()"
    company_url = "//a[@class='gb-company-logo__link']/@href"
    logo_re = "url[(](.*)[)]"

    def get_company_logo(self, xpath):
        return self.response.xpath(xpath).re(self.logo_re)[0]

    def get_valid_job(self, xpath):
        return self.response.xpath(xpath).re(self.valid_job_re)