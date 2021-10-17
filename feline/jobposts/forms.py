from django import forms
from .models import JobPost
from ckeditor.widgets import CKEditorWidget


class JobPostForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    how_to_apply = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = JobPost
        fields = ['company','title', 'description', 'location', 'how_to_apply', 'application_url', 'application_email', 'job_type', 'category', 'tags', 'currency','salary_range_start_at', 'salary_range_end_at', 'sponsor_relocation']