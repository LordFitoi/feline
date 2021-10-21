import factory
from factory import Faker, post_generation
from faker import Factory as FakerFactory
from factory.django import DjangoModelFactory
from feline.jobposts.models import Company


class CompanyFactory(DjangoModelFactory):
    description =  Faker("sentence")
    logo = Faker("file_name")
    name = Faker("name")
    email = Faker("email")
    verified = False
    company_url = Faker("hostname")
    country = factory.LazyAttribute(lambda n: FakerFactory.create().sentence()[:2])
    

    class Meta:
        model = Company