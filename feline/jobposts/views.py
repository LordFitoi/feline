from __future__ import annotations

from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView

from .forms import CompanyForm, JobPostForm
from .models import Company, JobPost 


class JobPostListView(ListView):
    model = JobPost
    paginate_by = 10


jobpost_list_view = JobPostListView.as_view()


class JobPostDetailView(DetailView):
    model = JobPost
    slug_field = "slug"
    slug_url_kwarg = "slug"


jobpost_detail_view = JobPostDetailView.as_view()


class JobPostCreateView(CreateView):
    form = JobPostForm
    model = JobPost
    success_url = "/"
    fields = ['company','title', 'description', 'location', 'how_to_apply', 'application_url', 'application_email', 'job_type', 'category', 'tags', 'currency','salary_range_start_at', 'salary_range_end_at', 'sponsor_relocation']

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'].fields['company'].queryset = Company.objects.filter(user=self.request.user)
        return context
        

jobpost_create_view = JobPostCreateView.as_view()


class CompanyCreateView(CreateView):
    form = CompanyForm
    model = Company
    success_url =  "/new"
    fields = ["logo", "name", "description", "email", "company_url", "country"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CompanyCreateView, self).form_valid(form)


company_create_view = CompanyCreateView.as_view()


class CompanyDetailView(DetailView):
    model = Company


company_detail_view = CompanyDetailView.as_view()