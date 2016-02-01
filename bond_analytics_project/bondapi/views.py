from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from bondapi.models import Bond
from bondapi.serializers import BondSerializer


class BondViewSet(ModelViewSet):
    serializer_class = BondSerializer
    queryset = Bond.objects.all()
