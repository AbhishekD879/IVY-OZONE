import argparse
import logging
import datetime
import os
import json
import sys
sys.path.append(os.getcwd())
import voltron
from crlat_gvc_wallet_client.client import GVCUserClient

logger = logging.getLogger('user_info_logger')

#command to run through terminal
#python get_user_balance_details.py --brand bma --user_types default_username --env prod

def parse_arguments():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--brand', '-brand', help='Brand of the product, e.g. bma, ladbrokes', default='ladbrokes',
                        type=str)
    parser.add_argument('--env', '-env', help='Backend environment, e.g. beta, prod, hl, tst, stg', default='beta',
                        type=str)
    parser.add_argument('--user_types', '-user_types',
                        help='List of User types are mandatory:(default_username,betplacement_user,freebet_user,zero_balance_user)',
                        default='quick_deposit_user'.strip(), type=str)
    parser.add_argument('--min_balance', '-min_balance', help='Minimum balance to filter users', default=0, type=int)
    parser.add_argument('--max_balance', '-max_balance', help='Maximum balance to filter users', default=float('inf'),
                        type=int)
    return parser.parse_args()


def get_users_data(brand, env, user_types):
    # Create GVCUserClient object and load user data from json file
    user_client = GVCUserClient(env=env, brand=brand)
    types_of_user = user_types.split(',')
    users_data = {}

    with open(os.path.join(os.path.split(voltron.__file__)[0], f'resources/uat_users/{brand}_uat_users.json'),
              encoding='utf-8') as users_file:
        users_json_data = json.load(users_file)

    for user_type in types_of_user:
        if 'beta' in env:
            users_data[user_type] = users_json_data['prod'][user_type]
        else:
            users_data[user_type] = users_json_data[env][user_type]

    return user_client, users_data


def filter_users(user_client, users_data, min_balance, max_balance):
    # Filter user data based on balance range
    from crlat_core.request.exceptions import InvalidResponseException
    user_info_list = []
    failed_users_list = []
    successful_login = False
    for user_type, username_list in users_data.items():
        for username in username_list:
            try:
                user_client.login(username=username)
                response = user_client.client_config_partial_logged_user_api_tokens()
                user_bal = int(response['vnBalanceProperties']['balanceProperties']['accountBalance'])

                if min_balance <= user_bal <= max_balance:
                    user_info_list.append([username, user_type, user_bal])
                successful_login = True
            except InvalidResponseException as e:
                logger.warning(f"Failed to login for user {username}. Error: {e}")
                failed_users_list.append([username, user_type])
            except Exception as e:
                logger.warning(f"An unexpected error occurred for user {username}. Error: {e}")
    return user_info_list, failed_users_list, successful_login


def save_user_info_to_file(user_info_list, failed_users_list, brand, env, user_types):
    # Save user information and failed user information to a file which is to be created in local
    # C folder as Automation_Logs
    FORMAT = '%Y-%m-%d-%H-%M-%S'
    path = 'C:\\Automation_Logs\\'
    new_path = f"{path}user_info_{brand}_{env}_{user_types}_{datetime.datetime.now().strftime(FORMAT)}.txt"

    with open(new_path, 'w') as file_handler:
        # Write header and user information
        file_handler.write(f"----------{brand.title()}_{env.title()}----------\n")
        file_handler.write("-----------------------------------------------------------------\n")
        file_handler.write(
            "| {:<15} | {:<10} | {:<10} | {:<15} | {:<15} |\n".format("USERNAME", "ENV", "BRAND", "USER_TYPE",
                                                                      "USER_BALANCE"))
        file_handler.write("-----------------------------------------------------------------\n")
        for item in user_info_list:
            file_handler.write(
                "| {:<15} | {:<10} | {:<10} | {:<15} | {:<15} |\n".format(item[0], env, brand, item[1], item[2]))
        file_handler.write("-----------------------------------------------------------------\n")
        file_handler.write("\nFAILED USERS\n")
        file_handler.write("------------------------------------------------\n")
        file_handler.write("| {:<15} | {:<15} |\n".format("USERNAME", "USER_TYPE"))
        file_handler.write("------------------------------------------------\n")
        for item in failed_users_list:
            file_handler.write("| {:<15} | {:<15} |\n".format(item[0], item[1]))
            file_handler.write("------------------------------------------------\n")


if __name__ == "__main__":
    args = parse_arguments()
    user_client, users_data = get_users_data(args.brand, args.env, args.user_types)
    filtered_users, failed_users, successful_login = filter_users(user_client, users_data, args.min_balance,
                                                                  args.max_balance)
    save_user_info_to_file(filtered_users, failed_users, args.brand, args.env, args.user_types)
