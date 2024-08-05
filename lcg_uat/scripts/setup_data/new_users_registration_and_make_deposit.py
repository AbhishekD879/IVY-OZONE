import logging
import datetime
from time import sleep
from crlat_gvc_wallet_client.client import GVCUserClient

logger = logging.getLogger('voltron_logger')

brand = 'ladbrokes'  # bma, ladbrokes
env = 'beta'  # prod, beta, qa2, qa3
total_user_balance = 400  # 400, 500, 600
deposit_per_transaction = 20  # value should be less than 22 as GVC wallet allow max 22 deposit at a time
users_count = 10

card_number = '5137651100600001'
card_type = 'mastercard'  # visa, mastercard, maestro
cvv = '123'
expiry_month = '12'
expiry_year = '2030'

if 'qa' in env:
    user_client = GVCUserClient(brand=brand, env_host=env)
else:
    user_client = GVCUserClient(env=env, brand=brand)

user_info_list = [['USER_NAME,  USER_BALANCE']]

all_users = [user_client._generate_username() for item in range(users_count)]

for user in all_users:
    try:
        user_info = user_client.register_new_user(username=user)

        user_client.login(username=user)
        loop_index = 0
        try:
            for loop_index in range(total_user_balance // deposit_per_transaction):
                # user_client.add_payment_card_and_deposit(amount=str(deposit_per_transaction),
                #                                          card_number=card_number,
                #                                          card_type=card_type, expiry_month=expiry_month,
                #                                          expiry_year=expiry_year,
                #                                          cvv=cvv)
                user_client.add_new_payment_card_and_deposit(username=user, amount=str(20),
                                                             card_number=card_number,
                                                             card_type=card_type, expiry_month=expiry_month,
                                                             expiry_year=expiry_year,
                                                             cvv=cvv)
            sleep(5)
        except Exception as e:
            logger.error(e)
            continue
        finally:
            updated_balance = deposit_per_transaction * (loop_index + 1)
            user_info_list.append(list([user, updated_balance]))
    except Exception as e:
        logger.error(e)
        continue

for item in user_info_list:
    print(item)

FORMAT = '%Y-%m-%d-%H-%M-%S'
path = 'C:\\Automation_Logs\\'
new_path = '%s_%s' % (path + env + '_balance_update', datetime.datetime.now().strftime(FORMAT)) + '.txt'

with open(new_path, 'w') as file_handler:
    for item in user_info_list:
        file_handler.write("{}\n".format(item))
