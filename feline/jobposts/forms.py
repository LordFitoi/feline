from django import forms
from .models import Category, Company, JobPost
from ckeditor.widgets import CKEditorWidget

JOB_CATEGORIES_CHOICES = [('--', 'Categoria')] + [(category.name, category.name) for category in Category.objects.all()]


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


class JobPostSearchForm(forms.Form):
    keyword = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Busca por titulo, descripción, carrera.'}))
    category = forms.ChoiceField(
        required=False,
        choices=JOB_CATEGORIES_CHOICES
    )

    def __init__(self, *args, **kwargs):
        super(JobPostSearchForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name == "category":
                visible.field.widget.attrs['class'] = 'category-field w-full mb-4 sm:ml-4 sm:w-52'

            if visible.name == 'keyword':
                visible.field.widget.attrs['class'] = 'keyword'


class ContactForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Introduce tu correo'}))