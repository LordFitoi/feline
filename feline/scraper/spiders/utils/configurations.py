

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
class HimalayasGenericConfig(Configuration):
    root_url = "https://himalayas.app/jobs"
    country = "//label/..//label[contains(text(), 'Countries')]/..//span/text()"
    pages_url = "//div[@role='navigation']/div[@id='page-nums']/a/text()"
    valid_job = "//*[@class='badge badge-gray no-hover']//span/@data-badge-value"
    
    def get_pages_url(self, xpath):
        pages_count = self.response.xpath(xpath)[-1].get()

        return [
            f"{self.root_url}?page={page}"
            for page in range(1, int(pages_count) + 1)
        ]


class HimalayasJobConfig(Configuration):
    application_url = "//h3[contains(text(), 'Apply now')]/../..//a/@href"
    cards = "//ul//*[@name='card']"
    category = "//label/..//label[contains(text(), 'Job categories')]/..//span/text()"
    description = "//*[@class='trix-content']"
    tags = "//label/..//label[contains(text(), 'Skills')]/.."
    title = "//h1/text()"
    job_type = "//label/..//label[contains(text(), 'Job type')]/..//p/text()"
    url = "@data-path"


class HimalayasCompanyConfig(Configuration):
    description = "//*[@class='trix-content']"
    logo = "//header//header//img/@src"
    name = "//h1//span/text()"
    url = "//label[contains(text(), 'Primary industry')]/../../..//a/@href"

    def get_logo(self, xpath):
        return self.response.xpath(xpath).get()

# GETONBRD CONFIGURATION
# --------------------------------------------------
class GetonbrdGenericConfig(Configuration):
    pages_url = "//a[@title]/@href"
    country = "//span[@class='location-flag']/../span[@itemprop]/@text()"
    valid_job = ".//span[@class='location']"
    valid_job_re = "Remote|remote"
        

class GetonbrdJobConfig(Configuration):
    cards = "//ul//a[@data-turbo='false']"
    url = "@href"
    application_url = "//a[@id='apply_bottom']/@href"
    title = "//h1/span/text()"
    description = "//div[@itemprop='description']"
    job_type = "//h2[@class='size1 mb-3 w400 lh2']/text()"
    category = "//h2[@class='size1 mb-3 w400 lh2']/text()"


class GetonbrdCompanyConfig(Configuration):
    url = "//a[@class='gb-company-logo__link']/@href"
    name = "//h2/text()"
    description = "//*[@id='about']"
    logo = "//span[@class='gb-header-brand__logo border-radius']/@style"
    logo_re = "url[(](.*)[)]"

    def get_logo(self, xpath):
        return self.response.xpath(xpath).re(self.logo_re)[0]