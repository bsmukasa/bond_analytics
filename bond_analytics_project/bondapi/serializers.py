from rest_framework import serializers

from bondapi.models import Bond, BondValuationTimeSeries


class BondSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bond
        fields = (
            'url',
            'name',
            'face_value',
            'annual_coupon_rate',
            'annual_required_return',
            'annual_payment_frequency',

            'semi_annual_coupon_payment',
            'bond_price',
            'bond_valuation',

            'issue_date',
            'settlement_date',
            'maturity_date',
            'years_to_maturity',
            'periods_to_maturity',

            'timeseries',
        )

    periods_to_maturity = serializers.ReadOnlyField()
    years_to_maturity = serializers.ReadOnlyField()
    semi_annual_coupon_payment = serializers.ReadOnlyField()
    bond_price = serializers.ReadOnlyField()
    bond_valuation = serializers.ReadOnlyField()

    timeseries = serializers.HyperlinkedIdentityField(view_name='timeseries-detail')


class BondValuationSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    bond = BondSerializer()
    valuation_date = serializers.DateField()
    maturity_period_elapsed = serializers.FloatField()
    dirty_price = serializers.FloatField()
    accrued_interest = serializers.FloatField()
    clean_price = serializers.FloatField()


class BondValuationTimeSeriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BondValuationTimeSeries
        fields = (
            'url',
            'bond',
            'timeseries',
        )

    bond = BondSerializer()
    timeseries = serializers.ReadOnlyField()
