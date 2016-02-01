from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from models import Bond
from serializers import BondSerializer


class BondViewSet(ModelViewSet):
    serializer_class = BondSerializer
    queryset = Bond.objects.all()
