import datetime
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bond_analytics_project.settings')
django.setup()

from bondapi.models import Bond

test_bond_list = [
    dict(name='test_bond_1', face_value=1000, annual_interest=27.5 * 2, annual_coupon_rate=5.50,
         market_interest_rate=5.75, issue_date=datetime.date(1978, 1, 26), settlement_date=datetime.date(2007, 1, 26),
         maturity_date=datetime.date(2008, 1, 26), term_to_maturity=1.0, bond_price=99.76, bond_valuation=997.6),

    dict(name='test_bond_2', face_value=1000, annual_interest=37.5 * 2, annual_coupon_rate=7.50,
         market_interest_rate=6.50, issue_date=datetime.date(1991, 2, 16), settlement_date=datetime.date(2007, 2, 16),
         maturity_date=datetime.date(2012, 2, 16), term_to_maturity=5.0, bond_price=104.21, bond_valuation=1042.13),

    dict(name='test_bond_3', face_value=1000, annual_interest=25.00 * 2, annual_coupon_rate=5.00,
         market_interest_rate=7.00, issue_date=datetime.date(1999, 4, 9), settlement_date=datetime.date(2007, 1, 14),
         maturity_date=datetime.date(2020, 4, 9), term_to_maturity=13.2, bond_price=82.92, bond_valuation=829.15),

    dict(name='test_bond_4', face_value=1000, annual_interest=45.00 * 2, annual_coupon_rate=9.00,
         market_interest_rate=7.25, issue_date=datetime.date(1987, 11, 6), settlement_date=datetime.date(2006, 7, 16),
         maturity_date=datetime.date(2028, 11, 6), term_to_maturity=22.3, bond_price=119.22, bond_valuation=1192.16),

    dict(name='test_bond_5', face_value=1000, annual_interest=35.00 * 2, annual_coupon_rate=7.00,
         market_interest_rate=7.25, issue_date=datetime.date(2006, 10, 12), settlement_date=datetime.date(2006, 10, 13),
         maturity_date=datetime.date(2036, 10, 13), term_to_maturity=30, bond_price=96.96, bond_valuation=969.58)
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
            issue_date=bond['issue_date'],
            settlement_date=bond['settlement_date'],
            maturity_date=bond['maturity_date'],
        )
        new_bond.save()

        print('Bond {} has been created and saved.'.format(new_bond.name))

    print('Seeding complete.')
