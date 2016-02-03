import datetime
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bond_analytics_project.settings')
django.setup()

from bondapi.models import Bond

test_bond_list = [
    dict(name='test_ppt_bond', face_value=1000, annual_interest=25, annual_coupon_rate=0.08,
         annual_required_return=0.095, issue_date=datetime.date(1978, 1, 16),
         settlement_date=datetime.date(2007, 3, 16), maturity_date=datetime.date(2010, 3, 16),
         term_to_maturity=3, bond_price=99.76, bond_valuation=972.23),

    dict(name='test_bond_1', face_value=1000, annual_interest=27.5 * 2, annual_coupon_rate=0.055,
         annual_required_return=0.0575, issue_date=datetime.date(1978, 1, 26),
         settlement_date=datetime.date(2007, 1, 26),
         maturity_date=datetime.date(2008, 1, 26), term_to_maturity=1.0, bond_price=99.76, bond_valuation=997.6),

    dict(name='test_bond_2', face_value=1000, annual_interest=37.5 * 2, annual_coupon_rate=0.075,
         annual_required_return=0.065, issue_date=datetime.date(1991, 2, 16),
         settlement_date=datetime.date(2007, 2, 16),
         maturity_date=datetime.date(2012, 2, 16), term_to_maturity=5.0, bond_price=104.21, bond_valuation=1042.13),

    dict(name='test_bond_3', face_value=1000, annual_interest=25.00 * 2, annual_coupon_rate=0.05,
         annual_required_return=0.07, issue_date=datetime.date(1999, 4, 9), settlement_date=datetime.date(2007, 1, 14),
         maturity_date=datetime.date(2020, 4, 9), term_to_maturity=13.2, bond_price=82.92, bond_valuation=829.15),

    dict(name='test_bond_4', face_value=1000, annual_interest=45.00 * 2, annual_coupon_rate=0.09,
         annual_required_return=0.0725, issue_date=datetime.date(1987, 11, 6),
         settlement_date=datetime.date(2006, 7, 16),
         maturity_date=datetime.date(2028, 11, 6), term_to_maturity=22.3, bond_price=119.22, bond_valuation=1192.16),
]

if __name__ == '__main__':
    print('Resetting database.')
    Bond.objects.all().delete()

    print('Starting seeding.')
    for bond in test_bond_list:
        new_bond = Bond(
            name=bond['name'],
            face_value=bond['face_value'],
            annual_payment_frequency=2,
            annual_coupon_rate=bond['annual_coupon_rate'],
            annual_required_return=bond['annual_required_return'],
            issue_date=bond['issue_date'],
            settlement_date=bond['settlement_date'],
            maturity_date=bond['maturity_date'],
        )
        new_bond.save()

        print('Bond {} has been created and saved.'.format(new_bond.name))

    print('Seeding complete.')
