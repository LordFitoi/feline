from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token
from feline.jobposts.views import company_create_view, company_detail_view, company_list_view, jobpost_create_view, jobpost_detail_view, jobpost_list_view, jobpost_update_view
from feline.users.views import spanish_password_change_view, spanish_login_view, spanish_password_reset_confirm_view


urlpatterns = [
    path("", jobpost_list_view, name="home"),
    path("new/", jobpost_create_view, name="create"),
    path("jobpost/<str:slug>/", jobpost_detail_view, name="jobpost-detail"),
    path("jobpost/<str:slug>/edit", jobpost_update_view, name="jobpost-edit"),
    path("companies/", company_list_view, name="company-list"),
    path("company/new/", company_create_view, name="company-create"),
    path("company/<str:slug>/", company_detail_view, name="company-detail"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    path(
        "privacy-policy/", TemplateView.as_view(template_name="privacy-policy.html"), name="privacy-policy"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    
    # User management
    path("users/", include("feline.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path('accounts/login/', spanish_login_view, name='login'),
    path('accounts/password_change/', spanish_password_change_view, name='password_change'),
    path('accounts/reset/<uidb64>/<token>/', spanish_password_reset_confirm_view, name='password_reset_confirm'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
