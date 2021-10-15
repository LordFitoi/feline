from django.shortcuts import render

from django.views.generic import DetailView, ListView, CreateView
from .models import JobPost


class JobPostListView(ListView):
    model = JobPost
    paginate_by = 10


jobpost_list_view = JobPostListView.as_view()


class JobPostDetailView(DetailView):
    model = JobPost
    slug_field = "slug"
    slug_url_kwarg = "slug"


jobpost_detail_view = JobPostDetailView.as_view()