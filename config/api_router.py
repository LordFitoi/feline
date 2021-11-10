from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from feline.users.api.views import UserViewSet, SubscribeViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("newsletter", SubscribeViewSet)


app_name = "api"
urlpatterns = router.urls
