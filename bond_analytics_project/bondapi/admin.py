from django.contrib import admin


class BondAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'face_value',
        'annual_coupon_rate',
        'annual_payment_frequency',
        'issue_date',
        'settlement_date',
        'maturity_date'
    ]
