import collections
import datetime

import numpy as np
from django.db import models
from jsonfield import JSONField

DAYS_PER_YEAR = 364.2425


class Bond(models.Model):
    name = models.CharField(max_length=128)
    face_value = models.DecimalField(max_digits=20, decimal_places=2)
    annual_coupon_rate = models.DecimalField(max_digits=5, decimal_places=2)
    annual_required_return = models.DecimalField(max_digits=5, decimal_places=2)
    annual_payment_frequency = models.IntegerField()

    semi_annual_coupon_payment = models.DecimalField(max_digits=10, decimal_places=2)
    bond_price = models.DecimalField(max_digits=10, decimal_places=2)
    bond_valuation = models.DecimalField(max_digits=10, decimal_places=2)

    issue_date = models.DateField()
    settlement_date = models.DateField()
    maturity_date = models.DateField()
    term_to_maturity = models.DecimalField(max_digits=5, decimal_places=2)
    periods_to_maturity = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def valuation_timeseries(self):
        return None

    def save(self, *args, **kwargs):
        # Bond valuation computations
        self.term_to_maturity = self.calculate_term_to_maturity()
        self.periods_to_maturity = self.term_to_maturity * self.annual_payment_frequency
        self.semi_annual_coupon_payment = self.calculate_semi_annual_coupon_payment()
        self.bond_price = self.calculate_bond_price()
        self.bond_valuation = self.bond_price * 10

        super(Bond, self).save(*args, **kwargs)

        timeseries = BondValuationTimeSeries(bond_id=self.id)
        timeseries.save()

    def calculate_term_to_maturity(self):
        days_to_maturity = (self.maturity_date - self.settlement_date)
        return days_to_maturity.days / DAYS_PER_YEAR

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
    def __init__(self, bond, elapsed_time=None, valuation_date=None):
        self.bond = bond
        self.valuation_date = self._calculate_valuation_date(valuation_date, elapsed_time)
        self.maturity_period_elapsed = self._calculate_maturity_periods_elapsed(elapsed_time)
        self.dirty_price = self._calculate_dirty_price()
        self.accrued_interest = self._calculate_accrued_interest()
        self.clean_price = self._calculate_clean_price()

    def _calculate_valuation_date(self, valuation_date, elapsed_maturity_periods):
        if valuation_date is None:
            from_date = self.bond.settlement_date
            valuation_date = from_date + datetime.timedelta(
                days=(elapsed_maturity_periods / self.bond.annual_payment_frequency * DAYS_PER_YEAR)
            )

        return valuation_date

    def _calculate_maturity_periods_elapsed(self, elapsed_time):
        maturity_periods_elapsed = elapsed_time
        if maturity_periods_elapsed is None:
            seconds_elapsed = self.valuation_date - self.bond.settlement_date
            years_elapsed = seconds_elapsed.days / DAYS_PER_YEAR
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


class BondValuationTimeSeries(models.Model):
    bond = models.ForeignKey(Bond, related_name='timeseries')
    timeseries = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict}, null=True)

    def save(self, *args, **kwargs):
        valuation_list = self._create_period_valuations()
        self.timeseries = valuation_list

        return super(BondValuationTimeSeries, self).save(*args, **kwargs)

    def _create_period_valuations(self):
        valuation_list = []
        periods_to_maturity = int(float(self.bond.periods_to_maturity))

        for elapsed_time in range(periods_to_maturity + 1):
            period_valuation = BondValuation(self.bond, elapsed_time)

            json_period_valuation = {
                'valuation_date': period_valuation.valuation_date,
                'maturity__period_elapsed': period_valuation.maturity_period_elapsed,
                'dirty_price': period_valuation.dirty_price,
                'accrued_interest': period_valuation.accrued_interest,
                'clean_price': period_valuation.clean_price,
            }
            valuation_list.append(json_period_valuation)

        return valuation_list
