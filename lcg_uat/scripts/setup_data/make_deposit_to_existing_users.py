import argparse
import logging
import datetime

import os
import voltron
import json
from time import sleep
from crlat_gvc_wallet_client.client import GVCUserClient

logger = logging.getLogger('voltron_logger')
parser = argparse.ArgumentParser()

parser.add_argument('--brand', '-brand', help='Brand of the product, e.g. bma, ladbrokes', default='bma', type=str)
parser.add_argument('--env', '-env', help='Backend environment, e.g. beta, prod, hl, tst, stg', default='beta', type=str)
parser.add_argument('--user_types', '-user_types', help='List of User types are mandatory', default='default_username,betplacement_user,freebet_user', type=str)
parser.add_argument('--total_amount', '-total_amount', help='Total Amount to deposit, e.g. 600', default=20, type=int)  # "total_amount" should always be greater that "deposit" variable
parser.add_argument('--card_type', '-card_type', help='Card type, e.g. visa, mastercard, maestro', default='mastercard', type=str)
parser.add_argument('--card_number', '-card_number', help='Credit card number, e.g. 1111 2222 3333 4444', default='5137651100600001', type=str)
parser.add_argument('--cvv', '-cvv', help='Card\'s CVV code, e.g. 123', default='123', type=str)
parser.add_argument('--expiry_month', '-expiry_month', help='Expiry month, e.g. 12', default='12', type=str)
parser.add_argument('--expiry_year', '-expiry_year', help='Expiry year e.g. 2030', default='2030', type=str)

parameters = {}
args = parser.parse_args()

brand = args.brand.lower()
env = args.env.lower()

user_types = args.user_types if args.user_types else None
total_amount = args.total_amount if args.total_amount else None

card_number = args.card_number if args.card_number else None
card_type = args.card_type if args.card_type else None

cvv = args.cvv if args.cvv else None
expiry_month = args.expiry_month if args.expiry_month else None
expiry_year = args.expiry_year if args.expiry_year else None

user_client = GVCUserClient(env=env, brand=brand)

for param, value in vars(args).items():
    if param in ['brand', 'env', 'username'] or value is None:
        continue
    else:
        parameters[param] = value


username_list = []
deposit = 10  # deposite shoud be always less than total amount

user_deposit_info = {}
user_info_list = [['USER_NAME,  USER_BALANCE,  USER_TYPE,  DEPOSITE_MSG']]

types_of_user = user_types.split(',')

with open(os.path.join(os.path.split(voltron.__file__)[0], f'resources/uat_users/{brand}_uat_users.json'),
          encoding='utf-8') as users_file:
    users_data = json.load(users_file)

for user_type in types_of_user:
    username_list.clear()
    if 'beta' in env:
        username_list.extend(users_data['prod'][user_type])
    else:
        username_list.extend(users_data[env][user_type])

    try:
        for username in username_list:
            deposit_msg = "deposit successfully done"
            user_client.login(username=username)
            response = user_client.client_config_partial_logged_user_api_tokens()
            work_flow = int(response['vnUser']['workflowType'])
            if work_flow == 19:
                session_token = user_client.get_logged_user_api_tokens().session_token
                funds = user_client.funds_regulation_data(session_token=session_token)
                user_client.finalize_workflow(sso_token=session_token)
                response = user_client.client_config_partial_logged_user_api_tokens()
            user_bal = int(response['vnBalanceProperties']['balanceProperties']['accountBalance'])
            loop_index = 0
            try:
                if total_amount > user_bal:
                    counter = (total_amount - user_bal) // deposit
                    for loop_index in range(counter):
                        try:
                            user_client.deposit_via_saved_card(username=username, amount=str(deposit), card_type=card_type,
                                                               card_number=card_number,
                                                               expiry_month=expiry_month,
                                                               expiry_year=expiry_year,
                                                               cvv=cvv,
                                                               call_from_balance_update=True
                                                               )
                        except Exception as e:
                            logger.error(e)
                            res = user_client.add_new_payment_card_and_deposit(username=username, amount=str(deposit),
                                                                         card_number=card_number,
                                                                         card_type=card_type, expiry_month=expiry_month,
                                                                         expiry_year=expiry_year,
                                                                         cvv=cvv,call_from_balance_update=True)
                            if res is None:
                                deposit_msg = "unable to deposit"
                                updated_balance = "--"
                                break
                        # Below call is for old Deposit API's flow
                        # user_client.add_payment_card_and_deposit(amount=str(deposit),
                        #                                          card_number=card_number,
                        #                                          card_type=card_type, expiry_month=expiry_month,
                        #                                          expiry_year=expiry_year,
                        #                                          cvv=cvv)
            except Exception as e:
                logger.error(e)
                continue
            finally:
                updated_balance = user_bal + deposit * (loop_index + 1)
                user_info_list.append(list([username, updated_balance, user_type, deposit_msg]))
    finally:
        logger.info('############### balance updated for ###############')
        for item in user_info_list:
            print(item)

FORMAT = '%Y-%m-%d-%H-%M-%S'
path = 'C:\\Automation_Logs\\'
new_path = '%s_%s' % (path + 'balance_update', datetime.datetime.now().strftime(FORMAT)) + '.txt'

with open(new_path, 'w') as file_handler:
    for item in user_info_list:
        file_handler.write("{}\n".format(item))
