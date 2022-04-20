import re
from datetime import datetime, timezone

class Configuration:
    def default_method(self, xpath):
        return self.response.xpath(xpath)

    def set_response(self, response):
        self.response = response

    def __getattr__(self, attr_name):
        try:
            if attr_name.startswith("_"):
                attr = getattr(self.__class__, attr_name[1:])
                attr_getter = self.__class__.__dict__.get(f"get{attr_name}")

                if not attr_getter:
                    attr_getter = getattr(self.__class__, "default_method")

                return attr_getter(self, attr)
                
        except AttributeError:
            return None

# HIMALAYAS CONFIGURATION
# --------------------------------------------------
class HimalayasConfig(Configuration):
    root_url = "https://himalayas.app/jobs"
    date_format = "%B %d %Y"
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
    job_salary = "//label/..//label[contains(text(), 'Salary range')]/..//p/text()"
    job_created_date = "//label/..//label[contains(text(), 'Job posted')]/..//p/text()"

    company_description = "//*[@class='trix-content']"
    company_logo = "//header//header//img/@src"
    company_name = "//h1//span/text()"
    company_url = "//label[contains(text(), 'Primary industry')]/../../..//a/@href"
    company_website = "//a/span[contains(text(), 'Visit')]/../@href"
    company_size = "//label[contains(text(), 'Company size')]/..//p/text()"

    def get_job_salary(self, xpath):
        data = {}

        if content := self.response.xpath(xpath).get():
            salary_range, data["currency"] = content.split()
            salary_range = salary_range.replace("k", "000").split("-")

            if len(salary_range) == 2: 
                data["salary_range_start_at"] = int(salary_range[0])
                data["salary_range_end_at"] = int(salary_range[1])
            
            else:
                data["salary_range_start_at"] = int(salary_range[0])
    
        return data

    def get_company_logo(self, xpath):
        return self.response.xpath(xpath).get()

    def get_pages_url(self, xpath):
        pages_count = self.response.xpath(xpath)[-1].get()

        return [
            f"{self.root_url}?page={page}"
            for page in range(1, int(pages_count) + 1)
        ]

    def get_job_created_date(self, xpath):
        content = self.response.xpath(xpath).get()
        content = re.sub("th,|rd,|nd,|st,", "", content)
  
        return datetime.strptime(content, self.date_format)

    def get_company_size(self, xpath):
        content = re.sub("[,+]", "", self.response.xpath(xpath).get())
        return int(content.split("-")[0])


# GETONBRD CONFIGURATION
# --------------------------------------------------
class GetonbrdConfig(Configuration):
    pages_url = "//a[@title]/@href"
    country = "//span[@class='location-flag']/../span[@itemprop]/@text()"
    valid_job = ".//span[@class='location']"
    valid_job_re = "Remote|remote"
        
    job_application_url = "//a[@id='apply_bottom']/@href"
    job_cards = "//a[contains(@class, 'gb-results-list__item')]"
    job_category = "//h2[@class='size1 mb-3 w400 lh2']/text()"
    job_description = "//div[@itemprop='description']"
    job_type = "//h2[@class='size1 mb-3 w400 lh2']/text()"
    job_title = "//h1/span/text()"
    job_url = "@href"
    job_created_date = "//time/@datetime"
    job_salary = "//span[contains(text(), 'Salary:')]/../strong/text()"

    company_description = "//div[@id='about']//h3/text()"
    company_logo = "//span[@class='gb-header-brand__logo border-radius']/@style"
    company_name = "//h2/text()"
    company_url = "//a[@class='gb-company-logo__link']/@href"
    company_website = "//a[contains(text(), 'Website')]/@href"
    logo_re = "url[(](.*)[)]"

    def get_company_logo(self, xpath):
        return self.response.xpath(xpath).re(self.logo_re)[0]

    def get_valid_job(self, xpath):
        return self.response.xpath(xpath).re(self.valid_job_re)

    def get_job_salary(self, xpath):
        data = {}
        
        if content := self.response.xpath(xpath).get():
            content = content.replace(" - ", "-")
            content = re.sub("month|[$,/]", "", content)
            salary_range, data["currency"] = content.split()

            if "-" in salary_range:
                salary_start, salary_end = salary_range.split("-")
                data["salary_range_start_at"] = int(salary_start) * 12
                data["salary_range_end_at"] = int(salary_end) * 12

            else:
                data["salary_range_start_at"] = int(salary_range) * 12
            
        return data

    def get_job_created_date(self, xpath):
        return self.response.xpath(xpath).get()
