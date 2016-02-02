from rest_framework import serializers

from bondapi.models import Bond


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
            'term_to_maturity'
        )

    term_to_maturity = serializers.ReadOnlyField()
    annual_interest = serializers.ReadOnlyField()
    semi_annual_coupon_payment = serializers.ReadOnlyField()
    bond_price = serializers.ReadOnlyField()
    bond_valuation = serializers.ReadOnlyField()
