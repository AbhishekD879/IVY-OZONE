from collections import namedtuple


class BMA(object):
    """
    src/app/lazy-modules/locale/translations/en-US/bma.lang.ts
    """
    JOIN_US = 'Join'
    JOIN_NOW = 'Join Now'
    SIGN_IN = 'Log In'
    SIGN_IN_BET = 'Log In & Place Bet'
    LOGIN = 'Login'

    _video_stream_register = namedtuple('video_stream_register', ['part1', 'part2', 'part3'])
    _video_stream_register_part1 = ' or '
    _video_stream_register_part2 = 'Register'
    _video_stream_register_part3 = ' to watch live streams now'
    VIDEO_STREAM_REGISTER = _video_stream_register(part1=_video_stream_register_part1,
                                                   part2=_video_stream_register_part2,
                                                   part3=_video_stream_register_part3)

    LOGIN_ERROR = 'Incorrect details. Please check and try again.'
    LOGIN_RETAIL_ERROR = 'Please use your username and password to log in'
    CHANGE_PASSWORD_COMMON_ERROR = 'Authentication error'
    BLOCKED_ACCOUNT = 'Please contact Customer Support. We apologise for any inconvenience caused.'
    FROZEN_OR_DUPLICATE_ACCOUNT = 'It appears you may already have an account with us. ' \
                                  'If you cannot remember your Username or Password, please click on \'Forgot Username?\' or \'Forgot Password?\' below or contact ' \
                                  'Customer Support'
    FRAUDULENT = 'Please contact Customer Support. We apologise for any inconvenience caused.'
    INCORRECT_PASSWORD = 'Incorrect old password'
    PASSWORD_USED = 'Password has already been used recently.'
    UNKNOWN_PLAYER = 'Unknown player'
    INVALID_EMAIL = 'Not valid user email'
    INVALID_BIRTH_DATE = 'Not valid birth date'
    TIMEOUT_ERR = 'Could not connect to the server. Please Try again.'
    NO_UNIQUE = 'No unique player was found.'
    HELP = 'Help'
    DOWNLOAD_CORAL_APPS = 'Download Coral Apps'
    SHOW_BALANCE = 'Show Balance'
    HIDE_BALANCE = 'Hide Balance'
    FREE_BETS_DESC = 'Free Bets Token Description'
    FREE_BETS = 'Free Bet'
    BINGO_BONUS = 'Bingo bonus'
    CASINO_PLAYABLE = 'Casino Playable Balance'
    TOKENS = 'Tokens'
    TOKEN = 'Token'
    FREE_BETS_TOTAL = 'Free Bets Token Total:'
    EXPIRES = 'Expires'
    OK = 'Ok'
    NO_FREE_BETS = 'No Free Bets Available'
    BET_NOW = 'Bet Now'

    NO_DATA = 'No Data'
    NO_DATA_MSG = 'No data found'
    OTHER = 'Other...'
    SELECT_VALUE = 'Please select a limit'
    NONE = 'None'
    HOUR = '%1 Hour'
    HOURS = '%1 Hours'
    AFTER_REGISTRATION_OVERLAY_TITLE = 'Deposit Limit'
    AFTER_REGISTRATION_OVERLAY_WELCOME_USER = 'Welcome {username} to Coral'
    AFTER_REGISTRATION_OVERLAY_ERROR_TITLE = 'Error in case of setting Deposit Limits or Game Play Reminder'
    AFTER_REGISTRATION_OVERLAY_ERROR_BODY = 'You can set Deposit Limits and Game Play Reminder in My Account - Limits page.'
    I_WOULD_LIKE_SET_DEPOSIT_LIMITS = 'I would like to Set Deposit Limits'
    LCCP_DEPOSIT_LIMITS_TITLE = 'If you would like to set your deposit limits, please enter amount below'
    DEPOSIT_LIMITS_CONTEXT = 'If you would like to set your deposit limits, please enter amount below'
    SET_LIMITS_BTN = 'Set my deposit limits'
    CONFIRM_BTN = 'Confirm'
    CLOSE_BTN = 'Close'

    TO_CORAL = 'New to Coral?'
    OR = 'or'
    CREATE_USER = 'Join us here'
    RESET_PASSWORD_LINK = 'Reset Password?'
    FORGOT_USERNAME = 'I forgot my Username'
    FORGOT_PASSWORD = 'I forgot my Password'
    FORGOT_DETAILS = 'Forgot login details?'
    LOGIN_SUCCESS = 'Sign In successful'
    REMEMBER_ME = 'Remember me'
    REMEMBER_NAME_CARD = 'Remember username or Connect Card number'
    REMEMBER_NAME = 'Remember username'
    DEPOSIT = 'Deposit'
    SELECT_A_DEPOSIT_METHOD = 'Select a deposit method'
    POPULAR_PAYMENT_METHODS = 'Popular Payment Methods'
    FORGOTTEN_PASSWORD_TEXT = 'FORGOTTEN PASSWORD'
    RESET_PASSWORD_MAIL_TEXT = 'Password reset email sent\nIf you don’t see the email in your inbox, please check ' \
                               'your spam or junk folder.'
    RESET_MAIL_TXT = 'We have sent an email to t*******@internalgvc.com with details on how to reset your password. If it doesn\'t arrive in a few minutes, check your spam folder'
    MY_ACC_DEPOSIT = 'DEPOSIT'
    MY_ACC_WITHDRAW = 'WITHDRAW'
    MY_ACC_ADDNEWPAYMENTTYPE = 'ADD NEW PAYMENT TYPE'
    MY_ACC_VOUCHERCODE = 'VOUCHER CODE'
    MY_ACC_BETHISTORY = 'BET HISTORY'
    MY_ACC_TRANSACTIONHISTORY = 'TRANSACTION HISTORY'
    MY_ACC_GAMINGHISTORY = 'GAMING HISTORY'
    MY_ACC_LIMITS = 'LIMITS'
    MY_ACC_CHANGEPASSWORD = 'CHANGE PASSWORD'
    MY_ACC_RESPONSIBLEGAMBLING = 'SAFER GAMBLING'
    OTHER_PAYMENT_OPTIONS = 'More Payment options'

    RIGHT_MENU_DEPOSIT = 'DEPOSIT'
    RIGHT_MENU_WITHDRAW = 'WITHDRAW'
    RIGHT_MENU_CANCELWITHDRAWAL = 'CANCEL WITHDRAWAL'
    RIGHT_MENU_MY_ACCOUNT = 'MY ACCOUNT'
    RIGHT_MENU_BETHISTORY = 'BET HISTORY'
    RIGHT_MENU_SETTINGS = 'SETTINGS'
    RIGHT_MENU_CONTACTUS = 'CONTACT US'
    RIGHT_MENU_LOGOUT = 'LOG OUT'

    # my balance items
    RIGHT_MENU_MY_BALANCE = 'MY BALANCE'
    MY_BALANCE_MENU_ITEMS = ['WITHDRAWABLE - ONLINE:', 'RESTRICTED', 'AVAILABLE BALANCE:', 'TOTAL BALANCE:']
    EXPECTED_MY_BALANCE_FOOTER_ITEMS_LIST = ['AVAILABLE TO USE ON:', 'SPORTS', 'CASINO', 'POKER', 'BINGO']
    FALLERS_INSURANCE = 'Faller\'s Insurance'
    BEATEN_BY_LENGTH = 'Beaten by a Length'
    EXTRA_PLACE = 'Extra Place'
    PRICE_BOOST = 'Smart Boost'
    MONEY_BACK = 'Money Back'
    DOUBLE_WINNINGS = 'Double Your Winnings'
    YOUR_CALL = 'Your call'
    ACCA_INSURANCE = 'Acca Insurance'
    CONTACT_US = 'Help and Contact'
    AZ_SPORTS = 'AZ Sports'
    CRICKET = 'Cricket'
    EMAIL = 'Email'
    EMAIL_ADDRESS = 'Email Address'
    REMIND_ME = 'Remind Me'
    GAMING = 'Gaming'
    GREYHOUNDS = 'Greyhounds'
    IN_PLAY = 'In-Play'
    LIVE_STREAM = 'Live Stream'
    SPORTS = 'Sports'
    GAME = 'Games'
    BETSLIP = 'Betslip'
    USER_NAME = 'Username'
    RESET_PASSWORD = 'Reset Password'
    FORGOT_USERNAME_TITLE = 'Forgot Username'
    RESPONSIBLE_GAMBLING = 'Responsible Gambling Policy'
    SNOOKER = 'Snooker'
    TENNIS = 'Tennis'

    SIGN_UP_TITLE = 'Registration'
    SIGN_UP_STEP = 'Step '
    SIGN_UP_TITLE_OF = ' of 2'
    MOBILE_SIGN_UP_TITLE_OF = ' of 3'
    PERSONAL_SECTION = 'Personal Section'
    PERSONAL_DETAILS = 'Personal Details'
    SOCIAL_STATUS = 'Title'
    FIRST_NAME = 'First Name'
    LAST_NAME = 'Last Name'
    BIRTH_DATE = 'Date of Birth'
    BIRTH_DATE_DAY = 'Day'
    BIRTH_DATE_MONTH = 'Month'
    BIRTH_DATE_YEAR = 'Year'
    GOOD = 'Good News!'
    PROTECT_MSG = 'We hold your money in am independent trust account to ensure that it is completely protected. ' \
                  'This meets the UK Gambling Commission\'s requirement for the protection of customer funds at the high level of protection. ' \
                  'For more information you can visit the UK Gambling Commission ' \
                  '<a href=\'http://www.gamblingcommission.gov.uk/Consumers/Protection-of-customer-funds.aspx\' target=\'_blank\'>here.</a>'
    CONTINUE = 'Continue'

    PASSWORD_CHANGE_DIALOGUE_HEADER = 'Change Password'
    PASSWORD_CHANGE_DIALOGUE_MESSAGE = 'Use the form below to change your password'
    PASSWORD_CHANGE_CHANGE_BUTTON = 'Change Password'
    PASSWORD_CHANGE_NEW_PASSWORD_VERIFY = 'Confirm New Password'
    TEMP_PASSWORD = 'Temporary Password'
    TYPE_PASSWORD = 'Type Password'
    OLD_PASSWORD = 'Old Password'
    PASSWORD_CHANGE_USER_NEW_PASSWORD = 'New Password'

    TERMS_AND_CONDITIONS_VIEW_TERMS = 'View Terms'
    TERMS_AND_CONDITIONS_TAC_TEASER = 'Our Terms and Conditions have changed to reflect the fact that our services to customers ' \
                                      'in the UK are now offered under a Licence issued by the UK Gambling Commission. The revised terms and conditions are below. ' \
                                      'Please acknowledge this change by clicking OK'
    TERMS_AND_CONDITIONS_DIALOGUE_HEADER = 'Terms &amp; Conditions'
    TERMS_AND_CONDITIONS_OK = 'OK'

    ERROR = 'Error'
    ERROR_OCCURRED = 'An error has occurred, Please try again later or contact Customer Support.'
    APOLOGIES = 'Apologies'
    BANNED_COUNTRY = 'Unfortunately Coral is not yet available in your country.'
    INVALID_PASSWORD = 'Your password is invalid. Please try again'

    _vip_level_names = namedtuple('vip_level_names', ['eleven', 'twelve', 'thirteen', 'fourteen'])
    _vip_level_names_eleven = 'BRONZE'
    _vip_level_names_twelve = 'SILVER'
    _vip_level_names_thirteen = 'GOLD'
    _vip_level_names_fourteen = 'PLATINUM'
    VIP_LEVEL_NAMES = _vip_level_names(eleven=_vip_level_names_eleven,
                                       twelve=_vip_level_names_twelve,
                                       thirteen=_vip_level_names_thirteen,
                                       fourteen=_vip_level_names_fourteen)

    MY_ACCOUNT = 'My Account'
    LOGGED_TIME = 'Logged in time:'
    CASH_BALANCE = 'Cash Balance'
    W_BACK = 'Welcome back'
    OPEN_BETS = 'Open Bets'
    LOG_OUT = 'Log Out'

    CANCEL = 'Cancel'
    FIND_BTN = 'Find'
    NEXT_STEP = 'Go to Step 2'
    NEXT_STEP_MOBILE = 'Next Step'
    SUBMIT = 'Complete Registration'
    PREV_STEP = 'Step 1'
    VIEW_FULL_RACE = 'View Full Race Card'

    TERMS_AND_CONDITIONS_LABEL = 'Terms &amp; Conditions'
    TERMS_AND_CONDITIONS_TEXT = 'I confirm that I am at least 18 years of age and that I accept the %1 (incorporating the Privacy Policy) ' \
                                'and Age Verification Policy as published on this site.'
    TERMS_AND_CONDITIONS_ON_STEP_1_AND_2 = 'In order to complete registration, you will be required to confirm that you are at least 18 years ' \
                                           'of age and that you accept the %1 (incorporating the Privacy Policy) and Age Verification Policy as published on this site.'

    LOGIN_NAME = 'Username'
    LOGIN_NAME_CARD = 'Enter your Coral online username or your Connect Cаrd numbеr'
    LOGIN_PASSWORD = 'Password'
    LOGIN_PASSWORD_PIN = 'Password or 4-digit pin'
    ADDRESS = 'Address'
    COUNTRY = 'Country of Residence'
    POSTCODE = 'Postcode'
    POSTCODE_UK = 'UK Postcode'
    UK_POST_CODE_ERROR = 'There are no any addresses by entered postcode'
    MANUAL_ADDRESS = 'Please %1 to enter your address manually'
    CLICK_HERE = 'click here'
    ADDRESS_1 = 'Address line 1'
    ADDRESS_2 = 'Address line 2'
    ADDRESS_3 = 'Address line 3'
    CITY = 'City/Town'
    CONTACT_DETAILS = 'Сontact Details'
    MOBILE = 'Mobile Number'
    EMAIL_VERIFICATION = 'Confirm Email'
    USERNAME_PASSWORD = 'Username/Password'
    USER_PASSWORD = 'Password'
    PASSWORD_VERIFY = 'Confirm Password'
    CURRENCY = 'Currency'
    DEPOSIT_LIMIT = 'Deposit Limit'
    MARKETING_MESSAGES = 'Marketing Messages'
    MARKETING_MESSAGES_TEXT = 'I would like to receive free bets and exciting offers from Coral.co.uk'
    ENTER_ADDRESS_MANUALLY = 'Enter address manually'
    ACCOUNT_DETAILS = 'Account Details'

    SUCCESS = 'Success'
    SUCCESS_MESSAGE = 'You was registered successful! Please check your e-mail.'
    USERNAME_SUCCESS_MESSAGE = 'Your Username has been sent to your registered email address. Please remember to check your Spam/Junk folder.'
    RESET_PASSWORD_SUCCESS_MESSAGE = 'A new password has been sent to your registered email address. ' \
                                     'Please remember to check your Spam/Junk folder.'
    PASSWORD_CHANGE_SUCCESS = 'Your password has been changed successfully.'

    LOGGED_OUT_BY_SERVER_TITLE = 'Logged Out'
    LOGGED_OUT_BY_SERVER_MESSAGE = 'You have been logged out.'

    ERROR_MESSAGE = 'An internal error occurred within the back end system. Contact Coral for more information.'
    LOGIN_TO_SEE_CASHOUT_MESSAGE = 'Please log in to see your Cash Out bets.'
    ERROR_SERVICE_DEPARTMENT_MESSAGE = 'If this problem persists, contact our '
    ERROR_SERVICE_DEPARTMENT_LINK = 'Customer Service Department'
    SERVER_ERROR = 'Server is unavailable at the moment, please try again later.'

    SIGNUP_TOOLTIP_INFO = 'Information'
    SIGNUP_TOOLTIP_DEPOSIT_LIMIT = 'Deposit limits must be positive, larger than £0.01, have a maximum of two decimals and maximum 7 digits.'

    VALIDATOR_TOOLTIPS_EQUAL_TO_EMAIL_VERIFICATION = 'The email address entered is different from the one above or previous entry is not valid, ' \
                                                     'please correct this.'
    VALIDATOR_TOOLTIPS_EQUAL_TO_PASSWORD_VERIFY = 'Sorry, password does not match the previous entry or previous entry is not valid, please retry.'
    VALIDATOR_TOOLTIPS_NOT_EQUAL_USER_PASSWORD = 'Your new password should not be same as old one.'

    VALIDATOR_TOOLTIPS_DEPOSIT_LIMITS_DAILY = 'The Daily limit must be lower than the weekly and monthly limit.'
    VALIDATOR_TOOLTIPS_DEPOSIT_LIMITS_WEEKLY = 'The Weekly limit must be higher than the daily limit and lower than the monthly limit.'
    VALIDATOR_TOOLTIPS_DEPOSIT_LIMITS_MONTHLY = 'The Monthly limit must be higher than the daily limit and higher than the weekly limit.'
    VALIDATOR_TOOLTIPS_DEPOSIT_LIMITS_DEPOSIT_LIMIT = 'Sorry, invalid character used or too high value (must be 0-99,000).'
    VALIDATOR_TOOLTIPS_DEPOSIT_LIMITS_MIN_DEPOSIT_LIMIT = 'Please enter an amount greater than '

    VALIDATOR_TOOLTIPS_DATE_FORMAT_INVALID_ENTRY = 'Invalid entry, please provide an accurate date of birth.'
    VALIDATOR_TOOLTIPS_DATE_FORMAT_NO_ENTRY = 'Please provide your date of birth'
    VALIDATOR_TOOLTIPS_DAY_FORMAT_NO_ENTRY = 'Please provide your day of birth'
    VALIDATOR_TOOLTIPS_ADULT_AGE = 'You must be over 18 to create an account'
    VALIDATOR_TOOLTIPS_EMAIL = 'Please enter a valid email address.'
    VALIDATOR_TOOLTIPS_USERNAME_UNAVAILABLE = 'Username you entered is already in use. Please enter a different username, ' \
                                              'or select one of the following proposed.'
    VALIDATOR_TOOLTIPS_OTHER = 'Other...'
    EMAIL_ALREADY_EXISTS_MESSAGE = 'It appears you may already have an account with us. If you cannot remember your Username or Password, ' \
                                   'please click on \'Forgot Username?\' or \'Forgot Password?\' below'

    VALIDATOR_TOOLTIPS_REQUIRED_USER_PASSWORD = 'Please enter your password.'
    VALIDATOR_TOOLTIPS_REQUIRED_PASSWORD_VERIFY = 'Please enter your password again.'
    VALIDATOR_TOOLTIPS_REGEXP_USER_NAME = 'Sorry, invalid username is entered (must be 6-32 characters long, using A-Z, a-z, 0-9, -, _). ' \
                                          'Please try again.'
    VALIDATOR_TOOLTIPS_REGEXP_USER_PASSWORD = 'Sorry, invalid password is entered (must be 6-10 characters long, ' \
                                              'using A-Z, a-z, 0-9, - ! ^ * ( ) _ + ). Please try again.'
    VALIDATOR_TOOLTIPS_REGEXP_PASSWORD_VERIFY = 'Sorry, invalid password is entered (must be 6-10 characters long, ' \
                                                'using A-Z, a-z, 0-9, - ! ^ * ( ) _ + ). Please try again.'
    VALIDATOR_TOOLTIPS_REQUIRED_EMAIL = 'Please enter email address.'
    VALIDATOR_TOOLTIPS_REQUIRED_USER_NAME = 'Please enter your username.'

    USER_SETTINGS_HEADING = 'Preferences'
    USER_SETTINGS_ODDS_FORMAT_LABEL = 'Select Odds Format'
    USER_SETTINGS_ODDS_FORMAT_FRAC = 'Fractional'
    USER_SETTINGS_ODDS_FORMAT_DEC = 'Decimal'
    USER_SETTINGS_TOUCH_ID_LOGIN = 'Touch/Face ID Login'
    USER_SETTINGS_FINGERPRINT_LOGIN = 'Fingerprint login'
    USER_SETTINGS_TOUCH_ID_LOGIN_ENABLED = 'Enabled'
    USER_SETTINGS_TOUCH_ID_LOGIN_DISABLED = 'Disabled'
    USER_SETTINGS_DIAGNOSTICS = 'Diagnostics'
    USER_SETTINGS_SEND_REPORT = 'Send report'
    USER_SETTINGS_QUICK_BET = 'Allow Quick Bet'

    FREEBETS_EXPIRY_MESSAGE = 'You have a free bet which is due to expire in'
    FREEBETS_AVAILABLE_MESSAGE = 'You have a free bet available !'
    FREEBETS_EXPIRY_HOURS = 'hours'
    FREEBETS_EXPIRY_MINS = 'mins'
    FREEBETS = 'My Freebets/Bonuses'
    FREEBET_DETAILS = 'Freebet Information'
    NO_FREE_BETS_FOUND = 'You currently have no Free Bets'
    CASH_BALANCE_FREE_BET = 'Cash Balance = '
    TOTAL_BALANCE = 'Total Balance = '
    FREE_BETS_NAME = 'Free Bets'
    FREE_BET_NAME = 'FreeBet'
    ADD_FREE_BET = 'Add'
    USE_BY = 'Use by = '
    EXPIRES_FREE_BETS = 'Expires = '

    SESSION_TIME_LIMIT = 'Session Time Limit'
    HI = 'Hi'
    ABOUT_TO_EXPIRE_WARN_MESSAGE = ' The session limit you selected will take effect in 5 minutes. ' \
                                   'Please note that you will be logged out at that time.'
    HOURLY_NOTIFICATION = 'Hourly Notification'
    HOURLY_NOTIFICATION_MESSAGE = 'This is your hourly notification.'

    TODAY = 'Today'
    TOMORROW = 'Tomorrow'
    MORE_INFORMATION = 'More information'
    MORE_INFO = 'More Info'
    ACCEPT = 'Accept & close'

    DEPOSIT_NOTIFICATION_HI = 'Hi '
    DEPOSIT_NOTIFICATION_TITLE = 'Quick Deposit'
    DEPOSIT_NOTIFICATION_1 = 'You currently have '
    DEPOSIT_NOTIFICATION_2 = ' in your account.'
    DEPOSIT_NOTIFICATION_BTN = 'Deposit Now'
    DEPOSIT_LIMITS_TITLE = 'You Have A Pending Deposit Limit Increase'

    DEPOSIT_NOTIFICATION_LIMIT_DECLINE = 'Decline'

    DEPOSIT_NOTIFICATION_LIMIT_1 = 'Click '
    DEPOSIT_NOTIFICATION_LIMIT_CONFIRM = 'Confirm '
    DEPOSIT_NOTIFICATION_LIMIT_3 = 'to confirm the new deposit limits:'
    DEPOSIT_NOTIFICATION_LIMIT_4 = 'Clicking on '
    DEPOSIT_NOTIFICATION_LIMIT_CANCEL = 'Cancel '
    DEPOSIT_NOTIFICATION_LIMIT_5 = 'will void the pending limits.'

    DEPOSIT_DAILY = 'Daily'
    DEPOSIT_WEEKLY = 'Weekly'
    DEPOSIT_MONTHLY = 'Monthly'

    VERIFICATION_BTN = 'Verify Me Now!'
    VERIFICATION_TITLE = 'Verify Your Account'
    VERIFICATION_BODY_PART_1 = 'We just need a few details'
    VERIFICATION_BODY_PART_2 = 'Due to our licensing commitments and for the safety of all our customers we are required to'
    VERIFICATION_BODY_PART_2A = 'verify all players'
    VERIFICATION_BODY_PART_2B = 'on our system.'
    VERIFICATION_BODY_PART_3 = 'Unfortunately we have not been able to verify your details'
    VERIFICATION_BODY_PART_3A = ' and therefore your account has been temporarily suspended'
    VERIFICATION_BODY_PART_4 = 'Using your device you can quickly and safely upload a photo of your driving lisence or ID document(s) through our secure service so that we can'
    VERIFICATION_BODY_PART_4A = 'complete your verification'
    VERIFICATION_BODY_PART_4B = ' and reactivate your account'
    VERIFICATION_BODY_PART_5 = 'This will prevent your account from being disabled.'

    SELF_EXCLUSION = 'Self Exclusion'
    SET_DEPOSIT = 'SET DEPOSIT LIMITS'
    SELF_EXCLUSION_INFO = 'Self-exclusion is a formal process whereby you request us to prevent you from being able to access ' \
                          'your online account for a specified period between 12 months and 5 years. Under such an agreement, we will \'close\' ' \
                          'any accounts you hold with us.'
    SELF_EXCLUSION_URI_TEXT = 'READ MORE ABOUT SELF EXCLUSION'
    SELF_EXCLUSION_FORM_URI = 'REQUEST A SELF EXCLUSION FORM'
    SELF_EXCLUDE_FORM = 'Request Self-Exclusion'
    SELF_EXCLUSION_TITLE = 'More About Self Exclusion'
    SELF_EXCLUSION_BTN = 'Click here'
    SELF_EXCLUSION_CONFIRM = 'to confirm that you wish to Self-Exclude.'
    SELF_EXCLUSION_SELECT_HEADER = 'Please select how long you would like to Self-Exclude for:'
    SELF_EXCLUSION_INPUT_HEADER = 'In order to complete Self-Exclusion, please provide your password:'
    CHOOSE_PERIOD = 'Choose Self Exclusion Period'
    CORAL = 'Coral'
    GALA_CORAL_INTERACTIVE = 'Gala Coral Interactive'
    DOWNLOAD = 'Download'
    MESSAGE_MAINTENANCE = 'Oops! Apologies, something went wrong. Click below to reload the page.'
    REFRESH = 'Reload'
    RETRY = 'Retry'
    CALL_TO_ACTION = 'Call To Action'
    NO_LOGIN = 'You must log in to view this page.'
    NO_PROMO = 'Promotion is expired or unavailable'

    LOGGED_OUT = 'You Are Logged Out'
    LOGGED_OUT_TITTLE = 'Sorry your session appears to have expired. Please login again.'
    LOGGED_OUT_TITTLE_SESSION_LIMIT = 'Your session has expired. Your current session time limit is set at %1 minutes. Please login again.'

    MOBENGA_UPGRADE_DIALOG_TITLE = 'Application Upgrade'
    COPY = 'Copy'
    COPIED = 'Copied'
    NOT_COPIED = 'Not copied'
    NEED_HELP = 'Need help?'

    INTERNET_ERROR = 'No internet connection'
    CONNECTION_LOST_MESSAGE = 'You are currently experiencing issues connecting to the internet. Please check your internet connection and try again.'
    ASYNC_OPENING_MESSAGE = 'Please wait while you are being redirected...'

    _v2_header = namedtuple('v2_header', ['balance', 'quick_deposit', 'bet_slip', 'account'])
    _v2_header_balance = 'Balance'
    _v2_header_quick_deposit = 'Quick Deposit'
    _v2_header_bet_slip = 'Bet Slip'
    _v2_header_account = 'Account'
    V2_HEADER = _v2_header(balance=_v2_header_balance,
                           quick_deposit=_v2_header_quick_deposit,
                           bet_slip=_v2_header_bet_slip,
                           account=_v2_header_account)

    ACCEPT_BONUS = 'ACCEPT'
    DECLINE_BONUS = 'DECLINE'
    BONUS_TITLE = 'Congratulations!'
    NO = 'No'
    BONUS_MESSAGE = 'Hi {name}, {msg}'
    ACCEPT_BTN = 'Accept'
    DECLINE_BTN = 'Decline'

    FUNCTIONALITY_DISABLED = 'This functionality is disabled.'
    SHOW_PASSWORD = 'Show'
    HIDE_PASSWORD = 'Hide'
    BACK = 'Back'

    CALL_FROM_UK = 'Call from UK'
    CALL_NOT_FROM_UK = 'Call from outside UK'
    MARKETING_PREFERENCES = 'Marketing Preferences'

    OFFERING_UPDATE_TYPES_CAPTION = 'We don’t want you to miss out on our latest prices, live betting updates and free bet offers. ' \
                                    'By ticking the boxes below, you’ll be kept informed of all our offerings. Your selections will automatically be saved.'
    GROUP_OF_BRANDS_CAPTION = 'Coral is a brand within the Ladbrokes Coral Group. Our group of brands offer online and offline sports betting, ' \
                              'casino, bingo and gaming services. If you would like to receive information and promotional offers from any of the other ' \
                              'brands within our Group, please select below = '
    ALL = 'All'
    SUBMIT_BTN = 'Submit'
    REG_OFFERING_TYPES_CAPTION = 'Receive communication via:'
    SAVE_PREFERENCES_BTN = 'Save my preferences'

    _brands = namedtuple('brands', ['ladbrokes', 'bingo', 'casino', 'spins'])
    _brands_ladbrokes = 'Ladbrokes'
    _brands_bingo = 'Gala Bingo'
    _brands_casino = 'Gala Casino'
    _brands_spins = 'Gala Spins'
    BRANDS = _brands(ladbrokes=_brands_ladbrokes,
                     bingo=_brands_bingo,
                     casino=_brands_casino,
                     spins=_brands_spins)

    _opt_in_splash = namedtuple('opt_in_splash', ['opt_in_button', 'skip_button', 'footer_note'])
    _opt_in_splash_opt_in_button = 'Opt In'
    _opt_in_splash_skip_button = 'No Thanks'
    _opt_in_splash_footer_note = 'Update your settings at any time in Account Preferences.'
    OPT_IN_SPLASH = _opt_in_splash(opt_in_button=_opt_in_splash_opt_in_button,
                                   skip_button=_opt_in_splash_skip_button,
                                   footer_note=_opt_in_splash_footer_note)

    PREFERENCES_ERROR = 'Sorry, we couldn\'t save your selected preferences. Please try again.'
    HIDE = 'Hide'
    SHOW = 'Show'

    YES = 'Yes'
    GAME_PLAY_REMINDER = ' Game play Reminder'
    DEPOSIT_LIMIT_LINK = 'Deposit Limit '
    IMPORTANT = 'Important'
    BYB = 'Build your Bet'

    _country_restriction = namedtuple('country_restriction', ['header', 'racing_message_body', 'lotto_message_body',
                                                              'jackpot_message_body'])
    _country_restriction_header = 'Country Restriction'
    _country_restriction_racing_message_body = 'We are unable to offer Horse Racing or Greyhound betting in your jurisdiction.'
    _country_restriction_lotto_message_body = 'We are unable to offer Lotto betting in your jurisdiction'
    _country_restriction_jackpot_message_body = 'We are unable to offer Football Jackpot betting in your jurisdiction'
    COUNTRY_RESTRICTION = _country_restriction(header=_country_restriction_header,
                                               racing_message_body=_country_restriction_racing_message_body,
                                               lotto_message_body=_country_restriction_lotto_message_body,
                                               jackpot_message_body=_country_restriction_jackpot_message_body)

    _otf = namedtuple('otf', ['btn_processing', 'bundle_loading', 'cancel_login', 'login_to_play', 'no_content',
                              'play_now', 'bundle_loading_error_msg', 'bundle_loading_error_btn'])
    _otf_btn_processing = 'Processing...'
    _otf_bundle_loading = 'Loading...'
    _otf_cancel_login = 'Cancel'
    _otf_login_to_play = 'Login to play'
    _otf_no_content = 'No content provided'
    _otf_play_now = 'Play Now'
    _otf_bundle_loading_error_msg = 'Sorry, we are having some technical issues. Please try again soon.'
    _otf_bundle_loading_error_btn = 'GO BACK'
    OTF = _otf(btn_processing=_otf_btn_processing,
               bundle_loading=_otf_bundle_loading,
               cancel_login=_otf_cancel_login,
               login_to_play=_otf_login_to_play,
               no_content=_otf_no_content,
               play_now=_otf_play_now,
               bundle_loading_error_btn=_otf_bundle_loading_error_btn,
               bundle_loading_error_msg=_otf_bundle_loading_error_msg)

    OTF_PAGE_TITLE = '1-2-Free'
    MINI_GAMES_ERROR = 'Mini Games currently unavailable, please try again later.'

    DEPOSIT_LIMIT_OPTION = 'Deposit Limits'
    TIME_MANAGEMENT_OPTION = 'Time Management'
    TIME_MANAGEMENT_TEXT = 'Control how long you spend gaming and get notified once your time limit is reachedYou can change your settings at any time'
    ACCOUNT_CLOSURE_AND_REOPENING_OPTION = 'Account Closure & Reopening'
    GAMBLING_CONTROLS = 'Gambling Controls'
    RESPONSIBLE_GAMING = 'RESPONSIBLE GAMING'
    HELP_GENERAL = 'GENERAL INFORMATION'

    ACCOUNT_CLOSURE_SECTIONS = ['Bingo', 'Casino', 'Poker', 'Sports']
    TIME_LIMIT_OPTIONS = ['15 Minutes ', '30 Minutes ', '45 Minutes ', '60 Minutes ', 'None ']
    YOUTUBE = 'youtube'
    TWITTER = 'twitter'
    FACEBOOK = 'facebook'

    LIST_OF_HELP_AND_CONTACT = ['Account Access', 'Casino', 'Promotions and Bonuses', 'Bingo', 'Poker', 'Deposit', 'Withdrawal', 'Account Details and Verification', 'eSports', 'Sports Rules', 'Virtual Sports', 'Retail', 'Responsible Gaming', 'Unable to Play']
    LIVE_CHAT_TEXT = "You're one step away from talking to one of our experts, they'll be with you shortly."
    LIVE_CHAT_PAGE_OPTIONS = ['Live Chat', 'Email', 'Visit Our Help Pages', 'Direct Message\non Twitter']
    LIVE_CHAT_HEADER_TITLE = 'LIVE CHAT'
    CLOSE_CHAT_CONFIRMATION = 'You are about to terminate this Live Help. Are you sure you got the answer to your question?'

    # Tutorial Overlay Elements
    TUTORIAL_ELEMENTS = ['Cash Out Open Bets Bet History', 'Check your Balance', 'Tap to open your My Account Menu',
                         'Save bets to your Betslip']

    FOOTBALL_TUTORIAL_ELEMENTS = ['Coral introduces new Favourites feature allowing you to easily access and follow several matches of your choice',
                                  'Pressing the star will add this match to your Favourites matches',
                                  'Here you can quickly and easily access your favourited matches']

    QUICK_LINK_MESSAGE = 'NOT FOUND WHAT YOU ARE LOOKING FOR? HIT A QUICK LINK'
    QUICK_LINK_HOMEPAGE = 'Homepage'

    # HELP & INFORMATION links
    _expected_links = namedtuple('links_list', ('about_us', 'contact_us', 'help',
                                                'affiliates', 'jobs', 'online_rules', 'shop_rules',
                                                'privacy_policy', 'cookie_policy', 'fairness', 'financial_controls',
                                                'responsible_gambling', 'terms_and_Conditions'))

    EXPECTED_LINKS_LIST = _expected_links(about_us='About Us',
                                          contact_us='Contact Us',
                                          help='Help',
                                          affiliates='Affiliates',
                                          jobs='Jobs',
                                          online_rules='Online Rules',
                                          shop_rules='Shop Rules',
                                          privacy_policy='Privacy Policy',
                                          cookie_policy='Cookie Policy',
                                          fairness='Fairness',
                                          financial_controls='Financial Controls',
                                          responsible_gambling='Safer Gambling',
                                          terms_and_Conditions='Terms and Conditions')
    FOOTER_LINK_UNIQUE_WORD = ['about-us', 'contact', 'help', 'entainpartners', 'entaincareers', 'sports-help',
                               'termsandconditions', 'privacy-policy', 'cookie-policy', 'fair-gaming', 'depositlimits',
                               'safer-gambling', 'terms-and-conditions']

    # Self-Exclusion
    ACCOUNT_CLOSURE_AND_REOPENING_OPTION_1 = 'I want to close my account or sections of it'
    ACCOUNT_CLOSURE_AND_REOPENING_OPTION_3 = 'I want to reopen my account or sections of it'
    ACCOUNT_CLOSURE_AND_REOPENING_OPTION_2 = "I'd like to take an irreversible time-out or exclude myself from gaming"
    SELF_EXCLUDED_INFO_MESSAGE = 'You have successfully excluded yourself from all our products.'
    SELF_EXCLUDED_LOGIN_ERROR_MESSAGE = 'Your account is currently blocked\nThis is because you opted to self-exclude yourself from our products.'
    SELF_EXCLUSION_USER_CONFIRMATION_TEXT_1 = 'I confirm that I wish to self exclude from coral.co.uk until 19/01/2021 and I understand that under no circumstances will I be able to access or reactivate my account within this period.'
    SELF_EXCLUSION_USER_CONFIRMATION_TEXT_2 = 'I understand that during this period I will no longer be permitted to open a new account on coral.co.uk.'
    SELF_EXCLUSION_PAGE2_HEADER = 'Time-out and self-exclusion'
    SELF_EXCLUSION_CONSEQUENCES = 'Consequences of Self-exclusion'
    SELF_EXCLUSION_AFTER_CONFIRMATION = 'After confirmation'
    SERVICE_CLOSURE_CONSEQUENCES_1 = 'play with real money on the products you choose to close'
    SERVICE_CLOSURE_CONSEQUENCES_2 = 'make deposits in case you close all available products (withdrawals are still possible)'
    SERVICE_CLOSURE_REOPENING_1 = 'your closed product will be reopened automatically as soon as the time period you set for the closure expires'
    SERVICE_CLOSURE_REOPENING_2 = 'you will still have an option to reopen the products before the date you specified as closure end'

    # Gaming Controls
    ACCOUNT_CLOSURE_AND_REOPENING_SPORTS_INFO_TEXT = 'Successfully closed: Sports'
    NO_MESSAGES = 'You have no messages!'

    # Payment History
    NET_DEPOSIT_POP_UP_MSG = 'Note : Net Deposits = Total Deposits - Total Withdrawals (using all payment methods since 1st April 2018 or the creation date, whichever is later).'

    ODDS_BOOST_MENU_ITEMS = ["Today's Odds Boosts", "Boosts available now", "Upcoming boosts", "Terms & conditions"]
    TOP_LEAGUE = 'Top Leagues'
    TEST_LEAGUE = 'Test Leagues'
    INVALID_LEAGUE = 'Invalid Leagues'
    CSP_COOKIE_SEGMENT = 'OX.Segment'
    CSP_CMS_SEGEMENT = "CSP_Auto_Test"
    UNIVERSAL_SEGMENT = "Universal"
