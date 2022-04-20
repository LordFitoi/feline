# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import requests, hashlib
from itemadapter import ItemAdapter
from django_countries import countries
from django.utils.translation import gettext_lazy as _

from feline.users.models import User
from feline.jobposts.models import Category, Company, JobPost

CATEGORIES_KEYWORDS = {
    "system": "Administradores de Sistemas",
    "backend": "Back End",
    "crypto": "Blockchain y Crypto",
    "mobile": "Desarrollador Mobile",
    "game": "Desarrollador Video Juegos",
    "software": "Desarrollo de Software",
    "devops": "Devops",
    "graphic": "Diseño Grafíco",
    "user experience": "Diseño de Experiencia de Usuario",
    "frontend": "Front End",
    "marketing": "Mercadeo",
    "customer service": "Servicio al Cliente"
}

COMPANY_SIZES = {
    10 : Company.CompanySize.SMALL,
    50 : Company.CompanySize.MEDIUM,
    500 : Company.CompanySize.LARGE,
    2000 : Company.CompanySize.X_LARGE
}

class JobPostPipeline:
    categories = {}

    def get_image(self, image_url, image_name, spider):
        image_store = spider.settings.get("IMAGES_STORE")
        image_hash = hashlib.sha256(image_name.encode())
        image_file = f"{image_hash.hexdigest()}.jpg"
        image_data = requests.get(image_url).content

        with open(f"{image_store}/{image_file}", 'wb') as handler:
            handler.write(image_data)
            return image_file

    def get_category(self, topic):
        topic = topic.lower()
        if category := self.categories.get(topic):
            return category

        for keyword in CATEGORIES_KEYWORDS:
            if keyword in topic:
                category = CATEGORIES_KEYWORDS[keyword]
                self.categories[topic] = category
                break
        else:
            category = "Otros"

        return category

    def get_company_size(self, employees_amount):
        company_size = Company.CompanySize.MICRO

        if not employees_amount:
            return company_size

        for min_employees_amount, value in COMPANY_SIZES.items():
            if employees_amount > min_employees_amount:
                company_size = COMPANY_SIZES[min_employees_amount]
                continue
            break

        return company_size

    def process_item(self, item, spider):
        source = item.get("source")
        jobpost_kwargs = item.get("jobpost")
        company_kwargs = item.get("company")

        if country := item.get("country"):
            country_iso = countries.by_name(_(item.get("country")))
            company_kwargs["country"] = country_iso
            jobpost_kwargs["location"] = country_iso

        # CREATING SCRAPER USER
        # -------------------------------------------------
        user = User.objects.get_or_create(
            username = f"@{source}_scraper")[0]

        # COMPANY PARSING DATA
        # -------------------------------------------------
        company_kwargs["user"] = user
        company_kwargs["company_size"] = self.get_company_size(
            company_kwargs["company_size"])
        
        try:
            company_search_kwargs = company_kwargs.copy()
            company_search_kwargs.pop("logo")

            company = Company.objects.get(**company_search_kwargs)

        except Company.DoesNotExist:
            company_kwargs["logo"] = self.get_image(
                company_kwargs["logo"],
                company_kwargs["name"],
                spider
            )

            company = Company.objects.create(
                source=source, **company_kwargs)

        # JOBPOST PARSING DATA
        # -------------------------------------------------
        jobpost_kwargs["is_remote"] = True
        jobpost_kwargs["company"] = company
        jobpost_kwargs["category"] = Category.objects.get(
            name=self.get_category(jobpost_kwargs["category"]))
        
        try:
            jobpost_search_kwargs = jobpost_kwargs.copy()
            jobpost_search_kwargs.pop("description")

            jobpost = JobPost.objects.get(**jobpost_search_kwargs)

        except JobPost.DoesNotExist:
            jobpost = JobPost.objects.create(
                source=source, **jobpost_kwargs)
        
        return jobpost
