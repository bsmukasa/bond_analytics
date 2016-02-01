from django.db import models


class Bond(models.Model):
    """A Django model class for a Bond financial instrument.

    A bond is a financial instrument issued by the government or corporations when they need to
    borrow money from the public on a long term basis to finance certain projects. Interest payments
    called coupons are typically paid out to bond holders on a regular basis while the entire loan
    amount called the Face or Par value is repaid at the end.

    Attributes:
        name: The name of the bond.
        face_value: The principal of the bond to be repaid at the end of the maturity period.
        annual_coupon_rate: The stated annual interest rate for a bond.
        annual_payment_frequency: The number of coupon interest payments made annually.
        issue_date: The date the bond was issued.
        settlement_date: The date the bond is purchased.
        maturity_date: The date the bond matures.

    """
    name = models.CharField(max_length=128)
    face_value = models.DecimalField(max_digits=20, decimal_places=2)
    annual_coupon_rate = models.DecimalField(max_digits=5, decimal_places=4)
    annual_payment_frequency = models.IntegerField()

    issue_date = models.DateField()
    settlement_date = models.DateField()
    maturity_date = models.DateField()