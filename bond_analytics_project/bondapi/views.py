from datetime import datetime

from django.http import Http404
from rest_framework.decorators import detail_route, api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException

from bondapi.models import Bond, BondValuation
from bondapi.serializers import BondSerializer, BondValuationSerializer


class BondViewSet(ModelViewSet):
    serializer_class = BondSerializer
    queryset = Bond.objects.all()

    @detail_route(methods=['GET'])
    def valuation_between_periods(self, request, pk=None):
        bond = self.get_object()
        bond_id = bond.id
        string_date = request.query_params.get('valuation_date', None)
        string_elapsed_time = request.query_params.get('elapsed_time', None)

        valuation_date, elapsed_time = None, None

        if string_date is not None:
            valuation_date = datetime.strptime(string_date, "%Y-%m-%d").date()
        elif string_elapsed_time is not None:
            elapsed_time = float(string_elapsed_time)
        else:
            raise Http404

        bond_valuation = BondValuation(bond, bond_id, elapsed_time, valuation_date)
        valuation_serializer = BondValuationSerializer(bond_valuation)

        return Response(valuation_serializer.data)
