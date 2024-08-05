from collections import namedtuple

from voltron.environments.constants.base.bma import BMA


class LadbrokesBMA(BMA):
    """
    src/platforms/ladbrokesMobile/lazy-modules/locale/translations/en-US/bma.lang.ts
    """
    PRICE_BOOST = 'Price Boost'

    SIGN_IN_JOIN = 'Login / Join'

    USER_SETTINGS_HEADING = 'Account Settings'
    USER_SETTINGS_ODDS_FORMAT_LABEL = 'Set odds to'

    USER_SETTINGS_TOUCH_ID_LOGIN_DESCRIPTION = 'Use Touch/Face ID for quick, simple and secure login.'
    USER_SETTINGS_FINGERPRINT_DESCRIPTION = 'Use Fingerprint for quick, simple and secure login.'

    USER_SETTINGS_QUICK_BET = 'Quick Bet'
    USER_SETTINGS_QUICK_BET_DESCRIPTION = 'If your betslip is empty, Quick Bet helps you place quick singles by presenting a betslip as soon as you select a price.'

    BANKING_MENU_HEADING = 'Banking'
    BANKING_MENU_BALANCE = 'Balance:'

    FREE_BET = 'Free Bet'
    FREE_BET_INFO = 'This freebet can be used for'

    GO_BETTING = 'Go Betting'

    EVENT = 'event'
    EVENTS = 'events'
    ANY = 'any'

    _login_dialog = namedtuple('login_dialog', ['header', 'title', 'placeholder_user_name', 'login_button_title',
                                                'register_button_title', 'forgot_details', 'new_to_ladbrokes',
                                                'need_help', 'chat_link', 'login_name', 'login_password',
                                                'login_title'])
    _login_dialog_header = 'Login / Register'
    _login_dialog_title = 'Enter your Ladbrokes username or your GRID card number'
    _login_dialog_placeholder_user_name = 'Username / Card Number'
    _login_dialog_login_button_title = 'LOGIN'
    _login_dialog_register_button_title = 'REGISTER'
    _login_dialog_forgot_details = 'FORGOT LOGIN DETAILS?'
    _login_dialog_new_to_ladbrokes = 'New to Ladbrokes?'
    _login_dialog_need_help = 'Need Help? Start'
    _login_dialog_chat_link = 'Live Chat'
    _login_dialog_login_name = 'Username / Card Number'
    _login_dialog_login_password = 'Password / Pin'
    _login_dialog_login_title = 'Login'
    LOGIN_DIALOG = _login_dialog(header=_login_dialog_header,
                                 title=_login_dialog_title,
                                 placeholder_user_name=_login_dialog_placeholder_user_name,
                                 login_button_title=_login_dialog_login_button_title,
                                 register_button_title=_login_dialog_register_button_title,
                                 forgot_details=_login_dialog_forgot_details,
                                 new_to_ladbrokes=_login_dialog_new_to_ladbrokes,
                                 need_help=_login_dialog_need_help,
                                 chat_link=_login_dialog_chat_link,
                                 login_name=_login_dialog_login_name,
                                 login_password=_login_dialog_login_password,
                                 login_title=_login_dialog_login_title)

    _opt_in_splash_skip_button = 'Not Now, Thanks'

    BYB = 'Bet Builder'
    USER_SETTINGS_ODDS_FORMAT_FRAC = BMA.USER_SETTINGS_ODDS_FORMAT_FRAC.upper()
    USER_SETTINGS_ODDS_FORMAT_DEC = BMA.USER_SETTINGS_ODDS_FORMAT_DEC.upper()

    # right menu  # Old list of right menu
    # EXPECTED_LIST_OF_RIGHT_MENU = ['Banking & Balances', 'Promotions', 'Odds Boosts', 'Sports Free Bets', 'My Bets',
    #                                'Messages', 'History', 'The Grid', 'Settings', 'Gambling Controls', 'Help & Contact',
    #                                'Log Out']
    # BANKING_MENU_ITEMS = ['My Balance', 'Deposit', 'Transfer', 'Withdraw', 'Payment History']
    # PROMOTIONS_MENU_ITEMS = ['Free Bets', 'Odds Boosts', 'Sports Promotions', 'Gaming Promotions']
    # HISTORY_MENU_ITEMS = ['Betting History', 'Payment History', 'Transactions History']
    # THE_GRID_MENU_ITEMS = ['The Grid Home', 'Join Grid', 'My Payout Settings', 'Shop Locator']
    # SETTINGS_MENU_ITEMS = ['My Account Details', 'Change Password', 'Communication Preferences', 'Betting Settings']
    # GAMBLING_CONTROLS_MENU_ITEMS = ['Spending Controls', 'Time Management', 'Account Closure & Reopening']
    # LIST_OF_HELP_AND_CONTACT = ['Account Access', 'Promotions and Bonuses', 'Sports Rules', 'Bingo', 'Poker', 'Casino',
    #                             'Deposit', 'Withdrawal', 'Account Details and Verification', 'eSports',
    #                             'Virtual Sports', 'Ladbrokes Exchange', 'Retail and Connect Cards', 'Unable to Play',
    #                             'Responsible Gaming']

    CHANGE_PASSWORD = 'Change Password'
    COMMUNICATION_PREFERENCES = 'Communication Preferences'
    BETTING_SETTINGS = 'Betting Settings'
    SECURITY = 'Security'
    APP_SETTINGS = 'App Settings'
    COOKIES_SETTINGS = 'Cookies Settings'
    TWO_FACTOR_AUTHENTICATION = 'Two-Factor Authentication'

    SETTINGS_MENU_ITEMS = [CHANGE_PASSWORD, COMMUNICATION_PREFERENCES, TWO_FACTOR_AUTHENTICATION, BETTING_SETTINGS]

    MY_INBOX = 'My Inbox'
    MY_BALANCE_MENU_ITEMS = ['Withdrawable - Online:', 'Available balance:', 'Total balance:']

    ACCOUNT_CLOSURE_AND_REOPENING_PAGE_TITLE = 'Ladbrokes Sports Betting - Football, Horse Racing and more!'
    ACCOUNT_CLOSURE_AND_REOPENING_INFO_TEXT = 'Successfully closed: Sports, Bingo, Casino, Poker'

    # New list of right menu
    _right_menu = namedtuple('right_menu', ['deposit', 'withdraw', 'transfer_to_from_exchange', 'payment_history',
                                            'manage_my_cards', 'sports_promotions',
                                            'gaming_promotions', 'free_bets', 'odds_boosts', 'my_bets',
                                            'my_account_details', 'settings', 'transaction_history',
                                            'the_grid', 'gambling_controls', 'help_contact', 'log_out'])

    EXPECTED_RIGHT_MENU = _right_menu(deposit='Deposit',
                                      withdraw='Withdraw',
                                      transfer_to_from_exchange='Transfer to/from Exchange',
                                      payment_history='Payment History',
                                      manage_my_cards='Manage My Cards',
                                      sports_promotions='Sports Promotions',
                                      gaming_promotions='Gaming Promotions',
                                      free_bets='Free Bets',
                                      odds_boosts='Odds Boosts',
                                      my_bets='My Bets',
                                      my_account_details='My Account Details',
                                      settings='Settings',
                                      transaction_history='Transaction History',
                                      the_grid='The Grid',
                                      gambling_controls='Gambling Controls',
                                      help_contact='Help & Contact',
                                      log_out='LOG OUT')

    # _history_menu = namedtuple('history_menu', ['betting_history', 'transaction_history', 'payment_history'])
    # EXPECTED_HISTORY_MENU = _history_menu(betting_history='Betting History',
    #                                       transaction_history='Transactions History',
    #                                       payment_history='Payment History')

    FREEBET_INFORMATION = 'FREE BET'

    COOKIES_DESCRIPTION = "By clicking \"Accept All Cookies\", you agree to the storing of cookies on your device to " \
                          "enhance site navigation, analyze site usage, and assist in our marketing efforts. Cookie " \
                          "Notice"

    TIMELINE_TITLE = 'LADBROKES LOUNGE'
    CONTACT_US = 'Help & Contact'

    # New list of free ride Pots
    _free_ride_pots = namedtuple('free_ride_pots',
                                 ['TopPlayer_BigStrong_GoodChance',
                                  'TopPlayer_BigStrong_NicePriceSurpriseMe',
                                  'TopPlayer_SmallNimbleSurpriseMe_GoodChance',
                                  'TopPlayer_SmallNimbleSurpriseMe_NicePriceSurpriseMe',
                                  'DarkHorseSurpriseMe_BigStrong_GoodChance',
                                  'DarkHorseSurpriseMe_BigStrong_NicePriceSurpriseMe',
                                  'DarkHorseSurpriseMe_SmallNimbleSurpriseMe_GoodChance',
                                  'DarkHorseSurpriseMe_SmallNimbleSurpriseMe_NicePriceSurpriseMe'])

    EXPECTED_FREE_RIDE_POTS = _free_ride_pots(TopPlayer_BigStrong_GoodChance=0,
                                              TopPlayer_BigStrong_NicePriceSurpriseMe=1,
                                              TopPlayer_SmallNimbleSurpriseMe_GoodChance=2,
                                              TopPlayer_SmallNimbleSurpriseMe_NicePriceSurpriseMe=3,
                                              DarkHorseSurpriseMe_BigStrong_GoodChance=4,
                                              DarkHorseSurpriseMe_BigStrong_NicePriceSurpriseMe=5,
                                              DarkHorseSurpriseMe_SmallNimbleSurpriseMe_GoodChance=6,
                                              DarkHorseSurpriseMe_SmallNimbleSurpriseMe_NicePriceSurpriseMe=7)
