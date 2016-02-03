from datetime import datetime

from django.http import Http404
from rest_framework.decorators import detail_route, api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException

from bondapi.models import Bond
from bondapi.serializers import BondSerializer


class BondViewSet(ModelViewSet):
    serializer_class = BondSerializer
    queryset = Bond.objects.all()

    @detail_route(methods=['GET'])
    def valuation_by_date(self, request, pk=None):
        bond = self.get_object()
        string_date = request.query_params.get('valuation_date', None)

        if string_date is not None:
            valuation_date = datetime.strptime(string_date, "%Y-%m-%d").date()
            fraction_of_period_elapsed = self._get_elapsed_fraction_of_period(bond, valuation_date)

            return Response({
                'bond_name': bond.name,
                'bond_valuation_date': valuation_date,
                'bond_settlement_date': bond.settlement_date,
                'bond_maturity_date': bond.maturity_date,
                'elapsed_period': fraction_of_period_elapsed,
            })
        else:
            raise Http404

    def _get_elapsed_fraction_of_period(self, bond, valuation_date):
        seconds_elapsed = valuation_date - bond.settlement_date
        years_elapsed = seconds_elapsed.days / 365
        fraction_of_period_elapsed = years_elapsed / bond.annual_payment_frequency

        return fraction_of_period_elapsed

# class BondValuationOnDateDetail(APIView):
#
#     def get_object(self, pk):
#         try:
#             return Bond.objects.get(pk=pk, available=True)
#
#         except Bond.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         bond = self.get_object(pk)
#
#         serializer = BondSerializer(bond, context={'request': request})
#
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         raise ForbiddenAccess
#
#     def delete(self, request, pk, format=None):
#         raise ForbiddenAccess
#
#
# class ForbiddenAccess(APIException):
#     status_code = 403
#     default_detail = 'Action Forbidden'
