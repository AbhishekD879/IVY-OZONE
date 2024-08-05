from voltron.environments.constants.base.bma import BMA
from collections import namedtuple


class CoralBMA(BMA):
    """
    src/app/lazy-modules/locale/translations/en-US/bma.lang.ts
    """
    SPORTS = BMA.SPORTS.upper()
    USER_SETTINGS_ODDS_FORMAT_FRAC = BMA.USER_SETTINGS_ODDS_FORMAT_FRAC.upper()
    USER_SETTINGS_ODDS_FORMAT_DEC = BMA.USER_SETTINGS_ODDS_FORMAT_DEC.upper()
    ACCOUNT_CLOSURE_AND_REOPENING_INFO_TEXT = 'Successfully closed: Poker, Bingo, Sports, Casino'
    ACCOUNT_CLOSURE_AND_REOPENING_PAGE_TITLE = 'Online Sports Betting and Latest Odds - Coral'

    # my account items  # Old Right Manu List
    # EXPECTED_LIST_OF_RIGHT_MENU = ['BANKING', 'OFFERS & FREE BETS', 'HISTORY', 'MESSAGES', 'CONNECT', 'SETTINGS',
    #                                'GAMBLING CONTROLS', 'HELP & CONTACT', 'LOG OUT', 'ODDS BOOSTS']
    # BANKING_MENU_ITEMS = ['MY BALANCE', 'DEPOSIT', 'WITHDRAW']
    # HISTORY_MENU_ITEMS = ['BETTING HISTORY', 'TRANSACTION HISTORY', 'PAYMENT HISTORY']
    # OFFERS_FREE_BETS_MENU_ITEMS = ['ODDS BOOST', 'SPORTS FREE BETS', 'SPORTS PROMOTIONS', 'GAMING PROMOTIONS',
    #                                'VOUCHER CODES']
    # CONNECT_MENU_ITEMS = ['JOIN CONNECT', 'SHOP EXCLUSIVE PROMOS', 'SHOP BET TRACKER', 'FOOTBALL BET FILTER',
    #                       'SHOP LOCATOR']
    # SETTINGS_MENU_ITEMS = ['MY ACCOUNT DETAILS', 'CHANGE PASSWORD', 'MARKETING PREFERENCES', 'BETTING SETTINGS']
    # GAMBLING_CONTROLS_MENU_ITEMS = ['Spending Controls', 'Time Management', 'Account Closure & Reopening']

    CHANGE_PASSWORD = 'Change Password'
    COMMUNICATION_PREFERENCES = 'Communication Preferences'
    BETTING_SETTINGS = 'Betting Settings'
    SECURITY = 'Security'
    TWO_FACTOR_AUTHENTICATION = '2-Factor authentication'

    SETTINGS_MENU_ITEMS = [CHANGE_PASSWORD, COMMUNICATION_PREFERENCES, BETTING_SETTINGS, TWO_FACTOR_AUTHENTICATION]
    # New list of right menu
    _right_menu = namedtuple('right_menu', ['deposit', 'withdraw', 'payment_history',
                                            'manage_my_cards', 'sports_free_bets', 'sports_promotions',
                                            'gaming_promotions', 'shop_exclusive_promotions', 'voucher_codes',
                                            'odds_boosts', 'my_bets', 'my_account_details', 'settings', 'connect',
                                            'transaction_history', 'gambling_controls', 'help_contact', 'log_out'])

    EXPECTED_RIGHT_MENU = _right_menu(deposit='Deposit',
                                      withdraw='Withdraw',
                                      payment_history='Payment History',
                                      manage_my_cards='Manage My Cards',
                                      sports_free_bets='Sports Free Bets',
                                      sports_promotions='Sports Promotions',
                                      gaming_promotions='Gaming Promotions',
                                      shop_exclusive_promotions='Shop Exclusive Promotions',
                                      voucher_codes='Voucher Codes',
                                      odds_boosts='Super Boosters',
                                      my_bets='My Bets',
                                      my_account_details='My Account Details',
                                      settings='Settings',
                                      connect='Connect',
                                      transaction_history='Transaction History',
                                      gambling_controls='Gambling Controls',
                                      help_contact='Help & Contact',
                                      log_out='LOG OUT')

    # _history_menu = namedtuple('history_menu', ['betting_history', 'transaction_history', 'payment_history'])
    # EXPECTED_HISTORY_MENU = _history_menu(betting_history='BETTING HISTORY',
    #                                       transaction_history='TRANSACTION HISTORY',
    #                                       payment_history='PAYMENT HISTORY')

    FREEBET_INFORMATION = 'MY FREE BETS'
    COOKIES_DESCRIPTION = "By clicking \"Accept All Cookies\", you agree to the storing of cookies on your device to " \
                          "enhance site navigation, analyze site usage, and assist in our marketing efforts. Cookie " \
                          "Notice"

    TIMELINE_TITLE = 'CORAL PULSE'
