from django.urls import path

from .views import (
    jobpost_list_view,
    jobpost_detail_view
)

app_name = "jobpost"
urlpatterns = [
    path("", view=jobpost_list_view, name="home"),
    path("<str:slug>/", view=jobpost_detail_view, name="detail"),
]