import pytest
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from django.test import RequestFactory
from django.urls import reverse

from feline.jobposts.tests.factories import CompanyFactory
from feline.jobposts.views import jobpost_create_view
from feline.users.models import User
from feline.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db



class TestJobPostCreateView:

    # Test user is redirected to create company view if he wants to create a new job if he has not created a company yet
    def test_authenticated_without_company(self, user: User, rf: RequestFactory):
        path = reverse("create")
        redirect_url = reverse("company-create")

        request = rf.get(path)
        request.user = UserFactory()
        
        
        response = jobpost_create_view(request)
        assert response.status_code == 302
        assert response.url == redirect_url

    # Test user can create a post if it already has a company when trying access Create Post
    def test_authenticated_with_company(self, user: User, rf: RequestFactory):
        path = reverse("create")

        request = rf.get(path)
        request.user = UserFactory()



    # Test user is redirected if it is not logged in when trying access Create company
    def test_not_authenticated(self, user: User, rf: RequestFactory):
        path = reverse("create")
        request = rf.get(path)
        request.user = AnonymousUser()
        
        response = jobpost_create_view(request)

        login_url = reverse(settings.LOGIN_URL)

        assert response.status_code == 302
        assert response.url == f"{login_url}?next={path}"


class TestCompanyCreateView:
    # Test user is redirected if it is not logged in when trying access Create company
    def test_not_authenticated(self, user: User, rf: RequestFactory):
        path = reverse("company-create")
        request = rf.get(path)
        request.user = AnonymousUser()
        
        response = jobpost_create_view(request)

        login_url = reverse(settings.LOGIN_URL)

        assert response.status_code == 302
        assert response.url == f"{login_url}?next={path}"    


# Test user is redirected if it is not logged in when trying access Edit profile

