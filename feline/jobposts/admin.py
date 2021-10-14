from django.contrib import admin

from .models import Category, Company, JobPost

admin.site.register(Category)
admin.site.register(Company)
admin.site.register(JobPost)
