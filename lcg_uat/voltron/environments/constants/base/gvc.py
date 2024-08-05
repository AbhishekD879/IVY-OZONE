from collections import namedtuple


class GVC(object):
    """
    GVC Cashier-related constants/messages
    """
    SELF_EXCLUDED_ERROR = 'You cannot register\nIt seems you have opted to exclude yourself indefinitely on one' \
                          ' of our labels. Please contact our Customer Service team.'
    YOU_ARE_REGISTERED_MESSAGE = 'You are registered!'
    MAKE_DEPOSIT_MESSAGE = 'Almost there, make a deposit and get your welcome bonus.'
    MAKE_DEPOSIT_MESSAGE_TST2 = 'SELECT A PAYMENT OPTION & MAKE A DEPOSIT TO GET YOUR BONUS.'
    SET_YOUR_DEPOSIT_LIMITS_TITLE = 'SET YOUR DEPOSIT LIMITS'
    YES_SET_LIMIT_NOW = 'YES, SET LIMIT NOW'
    NO_MAYBE_LATER = 'NO, MAYBE LATER'
    DAILY_LIMITS_CHANGED_POPUP_TEXT = 'DAILY DEPOSIT LIMIT: {}'
    WEEKLY_LIMITS_CHANGED_POPUP_TEXT = 'WEEKLY DEPOSIT LIMIT: {}'
    MONTHLY_LIMITS_CHANGED_POPUP_TEXT = 'MONTHLY DEPOSIT LIMIT: {}'
    LIMITS_CHANGED_POPUP_TEXT = 'DAILY DEPOSIT LIMIT,WEEKLY DEPOSIT LIMIT,MONTHLY DEPOSIT LIMIT: {}'

    DEPOSIT_LIMIT_WARNING_MESSAGE_TITLE = 'Warning: self-set deposit limit exceeded'
    DEPOSIT_LIMIT_WARNING_MESSAGE = '{firstname}  You have exceeded the daily deposit limit of {currencycode} {value} previously set by you.'
    DEPOSIT_NOW_BUTTON_NAME = 'DEPOSIT {currencycode} {value} NOW'

    DEPOSIT_DAILY_LIMIT_EXCEEDED = 'SELF-SET DEPOSIT LIMIT EXCEEDED\nYou have exceeded the daily deposit limit previously set by you.\n '

    INCORRECT_USER_ERROR = ("Account doesn't exist\n"
                                "We can’t find a registered account with this email or userID. Check your details and try again or Create an account.")

    INCORRECT_PASSWORD_ERROR = 'Login failed.\n' \
                               'Please review your details and try again.'
    PROBLEMS_LOGGING_IN = 'Looks like you’re having problems logging in.\n' \
                          'Try to reset your password to prevent your account from getting blocked.'
    INCORRECT_CREDENTIALS = 'Trouble logging in?\n' \
                            'Reset your password to get back into your account.'

    CHANGE_PASSWORD_SUCCESS_MSG = 'Password changed successfully!'

    MARKETING_PREFERENCES_DESKTOP = 'Communication Preferences'
    MARKETING_PREFERENCES_MOBILE = 'COMMUNICATION PREFERENCES'

    DEPOSIT_SUCCESSFUL_MESSAGE = 'Success! £{0:.2f} added to your account. Total Balance: £{0:.2f} DONE'
    SESSION_EXPIRED_DIALOG_TITLE = 'Your session expired. Please log in again.'

    # Quick deposit
    DEPOSIT_AND_PLACE_BTN = 'Deposit and Place Bet'.upper()
    FUNDS_NEEDED_FOR_BET = 'Funds needed for bet £ {0:.2f}.'

    WITHDRAWAL = 'Withdrawal'

    # Marketing Preferences
    COMMUNICATION_CHECKBOXES = ['Email', 'SMS', 'Phone call', 'Post']

    # Footer text links
    EXPECTED_REF_LINK_54743 = '54743'

    # Footer Text
    COMPLIANCE_INFORMATION = 'Coral is operated by LC International Limited who are licensed and regulated in Great ' \
                             'Britain by the Gambling Commission under account number 54743.'

    # Footer links
    _expected_footer_links = namedtuple('footer_links_list', ('gamecarecertify', 'gbga', 'ibas', 'norton', 'gamecare',
                                                              'gibraltar', 'eighteen', 'begambleaware', 'gambling_comission', 'gamestop'))

    FOOTER_LINKS_ALT_LIST = _expected_footer_links(gamecarecertify='GamcareCertify', gbga='GBGA', ibas='IBAS_40px',
                                                   norton='Norton_Secured', gamecare='GamCare - White BG',
                                                   gibraltar='hm-gov-of-gibraltar', eighteen='18_40px', begambleaware='begambleaware_40px',
                                                   gambling_comission='gamblingcomission_40px', gamestop='gamstop_40px')

    # Footer url words
    _expected_footer_url = namedtuple('footer_url_list', ('gamecarecertify', 'gbga', 'ibas', 'norton', 'gamecare',
                                                          'gibraltar', 'eighteen', 'begambleaware', 'gambling_comission', 'gamestop'))

    FOOTER_LOGO_URL = _expected_footer_url(gamecarecertify='gamcare', gbga='bgba', ibas='ibas',
                                           norton='norton', gamecare='gamcare',
                                           gibraltar='gibraltar', eighteen='18plus', begambleaware='begambleaware',
                                           gambling_comission='gamblingcommission', gamestop='gamstop')

    COOKIE_POLICY_FOOTER = 'Cookie Policy'
    PRIVACY_POLICY_FOOTER = 'Privacy Policy'
    EXPECTED_DEPOSIT_LIMIT_OPTIONS = [u'No Limit', u'£ 20', u'£ 50', u'£ 100', u'£ 200', u'£ 250', u'£ 500',
                                      u'£ 1000', u'£ 5000', u'£ 10000', u'£ 20000', u'£ 30000', u'£ 50000',
                                      u'£ 75000', u'£ 99000', 'Other...']
