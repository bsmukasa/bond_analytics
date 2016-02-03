import datetime

import numpy as np
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
        annual_interest: The dollar amount of interest earned annually.

        issue_date: The date the bond was issued.
        settlement_date: The date the bond is purchased.
        maturity_date: The date the bond matures.
        term_to_maturity: The number of years before the bond matures.

    """
    name = models.CharField(max_length=128)
    face_value = models.DecimalField(max_digits=20, decimal_places=2)
    annual_coupon_rate = models.DecimalField(max_digits=5, decimal_places=4)
    annual_required_return = models.DecimalField(max_digits=5, decimal_places=4)
    annual_payment_frequency = models.IntegerField()

    semi_annual_coupon_payment = models.DecimalField(max_digits=10, decimal_places=4)
    bond_price = models.DecimalField(max_digits=10, decimal_places=4)
    bond_valuation = models.DecimalField(max_digits=10, decimal_places=4)

    issue_date = models.DateField()
    settlement_date = models.DateField()
    maturity_date = models.DateField()
    term_to_maturity = models.DecimalField(max_digits=6, decimal_places=2)
    periods_to_maturity = models.DecimalField(max_digits=6, decimal_places=2)

    def save(self, *args, **kwargs):
        # Bond valuation computations
        self.term_to_maturity = self.calculate_term_to_maturity()
        self.periods_to_maturity = self.term_to_maturity * self.annual_payment_frequency
        self.semi_annual_coupon_payment = self.calculate_semi_annual_coupon_payment()
        self.bond_price = self.calculate_bond_price()
        self.bond_valuation = self.bond_price * 10

        super(Bond, self).save(*args, **kwargs)

    def calculate_term_to_maturity(self):
        days_to_maturity = (self.maturity_date - self.settlement_date)
        return days_to_maturity.days / 365

    def calculate_semi_annual_coupon_payment(self):
        return self.face_value * self.annual_coupon_rate / self.annual_payment_frequency

    # noinspection PyTypeChecker
    def calculate_bond_price(self):
        present_value = np.pv(
            rate=self.annual_required_return / self.annual_payment_frequency,
            nper=self.term_to_maturity * self.annual_payment_frequency,
            pmt=self.semi_annual_coupon_payment,
            fv=self.face_value
        )

        return -0.1 * present_value


class BondValuation:
    def __init__(self, bond, elapsed_time, valuation_date):
        self.bond = bond
        self.valuation_date = self._calculate_valuation_date(valuation_date, elapsed_time)
        self.maturity_period_elapsed = self._calculate_maturity_periods_elapsed(elapsed_time)
        # self.periods_to_maturity = float(bond.term_to_maturity * bond.annual_payment_frequency)
        self.dirty_price = self._calculate_dirty_price()
        self.accrued_interest = self._calculate_accrued_interest()
        self.clean_price = self._calculate_clean_price()

    DAYS_PER_YEAR = 364.2425

    def _calculate_valuation_date(self, valuation_date, elapsed_time):
        if valuation_date is None:
            from_date = self.bond.settlement_date
            valuation_date = from_date + datetime.timedelta(days=(elapsed_time * self.DAYS_PER_YEAR))

        return valuation_date

    def _calculate_maturity_periods_elapsed(self, elapsed_time):
        maturity_periods_elapsed = elapsed_time
        if maturity_periods_elapsed is None:
            seconds_elapsed = self.valuation_date - self.bond.settlement_date
            years_elapsed = seconds_elapsed.days / self.DAYS_PER_YEAR
            fraction_of_years_elapsed = years_elapsed * self.bond.annual_payment_frequency
            maturity_periods_elapsed = fraction_of_years_elapsed * self.bond.annual_payment_frequency

        return maturity_periods_elapsed

    def _calculate_clean_price(self):
        return self.dirty_price - self.accrued_interest

    def _calculate_accrued_interest(self):
        return self.maturity_period_elapsed * float(
            self.bond.annual_coupon_rate / self.bond.annual_payment_frequency * self.bond.face_value)

    def _calculate_dirty_price(self):
        return float(self.bond.bond_valuation) * float(
            (1 + self.bond.annual_required_return / self.bond.annual_payment_frequency)) ** self.maturity_period_elapsed
