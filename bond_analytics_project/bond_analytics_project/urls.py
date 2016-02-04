from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from bondapi.views import BondViewSet, BondValuationTimeSeriesViewSet

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'bond', BondViewSet)
router.register(r'bond_valuation_timeseries', BondValuationTimeSeriesViewSet)

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
