from enum import Enum
from feline.users.models import User
from django.db.models.fields.related import ForeignKey
from django_countries.fields import CountryField
from django.db import models
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TitleSlugDescriptionModel, TimeStampedModel
from django.urls import reverse

from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


class Category(TimeStampedModel, models.Model):
    name = models.CharField('nombre', max_length=255)
    description = models.TextField('descripción', blank=True, null=True)
    slug = AutoSlugField('slug', populate_from='name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']


class Company(TimeStampedModel, models.Model):
    logo = models.ImageField(blank=True, null=True)
    name = models.CharField('nombre', max_length=255)
    description = models.TextField('descripción', blank=True, null=True)
    slug = AutoSlugField('slug', populate_from='name')
    email = models.EmailField()
    verified = models.BooleanField()
    company_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    lindkedin_url = models.URLField(blank=True)
    country = CountryField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "companies"


class JobPost(TitleSlugDescriptionModel, TimeStampedModel, models.Model):
    class JobType(models.TextChoices):
        PART_TIME = "Part Time"
        FULL_TIME = "Full Time"
        CONTRACT = "Contract"
        INTERNSHIP = "Internship"


    class Status(models.TextChoices):
        NEW = "new"
        APPROVED = "approved"
        DELETED = "deleted"
        EXPIRED = "expired"


    class Currency(models.TextChoices):
        PESOS = "DOP"
        DOLLARS = "USD"
        EUROS = "EUR"

    description = RichTextField()
    company = ForeignKey(Company, on_delete=models.CASCADE)
    # TODO:    Location => Countries + ‘Remote’ (primera option) + Estados Unidos 
    #          + Republica Dominicana
    location = CountryField()
    how_to_apply = RichTextField()

    # TODO: Validation either the application_url or the application_email is fill out
    application_url = models.URLField(blank=True, null=True)
    application_email = models.EmailField(blank=True, null=True)

    status = models.CharField(
      max_length=20,
      choices=Status.choices,
      default=Status.NEW  
    )
    job_type = models.CharField(
      max_length=20,
      choices=JobType.choices
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = TaggableManager()

    currency =  models.CharField(
      max_length=20,
      choices=Currency.choices
    )

    salary_range_start_at =  models.IntegerField(blank=True, null=True)
    salary_range_end_at = models.IntegerField(blank=True, null=True)

    sponsor_relocation = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('jobpost-detail', args=[str(self.slug)])
