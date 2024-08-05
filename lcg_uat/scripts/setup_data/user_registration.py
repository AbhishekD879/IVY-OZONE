import argparse
import re
from datetime import datetime
from time import sleep

from crlat_gvc_wallet_client.client import GVCUserClient
from columnar import columnar
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tests  # noqa: E402 module level import not at top of file
from voltron.utils.exceptions.gvc_exeption import GVCException  # noqa: E402 module level import not at top of file


class WrapperGVCUserClient(GVCUserClient):
    def __init__(self, env, brand):
        super(WrapperGVCUserClient, self).__init__(env, brand)

    def add_card_and_deposit(self,
                             username: str,
                             amount: str,
                             card_number: str = tests.settings.visa_card,
                             expiry_month='',
                             expiry_year='',
                             cvv=None,
                             **kwargs):
        """
        Make initial deposit for specified user with using specified card

        :param username: User's name to deposit
        :param amount: Amount to deposit (limit is 22)
        :param card_number: Card's number
        :param expiry_month: Card's expiry month
        :param expiry_year: Card's expiry year
        :param cvv: Card's CVV
        """
        verified_card_type = None

        now = datetime.now()
        if not expiry_month:
            expiry_month = now.month
        if not expiry_year:
            shifted_year = str(now.year + 5)
            expiry_year = shifted_year

        card_type_regex = {
            "mastercard": '^5',
            "visa": '^4'
        }
        for card_type, regex in card_type_regex.items():
            if re.match(regex, card_number):
                verified_card_type = card_type
                break
        if not verified_card_type:
            raise GVCException(f'Card type of "{card_number}" card number was not defined')
        if verified_card_type == 'mastercard':
            cvv = tests.settings.master_card_cvv
        elif verified_card_type == 'visa':
            cvv = tests.settings.visa_card_cvv

        self.login(username=username)
        self.add_payment_card_and_deposit(amount=amount,
                                          card_number=card_number,
                                          card_type=verified_card_type,
                                          expiry_month=expiry_month,
                                          expiry_year=expiry_year,
                                          cvv=cvv,
                                          **kwargs)

    def deposit_with_existing_card_via_cashier(self, username: str, amount: float, **kwargs):
        """
        Make deposit using existing card

        :param username: User's name to deposit
        :param amount: Amount to deposit (no limits)
        """
        limit = 20
        self.login(username=username)
        if amount > limit:
            deposit_count = int(amount // limit)
            for _ in range(deposit_count):
                self.deposit_via_existing_card(username=username, amount=limit, **kwargs)
                sleep(10)  # because continuous depositing overloads cashier
            amount -= deposit_count * limit
        if amount:
            self.deposit_via_existing_card(username=username, amount=amount, **kwargs)


def configure_arg_parser():
    """
    Initiate the parser and add arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--brand', type=str, required=True)
    parser.add_argument('--env', type=str, required=True)
    parser.add_argument('--username', type=str)
    parser.add_argument('--quantity', type=int, required=True, default=1)
    parser.add_argument('--amount', type=int, help='minimum amount is 5')
    parser.add_argument('--card_number', '-card_number', help='Credit card number, e.g. 1111 2222 3333 4444', type=str)
    parser.add_argument('--emailaddress', type=str)
    parser.add_argument('--password', type=str)
    parser.add_argument('--currencycode', type=str)
    parser.add_argument('--addresscountrycode', type=str)
    parser.add_argument('--gender', type=str)
    parser.add_argument('--firstname', type=str)
    parser.add_argument('--lastname', type=str)
    parser.add_argument('--dateofbirth', type=str)
    parser.add_argument('--addressfinder', type=str)
    parser.add_argument('--addressline1', type=str)
    parser.add_argument('--addresscity', type=str)
    parser.add_argument('--addresszip', type=str)
    parser.add_argument('--mobilenumber', type=str)
    parser.add_argument('--mobilecountrycode', type=str)
    parser.add_argument('--limit_type', type=str)
    parser.add_argument('--daily_limit', type=int)
    parser.add_argument('--weekly_limit', type=int)
    parser.add_argument('--monthly_limit', type=int)
    return parser


if __name__ == "__main__":
    parser = configure_arg_parser()
    args = parser.parse_args()
    parameters = {}
    brand = args.brand.lower()
    env = args.env.lower()
    user_client = WrapperGVCUserClient(env=env, brand=brand)
    user_info_list = []
    min_amount = tests.settings.min_deposit_amount
    card_number = args.card_number

    all_users = [user_client._generate_username() for item in range(args.quantity)]
    if args.username is not None:
        all_users[0] = args.username

    for user_name in all_users:
        for param, value in vars(args).items():
            if param in ['brand', 'env', 'username'] or value is None:
                continue
            else:
                parameters[param] = value
        user_info = user_client.register_new_user(username=user_name, **parameters)

        if card_number:
            user_client.add_card_and_deposit(username=user_info.username,
                                             card_number=card_number,
                                             amount=min_amount)
            if args.amount is not None:
                amount = args.amount - int(min_amount)
                if amount > 0:
                    user_client.deposit_with_existing_card_via_cashier(username=user_info.username, amount=amount)

        user_info_list.append(list([
            user_info.username, user_info.password, user_info.emailaddress, user_info.currencycode,
            args.amount if card_number else 'card was not specified'
        ]))
        print(f'Registered new user with info: "{user_info}"\n')

    headers = ["USERNAME", "PASSWORD", "EMAIL", "CURRENCY", "DEPOSIT"]
    table = columnar(data=user_info_list, headers=headers, no_borders=True)
    print(table)
