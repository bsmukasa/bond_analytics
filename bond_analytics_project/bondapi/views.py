from datetime import datetime

from django.http import Http404
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bondapi.models import Bond, BondValuation
from bondapi.serializers import BondSerializer, BondValuationSerializer


class BondViewSet(ModelViewSet):
    serializer_class = BondSerializer
    queryset = Bond.objects.all()

    @detail_route(methods=['GET'])
    def valuation_between_periods(self, request, pk=None):
        bond = self.get_object()
        string_date = request.query_params.get('valuation_date', None)
        string_elapsed_time = request.query_params.get('elapsed_time', None)
        valuation_date, elapsed_time = None, None

        if string_date is not None and string_elapsed_time is None:
            valuation_date = datetime.strptime(string_date, "%Y-%m-%d").date()
        elif string_elapsed_time is not None and string_date is None:
            elapsed_time = float(string_elapsed_time)
        else:
            raise Http404

        bond_valuation = BondValuation(bond, bond.id, elapsed_time, valuation_date)
        bond__valuation_serializer = BondValuationSerializer(bond_valuation)

        return Response(bond__valuation_serializer.data)
