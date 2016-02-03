from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from bondapi.views import BondViewSet

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'bond', BondViewSet)

urlpatterns = [
    url(
        regex=r'^admin/',
        view=admin.site.urls
    ),

    url(
        regex=r'^',
        view=include(router.urls)
    ),
]
