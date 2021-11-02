from django import forms
from .models import Company, JobPost
from ckeditor.widgets import CKEditorWidget


class JobPostForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    how_to_apply = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = JobPost
        fields = ['company','title', 'description', 'location', 'how_to_apply', 'application_url', 'application_email', 'job_type', 'category', 'tags', 'currency','salary_range_start_at', 'salary_range_end_at', 'sponsor_relocation']


class CompanyForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Company
        fields = ["name", "tagline", "logo", "company_size",  "description", "email", "company_url", "country"]


class CompanySearchForm(forms.Form):
    keyword = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Busca por nombre de la compañía o palabra clave.'}))


class ContactForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Introduce tu correo'}))
