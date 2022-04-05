import scrapy


class HimalayasSpider(scrapy.Spider):
    name = 'himalayas'
    allowed_domains = ['himalayas.app']
    start_urls = ['https://himalayas.app/jobs']

    def parse_job(self, response):
        meta = response.xpath("//label/..")

        # ABOUT THIS ROLE
        job_type = meta.xpath("//label[contains(text(), 'Job type')]/..")
        job_categories = meta.xpath("//label[contains(text(), 'Job categories')]/..")[0]
        job_tags = meta.xpath("//label[contains(text(), 'Skills')]/..")[0]
        
        # ABOUT THE COMPANY
        company_meta = meta.xpath("//label[contains(text(), 'Primary industry')]/../../..//a")

        yield {
            "title": response.css("h1::text").get(),
            "description": response.css(".trix-content").get(),
            "job_type": job_type.css("p::text").get(),
            "categories": job_categories.css("span::text").getall(),
            "tags": job_tags.css("span::text").getall(),
            "company": {
                "name": company_meta.css("h3::text").get(),
                "url": company_meta.xpath("@href").get()
            }
        }

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
            page_href = f"{self.start_urls[0]}?page={page}"
            yield response.follow(page_href, callback=self.parse_job_list)
        