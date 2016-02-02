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
            'annual_payment_frequency',
            'annual_interest',

            'issue_date',
            'settlement_date',
            'maturity_date',
            'term_to_maturity'
        )

    term_to_maturity = serializers.ReadOnlyField()
    annual_interest = serializers.ReadOnlyField()
