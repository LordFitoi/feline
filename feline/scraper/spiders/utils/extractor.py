from urllib.parse import urlparse

class Extractor:
    config_class: object
    
    def __init__(self):
        self.config = self.config_class()
        
    # PARSING DATA:
    # --------------------------------------------
    def parse_config(self, response, **kwargs):
        self.config.set_response(response)

        kwargs["country"] = self.config._country.get()
        kwargs["company"] = {
            "logo": self.config._company_logo,
            "name": self.config._company_name.get(),
            "description": self.config._company_description.get()
        }

        return kwargs

    def parse_job(self, response, **kwargs):
        self.config.set_response(response)

        kwargs["jobpost"] = {
            "application_url": self.config._job_application_url.get(),
            "category": self.config._job_category.get(),
            "description": self.config._job_description.get(),
            "job_type": self.config._job_type.get(),
            "title": self.config._job_title.get()
        }

        return response.follow(
            url = self.config._company_url.get(),
            callback = self.parse_config,
            cb_kwargs = kwargs
        )

    def parse_page(self, response, **kwargs):
        self.config.set_response(response)
        
        for job_card in self.config._job_cards:
            self.config.set_response(job_card)

            if not self.config._valid_job:
                continue

            yield response.follow(
                url = self.config._job_url.get(),
                callback = self.parse_job,
                cb_kwargs = kwargs
            )

    def parse(self, response, source):
        self.config.set_response(response)

        for page_href in self.config._pages_url:
            yield response.follow(
                url = page_href,
                callback = self.parse_page,
                cb_kwargs=dict(source=source)
            )