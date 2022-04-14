from urllib.parse import urlparse
from .configurations import Configuration

class Extractor:
    generic_config_class: object
    job_config_class: object
    company_config_class: object
    
    def __init__(self):
        self.generic = self.generic_config_class()
        self.company = self.company_config_class()
        self.job = self.job_config_class()
        
    # PARSING DATA:
    # --------------------------------------------
    def is_valid_job(self, job_card):
        self.generic.set_response(job_card)
        return self.generic._valid_job.get()

    def parse_company(self, response, **kwargs):
        self.generic.set_response(response)
        self.company.set_response(response)

        kwargs["country"] = self.generic._country.get()
        kwargs["company"] = {
            "logo": self.company._logo,
            "name": self.company._name.get(),
            "description": self.company._description.get()
        }

        return kwargs

    def parse_job(self, response, **kwargs):
        self.job.set_response(response)

        kwargs["jobpost"] = {
            "application_url": self.job._application_url.get(),
            "category": self.job._category.get(),
            "description": self.job._description.get(),
            "job_type": self.job._job_type.get(),
            "title": self.job._title.get()
        }

        self.company.set_response(response)

        return response.follow(
            url = self.company._url.get(),
            callback = self.parse_company,
            cb_kwargs = kwargs
        )

    def parse_page(self, response, **kwargs):
        self.job.set_response(response)
        
        for job_card in self.job._cards:
            if not self.is_valid_job(job_card):
                continue

            self.job.set_response(job_card)

            yield response.follow(
                url = self.job._url.get(),
                callback = self.parse_job,
                cb_kwargs = kwargs
            )

    def parse(self, response, source):
        self.generic.set_response(response)

        for page_href in self.generic._pages_url:
            yield response.follow(
                url = page_href,
                callback = self.parse_page,
                cb_kwargs=dict(source=source)
            )

