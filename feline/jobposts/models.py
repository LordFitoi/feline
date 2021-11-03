from enum import Enum
from feline.users.models import User

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.fields.related import ForeignKey

from django_countries.fields import CountryField
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TitleSlugDescriptionModel, TimeStampedModel
from django.urls import reverse


from ckeditor.fields import RichTextField
from hitcount.conf import settings as hitcount_settings
from hitcount.mixins import HitCountModelMixin
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
    class CompanySize(models.TextChoices):
        MICRO = "Menos de 10"
        SMALL = "10-50 Empleados"
        MEDIUM = "50-500 Empleados"
        LARGE = "500-2000 Empleados"
        X_LARGE = "+2000 Empleados"

    description = RichTextField('descripción')
    logo = models.ImageField("Logo de la Compañía", blank=True, null=True)
    tagline = models.CharField("Slogan de la compañía", max_length=350, blank=True, null=True)
    name = models.CharField('Nombre de la Compañía', max_length=255)
    slug = AutoSlugField('slug', populate_from='name')
    email = models.EmailField()
    verified = models.BooleanField(blank=True, null=True)
    company_url = models.URLField("Pagina de la Compañía", blank=True)
    country = CountryField("País")
    company_size = models.CharField("Tamaño de la compañía",
      max_length=20,
      choices=CompanySize.choices,
      default=CompanySize.MICRO  
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # count views of the page
    hit_count_generic = GenericRelation(
        hitcount_settings.HITCOUNT_HITCOUNT_MODEL,
        object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "companies"

    def get_total_jobs(self) -> str:
        jobposts_count = self.jobpost_set.count()
        if jobposts_count == 1:
            return "1 Trabajo disponible"
        return f"{jobposts_count} Trabajos disponibles"

    def get_absolute_url(self) -> str:
        return reverse('company-detail', args=[str(self.slug)])


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
      choices=Currency.choices,
      blank=True,
      null=True
    )

    salary_range_start_at =  models.IntegerField(blank=True, null=True)
    salary_range_end_at = models.IntegerField(blank=True, null=True)

    sponsor_relocation = models.BooleanField(default=False)
    is_remote = models.BooleanField(default=False)

    # count views on the page
    hit_count_generic = GenericRelation(
        hitcount_settings.HITCOUNT_HITCOUNT_MODEL,
        object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )

    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        return self.title

    def has_application_url(self) -> bool:
        return any([self.application_email, self.application_url, self.company.company_url])

    def get_application_url(self) -> str:
        if self.application_url:
            return self.application_url
        if self.application_email:
            return f"mailto:{self.application_email}"

        return  self.company.company_url

    def get_salary_range(self) -> str:
        if self.salary_range_start_at and self.salary_range_end_at and self.currency:
            return f"{self.salary_range_start_at:>15,.2f}-{self.salary_range_end_at:>15,.2f} {self.currency}"
        elif self.salary_range_start_at:
            return f"desde  {self.salary_range_start_at:>15,.2f} {self.currency}"
        elif self.salary_range_end_at:
            return f"hasta {self.salary_range_end_at:>15,.2f} {self.currency}"

        return "No disponible"

    def get_absolute_url(self) -> str:
        return reverse('jobpost-detail', args=[str(self.slug)])
