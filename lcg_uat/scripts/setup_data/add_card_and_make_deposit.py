import argparse
import logging
from time import sleep

from crlat_gvc_wallet_client.client import GVCUserClient

logger = logging.getLogger('voltron_logger')
parser = argparse.ArgumentParser()

parser.add_argument('--brand', '-brand', help='Brand of the product, e.g. vanilla, ladbrokes', default='bma', type=str)
parser.add_argument('--env', '-env', help='Backend environment, e.g. prod, hl, tst, stg', default='tst2', type=str)
parser.add_argument('--username', '-username', help='Username is mandatory', type=str, required=True)
parser.add_argument('--amount', '-amount', help='Amount to deposit, e.g. 20', default=20, type=int)
parser.add_argument('--card_type', '-card_type', help='Card type, e.g. visa, mastercard, maestro', default='visa', type=str)
parser.add_argument('--card_number', '-card_number', help='Credit card number, e.g. 1111 2222 3333 4444', default='4142731270314439', type=str)
parser.add_argument('--cvv', '-cvv', help='Card\'s CVV code, e.g. 123', default='123', type=str)
parser.add_argument('--expiry_month', '-expiry_month', help='Expiry month, e.g. 12', default='12', type=str)
parser.add_argument('--expiry_year', '-expiry_year', help='Expiry year e.g. 2030', default='2030', type=str)

parameters = {}
args = parser.parse_args()

brand = args.brand.lower()
env = args.env.lower()

username = args.username if args.username else None
amount = args.amount if args.amount else None

card_number = args.card_number if args.card_number else None
card_type = args.card_type if args.card_type else None

cvv = args.cvv if args.cvv else None
expiry_month = args.expiry_month if args.expiry_month else None
expiry_year = args.expiry_year if args.expiry_year else None

user_client = GVCUserClient(env=env)

for param, value in vars(args).items():
    if param in ['brand', 'env', 'username'] or value is None:
        continue
    else:
        parameters[param] = value

user_client.login(username=username)

limit = 20
if amount > limit:
    deposit_count = int(amount // limit)
    for _ in range(deposit_count):
        user_client.add_payment_card_and_deposit(amount=limit, card_number=card_number, card_type=card_type,
                                                 expiry_month=expiry_month, expiry_year=expiry_year, cvv=cvv)
        sleep(10)  # because continuous depositing overloads cashier
    amount = amount - deposit_count * limit
if amount:
    user_client.add_payment_card_and_deposit(amount=amount, card_number=card_number, card_type=card_type,
                                             expiry_month=expiry_month, expiry_year=expiry_year, cvv=cvv)
