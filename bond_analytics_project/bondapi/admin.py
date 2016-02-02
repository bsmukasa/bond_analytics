from django.contrib import admin


class BondAdmin(admin.ModelAdmin):
    list_display = [
        'id',
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
    ]
