from __future__ import annotations

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
from django.shortcuts import redirect
from django.urls.base import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from hitcount.views import HitCountDetailView

from .forms import CompanyForm, CompanySearchForm, ContactForm, JobPostForm, JobPostSearchForm
from .models import Category, Company, JobPost 


class CompanyListView(ListView):
    model = Company
    paginate_by = 20
    form_class = CompanySearchForm
    search_fields = ('title', 'description', 'tag_line', 'country')

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return self.model.objects.annotate(search=SearchVector(*self.search_fields)).filter(search=form.cleaned_data['keyword'])
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CompanyListView, self).get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['contact_form'] = ContactForm()
        return context


company_list_view = CompanyListView.as_view()


class JobPostListView(ListView):
    model = JobPost
    paginate_by = 10
    form_class = JobPostSearchForm
    search_fields = ('title', 'description', 'how_to_apply', 'job_type', 'category')

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        queryset = self.model.objects.all()
        if form.is_valid():
            if form.cleaned_data['keyword']:
                queryset = queryset.annotate(search=SearchVector(*self.search_fields)).filter(search=form.cleaned_data['keyword'])
            if form.cleaned_data['category'] != '--':
                queryset = queryset.filter(category__name=form.cleaned_data['category'])
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(JobPostListView, self).get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['contact_form'] = ContactForm()
        context['keyword'] = self.request.GET.get('keyword', None)
        context['category'] = self.request.GET.get('category', None)
        return context


jobpost_list_view = JobPostListView.as_view()


class JobPostDetailView(HitCountDetailView):
    model = JobPost
    slug_field = "slug"
    slug_url_kwarg = "slug"
    count_hit = True 

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['other_jobs'] = JobPost.objects.filter(company=self.object.company).exclude(id=self.object.id)
        return context


jobpost_detail_view = JobPostDetailView.as_view()


class JobPostCreateView(LoginRequiredMixin, CreateView):
    form = JobPostForm
    model = JobPost
    success_url = "/"
    fields = ['company','title', 'description', 'location', 'how_to_apply', 'application_url', 'application_email', 'job_type', 'category', 'tags', 'currency','salary_range_start_at', 'salary_range_end_at', 'sponsor_relocation', 'is_remote']

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'].fields['company'].queryset = Company.objects.filter(user=self.request.user)
        return context

    def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated and  request.user.company_set.all().count() == 0:
            return redirect(reverse('company-create'))
        return super().dispatch(request, *args, **kwargs)


jobpost_create_view = JobPostCreateView.as_view()


class JobPostUpdateView(LoginRequiredMixin, UpdateView):
    form = JobPostForm
    model = JobPost
    success_url = "/"
    fields = ['company','title', 'description', 'location', 'how_to_apply', 'application_url', 'application_email', 'job_type', 'category', 'tags', 'currency','salary_range_start_at', 'salary_range_end_at', 'sponsor_relocation', 'is_remote']

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'].fields['company'].queryset = Company.objects.filter(user=self.request.user)
        return context


jobpost_update_view = JobPostUpdateView.as_view()


class CompanyCreateView(CreateView):
    form = CompanyForm
    model = Company
    success_url =  "/new"
    fields = ["logo", "name", "tagline", "description", "email", "company_url", "country"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CompanyCreateView, self).form_valid(form)


company_create_view = CompanyCreateView.as_view()


class CompanyDetailView(HitCountDetailView):
    model = Company
    count_hit = True 

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['jobs'] = JobPost.objects.filter(company=self.object)[:10]
        return context


company_detail_view = CompanyDetailView.as_view()